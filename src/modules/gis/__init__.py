from .controller import GISController

class GISModule:
    name = "Geoprocessamento"
    version = "1.0.0"
    
    def __init__(self, context):
        self.context = context
        self.controller = GISController(context)
        
    def get_view(self):
        from .view import GISView
        return GISView(self.controller)
