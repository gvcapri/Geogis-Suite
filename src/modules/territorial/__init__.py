from .controller import TerritorialController

class TerritorialModule:
    name = "Cadastro Territorial"
    version = "1.0.0"
    
    def __init__(self, context):
        self.context = context
        self.controller = TerritorialController(context)
        
    def get_view(self):
        from .view import TerritorialView
        return TerritorialView(self.controller)
