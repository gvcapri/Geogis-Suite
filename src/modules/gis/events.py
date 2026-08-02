from dataclasses import dataclass

@dataclass
class MapStateSavedEvent:
    project_id: int
    
@dataclass
class LayerAddedEvent:
    project_id: int
    layer_name: str
