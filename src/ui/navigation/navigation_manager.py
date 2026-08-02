from PySide6.QtWidgets import QStackedWidget, QWidget

class NavigationManager:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.stack = None
            cls._instance.pages = {}
        return cls._instance

    def register_page(self, page_id: str, widget: QWidget):
        if self.stack is None:
            self.stack = QStackedWidget()
        if page_id not in self.pages:
            index = self.stack.addWidget(widget)
            self.pages[page_id] = index

    def navigate_to(self, page_id: str):
        if page_id in self.pages:
            self.stack.setCurrentIndex(self.pages[page_id])
            return True
        return False

    def get_stack(self) -> QStackedWidget:
        if self.stack is None:
            self.stack = QStackedWidget()
        return self.stack

navigation_manager = NavigationManager()
