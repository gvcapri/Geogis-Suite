from sqlalchemy.orm import Session

class GISRepository:
    def __init__(self, session: Session):
        self.session = session
        
    # Stub for saving/loading map states linked to Project ID
