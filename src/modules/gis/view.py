from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QSplitter, QFileDialog, QMessageBox
from PySide6.QtCore import Qt
from .widgets.map_canvas import MapCanvas
from .widgets.layer_panel import LayerPanel
from .widgets.properties_panel import PropertiesPanel
from .widgets.toolbar import MapToolbar
from .widgets.status_bar import MapStatusBar

class GISView(QWidget):
    def __init__(self, controller, parent=None):
        super().__init__(parent)
        self.controller = controller
        self._setup_ui()
        self._connect_signals()
        
    def _setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Toolbar
        self.toolbar = MapToolbar()
        main_layout.addWidget(self.toolbar)
        
        # Splitter
        self.splitter = QSplitter(Qt.Horizontal)
        main_layout.addWidget(self.splitter, 1) # Give stretch factor 1
        
        # Left Panel (Layers)
        self.layer_panel = LayerPanel()
        self.splitter.addWidget(self.layer_panel)
        
        # Center (Map + Status)
        center_widget = QWidget()
        center_layout = QVBoxLayout(center_widget)
        center_layout.setContentsMargins(0, 0, 0, 0)
        center_layout.setSpacing(0)
        
        self.canvas = MapCanvas()
        center_layout.addWidget(self.canvas, 1)
        
        self.status_bar = MapStatusBar()
        center_layout.addWidget(self.status_bar)
        
        self.splitter.addWidget(center_widget)
        
        # Right Panel (Properties)
        self.properties_panel = PropertiesPanel()
        self.splitter.addWidget(self.properties_panel)
        
        self.splitter.setSizes([200, 600, 250])
        
    def _connect_signals(self):
        self.toolbar.action_add_layer.triggered.connect(self._on_add_layer)
        self.controller.layer_loaded.connect(self._on_layer_loaded)
        self.controller.error_occurred.connect(self._on_error)
        
    def _on_add_layer(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Adicionar Camada Vetorial", "", 
            "Shapefiles (*.shp);;GeoJSON (*.geojson);;Todos os Arquivos (*.*)"
        )
        if file_path:
            import os
            layer_name = os.path.basename(file_path)
            self.controller.add_layer_async(layer_name, file_path)
            
    def _on_layer_loaded(self, name: str, gdf):
        self.layer_panel.add_layer(name)
        self.canvas.render_layer(name, gdf)
        self.status_bar.features_label.setText(f"Feições: {len(gdf)}")
        
    def _on_error(self, err_msg: str):
        QMessageBox.critical(self, "Erro no GIS", f"Ocorreu um erro:\n{err_msg}")
