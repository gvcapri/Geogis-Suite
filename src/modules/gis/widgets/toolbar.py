from PySide6.QtWidgets import QToolBar
from PySide6.QtGui import QAction

class MapToolbar(QToolBar):
    def __init__(self, parent=None):
        super().__init__("GIS Toolbar", parent)
        
        self.action_add_layer = QAction("Adicionar Camada", self)
        self.addAction(self.action_add_layer)
        
        self.action_pan = QAction("Mover (Pan)", self)
        self.action_pan.setCheckable(True)
        self.action_pan.setChecked(True)
        self.addAction(self.action_pan)
        
        self.action_select = QAction("Selecionar", self)
        self.action_select.setCheckable(True)
        self.addAction(self.action_select)
        
        self.action_measure = QAction("Medir", self)
        self.action_measure.setCheckable(True)
        self.addAction(self.action_measure)
