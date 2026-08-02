from PySide6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QHeaderView
from typing import List, Dict, Any

class HistoryView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()
        
    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        self.table = QTableWidget(0, 4)
        self.table.setHorizontalHeaderLabels(["Data", "Usuário", "Tipo", "Resultado"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        
        layout.addWidget(self.table)
        
    def update_history(self, records: List[Dict[str, Any]]):
        self.table.setRowCount(0)
        for i, row_data in enumerate(records):
            self.table.insertRow(i)
            self.table.setItem(i, 0, QTableWidgetItem(str(row_data.get("date", ""))))
            self.table.setItem(i, 1, QTableWidgetItem(str(row_data.get("user", ""))))
            self.table.setItem(i, 2, QTableWidgetItem(str(row_data.get("type", ""))))
            self.table.setItem(i, 3, QTableWidgetItem(str(row_data.get("result", ""))))
