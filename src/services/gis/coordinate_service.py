class CoordinateService:
    @staticmethod
    def format_coordinate(x, y, crs):
        return f"X: {x:.2f}, Y: {y:.2f} ({crs})"