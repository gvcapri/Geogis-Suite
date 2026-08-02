from pathlib import Path
from typing import Dict
from .service import ComparisonService
from .repository import ComparisonRepository

class ComparisonsController:
    def __init__(self, context):
        self.context = context
        self.db_session = context.get_db_session()
        self.repository = ComparisonRepository(self.db_session)
        self.service = ComparisonService(self.repository)
        self._register_comparators()
        
    def _register_comparators(self):
        # Register comparators dynamically or statically
        # e.g., self.service.register_comparator("shp_mt", SHPMetricaComparator)
        pass

    def start_comparison(self, comparison_type: str, inputs: Dict[str, str], output_dir: str):
        project = self.context.get_current_project()
        user = self.context.get_current_user()
        if not project:
            raise ValueError("No active project.")
            
        path_inputs = {k: Path(v) for k, v in inputs.items()}
        out_path = Path(output_dir)
        
        execution_id = self.service.execute_comparison_async(
            project.id, user.id, comparison_type, path_inputs, out_path
        )
        return execution_id
