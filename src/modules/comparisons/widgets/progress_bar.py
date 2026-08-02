from PySide6.QtWidgets import QWidget, QVBoxLayout, QProgressBar, QLabel, QHBoxLayout
from PySide6.QtCore import Qt

class ComparisonProgressBar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()
        
    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Info row (Message + Time)
        info_layout = QHBoxLayout()
        self.message_label = QLabel("Pronto")
        self.time_label = QLabel("--:--")
        info_layout.addWidget(self.message_label)
        info_layout.addStretch()
        info_layout.addWidget(self.time_label)
        layout.addLayout(info_layout)
        
        # Progress Bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.progress_bar)
        
    def set_progress(self, percentage: int, message: str, estimated_time: str = "--:--"):
        self.progress_bar.setValue(percentage)
        self.message_label.setText(message)
        self.time_label.setText(f"Restante: {estimated_time}")
        
    def reset(self):
        self.set_progress(0, "Pronto", "--:--")
