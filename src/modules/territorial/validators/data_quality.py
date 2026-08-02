from typing import List
import logging

class DataQualityService:
    """
    Executa verificações automáticas sobre o cadastro territorial,
    sinalizando inconsistências (ex: lotes sem geometria, áreas divergentes, matrículas duplicadas).
    """
    def __init__(self, repository):
        self.repository = repository
        self.logger = logging.getLogger("DataQuality")
        
    def run_validations(self, entity_type: str, entity_id: int) -> List[str]:
        warnings = []
        if entity_type == "Lot":
            warnings.extend(self._validate_lot(entity_id))
        elif entity_type == "Subdivision":
            warnings.extend(self._validate_subdivision(entity_id))
            
        if warnings:
            self.logger.warning(f"DataQuality [ {entity_type} {entity_id} ]: {len(warnings)} avisos encontrados.")
        return warnings
        
    def _validate_lot(self, lot_id: int) -> List[str]:
        warnings = []
        lot = self.repository.get_lot(lot_id)
        if not lot:
            return ["Lote não encontrado."]
            
        if not lot.gis_feature_id:
            warnings.append("Lote não possui geometria espacial vinculada.")
            
        if not lot.nominal_area_sqm or lot.nominal_area_sqm <= 0:
            warnings.append("Área nominal ausente ou inválida.")
            
        if not lot.registries:
            warnings.append("Lote não possui matrícula vinculada.")
            
        # Stub for area divergence check (would require calling GIS GeometryService)
        # if abs(lot.nominal_area_sqm - gis_area) > tolerance: warnings.append(...)
        
        return warnings
        
    def _validate_subdivision(self, sub_id: int) -> List[str]:
        warnings = []
        # Stub for subdivision validation (e.g. sum of block areas > subdivision area)
        return warnings
