from .repository import EnvironmentalRepository
from .validators.compliance import ComplianceService

class EnvironmentalService:
    def __init__(self, repository: EnvironmentalRepository):
        self.repository = repository
        self.compliance = ComplianceService(repository)
        
    def calculate_compliance(self, process_id: int) -> dict:
        """Runs the background compliance checks and returns a snapshot."""
        return self.compliance.generate_snapshot(process_id)
