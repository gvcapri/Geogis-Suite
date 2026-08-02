import sys
from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QStackedWidget
from src.core.theme.theme_manager import theme_manager
from src.ui.sidebar.geo_sidebar import GeoSidebar
from src.ui.header.geo_header import GeoHeader
from src.ui.statusbar.geo_status_bar import GeoStatusBar
from src.ui.navigation.navigation_manager import navigation_manager
from src.modules.auth.login_view import LoginView
from src.services.auth_service import auth_service
from PySide6.QtGui import QIcon
from pathlib import Path

def get_base_path():
    if hasattr(sys, '_MEIPASS'):
        return Path(sys._MEIPASS)
    return Path(__file__).resolve().parent.parent.parent.parent

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("GEOGIS Suite - Enterprise Platform")
        self.setMinimumSize(1280, 800)
        
        icon_path = get_base_path() / "Gerenciador de scripts" / "icone_geogis.png"
        if icon_path.exists():
            self.setWindowIcon(QIcon(str(icon_path)))
            
        self.root_stack = QStackedWidget()
        self.setCentralWidget(self.root_stack)
        
        # Pagina 0: Login
        self.login_view = LoginView()
        self.login_view.login_successful.connect(self.on_login_success)
        self.root_stack.addWidget(self.login_view)
        
        # Pagina 1: Main App
        self.main_app_widget = QWidget()
        self.main_app_widget.setObjectName("central_widget")
        self.root_stack.addWidget(self.main_app_widget)
        
        main_layout = QHBoxLayout(self.main_app_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        self.sidebar = GeoSidebar()
        main_layout.addWidget(self.sidebar)
        
        right_container = QWidget()
        right_container.setObjectName("right_container")
        right_layout = QVBoxLayout(right_container)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(0)
        main_layout.addWidget(right_container, 1)
        
        self.header = GeoHeader()
        self.header.btn_theme.clicked.connect(self.toggle_theme)
        right_layout.addWidget(self.header)
        
        # Area Central
        self.content_stack = navigation_manager.get_stack()
        right_layout.addWidget(self.content_stack, 1)
        
        self.status_bar = GeoStatusBar()
        right_layout.addWidget(self.status_bar)
        
        theme_manager.apply_theme()
        
    def on_login_success(self):
        self.root_stack.setCurrentIndex(1)
        user = auth_service.get_current_user()
        self.header.set_title(f"Bem-vindo, {user.name}", "Setor: Nenhum")
        
        # Auditoria
        from src.core.events.event_bus import event_bus
        event_bus.publish("USER_LOGGED_IN", {"name": user.name})
        
        # Carrega modulos de acordo com permissoes
        self.setup_modules()
        
    def setup_modules(self):
        user = auth_service.get_current_user()
        is_admin = user and user.has_permission("all")
        
        # Fake modules to test UI
        self.sidebar.add_category("Geral")
        self.sidebar.add_module_route("dashboard", "Dashboard", 'mdi.view-dashboard')
        self.sidebar.add_module_route("projects", "Projetos", 'mdi.folder-multiple')
        
        # Acesso aos Comparativos
        self.sidebar.add_category("Ferramentas")
        self.sidebar.add_module_route("comparisons", "Comparativos", 'mdi.file-compare')
        
        # Settings (Apenas Administrador)
        if is_admin:
            self.sidebar.add_category("Administração")
            self.sidebar.add_module_route("users", "Usuários", 'mdi.account-multiple')
            self.sidebar.add_module_route("settings", "Configurações", 'mdi.cog')
        
        # Load dashboard view
        from src.modules.dashboard.view import DashboardView
        self.dashboard_view = DashboardView()
        navigation_manager.register_page("dashboard", self.dashboard_view)
        
        # Load projects view
        from src.modules.projects.view import ProjectsView
        self.projects_view = ProjectsView()
        navigation_manager.register_page("projects", self.projects_view)
        
        # Load comparisons view
        from src.modules.comparisons.module import ComparisonsModule
        from src.database.db_manager import SessionLocal
        
        class MockContext:
            def get_db_session(self): return SessionLocal()
            def get_current_project(self): return None
            def get_current_user(self): return user
            
        self.comparisons_module = ComparisonsModule(MockContext())
        navigation_manager.register_page("comparisons", self.comparisons_module.get_view())
        
        # Load documents view
        from src.modules.documents import DocumentsModule
        self.documents_module = DocumentsModule(MockContext())
        navigation_manager.register_page("documents", self.documents_module.get_view())
        
        # Load GIS view
        from src.modules.gis import GISModule
        self.gis_module = GISModule(MockContext())
        navigation_manager.register_page("gis", self.gis_module.get_view())
        
        # Load Territorial view
        from src.modules.territorial import TerritorialModule
        self.territorial_module = TerritorialModule(MockContext())
        navigation_manager.register_page("territorial", self.territorial_module.get_view())
        
        # Load Environmental view
        from src.modules.environmental import EnvironmentalModule
        self.environmental_module = EnvironmentalModule(MockContext())
        navigation_manager.register_page("environmental", self.environmental_module.get_view())
        
        # Load CRF view
        from src.modules.crf import CRFModule
        self.crf_module = CRFModule(MockContext())
        navigation_manager.register_page("crf", self.crf_module.get_view())
        
        # Sidebar Register
        self.sidebar.add_module_route("documents", "Documentos", 'mdi.file-document')
        self.sidebar.add_module_route("gis", "Geoprocessamento (GIS)", 'mdi.map')
        self.sidebar.add_module_route("territorial", "Cadastro Territorial", 'mdi.city')
        self.sidebar.add_module_route("environmental", "Meio Ambiente", 'mdi.leaf')
        self.sidebar.add_module_route("crf", "Reg. Fundiária (CRF)", 'mdi.file-certificate')
        
        navigation_manager.navigate_to("dashboard")
        
        self.sidebar.module_clicked.connect(self.on_module_selected)
        
    def on_module_selected(self, module_name: str):
        if module_name == "dashboard":
            navigation_manager.navigate_to("dashboard")
            self.header.set_title("GEOGIS Suite", "Dashboard Principal")
        elif module_name == "projects":
            navigation_manager.navigate_to("projects")
            self.header.set_title("Projetos", "Gerenciamento de Projetos e Workflows")
        elif module_name == "comparisons":
            navigation_manager.navigate_to("comparisons")
            self.header.set_title("Comparativos", "Comparação de bases de dados")
        elif module_name == "documents":
            navigation_manager.navigate_to("documents")
            self.header.set_title("Documentos", "GED - Gestão Eletrônica de Documentos")
        elif module_name == "gis":
            navigation_manager.navigate_to("gis")
            self.header.set_title("Geoprocessamento", "Visualização e análise de dados geográficos")
        elif module_name == "territorial":
            navigation_manager.navigate_to("territorial")
            self.header.set_title("Cadastro Territorial", "Gestão de propriedades, matrículas e lotes")
        elif module_name == "environmental":
            navigation_manager.navigate_to("environmental")
            self.header.set_title("Meio Ambiente", "Gestão de processos ambientais, licenças e APPs")
        elif module_name == "crf":
            navigation_manager.navigate_to("crf")
            self.header.set_title("Regularização Fundiária (CRF)", "Revisão e emissão documental")
            
    def toggle_theme(self):
        theme_manager.toggle_theme()
        self.header.update_theme()
        self.sidebar.update_theme()
        self.status_bar.update_theme()
        # update views inside stack if needed
