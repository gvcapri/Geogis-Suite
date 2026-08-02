from PySide6.QtCore import QObject, Signal
from .service import TerritorialService
from .repository import TerritorialRepository
from src.database.db_manager import SessionLocal
from src.core.events.event_bus import event_bus
from .events import LotSelectedEvent

class TerritorialController(QObject):
    data_loaded = Signal(object)
    search_results = Signal(list)
    error_occurred = Signal(str)
    
    def __init__(self, context):
        super().__init__()
        self.context = context
        self.session = SessionLocal()
        self.repository = TerritorialRepository(self.session)
        self.service = TerritorialService(self.repository)
        
        # Escutar eventos externos (ex: clique no mapa)
        event_bus.subscribe("gis.feature_clicked", self._on_feature_clicked)
        
    def load_tree_data(self):
        try:
            data = self.service.get_territorial_tree()
            self.data_loaded.emit(data)
        except Exception as e:
            self.error_occurred.emit(str(e))
            
    def perform_search(self, query: str):
        try:
            results = self.service.search_global(query)
            self.search_results.emit(results)
        except Exception as e:
            self.error_occurred.emit(str(e))
            
    def select_lot_in_map(self, lot_id: int):
        lot = self.repository.get_lot(lot_id)
        if lot and lot.gis_feature_id:
            event_bus.publish("territorial.lot_selected", LotSelectedEvent(lot_id=lot_id, gis_feature_id=lot.gis_feature_id))
            
    def _on_feature_clicked(self, event):
        # Callback when user clicks a feature in the GIS map
        feature_id = event.get("feature_id")
        if not feature_id: return
        lot = self.repository.get_lot_by_feature_id(feature_id)
        if lot:
            pass # TODO: Signal view to open this lot's form
