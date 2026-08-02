from PySide6.QtWidgets import QWidget, QVBoxLayout, QSplitter, QGroupBox
from PySide6.QtCore import Qt
from .widgets.territorial_tree import TerritorialTreeView
from .widgets.territorial_form import TerritorialForm
from .widgets.search_bar import SearchBar

class TerritorialView(QWidget):
    def __init__(self, controller, parent=None):
        super().__init__(parent)
        self.controller = controller
        self._setup_ui()
        self._connect_signals()
        
    def _setup_ui(self):
        main_layout = QVBoxLayout(self)
        
        # Search Bar
        self.search_bar = SearchBar()
        main_layout.addWidget(self.search_bar)
        
        self.splitter = QSplitter(Qt.Horizontal)
        main_layout.addWidget(self.splitter)
        
        # Left Panel (Tree)
        tree_group = QGroupBox("Navegação Territorial")
        tree_layout = QVBoxLayout(tree_group)
        self.tree = TerritorialTreeView()
        tree_layout.addWidget(self.tree)
        self.splitter.addWidget(tree_group)
        
        # Center Panel (Form)
        form_group = QGroupBox("Ficha Cadastral")
        form_layout = QVBoxLayout(form_group)
        self.form = TerritorialForm()
        form_layout.addWidget(self.form)
        self.splitter.addWidget(form_group)
        
        self.splitter.setSizes([300, 500])
        
    def _connect_signals(self):
        self.tree.item_selected.connect(self._on_tree_selected)
        self.search_bar.search_triggered.connect(self.controller.perform_search)
        
    def _on_tree_selected(self, entity_type: str, entity_id: int):
        # Stub: Load data from controller and update form
        self.form.load_entity(entity_type, {"id": entity_id, "mock": "data"})
