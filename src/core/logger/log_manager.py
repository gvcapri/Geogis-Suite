import logging
import sys
from pathlib import Path
from datetime import datetime

from src.core.config.settings import settings

def get_data_dir():
    if getattr(sys, 'frozen', False):
        return Path(sys.executable).parent
    return Path(__file__).resolve().parent.parent.parent.parent

LOGS_DIR = get_data_dir() / "logs"

def setup_logger():
    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    
    current_date = datetime.now().strftime("%Y-%m-%d")
    log_file = LOGS_DIR / f"app_{current_date}.log"
    
    log_level_str = settings.get("log_level", "INFO").upper()
    log_level = getattr(logging, log_level_str, logging.INFO)
    
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setFormatter(formatter)
    file_handler.setLevel(log_level)
    
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    console_handler.setLevel(log_level)
    
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    
    if not root_logger.handlers:
        root_logger.addHandler(file_handler)
        root_logger.addHandler(console_handler)

    logging.info("Sistema de logs (GEOGIS Suite) inicializado.")
