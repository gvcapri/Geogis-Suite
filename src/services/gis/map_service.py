from typing import Dict, Any, Optional

class MapService:
    def __init__(self):
        self.current_project_id: Optional[int] = None
        self.map_state: Dict[str, Any] = {}
        
    def load_project_map(self, project_id: int):
        self.current_project_id = project_id
        # In a real scenario, this fetches the last saved map state from DB
        self.map_state = {
            "center": (0, 0),
            "zoom": 1.0,
            "crs": "EPSG:31983", # SIRGAS 2000 UTM Zone 23S as default
            "layers": []
        }
        return self.map_state
        
    def save_map_state(self, state: Dict[str, Any]):
        self.map_state = state
        # In a real scenario, save to DB