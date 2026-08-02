from PySide6.QtWidgets import QWidget, QHBoxLayout, QLineEdit, QPushButton
from PySide6.QtCore import Signal

class SearchBar(QWidget):
    search_triggered = Signal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        self.input = QLineEdit()
        self.input.setPlaceholderText("Pesquisa global (CPF, Proprietário, Lote, Código)...")
        self.input.returnPressed.connect(self._on_search)
        
        self.btn_search = QPushButton("Buscar")
        self.btn_search.clicked.connect(self._on_search)
        
        layout.addWidget(self.input)
        layout.addWidget(self.btn_search)
        
    def _on_search(self):
        query = self.input.text().strip()
        if query:
            self.search_triggered.emit(query)
