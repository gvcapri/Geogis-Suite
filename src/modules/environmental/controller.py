from PySide6.QtCore import QObject, Signal
from .service import EnvironmentalService
from .repository import EnvironmentalRepository
from src.database.db_manager import SessionLocal
from src.core.events.event_bus import event_bus

class EnvironmentalController(QObject):
    process_loaded = Signal(object)
    compliance_updated = Signal(dict)
    error_occurred = Signal(str)
    
    def __init__(self, context):
        super().__init__()
        self.context = context
        self.session = SessionLocal()
        self.repository = EnvironmentalRepository(self.session)
        self.service = EnvironmentalService(self.repository)
        
        event_bus.subscribe("gis.feature_clicked", self._on_gis_feature_clicked)
        
    def load_environmental_process(self, process_id: int):
        try:
            process = self.repository.get_process(process_id)
            if process:
                self.process_loaded.emit(process)
                self._update_compliance(process_id)
        except Exception as e:
            self.error_occurred.emit(str(e))
            
    def _update_compliance(self, process_id: int):
        # Fire async compliance calculation
        from src.core.jobs.job_manager import job_manager
        
        def _calc():
            return self.service.calculate_compliance(process_id)
            
        def _on_success(compliance_data):
            self.compliance_updated.emit(compliance_data)
            
        job_manager.submit(_calc, on_success=_on_success)

    def _on_gis_feature_clicked(self, event):
        feature_id = event.get("feature_id")
        if not feature_id: return
        # Find if it's an APP, Reserve, etc.
        # Fire signal to UI to change tabs
        pass
