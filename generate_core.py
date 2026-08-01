import os

root_dir = r"c:\Users\guilh\OneDrive\Desktop\Geogis-Suite"

files_to_create = {
    r"src\core\project_context.py": """class ProjectContext:
    def __init__(self, project_id: int, client_id: int, name: str):
        self.project_id = project_id
        self.client_id = client_id
        self.name = name
""",
    r"src\services\files\__init__.py": "",
    r"src\services\files\file_service.py": """class FileService:\n    pass""",
    r"src\services\files\pdf_service.py": """class PDFService:\n    pass""",
    r"src\services\files\excel_service.py": """class ExcelService:\n    pass""",
    r"src\services\files\word_service.py": """class WordService:\n    pass""",
    r"src\services\files\shapefile_service.py": """class ShapefileService:\n    pass""",
    r"src\services\files\image_service.py": """class ImageService:\n    pass""",
    r"src\services\files\archive_service.py": """class ArchiveService:\n    pass""",
    
    r"src\services\gis\__init__.py": "",
    r"src\services\gis\geometry_service.py": """class GeometryService:\n    pass""",
    r"src\services\gis\projection_service.py": """class ProjectionService:\n    pass""",
    r"src\services\gis\map_service.py": """class MapService:\n    pass""",
    r"src\services\gis\spatial_service.py": """class SpatialService:\n    pass""",
    r"src\services\gis\coordinate_service.py": """class CoordinateService:\n    pass""",
    r"src\services\gis\geopackage_service.py": """class GeopackageService:\n    pass""",

    r"src\core\jobs\__init__.py": "",
    r"src\core\jobs\job_manager.py": """class JobManager:\n    pass""",
    r"src\core\jobs\task_queue.py": """class TaskQueue:\n    pass""",
    r"src\core\jobs\worker_pool.py": """class WorkerPool:\n    pass""",
    r"src\core\jobs\background_worker.py": """class BackgroundWorker:\n    pass""",
    r"src\core\jobs\progress_manager.py": """class ProgressManager:\n    pass""",

    r"src\core\events\__init__.py": "",
    r"src\core\events\event_bus.py": """class EventBus:
    def __init__(self):
        self._subscribers = {}
    def subscribe(self, event_type, callback):
        if event_type not in self._subscribers:
            self._subscribers[event_type] = []
        self._subscribers[event_type].append(callback)
    def publish(self, event_type, data):
        for callback in self._subscribers.get(event_type, []):
            callback(data)
""",
    
    r"src\core\plugin_loader.py": """import os
class PluginLoader:
    def __init__(self, modules_dir):
        self.modules_dir = modules_dir
    def load_plugins(self):
        pass
""",
    r"src\core\search_engine.py": """class SearchEngine:
    def search(self, query: str):
        pass
""",
    r"src\modules\notifications\__init__.py": "",
    r"src\modules\notifications\notification_center.py": """class NotificationCenter:
    def add_notification(self, title, message, type="info"):
        pass
""",
    r"src\modules\workflow\__init__.py": "",
    r"src\modules\workflow\workflow_engine.py": """class WorkflowEngine:
    def start_workflow(self, project_id, workflow_name):
        pass
"""
}

for rel_path, content in files_to_create.items():
    path = os.path.join(root_dir, rel_path)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

print("Core services generated.")
