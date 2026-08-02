from PySide6.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsPathItem
from PySide6.QtGui import QPainter, QPen, QBrush, QColor
from PySide6.QtCore import Qt, QRectF
from src.services.gis.render_service import RenderService

class MapCanvas(QGraphicsView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)
        
        self.setRenderHint(QPainter.Antialiasing)
        self.setDragMode(QGraphicsView.ScrollHandDrag)
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        
    def wheelEvent(self, event):
        """Implement zooming."""
        zoom_in_factor = 1.15
        zoom_out_factor = 1 / zoom_in_factor
        
        if event.angleDelta().y() > 0:
            zoom_factor = zoom_in_factor
        else:
            zoom_factor = zoom_out_factor
            
        self.scale(zoom_factor, zoom_factor)
        
    def render_layer(self, layer_name: str, gdf):
        """Renders a GeoDataFrame to the scene using RenderService."""
        # This is basic and not optimized for huge layers without spatial indexing.
        for idx, row in gdf.iterrows():
            geom = row.geometry
            if not geom:
                continue
            path = RenderService.geometry_to_path(geom)
            
            # Note: Geo coordinates Y is up, QGraphicsView Y is down, so we need to flip Y.
            # For this MVP stub, we just add the path as is.
            item = QGraphicsPathItem(path)
            item.setPen(QPen(QColor(0, 0, 0), 1.0))
            item.setBrush(QBrush(QColor(150, 150, 200, 100)))
            self.scene.addItem(item)
            
        # Fit in view
        self.fitInView(self.scene.itemsBoundingRect(), Qt.KeepAspectRatio)
