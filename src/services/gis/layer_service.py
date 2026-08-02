try:
    import geopandas as gpd
except ImportError:
    gpd = None
from pathlib import Path
from typing import Dict, Any

class LayerService:
    def __init__(self):
        self.layers: Dict[str, gpd.GeoDataFrame] = {}
        self.layer_order: list = []
        
    def load_layer(self, layer_name: str, file_path: str) -> gpd.GeoDataFrame:
        """Loads a spatial file into a GeoDataFrame."""
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"Arquivo não encontrado: {file_path}")
            
        # Lê o arquivo utilizando geopandas (suporta SHP, GeoJSON, GPKG, etc)
        gdf = gpd.read_file(file_path)
        self.layers[layer_name] = gdf
        self.layer_order.append(layer_name)
        return gdf
        
    def get_layer(self, layer_name: str) -> gpd.GeoDataFrame:
        return self.layers.get(layer_name)
        
    def remove_layer(self, layer_name: str):
        if layer_name in self.layers:
            del self.layers[layer_name]
        if layer_name in self.layer_order:
            self.layer_order.remove(layer_name)
            
    def reorder_layer(self, layer_name: str, new_index: int):
        if layer_name in self.layer_order:
            self.layer_order.remove(layer_name)
            self.layer_order.insert(new_index, layer_name)
