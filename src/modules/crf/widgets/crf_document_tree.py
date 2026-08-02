from PySide6.QtWidgets import QTreeWidget, QTreeWidgetItem
from PySide6.QtCore import Signal

class CRFDocumentTree(QTreeWidget):
    document_selected = Signal(int)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setHeaderLabel("Pastas Lógicas do Processo")
        self._populate_folders()
        
    def _populate_folders(self):
        folders = ["Minutas", "Revisões", "Versão Final", "ART", "Mapas", "Memorial", "Relatórios", "Anexos"]
        for f in folders:
            item = QTreeWidgetItem([f])
            self.addTopLevelItem(item)
