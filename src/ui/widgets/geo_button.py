from PySide6.QtWidgets import QPushButton

class GeoButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setStyleSheet("padding: 8px 16px; border-radius: 4px; font-weight: bold; background: #3498db; color: white;")
