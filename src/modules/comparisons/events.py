from dataclasses import dataclass
from typing import Dict, Any

@dataclass
class ComparisonStartedEvent:
    execution_id: int
    comparison_type: str
    project_id: int

@dataclass
class ComparisonFinishedEvent:
    execution_id: int
    success: bool
    discrepancies: int
    report_path: str
    error_message: str = ""

@dataclass
class ComparisonProgressEvent:
    execution_id: int
    percentage: int
    message: str
