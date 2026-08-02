from .controller import CRFController

class CRFModule:
    name = "Regularização Fundiária (CRF)"
    version = "1.0.0"
    
    def __init__(self, context):
        self.context = context
        self.controller = CRFController(context)
        
    def get_view(self):
        from .view import CRFView
        return CRFView(self.controller)
