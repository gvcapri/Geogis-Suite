# Arquitetura do Módulo CRF

O Módulo CRF (Regularização Fundiária) atua como o topo da pirâmide do GEOGIS Suite. Ele não "gera" dados (como o GIS e Territorial geram lotes, e o Ambiental gera licenças). Em vez disso, ele **consuma** os dados de todos os outros módulos.

## Camadas e Componentes

1. **EmissionAssistantService**: O maestro da integração. É um serviço que roda em background e cruza dependências: 
   - Busca no `Territorial` se há proprietários atrelados ao lote.
   - Busca no `Ambiental` se há licenças vigentes.
   - Retorna um *Score* (0 a 100%) para aprovar a emissão.
2. **Template Engine (DocumentGenerator)**: Responsável por materializar minutas dinâmicas transformando tags `{{NomeProjeto}}` em strings reais, focando na conversão para PDF ou HTML.
3. **CRFDocumentTree**: Estrutura visual lógica no frontend (PySide6) que evita o uso de arquivos soltos em pastas locais do Windows.
