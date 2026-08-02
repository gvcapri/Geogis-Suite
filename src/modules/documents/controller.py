from pathlib import Path
from src.database.db_manager import SessionLocal
from .repository import DocumentRepository
from .service import DocumentService
from src.core.events.event_bus import event_bus
from typing import List

class DocumentsController:
    def __init__(self, context):
        self.context = context
        self.db_session = context.get_db_session()
        self.repository = DocumentRepository(self.db_session)
        
        # In production this should come from config
        from src.database.db_manager import get_data_dir
        self.storage_path = get_data_dir() / "storage" / "documents"
        
        self.service = DocumentService(self.repository, str(self.storage_path))
        
    def load_project_structure(self):
        project = self.context.get_current_project()
        if not project:
            return []
            
        self.service.init_project_folders(project.id)
        return self.repository.get_folders_by_project(project.id)
        
    def load_documents(self, folder_id: int):
        return self.repository.get_documents_by_folder(folder_id)
        
    def get_document_versions(self, document_id: int):
        return self.repository.get_versions(document_id)
        
    def upload_file(self, folder_id: int, file_path: str):
        project = self.context.get_current_project()
        user = self.context.get_current_user()
        if not project or not user:
            raise ValueError("No active project or user.")
            
        return self.service.upload_document(project.id, folder_id, user.id, Path(file_path))
        
    def sign_version(self, version_id: int):
        user = self.context.get_current_user()
        if not user:
            raise ValueError("No active user.")
            
        self.service.sign_document(version_id, user.id, "127.0.0.1")
