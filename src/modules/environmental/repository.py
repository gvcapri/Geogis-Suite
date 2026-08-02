from sqlalchemy.orm import Session
from src.database.models import EnvironmentalProcess, APP, LegalReserve, License, Conditionant, EnvironmentalPhoto

class EnvironmentalRepository:
    def __init__(self, session: Session):
        self.session = session
        
    def get_process(self, process_id: int):
        return self.session.query(EnvironmentalProcess).filter(EnvironmentalProcess.id == process_id).first()
        
    def get_licenses(self, process_id: int):
        return self.session.query(License).filter(License.process_id == process_id).all()
        
    def get_conditionants(self, license_id: int):
        return self.session.query(Conditionant).filter(Conditionant.license_id == license_id).all()
        
    def get_photos(self, process_id: int):
        return self.session.query(EnvironmentalPhoto).filter(EnvironmentalPhoto.process_id == process_id).all()
