from PySide6.QtWidgets import QWidget, QVBoxLayout, QSplitter, QComboBox
from PySide6.QtCore import Qt
from .widgets.compliance_panel import CompliancePanel
from .widgets.environmental_tabs import EnvironmentalTabs
from .widgets.gallery_widget import GalleryWidget
from .widgets.checklist_widget import ChecklistWidget

class EnvironmentalView(QWidget):
    def __init__(self, controller, parent=None):
        super().__init__(parent)
        self.controller = controller
        self._setup_ui()
        self._connect_signals()
        
    def _setup_ui(self):
        main_layout = QVBoxLayout(self)
        
        # Top: Process Selector & Compliance Panel
        self.process_selector = QComboBox()
        self.process_selector.addItem("Processo: Padrão (Mock)")
        main_layout.addWidget(self.process_selector)
        
        self.compliance_panel = CompliancePanel()
        main_layout.addWidget(self.compliance_panel)
        
        # Splitter for Tabs / Checklist / Gallery
        self.splitter = QSplitter(Qt.Horizontal)
        main_layout.addWidget(self.splitter, 1)
        
        # Left: Main Data Tabs
        self.tabs = EnvironmentalTabs()
        self.splitter.addWidget(self.tabs)
        
        # Right: Sidebar (Checklist + Gallery)
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        self.checklist = ChecklistWidget()
        self.gallery = GalleryWidget()
        right_layout.addWidget(self.checklist)
        right_layout.addWidget(self.gallery)
        self.splitter.addWidget(right_panel)
        
        self.splitter.setSizes([700, 300])
        
    def _connect_signals(self):
        self.controller.compliance_updated.connect(self.compliance_panel.update_snapshot)
