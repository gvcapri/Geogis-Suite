class GeometryService:
    @staticmethod
    def get_bounds(gdf):
        """Returns the bounding box of a GeoDataFrame."""
        return gdf.total_bounds
        
    @staticmethod
    def calculate_area(geometry):
        """Calculates area of a shapely geometry."""
        return geometry.area
        
    @staticmethod
    def calculate_length(geometry):
        """Calculates length/perimeter of a shapely geometry."""
        return geometry.length