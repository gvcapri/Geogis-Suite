from PySide6.QtGui import QPainterPath, QPolygonF
from PySide6.QtCore import QPointF

class RenderService:
    @staticmethod
    def geometry_to_path(geometry) -> QPainterPath:
        """Converts a Shapely geometry into a QPainterPath for rendering."""
        path = QPainterPath()
        
        if geometry.is_empty:
            return path
            
        geom_type = geometry.geom_type
        
        if geom_type == 'Polygon':
            RenderService._add_polygon_to_path(path, geometry)
        elif geom_type == 'MultiPolygon':
            for poly in geometry.geoms:
                RenderService._add_polygon_to_path(path, poly)
        elif geom_type == 'LineString':
            RenderService._add_linestring_to_path(path, geometry)
        elif geom_type == 'MultiLineString':
            for line in geometry.geoms:
                RenderService._add_linestring_to_path(path, line)
        elif geom_type == 'Point':
            x, y = geometry.x, geometry.y
            path.addEllipse(QPointF(x, y), 2, 2)
            
        return path

    @staticmethod
    def _add_polygon_to_path(path: QPainterPath, polygon):
        exterior = polygon.exterior
        if not exterior:
            return
        
        coords = list(exterior.coords)
        poly = QPolygonF([QPointF(x, y) for x, y in coords])
        path.addPolygon(poly)
        
        for interior in polygon.interiors:
            int_coords = list(interior.coords)
            int_poly = QPolygonF([QPointF(x, y) for x, y in int_coords])
            path.addPolygon(int_poly)
            
    @staticmethod
    def _add_linestring_to_path(path: QPainterPath, linestring):
        coords = list(linestring.coords)
        if not coords:
            return
        path.moveTo(coords[0][0], coords[0][1])
        for x, y in coords[1:]:
            path.lineTo(x, y)
