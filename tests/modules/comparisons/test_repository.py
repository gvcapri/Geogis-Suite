import pytest
from unittest.mock import MagicMock
from src.modules.comparisons.repository import ComparisonRepository

def test_create_comparison():
    session = MagicMock()
    repo = ComparisonRepository(session)
    
    repo.create_comparison(1, "Test Comp", "shp_metrica")
    
    session.add.assert_called_once()
    session.commit.assert_called_once()
    session.refresh.assert_called_once()

def test_update_status():
    session = MagicMock()
    mock_exec = MagicMock()
    session.query().filter().first.return_value = mock_exec
    
    repo = ComparisonRepository(session)
    repo.update_execution_status(1, "completed")
    
    assert mock_exec.status == "completed"
    session.commit.assert_called_once()
