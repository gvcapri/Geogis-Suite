from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QProgressBar, QHBoxLayout, QGroupBox

class EmissionAssistantPanel(QGroupBox):
    def __init__(self, parent=None):
        super().__init__("Assistente de Emissão", parent)
        self.layout = QVBoxLayout(self)
        
        # Progress Bar
        self.progress_layout = QHBoxLayout()
        self.lbl_score = QLabel("Status Geral: 0%")
        self.progress = QProgressBar()
        self.progress.setValue(0)
        self.progress_layout.addWidget(self.lbl_score)
        self.progress_layout.addWidget(self.progress)
        self.layout.addLayout(self.progress_layout)
        
        # List of items
        self.items_layout = QVBoxLayout()
        self.layout.addLayout(self.items_layout)
        
        # Recommendation
        self.lbl_recommendation = QLabel("Próxima Ação Recomendada:\n--")
        self.lbl_recommendation.setStyleSheet("font-weight: bold; margin-top: 10px;")
        self.layout.addWidget(self.lbl_recommendation)
        
    def update_diagnosis(self, diagnosis: dict):
        # Update progress
        score = diagnosis.get("score", 0)
        self.progress.setValue(score)
        self.lbl_score.setText(f"Status Geral: {score}%")
        
        # Clear items
        while self.items_layout.count():
            item = self.items_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
                
        # Populate items
        for item in diagnosis.get("items", []):
            status = item.get("status")
            text = item.get("text")
            icon = "✔" if status == "ok" else "⚠" if status == "warning" else "✖"
            color = "green" if status == "ok" else "orange" if status == "warning" else "red"
            
            lbl = QLabel(f"<span style='color:{color}'>{icon}</span> {text}")
            self.items_layout.addWidget(lbl)
            
        self.lbl_recommendation.setText(f"Próxima Ação Recomendada:\n{diagnosis.get('next_action', '--')}")
