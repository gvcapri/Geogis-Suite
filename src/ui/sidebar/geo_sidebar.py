from PySide6.QtWidgets import QFrame, QVBoxLayout, QLabel, QTreeWidget, QTreeWidgetItem, QLineEdit
from PySide6.QtCore import Qt, Signal, QSize, QTimer
import unicodedata
from PySide6.QtGui import QPixmap, QIcon
from src.core.theme.theme_manager import theme_manager
import sys
import qtawesome as qta
from pathlib import Path

def get_base_path():
    if hasattr(sys, '_MEIPASS'):
        return Path(sys._MEIPASS)
    return Path(__file__).resolve().parent.parent.parent.parent

APP_DIR = get_base_path()
ICON_PATH = APP_DIR / "Gerenciador de scripts" / "icone_geogis.png" # Manter temporario ou mover depois

class GeoSidebar(QFrame):
    item_clicked = Signal(int, object)
    module_clicked = Signal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("sidebar")
        self.setFixedWidth(340)
        
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 24, 0, 24)
        self.layout.setSpacing(0)
        
        # Logo Area
        self.logo_label = QLabel()
        self.logo_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.logo_label)
        self.layout.addSpacing(24)
        
        # Search Area
        self.search_container = QFrame()
        self.search_layout = QVBoxLayout(self.search_container)
        self.search_layout.setContentsMargins(16, 0, 16, 16)
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Buscar ferramenta...")
        self.search_input.setObjectName("search_input")
        self.search_layout.addWidget(self.search_input)
        self.layout.addWidget(self.search_container)
        
        # Timer for Search Debounce
        self.search_timer = QTimer()
        self.search_timer.setSingleShot(True)
        self.search_timer.setInterval(300)
        self.search_timer.timeout.connect(self._perform_search)
        self.search_input.textChanged.connect(lambda text: self.search_timer.start())
        
        # Empty State
        self.empty_state = QLabel("Nenhuma ferramenta encontrada.")
        self.empty_state.setObjectName("empty_state")
        self.empty_state.setAlignment(Qt.AlignCenter)
        self.empty_state.setWordWrap(True)
        self.empty_state.hide()
        self.layout.addWidget(self.empty_state)
        
        # Tree Widget for Accordion
        self.tree = QTreeWidget()
        self.tree.setHeaderHidden(True)
        self.tree.setIndentation(12)
        self.tree.setAnimated(True)
        self.tree.setFocusPolicy(Qt.NoFocus)
        self.layout.addWidget(self.tree)
        
        self.tree.itemClicked.connect(self._on_item_clicked)
        
        self.categories = {}
        self.tools_map = {}
        self.modules_map = {}
        self.update_theme()
        
    def add_category(self, name: str):
        item = QTreeWidgetItem(self.tree)
        item.setText(0, name)
        item.setExpanded(True)
        item.setFlags(Qt.ItemIsEnabled)
        
        self.categories[name] = item
        
    def add_tool(self, name: str, tool_class, index: int):
        cat_name = getattr(tool_class, "category", "Outros")
        parent_item = self.categories.get(cat_name)
        if not parent_item:
            self.add_category(cat_name)
            parent_item = self.categories[cat_name]
            
        item = QTreeWidgetItem(parent_item)
        item.setText(0, name)
        item.setToolTip(0, name)
        item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
        
        item.setData(0, Qt.UserRole, name)
        self.tools_map[id(item)] = (index, tool_class)
        self.update_tool_icon(item)
        
    def add_module_route(self, module_name: str, display_name: str, icon_name: str = 'mdi.view-dashboard'):
        item = QTreeWidgetItem(self.tree)
        item.setText(0, display_name)
        item.setToolTip(0, display_name)
        item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
        
        item.setData(0, Qt.UserRole, display_name)
        
        # Custom properties for modules
        item.setData(0, Qt.UserRole + 1, icon_name)
        
        self.modules_map[id(item)] = module_name
        self.update_tool_icon(item)

    def update_tool_icon(self, item):
        name = item.data(0, Qt.UserRole)
        if name is None:
            name = item.text(0)
            
        icon_name = item.data(0, Qt.UserRole + 1) or 'mdi.file-document-outline'
        
        if 'Métrica' in name or 'Memorial' in name:
            icon_name = 'mdi.map-marker-path'
        elif 'PDF' in name:
            icon_name = 'mdi.file-pdf-box'
        elif 'SHP' in name or 'Shape' in name:
            icon_name = 'mdi.layers-outline'
            
        color = theme_manager.get_color('sidebar_text')
        if item.isSelected():
            color = theme_manager.get_color('sidebar_active_text')
            
        icon = qta.icon(icon_name, color=color)
        item.setIcon(0, icon)

    def _on_item_clicked(self, item, column):
        if item.childCount() > 0:
            item.setExpanded(not item.isExpanded())
            return
            
        if id(item) in self.tools_map or id(item) in self.modules_map:
            # Update all icons
            for i in range(self.tree.topLevelItemCount()):
                cat_or_mod = self.tree.topLevelItem(i)
                self.update_tool_icon(cat_or_mod)
                for j in range(cat_or_mod.childCount()):
                    self.update_tool_icon(cat_or_mod.child(j))
            
            if id(item) in self.tools_map:
                index, tool_class = self.tools_map[id(item)]
                self.item_clicked.emit(index, tool_class)
            elif id(item) in self.modules_map:
                module_name = self.modules_map[id(item)]
                self.module_clicked.emit(module_name)
            
    def _remove_accents(self, input_str: str) -> str:
        nfkd_form = unicodedata.normalize('NFKD', input_str)
        return u"".join([c for c in nfkd_form if not unicodedata.combining(c)])

    def _perform_search(self):
        query = self._remove_accents(self.search_input.text().lower().strip())
        
        has_any_match = False
        for i in range(self.tree.topLevelItemCount()):
            top_item = self.tree.topLevelItem(i)
            
            if top_item.childCount() > 0:
                cat_has_visible_child = False
                for j in range(top_item.childCount()):
                    child_item = top_item.child(j)
                    tool_name = child_item.text(0)
                    
                    if query == "" or query in self._remove_accents(tool_name.lower()):
                        child_item.setHidden(False)
                        cat_has_visible_child = True
                        has_any_match = True
                    else:
                        child_item.setHidden(True)
                
                if cat_has_visible_child:
                    top_item.setHidden(False)
                    if query != "":
                        top_item.setExpanded(True)
                else:
                    top_item.setHidden(True)
            else:
                tool_name = top_item.text(0)
                if query == "" or query in self._remove_accents(tool_name.lower()):
                    top_item.setHidden(False)
                    has_any_match = True
                else:
                    top_item.setHidden(True)
                
        if not has_any_match and query != "":
            self.tree.hide()
            self.empty_state.show()
        else:
            self.tree.show()
            self.empty_state.hide()
        
    def update_theme(self):
        self.setStyleSheet(f"""
            #sidebar {{
                background-color: {theme_manager.get_color('sidebar_bg')};
                border-right: 1px solid {theme_manager.get_color('border')};
            }}
            #search_input {{
                background-color: transparent;
                border: 1px solid {theme_manager.get_color('border')};
                border-radius: 6px;
                padding: 8px 12px;
                color: {theme_manager.get_color('sidebar_text')};
                font-size: 13px;
            }}
            #search_input:focus {{
                border: 1px solid {theme_manager.get_color('accent')};
                background-color: {theme_manager.get_color('bg_card')};
            }}
            #empty_state {{
                color: {theme_manager.get_color('sidebar_text_sec')};
                font-size: 14px;
                padding: 32px 16px;
            }}
            QTreeWidget {{
                background: transparent;
                border: none;
                color: {theme_manager.get_color('sidebar_text')};
                font-size: 14px;
                outline: none;
                show-decoration-selected: 0;
            }}
            QTreeWidget::item {{
                height: 42px;
                padding: 4px 8px;
                border-radius: 8px;
                margin: 4px 16px;
                border: 1px solid transparent;
            }}
            QTreeWidget::item:hover {{
                background-color: {theme_manager.get_color('sidebar_hover')};
            }}
            QTreeWidget::item:selected {{
                background-color: {theme_manager.get_color('sidebar_active_bg')};
                color: {theme_manager.get_color('sidebar_active_text')};
                font-weight: 600;
                border: 1px solid {theme_manager.get_color('border')};
            }}
            QTreeWidget::item:has-children {{
                font-size: 12px;
                font-weight: 700;
                color: {theme_manager.get_color('sidebar_text_sec')};
                text-transform: uppercase;
                margin-top: 20px;
                margin-bottom: 8px;
                margin-left: 16px;
                height: 28px;
            }}
            QTreeWidget::item:has-children:hover {{
                background: transparent;
            }}
            QTreeWidget::branch {{
                background: transparent;
            }}
            QTreeWidget::branch:hover, QTreeWidget::branch:selected {{
                background: transparent;
            }}
            QTreeWidget::branch:has-children:!has-siblings:closed,
            QTreeWidget::branch:closed:has-children:has-siblings,
            QTreeWidget::branch:open:has-children:!has-siblings,
            QTreeWidget::branch:open:has-children:has-siblings {{
                image: none;
            }}
        """)
        
        if ICON_PATH.exists():
            pixmap = QPixmap(str(ICON_PATH)).scaled(
                140, 28, Qt.KeepAspectRatio, Qt.SmoothTransformation
            )
            self.logo_label.setStyleSheet("margin: 8px 16px;")
            self.logo_label.setPixmap(pixmap)
        else:
            self.logo_label.setText("GEOGIS")
            self.logo_label.setStyleSheet(f"font-size: 18px; font-weight: bold; color: {theme_manager.get_color('accent')}; letter-spacing: 2px;")

        for name, item in self.categories.items():
            icon = qta.icon('mdi.folder', color=theme_manager.get_color('sidebar_text_sec'))
            item.setIcon(0, icon)
            for i in range(item.childCount()):
                self.update_tool_icon(item.child(i))

