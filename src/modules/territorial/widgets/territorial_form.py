from PySide6.QtWidgets import QWidget, QVBoxLayout, QFormLayout, QLineEdit, QPushButton, QLabel, QHBoxLayout

class TerritorialForm(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        
        self.title = QLabel("Selecione um item")
        self.title.setStyleSheet("font-size: 16px; font-weight: bold;")
        self.layout.addWidget(self.title)
        
        self.form_layout = QFormLayout()
        self.layout.addLayout(self.form_layout)
        
        self.layout.addStretch()
        
        btn_layout = QHBoxLayout()
        self.btn_save = QPushButton("Salvar")
        self.btn_map = QPushButton("Ver no Mapa")
        self.btn_map.setEnabled(False)
        
        btn_layout.addWidget(self.btn_save)
        btn_layout.addWidget(self.btn_map)
        self.layout.addLayout(btn_layout)
        
    def clear_form(self):
        while self.form_layout.count():
            item = self.form_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
                
    def load_entity(self, entity_type: str, data: dict):
        self.clear_form()
        self.title.setText(f"Detalhes: {entity_type}")
        
        for key, value in data.items():
            line_edit = QLineEdit(str(value))
            self.form_layout.addRow(key.capitalize(), line_edit)
            
        self.btn_map.setEnabled(entity_type == "Lot")
