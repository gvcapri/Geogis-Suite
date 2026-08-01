from PySide6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QStackedWidget
from src.ui.widgets.geo_sidebar import GeoSidebar
from src.modules.dashboard.views import DashboardView
from src.services.theme_service import ThemeManager

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("GEOGIS Suite - Enterprise Platform")
        self.resize(1280, 800)
        
        self.theme_manager = ThemeManager()
        self.setStyleSheet(self.theme_manager.get_style())
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QHBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        self.sidebar = GeoSidebar()
        self.content_stack = QStackedWidget()
        
        layout.addWidget(self.sidebar)
        layout.addWidget(self.content_stack, 1)
        
        self.setup_modules()
        
    def setup_modules(self):
        self.dashboard_view = DashboardView()
        self.content_stack.addWidget(self.dashboard_view)
        self.content_stack.setCurrentWidget(self.dashboard_view)
