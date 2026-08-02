import time
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Callable, Type
from src.core.jobs.job_manager import job_manager
from src.core.events.event_bus import event_bus
from .repository import ComparisonRepository
from .events import ComparisonStartedEvent, ComparisonFinishedEvent, ComparisonProgressEvent
from .comparators.base import BaseComparator
# Import specific comparators later as they are implemented

class ComparisonService:
    def __init__(self, repository: ComparisonRepository):
        self.repository = repository
        self._comparators: Dict[str, Type[BaseComparator]] = {}
        
    def register_comparator(self, type_id: str, comparator_class: Type[BaseComparator]):
        self._comparators[type_id] = comparator_class
        
    def get_available_comparators(self) -> Dict[str, str]:
        return {k: v.name for k, v in self._comparators.items()}
        
    def execute_comparison_async(
        self, 
        project_id: int, 
        user_id: int, 
        comparison_type: str, 
        inputs: Dict[str, Path], 
        output_dir: Path
    ) -> int:
        
        if comparison_type not in self._comparators:
            raise ValueError(f"Unknown comparison type: {comparison_type}")
            
        # 1. Create DB records
        comp_name = self._comparators[comparison_type].name
        comparison = self.repository.create_comparison(project_id, comp_name, comparison_type)
        execution = self.repository.create_execution(comparison.id, user_id)
        self.repository.add_history(comparison.id, user_id, "executed")
        
        # 2. Fire started event
        event_bus.publish(ComparisonStartedEvent(execution.id, comparison_type, project_id))
        
        # 3. Submit to job manager
        job_manager.submit(
            self._run_job,
            on_finished=lambda res: self._on_job_finished(execution.id, res),
            on_error=lambda err: self._on_job_error(execution.id, err),
            on_progress=lambda pct, msg: self._on_job_progress(execution.id, pct, msg),
            execution_id=execution.id,
            comparison_type=comparison_type,
            inputs=inputs,
            output_dir=output_dir
        )
        
        return execution.id
        
    def _run_job(self, execution_id: int, comparison_type: str, inputs: Dict[str, Path], output_dir: Path, progress_callback: Callable[[int, str], None] = None):
        start_time = time.time()
        
        comparator_class = self._comparators[comparison_type]
        comparator = comparator_class()
        
        # This execute method must be implemented by BaseComparator implementations
        result = comparator.execute(inputs, output_dir, progress_callback)
        
        duration = int(time.time() - start_time)
        result["duration"] = duration
        return result
        
    def _on_job_progress(self, execution_id: int, percentage: int, message: str):
        event_bus.publish(ComparisonProgressEvent(execution_id, percentage, message))
        
    def _on_job_finished(self, execution_id: int, result: Dict[str, Any]):
        self.repository.update_execution_status(execution_id, "completed", datetime.utcnow())
        discrepancies = result.get("discrepancies", 0)
        report_path = result.get("output_file", "")
        summary = json.dumps(result.get("summary", {}))
        
        self.repository.create_result(execution_id, result.get("duration", 0), discrepancies, summary, report_path)
        event_bus.publish(ComparisonFinishedEvent(execution_id, True, discrepancies, report_path))
        
    def _on_job_error(self, execution_id: int, error_msg: str):
        self.repository.update_execution_status(execution_id, "error", datetime.utcnow())
        event_bus.publish(ComparisonFinishedEvent(execution_id, False, 0, "", error_msg))
