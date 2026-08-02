import sys
import os
import ctypes

# Fix sys.path to run from root
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from PySide6.QtWidgets import QApplication
from src.core.logger.log_manager import setup_logger
from src.ui.main_window.main_window import MainWindow

def main():
    try:
        myappid = 'geogis.gerenciador_scripts.2.0'
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
    except Exception:
        pass

    setup_logger()

    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    
    # Initialize services
    from src.services.audit_service import audit_service
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
