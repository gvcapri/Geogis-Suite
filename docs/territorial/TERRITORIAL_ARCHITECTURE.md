# Arquitetura do Cadastro Territorial

O Módulo de Cadastro Territorial atua como o sistema nervoso relacional do GEOGIS Suite. 
Ele garante que uma geometria não seja apenas um desenho, e sim uma propriedade legal vinculada a um proprietário, endereço e matrícula.

## Pilares Arquiteturais

1. **Service Layer Pura (`src/modules/territorial/service.py`)**
   Toda a regra de salvamento e recuperação da hierarquia de lotes passa pelo *Service*. Nenhum widget executa `session.commit()` diretamente. O uso do Repository Pattern encapsula o SQLAlchemy, permitindo a mudança futura do SQLite para PostgreSQL sem impacto.

2. **Integração Fraca com o GIS via Eventos**
   Para evitar acoplamento (o Cadastro não deve "importar" o GIS e vice-versa diretamente no código), as comunicações ocorrem puramente pelo `event_bus` central:
   - *Territorial -> GIS*: Dispara `territorial.lot_selected(lot_id, gis_feature_id)`. O GIS escuta e move a câmera.
   - *GIS -> Territorial*: Dispara `gis.feature_clicked(feature_id)`. O Territorial escuta, busca o Lote no banco e abre sua ficha.

3. **Data Quality Module (`src/modules/territorial/validators/data_quality.py`)**
   Desenvolvido como um sub-serviço independente. O `DataQualityService` varre lotes criados ou alterados, retornando listas de *warnings* (ex: "Lote sem área nominal" ou "Sem geometria espacial vinculada"). Estes avisos sobem para a UI e alimentam indicadores do Dashboard.
