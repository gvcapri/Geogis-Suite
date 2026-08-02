from dataclasses import dataclass

@dataclass
class ProcessStatusChangedEvent:
    process_id: int
    old_status: str
    new_status: str
    
@dataclass
class DocumentRevisionCreatedEvent:
    document_id: int
    revision_id: int
