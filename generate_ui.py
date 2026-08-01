import os

root_dir = r"c:\Users\guilh\OneDrive\Desktop\Geogis-Suite"

ui_files = {
    r"src\services\theme_service.py": """class ThemeManager:
    def __init__(self):
        self.themes = {
            'light': {'primary': '#3498db', 'background': '#f5f6fa', 'text': '#2f3640'},
            'dark': {'primary': '#2980b9', 'background': '#2f3640', 'text': '#f5f6fa'},
            'corporate': {'primary': '#2c3e50', 'background': '#ecf0f1', 'text': '#2c3e50'},
        }
        self.current_theme = 'corporate'
    
    def get_style(self):
        return f"QWidget {{ background-color: {self.themes[self.current_theme]['background']}; color: {self.themes[self.current_theme]['text']}; }}"
""",
    r"src\ui\widgets\__init__.py": "",
    r"src\ui\widgets\geo_button.py": """from PySide6.QtWidgets import QPushButton

class GeoButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setStyleSheet("padding: 8px 16px; border-radius: 4px; font-weight: bold; background: #3498db; color: white;")
""",
    r"src\ui\widgets\geo_card.py": """from PySide6.QtWidgets import QFrame

class GeoCard(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("background: #ffffff; border: 1px solid #dcdde1; border-radius: 8px; padding: 15px;")
""",
    r"src\ui\widgets\geo_sidebar.py": """from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton

class GeoSidebar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setStyleSheet("background: #2c3e50; color: white;")
        self.setFixedWidth(250)
""",
    r"src\modules\dashboard\__init__.py": "",
    r"src\modules\dashboard\views.py": """from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
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
""",
    r"src\modules\dashboard\controllers.py": """class DashboardController:\n    pass\n""",
    r"src\ui\main_window.py": """from PySide6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QStackedWidget
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
""",
    r"main.py": """import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from PySide6.QtWidgets import QApplication
from src.ui.main_window import MainWindow

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
"""
}

for rel_path, content in ui_files.items():
    path = os.path.join(root_dir, rel_path)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

print("UI components and Main Window generated.")
