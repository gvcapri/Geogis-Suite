from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QScrollArea, QFrame
from PySide6.QtCore import Qt
from src.ui.widgets.geo_card import GeoCard
from src.core.theme.theme_manager import theme_manager

class DashboardView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("dashboard_view")
        
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        
        container = QWidget()
        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(32, 24, 32, 24)
        container_layout.setSpacing(24)
        
        # Resumo
        summary_layout = QHBoxLayout()
        summary_layout.setSpacing(16)
        
        summary_layout.addWidget(self._create_stat_card("Projetos Ativos", "12"))
        summary_layout.addWidget(self._create_stat_card("Pendências", "5"))
        summary_layout.addWidget(self._create_stat_card("Tarefas Concluídas", "47"))
        summary_layout.addWidget(self._create_stat_card("Módulos Ativos", "8"))
        
        container_layout.addLayout(summary_layout)
        
        # Grid inferior
        bottom_layout = QHBoxLayout()
        bottom_layout.setSpacing(24)
        
        recent_projects = GeoCard()
        rp_layout = QVBoxLayout(recent_projects)
        rp_title = QLabel("Projetos Recentes")
        rp_title.setStyleSheet(f"font-size: 16px; font-weight: bold; color: {theme_manager.get_color('text_main')};")
        rp_layout.addWidget(rp_title)
        rp_layout.addWidget(QLabel("1. Loteamento Residencial Sul"))
        rp_layout.addWidget(QLabel("2. Regularização Fundiária - Setor Norte"))
        rp_layout.addWidget(QLabel("3. Estudo Ambiental BR-101"))
        rp_layout.addStretch()
        
        recent_activities = GeoCard()
        ra_layout = QVBoxLayout(recent_activities)
        ra_title = QLabel("Atividades Recentes")
        ra_title.setStyleSheet(f"font-size: 16px; font-weight: bold; color: {theme_manager.get_color('text_main')};")
        ra_layout.addWidget(ra_title)
        ra_layout.addWidget(QLabel("• Planilha Métrica atualizada (há 2h)"))
        ra_layout.addWidget(QLabel("• Relatório PDF gerado (há 5h)"))
        ra_layout.addStretch()
        
        bottom_layout.addWidget(recent_projects, 1)
        bottom_layout.addWidget(recent_activities, 1)
        
        container_layout.addLayout(bottom_layout)
        container_layout.addStretch()
        
        scroll.setWidget(container)
        self.layout.addWidget(scroll)

    def _create_stat_card(self, title: str, value: str):
        card = GeoCard()
        layout = QVBoxLayout(card)
        lbl_title = QLabel(title)
        lbl_title.setStyleSheet(f"font-size: 13px; color: {theme_manager.get_color('text_sec')};")
        lbl_value = QLabel(value)
        lbl_value.setStyleSheet(f"font-size: 28px; font-weight: bold; color: {theme_manager.get_color('accent')};")
        layout.addWidget(lbl_title)
        layout.addWidget(lbl_value)
        return card

    def update_theme(self):
        pass # The cards and standard widgets update themselves if connected to theme manager, or we reload.
