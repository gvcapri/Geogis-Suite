# Entidades do Cadastro Territorial

A estrutura foi modelada no SQLAlchemy (`src/database/models/__init__.py`) para suportar a complexidade do direito imobiliário brasileiro:

## Hierarquia Espacial Restrita
`Municipality (1)` -> `(N) Neighborhood (1)` -> `(N) Subdivision (1)` -> `(N) Block (1)` -> `(N) Lot`
Um Lote pertence *obrigatoriamente* a uma Quadra, que pertence a um Loteamento. 

## Vínculos do Lote (`Lot`)
O `Lot` é a unidade de grão mais fino do modelo. Ele tem vínculos múltiplos:
1. **GIS:** Campo `gis_feature_id` (String) vincula a linha do Lote à geometria presente no Shapefile (carregado na tabela do GeoPandas).
2. **Matrícula (`Registry`):** Relação One-to-Many (`Lot` tem várias matrículas ao longo do histórico).
3. **Proprietário (`Owner`):** Relação Many-to-Many via tabela associativa `lot_owners`. Um lote pode pertencer a 2 irmãos (fração ideal), e uma construtora pode ser dona de 50 lotes diferentes simultaneamente.

## Estrutura do Proprietário
A entidade `Owner` possui `document_number` (CPF/CNPJ) e se relaciona com `Address` para endereçamento completo. A busca global indexará esses CPFs e Nomes para recuperação rápida (Search Bar).
