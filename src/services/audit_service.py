from src.core.events.event_bus import event_bus
from src.database.db_manager import SessionLocal
from src.database.models import AuditLog
from src.services.auth_service import auth_service

class AuditService:
    def __init__(self):
        # Assina eventos globais de auditoria
        event_bus.subscribe("USER_LOGGED_IN", self.on_user_login)
        event_bus.subscribe("PROJECT_CREATED", self.on_project_created)
        # Mais eventos podem ser assinados aqui...
        
    def log_action(self, action: str, details: str = ""):
        db = SessionLocal()
        try:
            user = auth_service.get_current_user()
            user_id = user.id if user else None
            
            audit = AuditLog(
                user_id=user_id,
                action=action,
                details=details
            )
            db.add(audit)
            db.commit()
        except Exception as e:
            db.rollback()
            print(f"Erro ao salvar audit log: {e}")
        finally:
            db.close()

    def on_user_login(self, data: dict):
        user_name = data.get("name", "Desconhecido")
        self.log_action("LOGIN", f"Usuário {user_name} entrou no sistema.")

    def on_project_created(self, data: dict):
        project_name = data.get("name", "Desconhecido")
        project_id = data.get("project_id", "?")
        self.log_action("PROJECT_CREATED", f"Projeto criado: {project_name} (ID: {project_id})")

audit_service = AuditService()
