from abc import ABC, abstractmethod
from typing import Dict, Any, Callable
from pathlib import Path

class BaseComparator(ABC):
    name: str = "Base"
    
    @abstractmethod
    def validate(self, context: Dict[str, Any]) -> bool:
        """Validates inputs before execution."""
        pass
        
    @abstractmethod
    def execute(self, inputs: Dict[str, Path], output_dir: Path, progress_callback: Callable[[int, str], None] = None) -> Dict[str, Any]:
        """Executes the comparison logic."""
        pass
        
    @abstractmethod
    def generate_report(self, result: Dict[str, Any]) -> str:
        """Generates the report file."""
        pass
