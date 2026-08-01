import os

root_dir = r"c:\Users\guilh\OneDrive\Desktop\Geogis-Suite"
docs_dir = os.path.join(root_dir, "docs")

docs = {
    os.path.join(root_dir, "ARCHITECTURE.md"): """# GEOGIS Suite - Arquitetura (Project-Centric)

## Visão Geral
O GEOGIS Suite é uma plataforma corporativa modular voltada para Engenharia, Geoprocessamento e Regularização Fundiária. 
Nenhuma funcionalidade de negócio será implementada de forma isolada; tudo gira em torno de um **Projeto**.

### Paradigma: Project-Centric
O **Projeto** é a entidade central. O `ProjectContext` é distribuído para todos os módulos.

## Componentes Core
1. **File Manager**: (`services/files/`)
2. **GIS Services**: (`services/gis/`)
3. **Job Manager**: (`core/jobs/`)
4. **Notification Center**
5. **Search Engine**
6. **Workflow Engine**

## Diagrama Principal
```mermaid
graph TD
    UI[Dashboard & Modules] --> |Eventos / Contexto| Core[ProjectContext & EventBus]
    Core --> Jobs[Job Manager]
    Core --> Files[File Services]
    Core --> GIS[GIS Services]
    Core --> DB[(Database)]
```
""",
    os.path.join(root_dir, "ROADMAP.md"): """# Roadmap - GEOGIS Suite

## Fase 1: Fundação & Core (Atual)
- Estrutura Project-Centric.
- Componentes Base (Job Manager, File Services, GIS Services, Event Bus).
- Definição do Database e ProjectContext.
- Theme Manager e UI Base.

## Fase 2: MVP
- Migração de "Comparativos" para o novo padrão.
- Módulo de Projetos Integrado.

## Fase 3: Beta
- Módulo Ambiental, CRF e Valuation.
- Workflow avançado.

## Fase 4: Produção 1.0
- Escala para PostgreSQL e nuvem.
""",
    os.path.join(docs_dir, "DATABASE.md"): """# Documentação do Banco de Dados

Utilizamos SQLAlchemy com `alembic` para migrações. O banco inicia em SQLite.

## Tabelas Principais
- **Users**: Usuários e roles.
- **Projects**: Core do sistema.
- **Clients**: Vinculados a projetos.
- **Files / Documents**: Metadados de arquivos.
- **Tasks / Workflows**: Gestão de etapas.
- **Notifications**: Notificações persistidas.
- **RecentFiles**: Arquivos recentes.

## Diagrama ER
```mermaid
erDiagram
    PROJECT ||--o{ DOCUMENT : contains
    PROJECT ||--o{ TASK : has
    CLIENT ||--o{ PROJECT : requests
```
""",
    os.path.join(docs_dir, "MODULES.md"): """# Módulos do Sistema

Todos os módulos residem em `src/modules/` e são independentes.
Eles recebem `ProjectContext` para atuar.

## Módulos Core
- **Dashboard**: Centro de produtividade.
- **Projects**: Gestão central do contexto.
- **Documents**: Visualização/edição.
- **Comparisons**: Análise de valores.
- **GIS**: Mapas.
- **Environmental**: Licenciamento.
- **CRF**: Regularização Fundiária.
""",
    os.path.join(docs_dir, "WORKFLOW.md"): """# Workflow Engine

O sistema gerencia fluxos de trabalho associados a cada projeto.

## Estrutura
Um `Workflow` possui várias `Tasks`. 
Exemplo: Cadastro -> Geo -> Comparativos -> Ambiental -> Revisão.

## Exemplo de Uso
```python
workflow_service = WorkflowService()
workflow_service.start_workflow(project_context.id, "REGULARIZACAO")
```

```mermaid
stateDiagram-v2
    [*] --> Cadastro
    Cadastro --> Geoprocessamento
    Geoprocessamento --> Revisão
    Revisão --> [*]
```
""",
    os.path.join(docs_dir, "PROJECT_CONTEXT.md"): """# Project Context

O `ProjectContext` é o núcleo da aplicação. 

## Definição
Ele encapsula IDs e metadados do projeto ativo para evitar a necessidade de passagens múltiplas de parâmetros.

## Exemplo
```python
class ProjectContext:
    def __init__(self, project_id, name, client_id, current_stage):
        self.project_id = project_id
        self.name = name
        self.client_id = client_id
        self.current_stage = current_stage
```
Nenhum módulo abre arquivos isolados. Eles acessam:
`file_service.get_project_files(context.project_id)`
""",
    os.path.join(docs_dir, "SERVICES.md"): """# Serviços e Infraestrutura

## File Services
Local: `services/files/`
Todo acesso a PDF, Shapefile, Imagens passa por aqui.
```python
pdf_service.extract_text(file_path)
```

## GIS Services
Local: `services/gis/`
Operações espaciais (GeoPandas, Shapely) encapsuladas.
```python
geometry_service.calculate_area(polygon)
```

## Job Manager
Local: `core/jobs/`
```python
job_manager.submit(long_running_task, callback=update_ui)
```
""",
    os.path.join(docs_dir, "EVENT_BUS.md"): """# Event Bus

Toda comunicação entre módulos ocorre via Event Bus para evitar acoplamento (imports diretos).

## Como funciona
1. Módulo A (Projetos) publica um evento:
```python
event_bus.publish("PROJECT_CREATED", {"id": 1})
```
2. Módulo B (Notificações) reage:
```python
event_bus.subscribe("PROJECT_CREATED", notify_user)
```
""",
    os.path.join(docs_dir, "PLUGIN_SYSTEM.md"): """# Sistema de Plugins

Novos módulos podem ser adicionados dinamicamente copiando uma pasta para `src/modules/`.

## Estrutura de um Plugin
```text
meu_modulo/
  __init__.py      # Registra o plugin no PluginLoader
  views.py         # Interface UI
  controllers.py   # Lógica local
```

O `PluginLoader` varre essas pastas, injeta as dependências (DI) e acopla a view no `MainWindow`.
"""
}

for path, content in docs.items():
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

print("Documentação gerada com sucesso!")
