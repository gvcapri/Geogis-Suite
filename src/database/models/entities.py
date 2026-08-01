from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from src.database.models.base import Base

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True)
    projects = relationship("Project", back_populates="owner")

class Client(Base):
    __tablename__ = 'clients'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    document = Column(String) # CPF/CNPJ
    projects = relationship("Project", back_populates="client")

class Project(Base):
    __tablename__ = 'projects'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    client_id = Column(Integer, ForeignKey('clients.id'))
    owner_id = Column(Integer, ForeignKey('users.id'))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    client = relationship("Client", back_populates="projects")
    owner = relationship("User", back_populates="projects")
    files = relationship("File", back_populates="project")
    documents = relationship("Document", back_populates="project")
    tasks = relationship("Task", back_populates="project")
    history = relationship("ProjectHistory", back_populates="project")

class File(Base):
    __tablename__ = 'files'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    path = Column(String, nullable=False)
    project_id = Column(Integer, ForeignKey('projects.id'))
    project = relationship("Project", back_populates="files")

class Document(Base):
    __tablename__ = 'documents'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    content = Column(Text)
    project_id = Column(Integer, ForeignKey('projects.id'))
    project = relationship("Project", back_populates="documents")

class Workflow(Base):
    __tablename__ = 'workflows'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    tasks = relationship("Task", back_populates="workflow")

class Task(Base):
    __tablename__ = 'tasks'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    status = Column(String, default="pending")
    workflow_id = Column(Integer, ForeignKey('workflows.id'))
    project_id = Column(Integer, ForeignKey('projects.id'))
    
    workflow = relationship("Workflow", back_populates="tasks")
    project = relationship("Project", back_populates="tasks")

class Notification(Base):
    __tablename__ = 'notifications'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    message = Column(Text)
    type = Column(String) # info, success, warning, error
    read = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class Log(Base):
    __tablename__ = 'logs'
    id = Column(Integer, primary_key=True, index=True)
    level = Column(String)
    message = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

class Module(Base):
    __tablename__ = 'modules'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    is_active = Column(Boolean, default=True)

class Setting(Base):
    __tablename__ = 'settings'
    key = Column(String, primary_key=True)
    value = Column(String)

class Permission(Base):
    __tablename__ = 'permissions'
    id = Column(Integer, primary_key=True, index=True)
    role_name = Column(String)
    resource = Column(String)
    can_read = Column(Boolean, default=False)
    can_write = Column(Boolean, default=False)

class ProjectHistory(Base):
    __tablename__ = 'project_history'
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey('projects.id'))
    action = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    project = relationship("Project", back_populates="history")

class RecentFile(Base):
    __tablename__ = 'recent_files'
    id = Column(Integer, primary_key=True, index=True)
    file_path = Column(String, nullable=False)
    opened_at = Column(DateTime, default=datetime.utcnow)
