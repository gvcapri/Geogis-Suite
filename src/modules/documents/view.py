from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QSplitter, 
    QGroupBox, QPushButton, QFileDialog, QMessageBox, QLabel
)
from PySide6.QtCore import Qt
from .widgets.folder_tree import FolderTreeView
from .widgets.document_list import DocumentListView
from .widgets.preview_pane import PreviewPane
from .widgets.version_history import VersionHistoryView

class DocumentsView(QWidget):
    def __init__(self, controller, parent=None):
        super().__init__(parent)
        self.controller = controller
        self.current_folder_id = None
        self.current_doc_id = None
        self._setup_ui()
        self._load_initial_data()
        
    def _setup_ui(self):
        main_layout = QVBoxLayout(self)
        
        # Header
        self.project_label = QLabel("Projeto: Nenhum")
        self.project_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        main_layout.addWidget(self.project_label)
        
        # Splitter main
        self.splitter = QSplitter(Qt.Horizontal)
        main_layout.addWidget(self.splitter)
        
        # Left Panel (Folders)
        folder_group = QGroupBox("Pastas")
        folder_layout = QVBoxLayout(folder_group)
        self.folder_tree = FolderTreeView()
        self.folder_tree.folder_selected.connect(self._on_folder_selected)
        folder_layout.addWidget(self.folder_tree)
        self.splitter.addWidget(folder_group)
        
        # Middle Panel (Documents list)
        doc_group = QGroupBox("Documentos")
        doc_layout = QVBoxLayout(doc_group)
        
        btn_layout = QHBoxLayout()
        self.btn_upload = QPushButton("Upload Arquivo")
        self.btn_upload.setEnabled(False)
        self.btn_upload.clicked.connect(self._on_upload)
        btn_layout.addWidget(self.btn_upload)
        doc_layout.addLayout(btn_layout)
        
        self.doc_list = DocumentListView()
        self.doc_list.document_selected.connect(self._on_document_selected)
        doc_layout.addWidget(self.doc_list)
        self.splitter.addWidget(doc_group)
        
        # Right Panel (Preview & Versions)
        right_splitter = QSplitter(Qt.Vertical)
        
        preview_group = QGroupBox("Visualização")
        preview_layout = QVBoxLayout(preview_group)
        self.preview_pane = PreviewPane()
        preview_layout.addWidget(self.preview_pane)
        right_splitter.addWidget(preview_group)
        
        version_group = QGroupBox("Histórico & Versões")
        version_layout = QVBoxLayout(version_group)
        self.version_history = VersionHistoryView()
        self.version_history.version_selected.connect(self._on_version_selected)
        self.version_history.sign_requested.connect(self._on_sign_requested)
        version_layout.addWidget(self.version_history)
        right_splitter.addWidget(version_group)
        
        self.splitter.addWidget(right_splitter)
        self.splitter.setSizes([200, 300, 400])
        
    def _load_initial_data(self):
        project = self.controller.context.get_current_project()
        if project:
            self.project_label.setText(f"Projeto: {project.name}")
            folders = self.controller.load_project_structure()
            self.folder_tree.populate(folders)
        else:
            self.project_label.setText("Nenhum projeto ativo")
            
    def _on_folder_selected(self, folder_id: int):
        self.current_folder_id = folder_id
        self.btn_upload.setEnabled(True)
        docs = self.controller.load_documents(folder_id)
        self.doc_list.populate(docs)
        self.current_doc_id = None
        self.version_history.populate([])
        
    def _on_document_selected(self, doc_id: int):
        self.current_doc_id = doc_id
        versions = self.controller.get_document_versions(doc_id)
        self.version_history.populate(versions)
        if versions:
            self.preview_pane.show_preview(versions[0])
            
    def _on_version_selected(self, version_id: int):
        versions = self.controller.get_document_versions(self.current_doc_id)
        version = next((v for v in versions if v.id == version_id), None)
        self.preview_pane.show_preview(version)
        
    def _on_upload(self):
        if not self.current_folder_id:
            return
            
        path, _ = QFileDialog.getOpenFileName(self, "Selecionar Arquivo")
        if path:
            try:
                self.controller.upload_file(self.current_folder_id, path)
                self._on_folder_selected(self.current_folder_id) # reload
                QMessageBox.information(self, "Sucesso", "Arquivo enviado com sucesso!")
            except Exception as e:
                QMessageBox.critical(self, "Erro", f"Erro ao enviar arquivo: {e}")
                
    def _on_sign_requested(self, version_id: int):
        try:
            self.controller.sign_version(version_id)
            QMessageBox.information(self, "Sucesso", "Documento assinado com sucesso!")
            self._on_document_selected(self.current_doc_id) # refresh
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao assinar documento: {e}")
