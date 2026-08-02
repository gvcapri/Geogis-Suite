from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel

class MapStatusBar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QHBoxLayout(self)
        
        self.coords_label = QLabel("X: -- Y: --")
        self.scale_label = QLabel("Escala: --")
        self.crs_label = QLabel("CRS: EPSG:31983")
        self.features_label = QLabel("Feições: 0")
        
        layout.addWidget(self.coords_label)
        layout.addWidget(self.scale_label)
        layout.addWidget(self.crs_label)
        layout.addWidget(self.features_label)
        layout.addStretch()
