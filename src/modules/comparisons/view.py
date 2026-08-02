from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, 
    QPushButton, QGroupBox, QFileDialog, QMessageBox, QTabWidget
)
from PySide6.QtCore import Qt, Slot
from src.core.events.event_bus import event_bus
from .events import ComparisonStartedEvent, ComparisonFinishedEvent, ComparisonProgressEvent
from .widgets.progress_bar import ComparisonProgressBar
from .widgets.history_view import HistoryView

class ComparisonsView(QWidget):
    def __init__(self, controller, parent=None):
        super().__init__(parent)
        self.controller = controller
        self.inputs_paths = {}
        self.output_dir = ""
        self._setup_ui()
        self._subscribe_events()
        
    def _setup_ui(self):
        main_layout = QVBoxLayout(self)
        
        # Header (Project context)
        header_layout = QHBoxLayout()
        self.project_label = QLabel("Projeto: Nenhum")
        self.project_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        header_layout.addWidget(self.project_label)
        header_layout.addStretch()
        main_layout.addLayout(header_layout)
        
        # Tabs
        self.tabs = QTabWidget()
        main_layout.addWidget(self.tabs)
        
        # --- TAB: Execução ---
        exec_tab = QWidget()
        exec_layout = QVBoxLayout(exec_tab)
        
        # Comparativos Group
        comp_group = QGroupBox("Comparativos")
        comp_layout = QVBoxLayout(comp_group)
        self.combo_type = QComboBox()
        self.combo_type.addItems(["SHP x Métrica", "Métrica x Memorial de Lotes", "Ecoleta x SHP", "CRF x SHP"])
        comp_layout.addWidget(self.combo_type)
        exec_layout.addWidget(comp_group)
        
        # Arquivos Group
        file_group = QGroupBox("Arquivos de Entrada e Saída")
        file_layout = QVBoxLayout(file_group)
        
        self.btn_select_shp = QPushButton("Selecionar SHP (Excel)")
        self.btn_select_shp.clicked.connect(lambda: self._select_file("SHP", "Excel (*.xlsx *.xls)"))
        
        self.btn_select_mt = QPushButton("Selecionar Métrica (Excel)")
        self.btn_select_mt.clicked.connect(lambda: self._select_file("MT", "Excel (*.xlsx *.xls)"))
        
        self.btn_select_out = QPushButton("Selecionar Pasta de Saída")
        self.btn_select_out.clicked.connect(self._select_out_dir)
        
        file_layout.addWidget(self.btn_select_shp)
        file_layout.addWidget(self.btn_select_mt)
        file_layout.addWidget(self.btn_select_out)
        exec_layout.addWidget(file_group)
        
        # Progresso
        self.progress_bar = ComparisonProgressBar()
        exec_layout.addWidget(self.progress_bar)
        
        # Ações
        action_layout = QHBoxLayout()
        self.btn_execute = QPushButton("Executar")
        self.btn_execute.setStyleSheet("background-color: #233A5E; color: white; padding: 10px; font-weight: bold;")
        self.btn_execute.clicked.connect(self._on_execute)
        action_layout.addStretch()
        action_layout.addWidget(self.btn_execute)
        exec_layout.addLayout(action_layout)
        
        self.tabs.addTab(exec_tab, "Executar")
        
        # --- TAB: Histórico ---
        hist_tab = QWidget()
        hist_layout = QVBoxLayout(hist_tab)
        self.history_view = HistoryView()
        hist_layout.addWidget(self.history_view)
        self.tabs.addTab(hist_tab, "Histórico")
        
        # Initial refresh
        self._refresh_project()
        
    def _subscribe_events(self):
        event_bus.subscribe(ComparisonProgressEvent, self._on_progress)
        event_bus.subscribe(ComparisonFinishedEvent, self._on_finished)
        
    def _refresh_project(self):
        proj = self.controller.context.get_current_project()
        if proj:
            self.project_label.setText(f"Projeto: {proj.name}")
        else:
            self.project_label.setText("Projeto: Nenhum")
            
    def _select_file(self, key: str, filter_str: str):
        path, _ = QFileDialog.getOpenFileName(self, f"Selecionar {key}", "", filter_str)
        if path:
            self.inputs_paths[key] = path
            
    def _select_out_dir(self):
        path = QFileDialog.getExistingDirectory(self, "Selecionar Pasta de Saída")
        if path:
            self.output_dir = path
            
    def _on_execute(self):
        if not self.output_dir:
            return
            
        comp_type_name = self.combo_type.currentText()
        comp_type_id = "shp_metrica" # map name to ID based on combo box in real app
        
        self.btn_execute.setEnabled(False)
        self.progress_bar.reset()
        
        try:
            self.controller.start_comparison(comp_type_id, self.inputs_paths, self.output_dir)
        except Exception as e:
            self.progress_bar.set_progress(0, f"Erro: {str(e)}")
            self.btn_execute.setEnabled(True)
            
    @Slot(object)
    def _on_progress(self, event: ComparisonProgressEvent):
        self.progress_bar.set_progress(event.percentage, event.message)
        
    @Slot(object)
    def _on_finished(self, event: ComparisonFinishedEvent):
        self.btn_execute.setEnabled(True)
        if event.success:
            self.progress_bar.set_progress(100, f"Concluído. {event.discrepancies} divergências.")
        else:
            self.progress_bar.set_progress(0, f"Falhou: {event.error_message}")
            
