from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton

class GeoSidebar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setStyleSheet("background: #2c3e50; color: white;")
        self.setFixedWidth(250)
