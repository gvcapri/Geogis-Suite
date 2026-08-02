from PySide6.QtWidgets import QTabWidget, QWidget, QVBoxLayout, QLabel

class EnvironmentalTabs(QTabWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Stubs for the tabs
        self.addTab(self._create_stub("Lista de APPs e Reservas Legais"), "Geometrias")
        self.addTab(self._create_stub("Tabela de Licenças e Condicionantes"), "Licenças")
        self.addTab(self._create_stub("Histórico de Inspeções"), "Inspeções")
        
    def _create_stub(self, text: str):
        w = QWidget()
        l = QVBoxLayout(w)
        l.addWidget(QLabel(text))
        return w
