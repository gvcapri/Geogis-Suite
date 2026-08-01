# Project Context

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
