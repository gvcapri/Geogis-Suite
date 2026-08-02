from .controller import EnvironmentalController

class EnvironmentalModule:
    name = "Gestão Ambiental"
    version = "1.0.0"
    
    def __init__(self, context):
        self.context = context
        self.controller = EnvironmentalController(context)
        
    def get_view(self):
        from .view import EnvironmentalView
        return EnvironmentalView(self.controller)
