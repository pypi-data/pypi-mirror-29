"""
GO Enrichment Analysis
----------------------

"""
import sys
import math
import gc
import webbrowser
import operator
import logging

from collections import defaultdict
from functools import reduce
from concurrent.futures import Future
from types import SimpleNamespace

from typing import Dict, List, Tuple

from AnyQt.QtWidgets import (
    QTreeWidget, QTreeWidgetItem, QTreeView, QMenu, QCheckBox, QSplitter,
    QDialog, QVBoxLayout, QLabel, QDialogButtonBox, QLayout, QItemDelegate
)
from AnyQt.QtGui import QBrush
from AnyQt.QtCore import Qt, QSize, QThread, QTimer
from AnyQt.QtCore import pyqtSlot as Slot

import numpy

import Orange.data
from Orange.widgets.utils.datacaching import data_hints

from Orange.widgets import widget, gui, settings
from Orange.widgets.utils.concurrent import (
    ThreadExecutor, FutureWatcher, methodinvoke
)

from requests.exceptions import ConnectTimeout, RequestException

from .. import gene, go, taxonomy
from ..utils import serverfiles
from ..utils import stats
from ..widgets.utils.download import EnsureDownloaded


def isstring(var):
    return isinstance(var, Orange.data.StringVariable)


class TreeNode(object):
    def __init__(self, value, children):
        self.value = value
        self.children = children


class GOTreeWidget(QTreeWidget):
    def contextMenuEvent(self, event):
        super().contextMenuEvent(event)
        term = self.itemAt(event.pos()).term
        self._currMenu = QMenu()
        self._currAction = self._currMenu.addAction("View term on AmiGO website")
        self._currAction.triggered.connect(lambda: self.BrowserAction(term))
        self._currMenu.popup(event.globalPos())

    def BrowserAction(self, term):
        if isinstance(term, go.Term):
            term = term.id
        webbrowser.open("http://amigo.geneontology.org/cgi-bin/amigo/term-details.cgi?term="+term)


class State:
    #: Ready to run
    Ready = 1
    #: Downloading datasets needed to run.
    Downloading = 2
    #: Running the enrichment task
    Running = 4
    #: The current executing task is stale. Need to reschedule another update
    #: once this one completes.
    #: Only applicable with Downloading and Running
    Stale = 8


