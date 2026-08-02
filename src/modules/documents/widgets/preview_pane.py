from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import Qt

class PreviewPane(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        
        self.label = QLabel("Selecione um documento para visualizar")
        self.label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.label)
        
    def show_preview(self, version):
        if not version:
            self.label.setText("Selecione um documento para visualizar")
            return
            
        file_ext = version.file_path.split(".")[-1].lower()
        if file_ext == "pdf":
            # For now just show info, QtPdf requires extra dependencies
            self.label.setText(f"Preview de PDF:\n{version.file_path}")
        else:
            self.label.setText(f"Visualização não suportada para o formato: {file_ext}\nBaixe o arquivo para abrir.")
