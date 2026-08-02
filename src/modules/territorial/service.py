from typing import Dict, Any, List
from .repository import TerritorialRepository
from .validators.data_quality import DataQualityService

class TerritorialService:
    def __init__(self, repository: TerritorialRepository):
        self.repository = repository
        self.data_quality = DataQualityService(repository)
        
    def get_territorial_tree(self) -> List[Dict]:
        """Returns the hierarchical tree: Municipality -> Neighborhood -> Subdivision -> Block -> Lot."""
        # For this MVP stub, we return an empty structure or mock.
        return self.repository.get_full_tree()
        
    def search_global(self, query: str) -> List[Dict]:
        """Searches across all territorial entities."""
        return self.repository.search(query)
        
    def validate_data_quality(self, entity_type: str, entity_id: int) -> List[str]:
        """Runs the Data Quality module validations in background."""
        return self.data_quality.run_validations(entity_type, entity_id)
