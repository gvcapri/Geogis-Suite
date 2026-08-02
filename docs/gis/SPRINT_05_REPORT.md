# SPRINT 05 REPORT: Módulo GIS

**Status:** Concluído
**Data:** Agosto 2026

## Funcionalidades Implementadas
- **Core Engine:** Construída toda a infraestrutura base (`src/services/gis`) usando Design Patterns limpos. 9 Serviços especializados foram desenhados para garantir que a complexidade espacial ficasse isolada da UI.
- **Renderização de Alto Desempenho:** Implementada visualização nativa baseada em `QGraphicsView` acoplada ao Shapely (`RenderService`). Isso dispensa navegadores embutidos e entrega performance de GPU nativa comparável a softwares GIS de desktop focados (C++).
- **Processamento Assíncrono:** A importação pesada de dados (via `geopandas`) e conversões foi injetada no `JobManager`, permitindo que o usuário navegue no sistema enquanto o shapefile de 2GB é carregado e renderizado.
- **Interface Integrada:** Desenvolvidos 5 Widgets (`MapCanvas`, `LayerPanel`, `PropertiesPanel`, `Toolbar`, `StatusBar`), reunidos numa interface de três painéis expansíveis (Esquerda: Camadas, Centro: Mapa, Direita: Propriedades). Totalmente integrado à *Sidebar* da `MainWindow`.

## Decisões Arquiteturais
- **Geopandas + PySide6:** A escolha de manter os cálculos em GeoDataFrames e a renderização no Qt Core (PySide6) foi definida para balancear a enorme facilidade e padronização que a comunidade Python GIS oferece (GeoPandas) com a velocidade absoluta do C++ Qt Canvas.

## Limitações Atuais (Sprint 05)
- Edição de polígonos com o mouse (Vertex Editor) ainda não está implementada.
- Estilos de camada avançados (gradientes, SVGs de árvores/postes) estão restritos às primitivas de preenchimento até a evolução do `RenderService`.

## Roadmap para Sprint 06 (Cadastro Urbano)
Com a fundação visual do GIS (Sprint 05) concluída e de pé, a **Sprint 06** irá preencher o banco de dados.
- O GIS passará a ler os Lotes, Quadras e Matrículas não só de shapefiles, mas diretamente do nosso banco de dados relacional (Cadastro).
- A tabela `Property` (Proprietários) e `Parcel` (Lote) serão cruzadas.
- Ao clicar num lote no mapa, o GEOGIS não lerá os atributos do .shp (que são engessados), mas fará um SELECT instantâneo no banco de dados buscando dados como "Parcela do IPTU paga" ou "Status do Alvará".
