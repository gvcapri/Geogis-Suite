import pytest
from unittest.mock import patch, MagicMock
from pathlib import Path
from src.modules.comparisons.comparators.shp_metrica import SHPMetricaComparator

def test_shp_metrica_validate():
    comp = SHPMetricaComparator()
    assert comp.validate({"inputs": {"SHP": "file.xlsx", "MT": "file.xlsx"}}) == True
    assert comp.validate({"inputs": {"SHP": "file.xlsx"}}) == False

@patch('src.modules.comparisons.comparators.shp_metrica.load_input')
@patch('src.modules.comparisons.comparators.shp_metrica.compare_sources')
@patch('src.modules.comparisons.comparators.shp_metrica.write_result')
def test_shp_metrica_execute(mock_write, mock_compare, mock_load):
    mock_load.return_value = [{"Quadra": "1", "Lote": "1"}]
    mock_compare.return_value = {"Comparacao": [{"Status": "OK"}], "Somente_SHP": [], "Somente_MT": []}
    
    comp = SHPMetricaComparator()
    inputs = {"SHP": Path("shp.xlsx"), "MT": Path("mt.xlsx")}
    result = comp.execute(inputs, Path("."), None)
    
    assert result["discrepancies"] == 0
    assert result["summary"]["shp_records"] == 1
    mock_write.assert_called_once()
