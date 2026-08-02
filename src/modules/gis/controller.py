from src.services.gis import MapService, LayerService
from src.core.jobs.job_manager import job_manager
from PySide6.QtCore import QObject, Signal

class GISController(QObject):
    layer_loaded = Signal(str, object)
    error_occurred = Signal(str)
    
    def __init__(self, context):
        super().__init__()
        self.context = context
        self.map_service = MapService()
        self.layer_service = LayerService()
        
    def load_project_state(self):
        project = self.context.get_current_project()
        if project:
            return self.map_service.load_project_map(project.id)
        return None
        
    def add_layer_async(self, layer_name: str, file_path: str):
        def _task(progress_callback=None):
            return self.layer_service.load_layer(layer_name, file_path)
            
        def _on_success(gdf):
            self.layer_loaded.emit(layer_name, gdf)
            
        def _on_error(err):
            self.error_occurred.emit(str(err))
            
        job_manager.submit(
            func=_task,
            on_success=_on_success,
            on_error=_on_error
        )
