class SelectionService:
    @staticmethod
    def select_by_point(gdf, point):
        """Returns features intersecting the point."""
        return gdf[gdf.intersects(point)]
        
    @staticmethod
    def select_by_attribute(gdf, column, value):
        return gdf[gdf[column] == value]
