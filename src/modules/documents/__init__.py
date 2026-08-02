"""
Documents Module for GEOGIS Suite.
Centralizes document management with versioning and preview capabilities.
"""
from .controller import DocumentsController

class DocumentsModule:
    name = "Documentos"
    version = "1.0.0"
    
    def __init__(self, context):
        self.context = context
        self.controller = DocumentsController(context)
        
    def get_view(self):
        from .view import DocumentsView
        return DocumentsView(self.controller)
