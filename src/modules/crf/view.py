from PySide6.QtWidgets import QWidget, QVBoxLayout, QSplitter, QComboBox, QTabWidget, QLabel
from PySide6.QtCore import Qt
from .widgets.emission_assistant_panel import EmissionAssistantPanel
from .widgets.crf_document_tree import CRFDocumentTree
from .widgets.approval_flow_widget import ApprovalFlowWidget

class CRFView(QWidget):
    def __init__(self, controller, parent=None):
        super().__init__(parent)
        self.controller = controller
        self._setup_ui()
        self._connect_signals()
        
    def _setup_ui(self):
        main_layout = QVBoxLayout(self)
        
        # Top Flow
        self.approval_flow = ApprovalFlowWidget()
        main_layout.addWidget(self.approval_flow)
        
        # Splitter
        self.splitter = QSplitter(Qt.Horizontal)
        main_layout.addWidget(self.splitter, 1)
        
        # Left Panel (Assistant + Actions)
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        
        self.process_selector = QComboBox()
        self.process_selector.addItem("Processo CRF: Loteamento Jd. Primavera")
        left_layout.addWidget(self.process_selector)
        
        self.assistant_panel = EmissionAssistantPanel()
        left_layout.addWidget(self.assistant_panel)
        left_layout.addStretch()
        
        self.splitter.addWidget(left_panel)
        
        # Center Panel (Document Tree + Tabs)
        center_panel = QWidget()
        center_layout = QVBoxLayout(center_panel)
        
        self.tabs = QTabWidget()
        
        self.doc_tree = CRFDocumentTree()
        self.tabs.addTab(self.doc_tree, "Documentos e Minutas")
        
        self.checklist_tab = QLabel("Checklist de Requisitos")
        self.tabs.addTab(self.checklist_tab, "Checklist")
        
        self.history_tab = QLabel("Histórico de Revisões")
        self.tabs.addTab(self.history_tab, "Histórico")
        
        center_layout.addWidget(self.tabs)
        self.splitter.addWidget(center_panel)
        
        self.splitter.setSizes([350, 650])
        self.approval_flow.set_current_stage("Rascunho")
        
    def _connect_signals(self):
        self.controller.assistant_updated.connect(self.assistant_panel.update_diagnosis)
        # Load a mock process immediately for testing
        self.controller.run_assistant(1)
