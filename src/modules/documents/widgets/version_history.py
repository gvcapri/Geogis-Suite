from PySide6.QtWidgets import QWidget, QVBoxLayout, QListWidget, QPushButton, QHBoxLayout
from PySide6.QtCore import Signal

class VersionHistoryView(QWidget):
    version_selected = Signal(int)
    sign_requested = Signal(int)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        
        self.list_widget = QListWidget()
        self.list_widget.itemSelectionChanged.connect(self._on_selection)
        self.layout.addWidget(self.list_widget)
        
        btn_layout = QHBoxLayout()
        self.btn_sign = QPushButton("Assinar Eletronicamente")
        self.btn_sign.setEnabled(False)
        self.btn_sign.clicked.connect(self._on_sign)
        btn_layout.addWidget(self.btn_sign)
        self.layout.addLayout(btn_layout)
        
        self.versions = []
        
    def populate(self, versions):
        self.versions = versions
        self.list_widget.clear()
        for v in versions:
            item_text = f"v{v.version_number} - {v.uploaded_at.strftime('%d/%m/%Y')} - {v.uploader.name if v.uploader else 'Desconhecido'}"
            self.list_widget.addItem(item_text)
            
    def _on_selection(self):
        idx = self.list_widget.currentRow()
        if idx >= 0 and idx < len(self.versions):
            version = self.versions[idx]
            self.btn_sign.setEnabled(True)
            self.version_selected.emit(version.id)
            
    def _on_sign(self):
        idx = self.list_widget.currentRow()
        if idx >= 0 and idx < len(self.versions):
            version = self.versions[idx]
            self.sign_requested.emit(version.id)
