from PySide6.QtWidgets import QTableWidget, QTableWidgetItem, QHeaderView
from PySide6.QtCore import Signal
from typing import List

class DocumentListView(QTableWidget):
    document_selected = Signal(int)
    
    def __init__(self, parent=None):
        super().__init__(0, 3, parent)
        self.setHorizontalHeaderLabels(["Nome", "Tipo", "Modificado"])
        self.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.setSelectionBehavior(QTableWidget.SelectRows)
        self.setEditTriggers(QTableWidget.NoEditTriggers)
        self.itemSelectionChanged.connect(self._on_selection_changed)
        
    def populate(self, documents: List):
        self.setRowCount(0)
        for i, doc in enumerate(documents):
            self.insertRow(i)
            name_item = QTableWidgetItem(doc.name)
            name_item.setData(1, doc.id)
            self.setItem(i, 0, name_item)
            self.setItem(i, 1, QTableWidgetItem(doc.doc_type))
            self.setItem(i, 2, QTableWidgetItem(str(doc.created_at.strftime("%d/%m/%Y %H:%M"))))
            
    def _on_selection_changed(self):
        items = self.selectedItems()
        if items:
            doc_id = items[0].data(1)
            self.document_selected.emit(doc_id)
