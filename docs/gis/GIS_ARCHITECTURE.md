# Arquitetura do Módulo GIS

O Módulo GIS foi desenhado para ser o motor espacial nativo do GEOGIS Suite, permitindo que a equipe execute as rotinas do dia a dia (análise, visualização, seleção e auditoria de lotes) sem a necessidade de alternar para o QGIS.

## Princípios (SOLID e Clean Architecture)

1. **Service Layer Isolada (`src/services/gis`):**
   Nenhum objeto do PyQt/PySide6 (widgets, janelas) interage diretamente com bibliotecas pesadas como `geopandas` ou `shapely`. Toda a inteligência é roteada através dos *Services*. Isso permite testes unitários rápidos e previne que mudanças na UI quebrem a lógica espacial.

2. **Renderização Nativa e Assíncrona (`src/modules/gis/widgets/map_canvas.py`):**
   A arquitetura optou por usar `QGraphicsView` no lugar de `QWebEngineView` (HTML/Leaflet). O `QGraphicsView` utiliza aceleração gráfica (QPainterPath) nativa do C++. A conversão das geometrias lógicas (Shapely) para visuais (QPainterPath) é feita pelo `RenderService` em background (utilizando o *Job Manager*), garantindo que a thread principal da UI (janela) nunca congele ao carregar shapefiles pesados (ex: >100.000 lotes).

3. **Injeção de Dependências & Event Bus:**
   O `GISController` atua como ponte. Quando o módulo "Comparativos" encontra um erro em uma matrícula, ele dispara um evento. O GIS escuta no `event_bus`, passa as coordenadas para o `SelectionService`, e o `RenderService` destaca a geometria correspondente em vermelho, movendo a câmera via `MapCanvas`.

## Fluxo de Dados (Exemplo: Abrir Shapefile)
`Usuário Clica (View)` -> `Controller (Async Job)` -> `LayerService (Lê SHP)` -> `RenderService (Converte Geometrias)` -> `View (Desenha no Canvas)`.
