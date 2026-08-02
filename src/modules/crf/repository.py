from sqlalchemy.orm import Session
from src.database.models import CRFProcess, CRFDocument, CRFRevision, CRFApproval

class CRFRepository:
    def __init__(self, session: Session):
        self.session = session
        
    def get_process(self, process_id: int):
        return self.session.query(CRFProcess).filter(CRFProcess.id == process_id).first()
        
    def get_documents(self, process_id: int):
        return self.session.query(CRFDocument).filter(CRFDocument.process_id == process_id).all()
        
    def save_approval(self, process_id: int, user_id: int, action: str):
        appr = CRFApproval(process_id=process_id, user_id=user_id, action=action)
        self.session.add(appr)
        
    def commit(self):
        self.session.commit()
