from dataclasses import dataclass

@dataclass
class AppSelectedEvent:
    app_id: int
    gis_feature_id: str
    
@dataclass
class InspectionCreatedEvent:
    inspection_id: int
    process_id: int
