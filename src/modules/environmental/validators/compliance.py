import datetime

class ComplianceService:
    def __init__(self, repository):
        self.repository = repository
        
    def generate_snapshot(self, process_id: int) -> dict:
        """
        Calculates compliance indexes for an environmental process.
        Returns a dict structured for UI consumption (🟢🟡🔴 indicators).
        """
        snapshot = {
            "licenses": {"score": 0, "status": "gray", "message": "Nenhuma licença"},
            "conditionants": {"score": 0, "status": "gray", "message": "Nenhuma condicionante"},
            "overall_health": 0
        }
        
        # 1. Licenses
        licenses = self.repository.get_licenses(process_id)
        if licenses:
            valid = 0
            near_expiry = 0
            expired = 0
            now = datetime.datetime.utcnow()
            for lic in licenses:
                if not lic.expiry_date: continue
                days_left = (lic.expiry_date - now).days
                if days_left < 0:
                    expired += 1
                elif days_left <= 30:
                    near_expiry += 1
                else:
                    valid += 1
                    
            if expired > 0:
                snapshot["licenses"] = {"status": "red", "message": f"{expired} vencidas!"}
            elif near_expiry > 0:
                snapshot["licenses"] = {"status": "yellow", "message": f"{near_expiry} vencem em <30d"}
            else:
                snapshot["licenses"] = {"status": "green", "message": "100% válidas"}
                
        # 2. Conditionants
        # Stub: logic to check if conditionants are overdue
        snapshot["conditionants"] = {"status": "green", "message": "Todas em dia"}
        
        return snapshot
