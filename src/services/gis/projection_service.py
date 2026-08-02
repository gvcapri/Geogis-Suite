class ProjectionService:
    @staticmethod
    def reproject(gdf, target_crs):
        if gdf.crs and gdf.crs != target_crs:
            return gdf.to_crs(target_crs)
        return gdf