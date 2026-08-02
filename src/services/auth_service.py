import bcrypt
from typing import Optional
import datetime

from sqlalchemy.orm import joinedload
from src.database.db_manager import SessionLocal
from src.database.models import User, Role

class AuthService:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.current_user: Optional[User] = None
        return cls._instance

    def login(self, login: str, password: str) -> tuple[bool, str]:
        db = SessionLocal()
        try:
            user = db.query(User).options(
                joinedload(User.roles).joinedload(Role.permissions)
            ).filter(User.login == login).first()
            if not user:
                return False, "Usuário não encontrado."
                
            if not user.is_active:
                return False, "Usuário inativo."
                
            # Check password
            if bcrypt.checkpw(password.encode('utf-8'), user.password_hash.encode('utf-8')):
                self.current_user = user
                
                # Update last login
                user.last_login = datetime.datetime.utcnow()
                db.commit()
                db.refresh(user)
                return True, "Login realizado com sucesso."
            else:
                return False, "Senha incorreta."
        except Exception as e:
            return False, f"Erro interno: {e}"
        finally:
            db.close()

    def logout(self):
        self.current_user = None

    def get_current_user(self) -> Optional[User]:
        return self.current_user
        
    def hash_password(self, password: str) -> str:
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

auth_service = AuthService()
