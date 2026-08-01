from PySide6.QtWidgets import QFrame

class GeoCard(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("background: #ffffff; border: 1px solid #dcdde1; border-radius: 8px; padding: 15px;")