class OWGOEnrichmentAnalysis(widget.OWWidget):
    name = "GO Browser"
    description = "Enrichment analysis for Gene Ontology terms."
    icon = "../widgets/icons/GOBrowser.svg"
    priority = 2020

    inputs = [("Cluster Data", Orange.data.Table,
               "setDataset", widget.Single + widget.Default),
              ("Reference Data", Orange.data.Table,
               "setReferenceDataset")]

    outputs = [("Data on Selected Genes", Orange.data.Table),
               ("Data on Unselected Genes", Orange.data.Table),
               ("Data on Unknown Genes", Orange.data.Table),
               ("Enrichment Report", Orange.data.Table)]

    settingsHandler = settings.DomainContextHandler()

    annotationIndex = settings.ContextSetting(0)
    geneAttrIndex = settings.ContextSetting(0)
    useAttrNames = settings.ContextSetting(False)
    geneMatcherSettings = settings.Setting([True, False, False, False])
    useReferenceDataset = settings.Setting(False)
    aspectIndex = settings.Setting(0)

    useEvidenceType = settings.Setting(
        {et: True for et in go.evidenceTypesOrdered})

    filterByNumOfInstances = settings.Setting(False)
    minNumOfInstances = settings.Setting(1)
    filterByPValue = settings.Setting(True)
    maxPValue = settings.Setting(0.2)
    filterByPValue_nofdr = settings.Setting(False)
    maxPValue_nofdr = settings.Setting(0.01)
    probFunc = settings.Setting(0)

    selectionDirectAnnotation = settings.Setting(0)
    selectionDisjoint = settings.Setting(0)
    selectionAddTermAsClass = settings.Setting(0)

    def __init__(self, parent=None):
        super().__init__(self, parent)

        self.clusterDataset = None
        self.referenceDataset = None
        self.ontology = None
        self.annotations = None
        self.loadedAnnotationCode = None
        self.treeStructRootKey = None
        self.probFunctions = [stats.Binomial(), stats.Hypergeometric()]
        self.selectedTerms = []

        self.selectionChanging = 0
        self.__state = State.Ready
        self.__scheduletimer = QTimer(self, singleShot=True)
        self.__scheduletimer.timeout.connect(self.__update)


        #############
        ## GUI
        #############
        self.tabs = gui.tabWidget(self.controlArea)
        ## Input tab
        self.inputTab = gui.createTabPage(self.tabs, "Input")
        box = gui.widgetBox(self.inputTab, "Info")
        self.infoLabel = gui.widgetLabel(box, "No data on input\n")

        gui.button(box, self, "Ontology/Annotation Info",
                   callback=self.ShowInfo,
                   tooltip="Show information on loaded ontology and annotations")

        box = gui.widgetBox(self.inputTab, "Organism")
        self.annotationComboBox = gui.comboBox(
            box, self, "annotationIndex", items=[],
            callback=self.__invalidateAnnotations, tooltip="Select organism"
        )

        genebox = gui.widgetBox(self.inputTab, "Gene Names")
        self.geneAttrIndexCombo = gui.comboBox(
            genebox, self, "geneAttrIndex", callback=self.__invalidate,
            tooltip="Use this attribute to extract gene names from input data")
        self.geneAttrIndexCombo.setDisabled(self.useAttrNames)

        cb = gui.checkBox(genebox, self, "useAttrNames", "Use column names",
                          tooltip="Use column names for gene names",
                          callback=self.__invalidate)
        cb.toggled[bool].connect(self.geneAttrIndexCombo.setDisabled)

        gui.button(genebox, self, "Gene matcher settings",
                   callback=self.UpdateGeneMatcher,
                   tooltip="Open gene matching settings dialog")

        self.referenceRadioBox = gui.radioButtonsInBox(
            self.inputTab, self, "useReferenceDataset",
            ["Entire genome", "Reference set (input)"],
            tooltips=["Use entire genome for reference",
                      "Use genes from Referece Examples input signal as reference"],
            box="Reference", callback=self.__invalidate)

        self.referenceRadioBox.buttons[1].setDisabled(True)
        gui.radioButtonsInBox(
            self.inputTab, self, "aspectIndex",
            ["Biological process", "Cellular component", "Molecular function"],
            box="Aspect", callback=self.__invalidate)

        ## Filter tab
        self.filterTab = gui.createTabPage(self.tabs, "Filter")
        box = gui.widgetBox(self.filterTab, "Filter GO Term Nodes")
        gui.checkBox(box, self, "filterByNumOfInstances", "Genes",
                     callback=self.FilterAndDisplayGraph, 
                     tooltip="Filter by number of input genes mapped to a term")
        ibox = gui.indentedBox(box)
        gui.spin(ibox, self, 'minNumOfInstances', 1, 100,
                 step=1, label='#:', labelWidth=15,
                 callback=self.FilterAndDisplayGraph,
                 callbackOnReturn=True,
                 tooltip="Min. number of input genes mapped to a term")

        gui.checkBox(box, self, "filterByPValue_nofdr", "p-value",
                     callback=self.FilterAndDisplayGraph,
                     tooltip="Filter by term p-value")

        gui.doubleSpin(gui.indentedBox(box), self, 'maxPValue_nofdr', 1e-8, 1,
                       step=1e-8,  label='p:', labelWidth=15,
                       callback=self.FilterAndDisplayGraph,
                       callbackOnReturn=True,
                       tooltip="Max term p-value")

        #use filterByPValue for FDR, as it was the default in prior versions
        gui.checkBox(box, self, "filterByPValue", "FDR",
                     callback=self.FilterAndDisplayGraph,
                     tooltip="Filter by term FDR")
        gui.doubleSpin(gui.indentedBox(box), self, 'maxPValue', 1e-8, 1,
                       step=1e-8,  label='p:', labelWidth=15,
                       callback=self.FilterAndDisplayGraph,
                       callbackOnReturn=True,
                       tooltip="Max term p-value")

        box = gui.widgetBox(box, "Significance test")

        gui.radioButtonsInBox(box, self, "probFunc", ["Binomial", "Hypergeometric"],
                              tooltips=["Use binomial distribution test",
                                        "Use hypergeometric distribution test"],
                              callback=self.__invalidate)  # TODO: only update the p values
        box = gui.widgetBox(self.filterTab, "Evidence codes in annotation",
                              addSpace=True)
        self.evidenceCheckBoxDict = {}
        for etype in go.evidenceTypesOrdered:
            ecb = QCheckBox(
                etype, toolTip=go.evidenceTypes[etype],
                checked=self.useEvidenceType[etype])
            ecb.toggled.connect(self.__on_evidenceChanged)
            box.layout().addWidget(ecb)
            self.evidenceCheckBoxDict[etype] = ecb

        ## Select tab
        self.selectTab = gui.createTabPage(self.tabs, "Select")
        box = gui.radioButtonsInBox(
            self.selectTab, self, "selectionDirectAnnotation",
            ["Directly or Indirectly", "Directly"],
            box="Annotated genes",
            callback=self.ExampleSelection)

        box = gui.widgetBox(self.selectTab, "Output", addSpace=True)
        gui.radioButtonsInBox(
            box, self, "selectionDisjoint",
            btnLabels=["All selected genes",
                       "Term-specific genes",
                       "Common term genes"],
            tooltips=["Outputs genes annotated to all selected GO terms",
                      "Outputs genes that appear in only one of selected GO terms", 
                      "Outputs genes common to all selected GO terms"],
            callback=[self.ExampleSelection,
                      self.UpdateAddClassButton])

        self.addClassCB = gui.checkBox(
            box, self, "selectionAddTermAsClass", "Add GO Term as class",
            callback=self.ExampleSelection)

        # ListView for DAG, and table for significant GOIDs
        self.DAGcolumns = ['GO term', 'Cluster', 'Reference', 'p-value',
                           'FDR', 'Genes', 'Enrichment']

        self.splitter = QSplitter(Qt.Vertical, self.mainArea)
        self.mainArea.layout().addWidget(self.splitter)

        # list view
        self.listView = GOTreeWidget(self.splitter)
        self.listView.setSelectionMode(QTreeView.ExtendedSelection)
        self.listView.setAllColumnsShowFocus(1)
        self.listView.setColumnCount(len(self.DAGcolumns))
        self.listView.setHeaderLabels(self.DAGcolumns)

        self.listView.header().setSectionsClickable(True)
        self.listView.header().setSortIndicatorShown(True)
        self.listView.setSortingEnabled(True)
        self.listView.setItemDelegateForColumn(
            6, EnrichmentColumnItemDelegate(self))
        self.listView.setRootIsDecorated(True)

        self.listView.itemSelectionChanged.connect(self.ViewSelectionChanged)

        # table of significant GO terms
        self.sigTerms = QTreeWidget(self.splitter)
        self.sigTerms.setColumnCount(len(self.DAGcolumns))
        self.sigTerms.setHeaderLabels(self.DAGcolumns)
        self.sigTerms.setSortingEnabled(True)
        self.sigTerms.setSelectionMode(QTreeView.ExtendedSelection)
        self.sigTerms.setItemDelegateForColumn(
            6, EnrichmentColumnItemDelegate(self))

        self.sigTerms.itemSelectionChanged.connect(self.TableSelectionChanged)

        self.sigTableTermsSorted = []
        self.graph = {}
        self.originalGraph = None

        self.inputTab.layout().addStretch(1)
        self.filterTab.layout().addStretch(1)
        self.selectTab.layout().addStretch(1)

        class AnnotationSlot(SimpleNamespace):
            taxid = ...  # type: str
            name = ...   # type: str
            orgcode = ...  # type: str
            filename = ...  # type:str

        available_annotations = [
            AnnotationSlot(
                taxid=taxid,
                name=taxonomy.common_taxid_to_name(taxid),
                orgcode=go.from_taxid(taxid),
                filename="gene_association.{}.tar.gz"
                         .format(go.from_taxid(taxid))
            )
            for taxid in taxonomy.common_taxids()
            if go.from_taxid(taxid)
        ]
        self.availableAnnotations = sorted(
            available_annotations, key=lambda a: a.name
        )
        self.annotationComboBox.clear()

        for a in self.availableAnnotations:
            self.annotationComboBox.addItem(a.name)

        self.annotationComboBox.setCurrentIndex(self.annotationIndex)
        self.annotationIndex = self.annotationComboBox.currentIndex()

        self._executor = ThreadExecutor()

    def sizeHint(self):
        return QSize(1000, 700)

    def __on_evidenceChanged(self):
        for etype, cb in self.evidenceCheckBoxDict.items():
            self.useEvidenceType[etype] = cb.isChecked()
        self.__invalidate()

    def UpdateGeneMatcher(self):
        """Open the Gene matcher settings dialog."""
        dialog = GeneMatcherDialog(self, defaults=self.geneMatcherSettings, modal=True)
        if dialog.exec_() != QDialog.Rejected:
            self.geneMatcherSettings = [getattr(dialog, item[0]) for item in dialog.items]
            self.__invalidateAnnotations()

    def clear(self):
        self.infoLabel.setText("No data on input\n")
        self.warning(0)
        self.warning(1)
        self.geneAttrIndexCombo.clear()
        self.ClearGraph()

        self.send("Data on Selected Genes", None)
        self.send("Data on Unselected Genes", None)
        self.send("Data on Unknown Genes", None)
        self.send("Enrichment Report", None)

    def setDataset(self, data=None):
        self.closeContext()
        self.clear()
        self.clusterDataset = data

        if data is not None:
            domain = data.domain
            allvars = domain.variables + domain.metas
            self.candidateGeneAttrs = [var for var in allvars if isstring(var)]

            self.geneAttrIndexCombo.clear()
            for var in self.candidateGeneAttrs:
                self.geneAttrIndexCombo.addItem(*gui.attributeItem(var))
            taxid = data_hints.get_hint(data, "taxid", "")

            try:
                code = go.from_taxid(taxid)
            except KeyError:
                pass
            else:
                _c2i = {a.orgcode: i
                        for i, a in enumerate(self.availableAnnotations)}
                try:
                    self.annotationIndex = _c2i[code]
                except KeyError:
                    pass

            self.useAttrNames = data_hints.get_hint(data, "genesinrows",
                                                    self.useAttrNames)
            self.openContext(data)

            self.geneAttrIndex = min(self.geneAttrIndex,
                                     len(self.candidateGeneAttrs) - 1)
            if len(self.candidateGeneAttrs) == 0:
                self.useAttrNames = True
                self.geneAttrIndex = -1
            elif self.geneAttrIndex < len(self.candidateGeneAttrs):
                self.geneAttrIndex = len(self.candidateGeneAttrs) - 1

            self.__invalidate()

    def setReferenceDataset(self, data=None):
        self.referenceDataset = data
        self.referenceRadioBox.buttons[1].setDisabled(not bool(data))
        self.referenceRadioBox.buttons[1].setText("Reference set")
        if self.clusterDataset is not None and self.useReferenceDataset:
            self.useReferenceDataset = 0 if not data else 1
            self.__invalidate()
        elif self.clusterDataset:
            self.__updateReferenceSetButton()

    def handleNewSignals(self):
        super().handleNewSignals()
        self.__update()

    @Slot()
    def __invalidate(self):
        # Invalidate the current results or pending task and schedule an
        # update.
        self.__scheduletimer.start()
        if self.__state != State.Ready:
            self.__state |= State.Stale

        self.SetGraph({})
        self.referenceGenes = None
        self.clusterGenes = None

    def __invalidateAnnotations(self):
        self.annotations = None
        self.loadedAnnotationCode = None
        if self.clusterDataset:
            self.infoLabel.setText("...\n")
        self.__updateReferenceSetButton()
        self.__invalidate()

    @Slot()
    def __update(self):
        self.__scheduletimer.stop()
        if self.clusterDataset is None:
            return

        if self.__state & State.Running:
            self.__state |= State.Stale
        elif self.__state & State.Downloading:
            self.__state |= State.Stale
        elif self.__state & State.Ready:
            if self.__ensure_data():
                self.Load()
                self.Enrichment()
            else:
                assert self.__state & State.Downloading
                assert self.isBlocking()

    def __updateReferenceSetButton(self):
        allgenes, refgenes = None, None
        if self.referenceDataset and self.annotations is not None:
            try:
                allgenes = self.genesFromTable(self.referenceDataset)
            except Exception:
                allgenes = []
            refgenes, unknown = self.FilterAnnotatedGenes(allgenes)
        self.referenceRadioBox.buttons[1].setDisabled(not bool(allgenes))
        self.referenceRadioBox.buttons[1].setText("Reference set " + ("(%i genes, %i matched)" % (len(allgenes), len(refgenes)) if allgenes and refgenes else ""))

    def genesFromTable(self, data):
        if self.useAttrNames:
            genes = [v.name for v in data.domain.variables]
        else:
            attr = self.candidateGeneAttrs[min(self.geneAttrIndex, len(self.candidateGeneAttrs) - 1)]
            genes = [str(ex[attr]) for ex in data if not numpy.isnan(ex[attr])]
            if any("," in gene for gene in genes):
                self.information(0, "Separators detected in gene names. Assuming multiple genes per example.")
                genes = reduce(operator.iadd, (genes.split(",") for genes in genes), [])
        return genes

    def FilterAnnotatedGenes(self, genes):
        matchedgenes = self.annotations.get_gene_names_translator(genes).values()
        return matchedgenes, [gene for gene in genes if gene not in matchedgenes]

    def FilterUnknownGenes(self):
        if not self.useAttrNames and self.candidateGeneAttrs:
            geneAttr = self.candidateGeneAttrs[min(self.geneAttrIndex, len(self.candidateGeneAttrs)-1)]
            indices = []
            for i, ex in enumerate(self.clusterDataset):
                if not any(self.annotations.genematcher.match(n.strip()) for n in str(ex[geneAttr]).split(",")):
                    indices.append(i)
            if indices:
                data = self.clusterDataset[indices]
            else:
                data = None
            self.send("Data on Unknown Genes", data)
        else:
            self.send("Data on Unknown Genes", None)

    def __start_download(self, files_list):
        # type: (List[Tuple[str, str]]) -> None
        task = EnsureDownloaded(files_list)
        task.progress.connect(self._progressBarSet)
        f = self._executor.submit(task)
        fw = FutureWatcher(f, self)
        fw.finished.connect(self.__download_finish)
        fw.finished.connect(fw.deleteLater)
        fw.resultReady.connect(self.__invalidate)

        self.progressBarInit(processEvents=None)
        self.setBlocking(True)
        self.setStatusMessage("Downloading")
        self.__state = State.Downloading

    @Slot(Future)
    def __download_finish(self, result):
        # type: (Future[None]) -> None
        assert QThread.currentThread() is self.thread()
        assert result.done()
        self.setBlocking(False)
        self.setStatusMessage("")
        self.progressBarFinished(processEvents=False)
        try:
            result.result()
        except ConnectTimeout:
            logging.getLogger(__name__).error("Error:")
            self.error(2, "Internet connection error, unable to load data. " +
                       "Check connection and create a new GO Browser widget.")
        except RequestException as err:
            logging.getLogger(__name__).error("Error:")
            self.error(2, "Internet error:\n" + str(err))
        except BaseException as err:
            logging.getLogger(__name__).error("Error:")
            self.error(2, "Error:\n" + str(err))
            raise
        else:
            self.error(2)
        finally:
            self.__state = State.Ready

    def __ensure_data(self):
        # Ensure that all required database (ontology and annotations for
        # the current selected organism are present. If not start a download in
        # the background. Return True if all dbs are present and false
        # otherwise
        assert self.__state == State.Ready
        annotation = self.availableAnnotations[self.annotationIndex]
        go_files = serverfiles.listfiles("GO")
        files = []

        if annotation.filename not in go_files:
            files.append(("GO", annotation.filename))

        if go.Ontology.FILENAME not in go_files:
            files.append((go.Ontology.DOMAIN, go.Ontology.FILENAME))

        gene_info_files = serverfiles.listfiles(gene.NCBIGeneInfo.DOMAIN)
        gi_filename = gene.NCBIGeneInfo.FILENAME.format(
            taxid=gene.NCBIGeneInfo.TAX_MAP.get(
                annotation.taxid, annotation.taxid)
        )

        if gi_filename not in gene_info_files and self.geneMatcherSettings[2]:
            files.append((gene.NCBIGeneInfo.DOMAIN, gi_filename))

        if files:
            self.__start_download(files)
            assert self.__state == State.Downloading
            return False
        else:
            return True

    def Load(self):
        a = self.availableAnnotations[self.annotationIndex]

        if self.ontology is None:
            self.ontology = go.Ontology()

        if a.orgcode != self.loadedAnnotationCode:
            self.annotations = None
            gc.collect()  # Force run garbage collection
            self.annotations = go.Annotations(a.orgcode, genematcher=gene.GMDirect())
            self.loadedAnnotationCode = a.orgcode
            count = defaultdict(int)
            geneSets = defaultdict(set)

            for anno in self.annotations.annotations:
                count[anno.evidence] += 1
                geneSets[anno.evidence].add(anno.geneName)
            for etype in go.evidenceTypesOrdered:
                ecb = self.evidenceCheckBoxDict[etype]
                ecb.setEnabled(bool(count[etype]))
                ecb.setText(etype + ": %i annots(%i genes)" % (count[etype], len(geneSets[etype])))

            self.__updateReferenceSetButton()

    def SetGeneMatcher(self):
        if self.annotations:
            taxid = self.annotations.taxid
            matchers = []
            for matcher, use in zip([gene.GMGO, gene.GMKEGG, gene.GMNCBI, gene.GMAffy], self.geneMatcherSettings):
                if use:
                    try:
                        if taxid == "352472":
                            matchers.extend([matcher(taxid), gene.GMDicty(),
                                             [matcher(taxid), gene.GMDicty()]])
                            # The reason machers are duplicated is that we want `matcher` or `GMDicty` to
                            # match genes by them self if possible. Only use the joint matcher if they fail.   
                        else:
                            matchers.append(matcher(taxid))
                    except Exception as ex:
                        print(ex)
            self.annotations.genematcher = gene.matcher(matchers)
            self.annotations.genematcher.set_targets(self.annotations.gene_names)
            self.__updateReferenceSetButton()

    def Enrichment(self):
        assert self.clusterDataset is not None
        assert self.__state == State.Ready

        if not self.annotations.ontology:
            self.annotations.ontology = self.ontology

        if isinstance(self.annotations.genematcher, gene.GMDirect):
            self.SetGeneMatcher()
        self.error(1)
        self.warning([0, 1])

        if self.useAttrNames:
            clusterGenes = [v.name for v in self.clusterDataset.domain.attributes]
            self.information(0)
        elif 0 <= self.geneAttrIndex < len(self.candidateGeneAttrs):
            geneAttr = self.candidateGeneAttrs[self.geneAttrIndex]
            clusterGenes = [str(ex[geneAttr]) for ex in self.clusterDataset
                            if not numpy.isnan(ex[geneAttr])]
            if any("," in gene for gene in clusterGenes):
                self.information(0, "Separators detected in cluster gene names. Assuming multiple genes per example.")
                clusterGenes = reduce(operator.iadd, (genes.split(",") for genes in clusterGenes), [])
            else:
                self.information(0)
        else:
            self.error(1, "Failed to extract gene names from input dataset!")
            return {}

        genesSetCount = len(set(clusterGenes))

        self.clusterGenes = clusterGenes = self.annotations.get_gene_names_translator(clusterGenes).values()

        self.infoLabel.setText("%i unique genes on input\n%i (%.1f%%) genes with known annotations" % (genesSetCount, len(clusterGenes), 100.0*len(clusterGenes)/genesSetCount if genesSetCount else 0.0))

        referenceGenes = None
        if not self.useReferenceDataset or self.referenceDataset is None:
            self.information(2)
            self.information(1)
            referenceGenes = self.annotations.gene_names

        elif self.referenceDataset is not None:
            if self.useAttrNames:
                referenceGenes = [v.name for v in self.referenceDataset.domain.attributes]
                self.information(1)
            elif geneAttr in (self.referenceDataset.domain.variables +
                              self.referenceDataset.domain.metas):
                referenceGenes = [str(ex[geneAttr]) for ex in self.referenceDataset
                                  if not numpy.isnan(ex[geneAttr])]
                if any("," in gene for gene in clusterGenes):
                    self.information(1, "Separators detected in reference gene names. Assuming multiple genes per example.")
                    referenceGenes = reduce(operator.iadd, (genes.split(",") for genes in referenceGenes), [])
                else:
                    self.information(1)
            else:
                self.information(1)
                referenceGenes = None

            if referenceGenes is None:
                referenceGenes = list(self.annotations.gene_names)
                self.referenceRadioBox.buttons[1].setText("Reference set")
                self.referenceRadioBox.buttons[1].setDisabled(True)
                self.information(2, "Unable to extract gene names from reference dataset. Using entire genome for reference")
                self.useReferenceDataset = 0
            else:
                refc = len(referenceGenes)
                referenceGenes = self.annotations.get_gene_names_translator(referenceGenes).values()
                self.referenceRadioBox.buttons[1].setText("Reference set (%i genes, %i matched)" % (refc, len(referenceGenes)))
                self.referenceRadioBox.buttons[1].setDisabled(False)
                self.information(2)
        else:
            self.useReferenceDataset = 0

        if not referenceGenes:
            self.error(1, "No valid reference set")
            return {}

        self.referenceGenes = referenceGenes
        evidences = []
        for etype in go.evidenceTypesOrdered:
            if self.useEvidenceType[etype]:
                evidences.append(etype)
        aspect = ["P", "C", "F"][self.aspectIndex]

        self.progressBarInit(processEvents=False)
        self.setBlocking(True)
        self.__state = State.Running

        if clusterGenes:
            f = self._executor.submit(
                self.annotations.get_enriched_terms,
                clusterGenes, referenceGenes, evidences, aspect=aspect,
                prob=self.probFunctions[self.probFunc], use_fdr=False,
                progress_callback=methodinvoke(
                    self, "_progressBarSet", (float,))
            )
            fw = FutureWatcher(f, parent=self)
            fw.done.connect(self.__on_enrichment_done)
            fw.done.connect(fw.deleteLater)
            return
        else:
            f = Future()
            f.set_result({})
            self.__on_enrichment_done(f)

    def __on_enrichment_done(self, results):
        # type: (Future[Dict[str, tuple]]) -> None
        self.progressBarFinished(processEvents=False)
        self.setBlocking(False)
        self.setStatusMessage("")
        if self.__state & State.Stale:
            self.__state = State.Ready
            self.__invalidate()
            return

        self.__state = State.Ready
        try:
            results = results.result()  # type: Dict[str, tuple]
        except Exception as ex:
            results = {}
            error = str(ex)
            self.error(1, error)

        if results:
            terms = list(results.items())
            fdr_vals = stats.FDR([d[1] for _, d in terms])
            terms = [(key, d + (fdr,))
                     for (key, d), fdr in zip(terms, fdr_vals)]
            terms = dict(terms)
        else:
            terms = {}

        self.terms = terms

        if not self.terms:
            self.warning(0, "No enriched terms found.")
        else:
            self.warning(0)

        self.treeStructDict = {}
        ids = self.terms.keys()

        self.treeStructRootKey = None

        parents = {}
        for id in ids:
            parents[id] = set([term for _, term in self.ontology[id].related])

        children = {}
        for term in self.terms:
            children[term] = set([id for id in ids if term in parents[id]])

        for term in self.terms:
            self.treeStructDict[term] = TreeNode(self.terms[term], children[term])
            if not self.ontology[term].related and not getattr(self.ontology[term], "is_obsolete", False):
                self.treeStructRootKey = term

        self.FilterUnknownGenes()
        self.SetGraph(terms)
        self._updateEnrichmentReportOutput()
        self.commit()

    def _updateEnrichmentReportOutput(self):
        terms = sorted(self.terms.items(), key=lambda item: item[1][1])
        # Create and send the enrichemnt report table.
        termsDomain = Orange.data.Domain(
            [], [],
            # All is meta!
            [Orange.data.StringVariable("GO Term Id"),
             Orange.data.StringVariable("GO Term Name"),
             Orange.data.ContinuousVariable("Cluster Frequency"),
             Orange.data.ContinuousVariable("Genes in Cluster",
                                            number_of_decimals=0),
             Orange.data.ContinuousVariable("Reference Frequency"),
             Orange.data.ContinuousVariable("Genes in Reference",
                                            number_of_decimals=0),
             Orange.data.ContinuousVariable("p-value"),
             Orange.data.ContinuousVariable("FDR"),
             Orange.data.ContinuousVariable("Enrichment"),
             Orange.data.StringVariable("Genes")])

        terms = [[t_id,
                  self.ontology[t_id].name,
                  len(genes) / len(self.clusterGenes),
                  len(genes),
                  r_count / len(self.referenceGenes),
                  r_count,
                  p_value,
                  fdr,
                  len(genes) / len(self.clusterGenes) * \
                  len(self.referenceGenes) / r_count,
                  ",".join(genes)
                  ]
                 for t_id, (genes, p_value, r_count, fdr) in terms
                 if genes and r_count]

        if terms:
            X = numpy.empty((len(terms), 0))
            M = numpy.array(terms, dtype=object)
            termsTable = Orange.data.Table.from_numpy(termsDomain, X,
                                                      metas=M)
        else:
            termsTable = None
        self.send("Enrichment Report", termsTable)

    @Slot(float)
    def _progressBarSet(self, value):
        assert QThread.currentThread() is self.thread()
        self.progressBarSet(value, processEvents=None)

    @Slot()
    def _progressBarFinish(self):
        assert QThread.currentThread() is self.thread()
        self.progressBarFinished(processEvents=None)

    def FilterGraph(self, graph):
        if self.filterByPValue_nofdr:
            graph = go.filterByPValue(graph, self.maxPValue_nofdr)
        if self.filterByPValue: #FDR
            graph = dict(filter(lambda item: item[1][3] <= self.maxPValue, graph.items()))
        if self.filterByNumOfInstances:
            graph = dict(filter(lambda item: len(item[1][0]) >= self.minNumOfInstances, graph.items()))
        return graph

    def FilterAndDisplayGraph(self):
        if self.clusterDataset and self.originalGraph is not None:
            self.graph = self.FilterGraph(self.originalGraph)
            if self.originalGraph and not self.graph:
                self.warning(1, "All found terms were filtered out.")
            else:
                self.warning(1)
            self.ClearGraph()
            self.DisplayGraph()

    def SetGraph(self, graph=None):
        self.originalGraph = graph
        if graph:
            self.FilterAndDisplayGraph()
        else:
            self.graph = {}
            self.ClearGraph()

    def ClearGraph(self):
        self.listView.clear()
        self.listViewItems=[]
        self.sigTerms.clear()

    def DisplayGraph(self):
        fromParentDict = {}
        self.termListViewItemDict = {}
        self.listViewItems = []
        enrichment = lambda t: len(t[0]) / t[2] * (len(self.referenceGenes) / len(self.clusterGenes))
        maxFoldEnrichment = max([enrichment(term) for term in self.graph.values()] or [1])

        def addNode(term, parent, parentDisplayNode):
            if (parent, term) in fromParentDict:
                return
            if term in self.graph:
                displayNode = GOTreeWidgetItem(self.ontology[term], self.graph[term], len(self.clusterGenes), len(self.referenceGenes), maxFoldEnrichment, parentDisplayNode)
                displayNode.goId = term
                self.listViewItems.append(displayNode)
                if term in self.termListViewItemDict:
                    self.termListViewItemDict[term].append(displayNode)
                else:
                    self.termListViewItemDict[term] = [displayNode]
                fromParentDict[(parent, term)] = True
                parent = term
            else:
                displayNode = parentDisplayNode

            for c in self.treeStructDict[term].children:
                addNode(c, parent, displayNode)

        if self.treeStructDict:
            addNode(self.treeStructRootKey, None, self.listView)

        terms = self.graph.items()
        terms = sorted(terms, key=lambda item: item[1][1])
        self.sigTableTermsSorted = [t[0] for t in terms]

        self.sigTerms.clear()
        for i, (t_id, (genes, p_value, refCount, fdr)) in enumerate(terms):
            item = GOTreeWidgetItem(self.ontology[t_id],
                                    (genes, p_value, refCount, fdr),
                                    len(self.clusterGenes),
                                    len(self.referenceGenes),
                                    maxFoldEnrichment,
                                    self.sigTerms)
            item.goId = t_id

        self.listView.expandAll()
        for i in range(5):
            self.listView.resizeColumnToContents(i)
            self.sigTerms.resizeColumnToContents(i)
        self.sigTerms.resizeColumnToContents(6)
        width = min(self.listView.columnWidth(0), 350)
        self.listView.setColumnWidth(0, width)
        self.sigTerms.setColumnWidth(0, width)

    def ViewSelectionChanged(self):
        if self.selectionChanging:
            return

        self.selectionChanging = 1
        self.selectedTerms = []
        selected = self.listView.selectedItems()
        self.selectedTerms = list(set([lvi.term.id for lvi in selected]))
        self.ExampleSelection()
        self.selectionChanging = 0

    def TableSelectionChanged(self):
        if self.selectionChanging:
            return

        self.selectionChanging = 1
        self.selectedTerms = []
        selectedIds = set([self.sigTerms.itemFromIndex(index).goId for index in self.sigTerms.selectedIndexes()])

        for i in range(self.sigTerms.topLevelItemCount()):
            item = self.sigTerms.topLevelItem(i)
            selected = item.goId in selectedIds
            term = item.goId

            if selected:
                self.selectedTerms.append(term)

            for lvi in self.termListViewItemDict[term]:
                try:
                    lvi.setSelected(selected)
                    if selected:
                        lvi.setExpanded(True)
                except RuntimeError:  # Underlying C/C++ object deleted
                    pass
        self.selectionChanging = 0
        self.ExampleSelection()

    def UpdateAddClassButton(self):
        self.addClassCB.setEnabled(self.selectionDisjoint == 1)

    def ExampleSelection(self):
        self.commit()

    def commit(self):
        if self.clusterDataset is None or self.originalGraph is None or \
                self.annotations is None:
            return
        if self.__state & State.Stale:
            return

        terms = set(self.selectedTerms)
        genes = reduce(operator.ior,
                       (set(self.graph[term][0]) for term in terms), set())

        evidences = []
        for etype in go.evidenceTypesOrdered:
            if self.useEvidenceType[etype]:
                evidences.append(etype)
        allTerms = self.annotations.get_annotated_terms(
            genes, direct_annotation_only=self.selectionDirectAnnotation,
            evidence_codes=evidences)

        if self.selectionDisjoint > 0:
            count = defaultdict(int)
            for term in self.selectedTerms:
                for g in allTerms.get(term, []):
                    count[g] += 1
            ccount = 1 if self.selectionDisjoint == 1 else len(self.selectedTerms)
            selectedGenes = [gene for gene, c in count.items()
                             if c == ccount and gene in genes]
        else:
            selectedGenes = reduce(
                operator.ior,
                (set(allTerms.get(term, [])) for term in self.selectedTerms),
                set())

        if self.useAttrNames:
            vars = [self.clusterDataset.domain[gene]
                    for gene in set(selectedGenes)]
            domain = Orange.data.Domain(
                vars, self.clusterDataset.domain.class_vars,
                self.clusterDataset.domain.metas)
            newdata = self.clusterDataset.from_table(domain, self.clusterDataset)

            self.send("Data on Selected Genes", newdata)
            self.send("Data on Unselected Genes", None)
        elif self.candidateGeneAttrs:
            selectedExamples = []
            unselectedExamples = []

            geneAttr = self.candidateGeneAttrs[min(self.geneAttrIndex, len(self.candidateGeneAttrs)-1)]

            if self.selectionDisjoint == 1:
                goVar = Orange.data.DiscreteVariable(
                    "GO Term", values=list(self.selectedTerms))
                newDomain = Orange.data.Domain(
                    self.clusterDataset.domain.variables, goVar,
                    self.clusterDataset.domain.metas)
                goColumn = []
            for i, ex in enumerate(self.clusterDataset):
                if not numpy.isnan(ex[geneAttr]) and any(gene in selectedGenes for gene in str(ex[geneAttr]).split(",")):
                    if self.selectionDisjoint == 1 and self.selectionAddTermAsClass:
                        terms = filter(lambda term: any(gene in self.graph[term][0] for gene in str(ex[geneAttr]).split(",")) , self.selectedTerms)
                        term = sorted(terms)[0]
                        goColumn.append(goVar.values.index(term))
                    selectedExamples.append(i)
                else:
                    unselectedExamples.append(i)

            if selectedExamples:
                selectedExamples = self.clusterDataset[selectedExamples]
                if self.selectionDisjoint == 1 and self.selectionAddTermAsClass:
                    selectedExamples = Orange.data.Table.from_table(newDomain, selectedExamples)
                    view, issparse = selectedExamples.get_column_view(goVar)
                    assert not issparse
                    view[:] = goColumn
            else:
                selectedExamples = None

            if unselectedExamples:
                unselectedExamples = self.clusterDataset[unselectedExamples]
            else:
                unselectedExamples = None

            self.send("Data on Selected Genes", selectedExamples)
            self.send("Data on Unselected Genes", unselectedExamples)

    def ShowInfo(self):
        dialog = QDialog(self)
        dialog.setModal(False)
        dialog.setLayout(QVBoxLayout())
        label = QLabel(dialog)
        label.setText("Ontology:\n" + self.ontology.header
                      if self.ontology else "Ontology not loaded!")
        dialog.layout().addWidget(label)

        label = QLabel(dialog)
        label.setText("Annotations:\n" + self.annotations.header.replace("!", "")
                      if self.annotations else "Annotations not loaded!")
        dialog.layout().addWidget(label)
        dialog.show()

    def onDeleteWidget(self):
        """Called before the widget is removed from the canvas.
        """
        self.annotations = None
        self.ontology = None
        gc.collect()  # Force collection


