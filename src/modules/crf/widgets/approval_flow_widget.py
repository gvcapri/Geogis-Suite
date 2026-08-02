from PySide6.QtWidgets import QWidget, HttpBoxLayout, QLabel, QHBoxLayout

class ApprovalFlowWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QHBoxLayout(self)
        
        stages = ["Rascunho", "Revisão Técnica", "Aprovado Gestor", "Emitido"]
        self.labels = {}
        
        for stage in stages:
            lbl = QLabel(stage)
            lbl.setStyleSheet("padding: 5px; border: 1px solid gray; border-radius: 10px; background-color: #f0f0f0; color: gray;")
            self.layout.addWidget(lbl)
            self.labels[stage] = lbl
            
    def set_current_stage(self, current_stage: str):
        for stage, lbl in self.labels.items():
            if stage == current_stage:
                lbl.setStyleSheet("padding: 5px; border: 2px solid green; border-radius: 10px; background-color: #A5D6A7; color: black; font-weight: bold;")
            else:
                lbl.setStyleSheet("padding: 5px; border: 1px solid gray; border-radius: 10px; background-color: #f0f0f0; color: gray;")
