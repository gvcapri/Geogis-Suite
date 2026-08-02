import importlib
import logging
import os
import sys
from pathlib import Path
from typing import Dict, List, Any

logger = logging.getLogger(__name__)

def get_base_path():
    if hasattr(sys, '_MEIPASS'):
        return Path(sys._MEIPASS)
    return Path(__file__).resolve().parent.parent.parent.parent

class PluginLoader:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.modules = {}
        return cls._instance

    def discover_modules(self):
        """
        Descobre e carrega módulos dentro de src/modules/
        Por enquanto carrega o dashboard estaticamente e varre a pasta.
        """
        modules_dir = get_base_path() / "src" / "modules"
        
        if not modules_dir.exists():
            return
            
        for module_path in modules_dir.iterdir():
            if module_path.is_dir() and not module_path.name.startswith("__"):
                module_name = module_path.name
                try:
                    # Import dynamic module
                    mod = importlib.import_module(f"src.modules.{module_name}")
                    self.modules[module_name] = mod
                    logger.info(f"Módulo carregado: {module_name}")
                except Exception as e:
                    logger.error(f"Erro ao carregar módulo {module_name}: {e}")

    def get_module(self, name: str) -> Any:
        return self.modules.get(name)

plugin_loader = PluginLoader()
