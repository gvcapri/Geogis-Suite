# Especificação dos Serviços GIS (GIS_SERVICES)

A camada de serviços concentra toda a lógica espacial do sistema. Segue a estrutura implementada:

### `MapService` (`map_service.py`)
Gerencia o estado global do mapa em relação ao Projeto ativo. Controla zoom, coordenadas centrais, CRS ativo e quais camadas estão visíveis, permitindo salvar essa "sessão" no banco de dados.

### `LayerService` (`layer_service.py`)
Utiliza o `geopandas` para ler nativamente arquivos espaciais (.shp, .geojson, .gpkg). Mantém um registro em memória (`GeoDataFrame`) de todas as camadas, controlando a ordem Z (o que aparece por cima).

### `GeometryService` (`geometry_service.py`)
Lida diretamente com o objeto `shapely.geometry`. Responsável por analisar bounding boxes (para centrar o zoom) e validações topológicas básicas (feições inválidas ou cruzadas).

### `ProjectionService` (`projection_service.py`)
Baseado no `pyproj`. Encarregado de reprojetar camadas inteiras ou pontos únicos on-the-fly para que todas as camadas no Canvas conversem no mesmo Sistema de Referência de Coordenadas (CRS).

### `CoordinateService` (`coordinate_service.py`)
Converte os cliques do mouse da tela (pixels) para o mundo real (coordenadas UTM ou Lat/Lon), formatando-as em tempo real para a Barra de Status.

### `SelectionService` (`selection_service.py`)
Executa operações espaciais como `intersects` ou `contains`. Dado um ponto (clique), varre os `GeoDataFrames` carregados para descobrir qual feição (ex: qual Lote) foi clicada.

### `MeasurementService` (`measurement_service.py`)
Calcula distâncias geodésicas e áreas exatas dos polígonos.

### `RenderService` (`render_service.py`)
Traduz geometrias lógicas matemáticas em polígonos gráficos (`QPainterPath`). Ele entende as Regras de Estilo (cor, espessura, opacidade) e constrói o objeto visual bruto para a UI injetar no Canvas.

### `ExportService` (`export_service.py`)
Responsável por orquestrar a exportação da vista atual (Canvas) para PNG ou PDF, ou as geometrias selecionadas para um novo `.shp`.
