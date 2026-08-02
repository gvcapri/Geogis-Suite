import pytest
from unittest.mock import MagicMock, patch
from src.modules.comparisons.service import ComparisonService
from src.modules.comparisons.comparators.base import BaseComparator

class MockComparator(BaseComparator):
    name = "Mock"
    def validate(self, context): return True
    def execute(self, inputs, output_dir, progress):
        return {"output_file": "report.pdf", "summary": {"compared": 10}, "discrepancies": 0}
    def generate_report(self, result): return ""

def test_service_execution():
    repo = MagicMock()
    repo.create_comparison.return_value = MagicMock(id=1)
    repo.create_execution.return_value = MagicMock(id=10)
    
    service = ComparisonService(repo)
    service.register_comparator("mock", MockComparator)
    
    with patch('src.modules.comparisons.service.job_manager') as mock_jm:
        exec_id = service.execute_comparison_async(1, 1, "mock", {}, MagicMock())
        assert exec_id == 10
        mock_jm.submit.assert_called_once()
