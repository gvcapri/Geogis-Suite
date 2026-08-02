from dataclasses import dataclass

@dataclass
class DocumentUploadedEvent:
    document_id: int
    version_id: int
    project_id: int

@dataclass
class DocumentSignedEvent:
    version_id: int
    signature_id: int
