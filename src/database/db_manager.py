import sys
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import bcrypt

from src.database.models import Base, User, Role, Permission, Department

def get_data_dir():
    if getattr(sys, 'frozen', False):
        return Path(sys.executable).parent
    return Path(__file__).resolve().parent.parent.parent.parent

DB_PATH = get_data_dir() / "geogis.db"

engine = create_engine(f"sqlite:///{DB_PATH}", echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    # Cria todas as tabelas
    Base.metadata.create_all(bind=engine)
    
    # Seeding inicial (apenas se estiver vazio)
    db = SessionLocal()
    try:
        admin_role = db.query(Role).filter(Role.name == "Super Administrador").first()
        if not admin_role:
            # Cria permissoes fundamentais
            perm_all = Permission(name="all", description="Acesso total ao sistema")
            db.add(perm_all)
            
            # Cria papéis
            admin_role = Role(name="Super Administrador", permissions=[perm_all])
            gestor_role = Role(name="Administrador do Setor")
            engenheiro_role = Role(name="Engenheiro")
            analista_amb_role = Role(name="Analista Ambiental")
            analista_cad_role = Role(name="Analista de Cadastro")
            operador_role = Role(name="Operador")
            estagiario_role = Role(name="Estagiário")
            consulta_role = Role(name="Consulta")
            
            db.add_all([
                admin_role, gestor_role, engenheiro_role, 
                analista_amb_role, analista_cad_role, 
                operador_role, estagiario_role, consulta_role
            ])
            
            # Cria Setores
            setor_admin = Department(name="Administrativo")
            setor_eng = Department(name="Engenharia")
            setor_amb = Department(name="Ambiental")
            setor_crf = Department(name="CRF")
            setor_cad = Department(name="Cadastro Urbano")
            
            db.add_all([setor_admin, setor_eng, setor_amb, setor_crf, setor_cad])
            
            # Cria o Super Administrador padrao
            salt = bcrypt.gensalt()
            hashed = bcrypt.hashpw("admin".encode('utf-8'), salt).decode('utf-8')
            
            default_user = User(
                name="Administrador Principal",
                login="admin",
                password_hash=hashed,
                email="admin@geogis.com",
                position="Super Administrador",
                department=setor_admin,
                roles=[admin_role]
            )
            db.add(default_user)
            db.commit()
            print("Banco de dados inicializado com sucesso. Usuário padrão criado.")
    except Exception as e:
        db.rollback()
        print(f"Erro ao inicializar o banco de dados: {e}")
    finally:
        db.close()
