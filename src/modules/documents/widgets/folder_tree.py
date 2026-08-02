from PySide6.QtWidgets import QTreeWidget, QTreeWidgetItem
from PySide6.QtCore import Signal
from typing import List

class FolderTreeView(QTreeWidget):
    folder_selected = Signal(int)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setHeaderHidden(True)
        self.itemClicked.connect(self._on_item_clicked)
        
    def populate(self, folders: List):
        self.clear()
        
        # Build tree structure
        items = {}
        for folder in folders:
            item = QTreeWidgetItem([folder.name])
            item.setData(0, 1, folder.id)
            items[folder.id] = (item, folder.parent_id)
            
        for folder_id, (item, parent_id) in items.items():
            if parent_id and parent_id in items:
                items[parent_id][0].addChild(item)
            else:
                self.addTopLevelItem(item)
                
        self.expandAll()
        
    def _on_item_clicked(self, item, column):
        folder_id = item.data(0, 1)
        self.folder_selected.emit(folder_id)
