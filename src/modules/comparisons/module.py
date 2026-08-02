from src.modules.comparisons.view import ComparisonsView
from src.modules.comparisons.controller import ComparisonsController

class ComparisonsModule:
    """Entry point for the Comparisons module to be loaded by the main application."""
    
    name = "Comparativos"
    version = "1.0.0"
    
    def __init__(self, context):
        self.context = context
        self.controller = ComparisonsController(context)
        
    def get_view(self):
        return ComparisonsView(self.controller)
        
    def get_permissions(self):
        return [
            "comparisons.execute",
            "comparisons.view_results",
            "comparisons.delete_results",
            "comparisons.export_reports",
            "comparisons.approve_results"
        ]
        
    def get_dashboard_cards(self):
        """Returns statistics for the dashboard."""
        return [
            {"title": "Comparativos hoje", "value": "18", "type": "info"},
            {"title": "Pendentes", "value": "3", "type": "warning"},
            {"title": "Último resultado", "value": "Vista Verde", "type": "success"},
            {"title": "Tempo médio", "value": "2m34s", "type": "info"}
        ]
        
    def register(self):
        # Register into main context
        pass
