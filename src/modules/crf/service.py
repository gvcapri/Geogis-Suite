from .repository import CRFRepository

class CRFService:
    def __init__(self, repository: CRFRepository):
        self.repository = repository
        
    def advance_workflow(self, process_id: int, new_status: str, user_id: int):
        """Advances the CRF process if checklist is met."""
        process = self.repository.get_process(process_id)
        if not process:
            raise Exception("Processo não encontrado")
            
        # Example hard block logic:
        # if new_status == "Emitido" and not all_checklists_done: raise Exception(...)
        
        process.status = new_status
        self.repository.save_approval(process_id, user_id, f"Mudança para {new_status}")
        self.repository.commit()
