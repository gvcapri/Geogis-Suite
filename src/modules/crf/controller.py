from PySide6.QtCore import QObject, Signal
from .service import CRFService
from .repository import CRFRepository
from src.database.db_manager import SessionLocal

class CRFController(QObject):
    process_loaded = Signal(object)
    assistant_updated = Signal(dict)
    error_occurred = Signal(str)
    
    def __init__(self, context):
        super().__init__()
        self.context = context
        self.session = SessionLocal()
        self.repository = CRFRepository(self.session)
        self.service = CRFService(self.repository)
        
    def load_process(self, process_id: int):
        try:
            process = self.repository.get_process(process_id)
            if process:
                self.process_loaded.emit(process)
                self.run_assistant(process_id)
        except Exception as e:
            self.error_occurred.emit(str(e))
            
    def run_assistant(self, process_id: int):
        # Run Emission Assistant in background
        from src.core.jobs.job_manager import job_manager
        
        def _task():
            from .approvals.emission_assistant import EmissionAssistantService
            assistant = EmissionAssistantService(self.repository)
            return assistant.analyze(process_id)
            
        def _on_success(diagnosis):
            self.assistant_updated.emit(diagnosis)
            
        job_manager.submit(_task, on_success=_on_success)
