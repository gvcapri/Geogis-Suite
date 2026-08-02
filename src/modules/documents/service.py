import hashlib
import os
import shutil
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime
from src.database.models import Document, DocumentVersion
from .repository import DocumentRepository
from src.core.events.event_bus import event_bus
from .events import DocumentUploadedEvent, DocumentSignedEvent

class DocumentService:
    def __init__(self, repository: DocumentRepository, storage_base_path: str):
        self.repository = repository
        self.storage_base_path = Path(storage_base_path)
        
    def init_project_folders(self, project_id: int):
        self.repository.ensure_system_folders(project_id)
        
    def _calculate_hash(self, file_path: Path) -> str:
        sha256 = hashlib.sha256()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                sha256.update(chunk)
        return sha256.hexdigest()
        
    def upload_document(self, project_id: int, folder_id: int, user_id: int, source_path: Path) -> DocumentVersion:
        # Check if a document with this name already exists in this folder
        existing_docs = self.repository.get_documents_by_folder(folder_id)
        doc = next((d for d in existing_docs if d.name == source_path.name), None)
        
        if not doc:
            doc = self.repository.create_document(folder_id, project_id, source_path.name, source_path.suffix)
            version_number = 1
        else:
            versions = self.repository.get_versions(doc.id)
            version_number = versions[0].version_number + 1 if versions else 1
            
        # Prepare storage
        target_dir = self.storage_base_path / str(project_id) / str(folder_id) / str(doc.id)
        target_dir.mkdir(parents=True, exist_ok=True)
        target_path = target_dir / f"v{version_number}_{source_path.name}"
        
        # Copy file
        shutil.copy2(source_path, target_path)
        file_size = os.path.getsize(target_path)
        file_hash = self._calculate_hash(target_path)
        
        # Save to DB
        version = self.repository.add_document_version(doc.id, version_number, str(target_path), file_size, file_hash, user_id)
        
        event_bus.publish(DocumentUploadedEvent(doc.id, version.id, project_id))
        return version
        
    def sign_document(self, version_id: int, user_id: int, ip_address: str) -> None:
        # In a real PKI system this would hash the file + timestamp + user certificate
        # Here we do a simplified internal signature hash
        signature_raw = f"{version_id}:{user_id}:{ip_address}:{datetime.utcnow().isoformat()}"
        signature_hash = hashlib.sha256(signature_raw.encode()).hexdigest()
        
        sig = self.repository.sign_version(version_id, user_id, ip_address, signature_hash)
        event_bus.publish(DocumentSignedEvent(version_id, sig.id))
