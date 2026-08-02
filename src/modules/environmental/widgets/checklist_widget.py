from PySide6.QtWidgets import QWidget, QVBoxLayout, QCheckBox, QLabel

class ChecklistWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(QLabel("Checklist Ambiental:"))
        
        # Mock items
        self.layout.addWidget(QCheckBox("APP delimitada"))
        self.layout.addWidget(QCheckBox("Reserva Legal definida"))
        self.layout.addWidget(QCheckBox("Licença anexada"))
        self.layout.addWidget(QCheckBox("Fotografias preenchidas"))
        self.layout.addStretch()
