from PySide6.QtWidgets import QTreeWidget, QTreeWidgetItem
from PySide6.QtCore import Signal
from typing import List

class TerritorialTreeView(QTreeWidget):
    item_selected = Signal(str, int) # entity_type, entity_id
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setHeaderHidden(True)
        self.itemClicked.connect(self._on_item_clicked)
        
    def populate(self, tree_data: List):
        self.clear()
        # Mock population
        item = QTreeWidgetItem(["Projetos"])
        self.addTopLevelItem(item)
        self.expandAll()
        
    def _on_item_clicked(self, item, column):
        entity_type = item.data(0, 1)
        entity_id = item.data(0, 2)
        if entity_type and entity_id:
            self.item_selected.emit(entity_type, entity_id)
