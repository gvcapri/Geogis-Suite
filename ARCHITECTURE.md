# GEOGIS Suite - Arquitetura (Project-Centric)

## Padrões Adotados (Implementados na Sprint 01)
- **Clean Architecture & SOLID**: Separação clara em `src/core`, `src/ui`, `src/modules`.
- **Event-Driven & Dependency Injection**: Padrões implementados no `EventBus` e `JobManager`.
- **Plugin Architecture**: Sistema de roteamento dinâmico via `NavigationManager` e `PluginLoader`.
- **UI Premium (Single-Window)**: Utilização de `QStackedWidget` centralizado via `MainWindow` unificada com painéis dinâmicos (`GeoSidebar`, `GeoHeader`, `GeoStatusBar`).

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
