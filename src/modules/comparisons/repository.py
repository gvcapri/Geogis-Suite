from typing import List, Optional
from sqlalchemy.orm import Session
from src.database.models.entities import (
    Comparison, ComparisonExecution, ComparisonResult, 
    ComparisonHistory, ComparisonTemplate
)

class ComparisonRepository:
    def __init__(self, session: Session):
        self.session = session
        
    def get_comparison(self, comparison_id: int) -> Optional[Comparison]:
        return self.session.query(Comparison).filter(Comparison.id == comparison_id).first()
        
    def get_comparisons_by_project(self, project_id: int) -> List[Comparison]:
        return self.session.query(Comparison).filter(Comparison.project_id == project_id).all()
        
    def create_comparison(self, project_id: int, name: str, comparison_type: str, template_id: Optional[int] = None) -> Comparison:
        comparison = Comparison(
            project_id=project_id,
            name=name,
            comparison_type=comparison_type,
            template_id=template_id
        )
        self.session.add(comparison)
        self.session.commit()
        self.session.refresh(comparison)
        return comparison
        
    def create_execution(self, comparison_id: int, user_id: int) -> ComparisonExecution:
        execution = ComparisonExecution(
            comparison_id=comparison_id,
            user_id=user_id,
            status="running"
        )
        self.session.add(execution)
        self.session.commit()
        self.session.refresh(execution)
        return execution
        
    def update_execution_status(self, execution_id: int, status: str, completed_at=None):
        execution = self.session.query(ComparisonExecution).filter(ComparisonExecution.id == execution_id).first()
        if execution:
            execution.status = status
            if completed_at:
                execution.completed_at = completed_at
            self.session.commit()
            
    def create_result(self, execution_id: int, duration: int, discrepancies: int, summary: str, report_path: str) -> ComparisonResult:
        result = ComparisonResult(
            execution_id=execution_id,
            duration_seconds=duration,
            discrepancies_count=discrepancies,
            summary=summary,
            report_path=report_path
        )
        self.session.add(result)
        self.session.commit()
        self.session.refresh(result)
        return result
        
    def add_history(self, comparison_id: int, user_id: int, action: str, details: str = ""):
        history = ComparisonHistory(
            comparison_id=comparison_id,
            user_id=user_id,
            action=action,
            details=details
        )
        self.session.add(history)
        self.session.commit()
