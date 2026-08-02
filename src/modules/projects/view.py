from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QPushButton, QTableWidget, QTableWidgetItem, QHeaderView)
from PySide6.QtCore import Qt
from src.core.theme.theme_manager import theme_manager
from src.modules.projects.service import project_service

class ProjectsView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(30, 30, 30, 30)
        self.layout.setSpacing(20)
        
        # Header Area
        header_layout = QHBoxLayout()
        title = QLabel("Projetos")
        title.setStyleSheet(f"font-size: 24px; font-weight: bold; color: {theme_manager.get_color('text_main')}")
        header_layout.addWidget(title)
        
        self.btn_new = QPushButton("+ Novo Projeto")
        self.btn_new.setFixedSize(140, 40)
        self.btn_new.setStyleSheet(f"""
            QPushButton {{
                background-color: {theme_manager.get_color('accent')};
                color: white;
                font-weight: bold;
                border-radius: 6px;
            }}
            QPushButton:hover {{
                background-color: {theme_manager.get_color('accent_hover')};
            }}
        """)
        header_layout.addWidget(self.btn_new, alignment=Qt.AlignRight)
        
        self.layout.addLayout(header_layout)
        
        # Table
        self.table = QTableWidget(0, 5)
        self.table.setHorizontalHeaderLabels(["ID", "Nome", "Cliente", "Status", "Data"])
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.table.setStyleSheet(f"""
            QTableWidget {{
                background-color: {theme_manager.get_color('bg_card')};
                border: 1px solid {theme_manager.get_color('border')};
                border-radius: 8px;
                color: {theme_manager.get_color('text_main')};
            }}
            QHeaderView::section {{
                background-color: {theme_manager.get_color('sidebar_bg')};
                padding: 4px;
                border: none;
                border-bottom: 1px solid {theme_manager.get_color('border')};
                font-weight: bold;
            }}
        """)
        self.layout.addWidget(self.table)
        
        self.load_data()
        
    def load_data(self):
        projects = project_service.list_projects()
        self.table.setRowCount(len(projects))
        
        for row, p in enumerate(projects):
            self.table.setItem(row, 0, QTableWidgetItem(str(p.id)))
            self.table.setItem(row, 1, QTableWidgetItem(p.name))
            self.table.setItem(row, 2, QTableWidgetItem(p.client))
            self.table.setItem(row, 3, QTableWidgetItem(p.status))
            date_str = p.created_at.strftime("%d/%m/%Y") if p.created_at else ""
            self.table.setItem(row, 4, QTableWidgetItem(date_str))
