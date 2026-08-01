from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from src.ui.widgets.geo_card import GeoCard

class DashboardView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        title = QLabel("Dashboard - Centro de Produtividade")
        title.setStyleSheet("font-size: 24px; font-weight: bold; margin-bottom: 20px;")
        layout.addWidget(title)
        
        card = GeoCard()
        card_layout = QVBoxLayout(card)
        card_layout.addWidget(QLabel("Projetos Recentes"))
        layout.addWidget(card)
        
        layout.addStretch()
