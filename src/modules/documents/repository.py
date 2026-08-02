from typing import List, Optional
from sqlalchemy.orm import Session
from src.database.models import DocumentFolder, Document, DocumentVersion, DocumentSignature

class DocumentRepository:
    def __init__(self, session: Session):
        self.session = session
        
    def get_folders_by_project(self, project_id: int) -> List[DocumentFolder]:
        return self.session.query(DocumentFolder).filter(DocumentFolder.project_id == project_id).all()
        
    def create_folder(self, project_id: int, name: str, parent_id: Optional[int] = None, is_system: bool = False) -> DocumentFolder:
        folder = DocumentFolder(project_id=project_id, name=name, parent_id=parent_id, is_system_folder=is_system)
        self.session.add(folder)
        self.session.commit()
        self.session.refresh(folder)
        return folder
        
    def ensure_system_folders(self, project_id: int):
        system_folders = ["Memorial", "CRF", "Relatórios", "Licenças", "Mapas", "PDFs", "Planilhas", "Outros"]
        existing = {f.name for f in self.get_folders_by_project(project_id) if f.is_system_folder}
        
        for name in system_folders:
            if name not in existing:
                self.create_folder(project_id, name, is_system=True)
                
    def get_documents_by_folder(self, folder_id: int) -> List[Document]:
        return self.session.query(Document).filter(Document.folder_id == folder_id).all()
        
    def create_document(self, folder_id: int, project_id: int, name: str, doc_type: str, description: str = "") -> Document:
        doc = Document(folder_id=folder_id, project_id=project_id, name=name, doc_type=doc_type, description=description)
        self.session.add(doc)
        self.session.commit()
        self.session.refresh(doc)
        return doc
        
    def add_document_version(self, document_id: int, version_number: int, file_path: str, file_size: int, file_hash: str, user_id: int) -> DocumentVersion:
        version = DocumentVersion(
            document_id=document_id,
            version_number=version_number,
            file_path=file_path,
            file_size=file_size,
            file_hash=file_hash,
            uploaded_by=user_id
        )
        self.session.add(version)
        self.session.commit()
        self.session.refresh(version)
        return version
        
    def get_versions(self, document_id: int) -> List[DocumentVersion]:
        return self.session.query(DocumentVersion).filter(DocumentVersion.document_id == document_id).order_by(DocumentVersion.version_number.desc()).all()
        
    def sign_version(self, version_id: int, user_id: int, ip_address: str, signature_hash: str) -> DocumentSignature:
        sig = DocumentSignature(
            version_id=version_id,
            user_id=user_id,
            ip_address=ip_address,
            signature_hash=signature_hash
        )
        self.session.add(sig)
        self.session.commit()
        self.session.refresh(sig)
        return sig
