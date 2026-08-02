import sys
import logging
import ctypes
from pathlib import Path
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon

from backend.utils.logger import setup_logger
from backend.core.registry import registry
from frontend.ui.main_window import MainWindow

def get_base_path():
    if hasattr(sys, '_MEIPASS'):
        return Path(sys._MEIPASS)
    return Path(__file__).resolve().parent

def main():
    # Correção para o ícone aparecer na barra de tarefas do Windows
    try:
        myappid = 'geogis.gerenciador_scripts.1.0'
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
    except Exception:
        pass

    # Setup inicial
    setup_logger()
    logging.info("Iniciando Gerenciador de Scripts Geogis...")
    
    # Descobre todos os plugins/ferramentas na pasta backend.tools
    registry.discover_tools()
    
    # Inicializa Interface Gráfica
    app = QApplication(sys.argv)
    
    icon_path = get_base_path() / "icone_geogis.png"
    if icon_path.exists():
        app.setWindowIcon(QIcon(str(icon_path)))

    app.setStyle("Fusion")
    
    window = MainWindow()
    if icon_path.exists():
        window.setWindowIcon(QIcon(str(icon_path)))
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
