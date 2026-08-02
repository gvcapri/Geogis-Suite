import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Table
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

# Many-to-Many association tables
user_roles = Table(
    'user_roles',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True),
    Column('role_id', Integer, ForeignKey('roles.id'), primary_key=True)
)

role_permissions = Table(
    'role_permissions',
    Base.metadata,
    Column('role_id', Integer, ForeignKey('roles.id'), primary_key=True),
    Column('permission_id', Integer, ForeignKey('permissions.id'), primary_key=True)
)

project_departments = Table(
    'project_departments',
    Base.metadata,
    Column('project_id', Integer, ForeignKey('projects.id'), primary_key=True),
    Column('department_id', Integer, ForeignKey('departments.id'), primary_key=True)
)

class Department(Base):
    __tablename__ = 'departments'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)
    
    users = relationship("User", back_populates="department")
    projects = relationship("Project", secondary=project_departments, back_populates="departments")

class Permission(Base):
    __tablename__ = 'permissions'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)
    description = Column(String(200))

class Role(Base):
    __tablename__ = 'roles'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)
    
    permissions = relationship("Permission", secondary=role_permissions)

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    login = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(200), nullable=False)
    email = Column(String(100))
    position = Column(String(100))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    last_login = Column(DateTime, nullable=True)
    
    department_id = Column(Integer, ForeignKey('departments.id'), nullable=True)
    department = relationship("Department", back_populates="users")
    
    roles = relationship("Role", secondary=user_roles)
    
    def has_permission(self, permission_name: str) -> bool:
        for role in self.roles:
            for perm in role.permissions:
                if perm.name == permission_name:
                    return True
        return False

class Project(Base):
    __tablename__ = 'projects'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    client = Column(String(150))
    city = Column(String(100))
    allotment = Column(String(100))
    registration = Column(String(100)) # Matricula
    status = Column(String(50), default="Em andamento")
    
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    departments = relationship("Department", secondary=project_departments, back_populates="projects")
    workflows = relationship("Workflow", back_populates="project")

class Workflow(Base):
    __tablename__ = 'workflows'
    
    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey('projects.id'))
    step_name = Column(String(100), nullable=False)
    status = Column(String(50), default="Pendente")
    assigned_user_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    
    project = relationship("Project", back_populates="workflows")

class AuditLog(Base):
    __tablename__ = 'audit_logs'
    
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    action = Column(String(255), nullable=False)
    details = Column(String(1000))

# --- Document Module Entities ---

class DocumentFolder(Base):
    __tablename__ = 'document_folders'
    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey('projects.id'), nullable=False)
    parent_id = Column(Integer, ForeignKey('document_folders.id'), nullable=True)
    name = Column(String(100), nullable=False)
    is_system_folder = Column(Boolean, default=False)
    
    project = relationship("Project")
    children = relationship("DocumentFolder", backref="parent", remote_side=[id])
    documents = relationship("Document", back_populates="folder", cascade="all, delete-orphan")

