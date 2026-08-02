from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel

class GalleryWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Galeria de Fotos (Em breve)"))
