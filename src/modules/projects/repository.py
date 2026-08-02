from typing import List, Optional
from src.database.db_manager import SessionLocal
from src.database.models import Project, Department

class ProjectRepository:
    def get_all(self) -> List[Project]:
        db = SessionLocal()
        try:
            return db.query(Project).all()
        finally:
            db.close()
            
    def get_by_id(self, project_id: int) -> Optional[Project]:
        db = SessionLocal()
        try:
            return db.query(Project).filter(Project.id == project_id).first()
        finally:
            db.close()
            
    def create(self, name: str, client: str, city: str, allotment: str, registration: str, departments: List[int]) -> Project:
        db = SessionLocal()
        try:
            project = Project(
                name=name,
                client=client,
                city=city,
                allotment=allotment,
                registration=registration
            )
            
            if departments:
                depts = db.query(Department).filter(Department.id.in_(departments)).all()
                project.departments.extend(depts)
                
            db.add(project)
            db.commit()
            db.refresh(project)
            
            # The session is closed in finally, so if we want to return a detached instance:
            # We can use expunge or return data dict. For now we just return the object, 
            # though accessing relationships after session close might fail (DetachedInstanceError).
            # To fix this properly, we expunge:
            db.expunge(project)
            return project
        except Exception as e:
            db.rollback()
            raise e
        finally:
            db.close()