class Document(Base):
    __tablename__ = 'documents'
    id = Column(Integer, primary_key=True)
    folder_id = Column(Integer, ForeignKey('document_folders.id'), nullable=False)
    project_id = Column(Integer, ForeignKey('projects.id'), nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(String(500))
    doc_type = Column(String(50)) # e.g. "PDF", "XLSX"
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    folder = relationship("DocumentFolder", back_populates="documents")
    project = relationship("Project")
    versions = relationship("DocumentVersion", back_populates="document", cascade="all, delete-orphan")

class DocumentVersion(Base):
    __tablename__ = 'document_versions'
    id = Column(Integer, primary_key=True)
    document_id = Column(Integer, ForeignKey('documents.id'), nullable=False)
    version_number = Column(Integer, nullable=False, default=1)
    file_path = Column(String(500), nullable=False)
    file_size = Column(Integer) # in bytes
    file_hash = Column(String(255))
    uploaded_by = Column(Integer, ForeignKey('users.id'))
    uploaded_at = Column(DateTime, default=datetime.datetime.utcnow)
    change_log = Column(String(500))
    
    document = relationship("Document", back_populates="versions")
    uploader = relationship("User")
    signatures = relationship("DocumentSignature", back_populates="version", cascade="all, delete-orphan")

class DocumentTemplate(Base):
    __tablename__ = 'document_templates'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    doc_type = Column(String(50))
    file_path = Column(String(500), nullable=False)
    
class DocumentSignature(Base):
    __tablename__ = 'document_signatures'
    id = Column(Integer, primary_key=True)
    version_id = Column(Integer, ForeignKey('document_versions.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    signed_at = Column(DateTime, default=datetime.datetime.utcnow)
    ip_address = Column(String(50))
    signature_hash = Column(String(255), nullable=False)
    
    version = relationship("DocumentVersion", back_populates="signatures")
    user = relationship("User")

# --- Territorial Module Entities ---

# Association table for Lot and Owner (Many-to-Many if fractions exist)
lot_owners = Table(
    'lot_owners',
    Base.metadata,
    Column('lot_id', Integer, ForeignKey('lots.id'), primary_key=True),
    Column('owner_id', Integer, ForeignKey('owners.id'), primary_key=True)
)

class Municipality(Base):
    __tablename__ = 'municipalities'
    id = Column(Integer, primary_key=True)
    code = Column(String(50), unique=True)
    name = Column(String(100), nullable=False)
    state = Column(String(2)) # UF
    region = Column(String(100))
    notes = Column(String(500))
    
    neighborhoods = relationship("Neighborhood", back_populates="municipality")

class Neighborhood(Base):
    __tablename__ = 'neighborhoods'
    id = Column(Integer, primary_key=True)
    municipality_id = Column(Integer, ForeignKey('municipalities.id'), nullable=False)
    code = Column(String(50))
    name = Column(String(100), nullable=False)
    area_sqm = Column(Integer)
    notes = Column(String(500))
    
    municipality = relationship("Municipality", back_populates="neighborhoods")
    subdivisions = relationship("Subdivision", back_populates="neighborhood")

class Subdivision(Base): # Loteamento
    __tablename__ = 'subdivisions'
    id = Column(Integer, primary_key=True)
    neighborhood_id = Column(Integer, ForeignKey('neighborhoods.id'), nullable=False)
    name = Column(String(150), nullable=False)
    client_name = Column(String(150))
    status = Column(String(50))
    total_area_sqm = Column(Integer)
    total_blocks = Column(Integer, default=0)
    total_lots = Column(Integer, default=0)
    
    neighborhood = relationship("Neighborhood", back_populates="subdivisions")
    blocks = relationship("Block", back_populates="subdivision", cascade="all, delete-orphan")

class Block(Base): # Quadra
    __tablename__ = 'blocks'
    id = Column(Integer, primary_key=True)
    subdivision_id = Column(Integer, ForeignKey('subdivisions.id'), nullable=False)
    code = Column(String(50), nullable=False)
    area_sqm = Column(Integer)
    lot_count = Column(Integer, default=0)
    
    subdivision = relationship("Subdivision", back_populates="blocks")
    lots = relationship("Lot", back_populates="block", cascade="all, delete-orphan")

class Lot(Base): # Lote
    __tablename__ = 'lots'
    id = Column(Integer, primary_key=True)
    block_id = Column(Integer, ForeignKey('blocks.id'), nullable=False)
    project_id = Column(Integer, ForeignKey('projects.id'), nullable=True) # Linked to a GEOGIS Project
    number = Column(String(50), nullable=False)
    nominal_area_sqm = Column(Integer)
    perimeter_m = Column(Integer)
    frontage_m = Column(Integer) # Frente
    status = Column(String(50))
    
    # GIS Integration fields
    gis_feature_id = Column(String(100)) # ID used in the GeoDataFrame/Shapefile
    latitude = Column(String(50))
    longitude = Column(String(50))
    
    block = relationship("Block", back_populates="lots")
    project = relationship("Project")
    registries = relationship("Registry", back_populates="lot")
    owners = relationship("Owner", secondary=lot_owners, back_populates="lots")

class Owner(Base): # Proprietário
    __tablename__ = 'owners'
    id = Column(Integer, primary_key=True)
    name = Column(String(150), nullable=False)
    document_number = Column(String(50)) # CPF/CNPJ
    contact_info = Column(String(200))
    
    address_id = Column(Integer, ForeignKey('addresses.id'))
    address = relationship("Address")
    
    lots = relationship("Lot", secondary=lot_owners, back_populates="owners")

class Registry(Base): # Matrícula
    __tablename__ = 'registries'
    id = Column(Integer, primary_key=True)
    lot_id = Column(Integer, ForeignKey('lots.id'), nullable=False)
    number = Column(String(100), nullable=False)
    registry_office = Column(String(150)) # Cartório
    book = Column(String(50))
    page = Column(String(50))
    registration_date = Column(DateTime)
    
    lot = relationship("Lot", back_populates="registries")

class Address(Base):
    __tablename__ = 'addresses'
    id = Column(Integer, primary_key=True)
    street = Column(String(200))
    number = Column(String(50))
    zip_code = Column(String(20)) # CEP
    city = Column(String(100))

# --- Environmental Module Entities ---

class EnvironmentalProcess(Base):
    __tablename__ = 'environmental_processes'
    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey('projects.id'), nullable=False)
    process_type = Column(String(100))
    responsible_user_id = Column(Integer, ForeignKey('users.id'))
    status = Column(String(50), default="Aberto")
    open_date = Column(DateTime, default=datetime.datetime.utcnow)
    deadline_date = Column(DateTime)
    notes = Column(String(1000))
    
    project = relationship("Project")
    responsible = relationship("User")

class APP(Base):
    __tablename__ = 'environmental_apps'
    id = Column(Integer, primary_key=True)
    process_id = Column(Integer, ForeignKey('environmental_processes.id'))
    name = Column(String(100))
    area_sqm = Column(Integer)
    status = Column(String(50))
    notes = Column(String(500))
    gis_feature_id = Column(String(100))

class LegalReserve(Base):
    __tablename__ = 'environmental_reserves'
    id = Column(Integer, primary_key=True)
    process_id = Column(Integer, ForeignKey('environmental_processes.id'))
    area_sqm = Column(Integer)
    percentage = Column(Integer)
    status = Column(String(50))
    gis_feature_id = Column(String(100))

class WaterResource(Base):
    __tablename__ = 'environmental_water_resources'
    id = Column(Integer, primary_key=True)
    process_id = Column(Integer, ForeignKey('environmental_processes.id'))
    resource_type = Column(String(50)) # Rio, Nascente, etc
    name = Column(String(100))
    influence_area_sqm = Column(Integer)
    gis_feature_id = Column(String(100))

class Vegetation(Base):
    __tablename__ = 'environmental_vegetation'
    id = Column(Integer, primary_key=True)
    process_id = Column(Integer, ForeignKey('environmental_processes.id'))
    veg_type = Column(String(100))
    area_sqm = Column(Integer)
    conservation_status = Column(String(100))
    gis_feature_id = Column(String(100))

class License(Base):
    __tablename__ = 'environmental_licenses'
    id = Column(Integer, primary_key=True)
    process_id = Column(Integer, ForeignKey('environmental_processes.id'))
    number = Column(String(100), nullable=False)
    agency = Column(String(100)) # Órgão
    license_type = Column(String(50))
    issue_date = Column(DateTime)
    expiry_date = Column(DateTime)
    status = Column(String(50))

class Conditionant(Base):
    __tablename__ = 'environmental_conditionants'
    id = Column(Integer, primary_key=True)
    license_id = Column(Integer, ForeignKey('environmental_licenses.id'))
    description = Column(String(500))
    responsible_user_id = Column(Integer, ForeignKey('users.id'))
    deadline = Column(DateTime)
    status = Column(String(50))

class Inspection(Base):
    __tablename__ = 'environmental_inspections'
    id = Column(Integer, primary_key=True)
    process_id = Column(Integer, ForeignKey('environmental_processes.id'))
    inspection_date = Column(DateTime, default=datetime.datetime.utcnow)
    responsible_user_id = Column(Integer, ForeignKey('users.id'))
    location = Column(String(200))
    notes = Column(String(1000))
    pending_items = Column(String(500))
    result = Column(String(50))

class EnvironmentalPhoto(Base):
    __tablename__ = 'environmental_photos'
    id = Column(Integer, primary_key=True)
    process_id = Column(Integer, ForeignKey('environmental_processes.id'))
    inspection_id = Column(Integer, ForeignKey('environmental_inspections.id'), nullable=True)
    file_path = Column(String(500))
    capture_date = Column(DateTime)
    location_coords = Column(String(100))
    description = Column(String(300))
    category = Column(String(50))
    uploaded_by = Column(Integer, ForeignKey('users.id'))

class ChecklistTemplate(Base):
    __tablename__ = 'environmental_checklist_templates'
    id = Column(Integer, primary_key=True)
    item_name = Column(String(200), nullable=False)
    is_required = Column(Boolean, default=True)

class ChecklistAnswer(Base):
    __tablename__ = 'environmental_checklist_answers'
    id = Column(Integer, primary_key=True)
    process_id = Column(Integer, ForeignKey('environmental_processes.id'))
    template_id = Column(Integer, ForeignKey('environmental_checklist_templates.id'))
    is_checked = Column(Boolean, default=False)

# --- CRF Module Entities ---

class CRFProcess(Base):
    __tablename__ = 'crf_processes'
    id = Column(Integer, primary_key=True)
    number = Column(String(100), unique=True, nullable=False)
    project_id = Column(Integer, ForeignKey('projects.id'), nullable=False)
    client_id = Column(Integer, nullable=True) # Assuming a client table or field in Territorial
    responsible_tech_id = Column(Integer, ForeignKey('users.id'))
    status = Column(String(50), default="Rascunho") # Rascunho, Em Revisão, Aprovado, Emitido
    open_date = Column(DateTime, default=datetime.datetime.utcnow)
    target_date = Column(DateTime)
    completion_date = Column(DateTime)
    
    project = relationship("Project")
    responsible = relationship("User")

class CRFDocument(Base):
    __tablename__ = 'crf_documents'
    id = Column(Integer, primary_key=True)
    process_id = Column(Integer, ForeignKey('crf_processes.id'))
    name = Column(String(200), nullable=False)
    category = Column(String(100)) # Minutas, Versão Final, Mapas, Memorial
    current_revision_id = Column(Integer, nullable=True) # Points to active revision
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class CRFRevision(Base):
    __tablename__ = 'crf_revisions'
    id = Column(Integer, primary_key=True)
    document_id = Column(Integer, ForeignKey('crf_documents.id'))
    author_id = Column(Integer, ForeignKey('users.id'))
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    reason = Column(String(500))
    file_path = Column(String(500))
    file_hash = Column(String(255))
    status = Column(String(50)) # Pendente, Aprovado, Rejeitado

class CRFTemplate(Base):
    __tablename__ = 'crf_templates'
    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    content_html = Column(String) # Jinja2 HTML Template
    required_variables = Column(String(500)) # Comma separated {{Var}}
    is_active = Column(Boolean, default=True)

class CRFChecklist(Base):
    __tablename__ = 'crf_checklist_templates'
    id = Column(Integer, primary_key=True)
    item_name = Column(String(200), nullable=False)
    is_required = Column(Boolean, default=True)

class CRFChecklistAnswer(Base):
    __tablename__ = 'crf_checklist_answers'
    id = Column(Integer, primary_key=True)
    process_id = Column(Integer, ForeignKey('crf_processes.id'))
    checklist_id = Column(Integer, ForeignKey('crf_checklist_templates.id'))
    is_checked = Column(Boolean, default=False)

class CRFApproval(Base):
    __tablename__ = 'crf_approvals'
    id = Column(Integer, primary_key=True)
    process_id = Column(Integer, ForeignKey('crf_processes.id'))
    user_id = Column(Integer, ForeignKey('users.id'))
    action = Column(String(50)) # Aprovar, Rejeitar
    justification = Column(String(1000))
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)