fmtp = lambda score: "%0.5f" % score if score > 10e-4 else "%0.1e" % score
fmtpdet = lambda score: "%0.9f" % score if score > 10e-4 else "%0.5e" % score


class GOTreeWidgetItem(QTreeWidgetItem):
    def __init__(self, term, enrichmentResult, nClusterGenes, nRefGenes,
                 maxFoldEnrichment, parent):
        super().__init__(parent)
        self.term = term
        self.enrichmentResult = enrichmentResult
        self.nClusterGenes = nClusterGenes
        self.nRefGenes = nRefGenes
        self.maxFoldEnrichment = maxFoldEnrichment

        querymapped, pvalue, refmappedcount, fdr = enrichmentResult

        querymappedcount = len(querymapped)
        if refmappedcount > 0 and nRefGenes > 0 and nClusterGenes > 0:
            enrichment = (querymappedcount / refmappedcount) * (nRefGenes / nClusterGenes)
        else:
            enrichment = numpy.nan

        self.enrichment = enrichment

        self.setText(0, term.name)

        fmt = "%" + str(-int(math.log(max(nClusterGenes, 1)))) + "i (%.2f%%)"
        self.setText(1, fmt % (querymappedcount,
                               100.0 * querymappedcount / (nClusterGenes or 1)))

        fmt = "%" + str(-int(math.log(max(nRefGenes, 1)))) + "i (%.2f%%)"
        self.setText(2, fmt % (refmappedcount,
                               100.0 * refmappedcount / (nRefGenes or 1)))

        self.setText(3, fmtp(pvalue))
        self.setToolTip(3, fmtpdet(pvalue))
        self.setText(4, fmtp(fdr))  # FDR
        self.setToolTip(4, fmtpdet(fdr))
        self.setText(5, ", ".join(querymapped))
        self.setText(6, "%.2f" % (enrichment))
        self.setToolTip(6, "%.2f" % (enrichment))
        self.setToolTip(0, "<p>" + term.__repr__()[6:].strip().replace("\n", "<br>"))
        self.sortByData = [term.name, querymappedcount, refmappedcount,
                           pvalue, fdr, ", ".join(querymapped), enrichment]

    def data(self, col, role):
        if role == Qt.UserRole:
            if self.maxFoldEnrichment > 0:
                return self.enrichment / self.maxFoldEnrichment
            else:
                return numpy.nan
        else:
            return super().data(col, role)

    def __lt__(self, other):
        col = self.treeWidget().sortColumn()
        return self.sortByData[col] < other.sortByData[col]


