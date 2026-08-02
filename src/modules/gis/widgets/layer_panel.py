from PySide6.QtWidgets import QListWidget, QListWidgetItem, QWidget, QVBoxLayout
from PySide6.QtCore import Qt

class LayerPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        self.list_widget = QListWidget()
        self.list_widget.setDragDropMode(QListWidget.InternalMove)
        layout.addWidget(self.list_widget)
        
    def add_layer(self, name: str):
        item = QListWidgetItem(name)
        item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
        item.setCheckState(Qt.Checked)
        self.list_widget.insertItem(0, item) # Add to top
