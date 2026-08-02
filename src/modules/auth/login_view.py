from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QLineEdit, QPushButton, QFrame, QGraphicsDropShadowEffect)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QColor, QCursor
import qtawesome as qta

from src.core.theme.theme_manager import theme_manager
from src.services.auth_service import auth_service

class LoginView(QWidget):
    login_successful = Signal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("login_view")
        
        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignCenter)
        
        self.card = QFrame()
        self.card.setObjectName("login_card")
        self.card.setFixedSize(400, 500)
        
        # Sombra
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(30)
        shadow.setXOffset(0)
        shadow.setYOffset(4)
        shadow.setColor(QColor(0, 0, 0, 40))
        self.card.setGraphicsEffect(shadow)
        
        layout = QVBoxLayout(self.card)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(20)
        
        # Logo
        self.lbl_logo = QLabel("GEOGIS Suite")
        self.lbl_logo.setAlignment(Qt.AlignCenter)
        self.lbl_logo.setStyleSheet(f"font-size: 28px; font-weight: 800; color: {theme_manager.get_color('accent')}; letter-spacing: 2px;")
        
        self.lbl_subtitle = QLabel("Plataforma Corporativa")
        self.lbl_subtitle.setAlignment(Qt.AlignCenter)
        self.lbl_subtitle.setStyleSheet(f"font-size: 14px; color: {theme_manager.get_color('text_sec')}; margin-bottom: 20px;")
        
        # Inputs
        self.inp_user = QLineEdit()
        self.inp_user.setPlaceholderText("Usuário")
        self.inp_user.setFixedHeight(45)
        
        self.inp_pass = QLineEdit()
        self.inp_pass.setPlaceholderText("Senha")
        self.inp_pass.setEchoMode(QLineEdit.Password)
        self.inp_pass.setFixedHeight(45)
        
        self.lbl_error = QLabel("")
        self.lbl_error.setStyleSheet("color: #Ef4444; font-size: 12px;")
        self.lbl_error.setAlignment(Qt.AlignCenter)
        self.lbl_error.hide()
        
        self.btn_login = QPushButton("Entrar")
        self.btn_login.setFixedHeight(45)
        self.btn_login.setCursor(QCursor(Qt.PointingHandCursor))
        self.btn_login.clicked.connect(self.do_login)
        
        self.btn_forgot = QPushButton("Esqueci minha senha")
        self.btn_forgot.setCursor(QCursor(Qt.PointingHandCursor))
        self.btn_forgot.setObjectName("btn_forgot")
        
        layout.addWidget(self.lbl_logo)
        layout.addWidget(self.lbl_subtitle)
        layout.addWidget(self.inp_user)
        layout.addWidget(self.inp_pass)
        layout.addWidget(self.lbl_error)
        layout.addWidget(self.btn_login)
        layout.addStretch()
        layout.addWidget(self.btn_forgot, alignment=Qt.AlignCenter)
        
        main_layout.addWidget(self.card)
        
        self.update_theme()
        
        # Pressionar Enter = Login
        self.inp_user.returnPressed.connect(self.do_login)
        self.inp_pass.returnPressed.connect(self.do_login)

    def do_login(self):
        login = self.inp_user.text().strip()
        password = self.inp_pass.text()
        
        if not login or not password:
            self.show_error("Preencha usuário e senha.")
            return
            
        self.btn_login.setText("Entrando...")
        self.btn_login.setEnabled(False)
        
        success, message = auth_service.login(login, password)
        
        self.btn_login.setEnabled(True)
        self.btn_login.setText("Entrar")
        
        if success:
            self.lbl_error.hide()
            self.login_successful.emit()
        else:
            self.show_error(message)
            
    def show_error(self, msg: str):
        self.lbl_error.setText(msg)
        self.lbl_error.show()
        
    def update_theme(self):
        self.setStyleSheet(f"""
            #login_view {{
                background-color: {theme_manager.get_color('bg_base')};
            }}
            #login_card {{
                background-color: {theme_manager.get_color('bg_card')};
                border-radius: 12px;
                border: 1px solid {theme_manager.get_color('border')};
            }}
            QLineEdit {{
                border: 1px solid {theme_manager.get_color('border')};
                border-radius: 6px;
                padding: 0 16px;
                background-color: {theme_manager.get_color('bg_base')};
                color: {theme_manager.get_color('text_main')};
                font-size: 14px;
            }}
            QLineEdit:focus {{
                border: 2px solid {theme_manager.get_color('accent')};
            }}
            QPushButton {{
                background-color: {theme_manager.get_color('accent')};
                color: white;
                border-radius: 6px;
                font-size: 14px;
                font-weight: bold;
                border: none;
            }}
            QPushButton:hover {{
                background-color: {theme_manager.get_color('accent_hover')};
            }}
            #btn_forgot {{
                background-color: transparent;
                color: {theme_manager.get_color('text_sec')};
                font-weight: normal;
                font-size: 13px;
            }}
            #btn_forgot:hover {{
                color: {theme_manager.get_color('accent')};
                text-decoration: underline;
            }}
        """)
