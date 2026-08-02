from dataclasses import dataclass

@dataclass
class LotSelectedEvent:
    lot_id: int
    gis_feature_id: str

@dataclass
class EntityUpdatedEvent:
    entity_type: str
    entity_id: int
    changes: dict
