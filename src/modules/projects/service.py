from typing import List, Optional
from src.database.models import Project
from src.modules.projects.repository import ProjectRepository

class ProjectService:
    def __init__(self):
        self.repo = ProjectRepository()
        
    def list_projects(self) -> List[Project]:
        return self.repo.get_all()
        
    def create_project(self, name: str, client: str, city: str, allotment: str, registration: str, departments: List[int] = None) -> Project:
        if not name:
            raise ValueError("O nome do projeto é obrigatório.")
            
        departments = departments or []
        
        project = self.repo.create(
            name=name,
            client=client,
            city=city,
            allotment=allotment,
            registration=registration,
            departments=departments
        )
        
        # Emit event to Audit Log via EventBus in the future
        from src.core.events.event_bus import event_bus
        event_bus.publish("PROJECT_CREATED", {"project_id": project.id, "name": project.name})
        
        return project

project_service = ProjectService()