class EnrichmentColumnItemDelegate(QItemDelegate):
    def paint(self, painter, option, index):
        self.drawBackground(painter, option, index)
        value = index.data(Qt.UserRole)
        if isinstance(value, float) and numpy.isfinite(value):
            painter.save()
            painter.setBrush(QBrush(Qt.blue, Qt.SolidPattern))
            painter.drawRect(option.rect.x(), option.rect.y(),
                             int(value * (option.rect.width() - 1)),
                             option.rect.height() - 1)
            painter.restore()
        else:
            super().paint(painter, option, index)


class GeneMatcherDialog(QDialog):
    items = [("useGO", "Use gene names from Gene Ontology annotations"),
             ("useKEGG", "Use gene names from KEGG Genes database"),
             ("useNCBI", "Use gene names from NCBI Gene info database"),
             ("useAffy", "Use Affymetrix platform reference ids")]

    def __init__(self, parent=None, defaults=[True, False, False, False],
                 enabled=[False, True, True, True], **kwargs):
        super().__init__(parent, **kwargs)
        self.setLayout(QVBoxLayout())
        for item, default in zip(self.items, defaults):
            setattr(self, item[0], default)

        for item, enable, checked in zip(self.items, enabled, defaults):
            cb = QCheckBox(text=item[1], checked=checked, enabled=enable)
            cb.toggled[bool].connect(
                lambda state, name=item[0]:
                    setattr(self, name, state)
            )
            self.layout().addWidget(cb)

        bbox = QDialogButtonBox(
            Qt.Horizontal,
            standardButtons=QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        )
        bbox.accepted.connect(self.accept)
        bbox.rejected.connect(self.reject)

        self.layout().addWidget(bbox)

        self.layout().setSizeConstraint(QLayout.SetFixedSize)


def main(argv=sys.argv):
    from AnyQt.QtWidgets import QApplication
    app = QApplication(list(argv))
    argv = app.arguments()
    if len(argv) > 1:
        data = Orange.data.Table(argv[1])
    else:
        data = None

    w = OWGOEnrichmentAnalysis()
    w.show()
    w.raise_()
    w.setDataset(data)
    w.handleNewSignals()
    rval = app.exec_()
    w.setDataset(None)
    w.handleNewSignals()
    w.saveSettings()
    w.onDeleteWidget()
    return rval


if __name__ == "__main__":
    sys.exit(main())
