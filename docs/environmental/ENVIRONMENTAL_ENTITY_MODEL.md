# Modelo de Entidades Ambientais

Toda atividade ambiental orbita ao redor do **`EnvironmentalProcess`**, que por sua vez pertence a um **`Project`**.

## Entidades Espaciais
- **APP**, **LegalReserve**, **WaterResource**, **Vegetation**: Todas possuem uma área, um *status*, e crucialmente, o `gis_feature_id` que as liga às geometrias do Mapa.

## Gestão Burocrática
- **License**: Representa a licença (LP, LI, LO). Controla a data de validade que alimenta os cálculos de vencimento.
- **Conditionant**: Relacionada Many-to-One com `License`. Controla prazos de cumprimento.

## Trabalho de Campo
- **Inspection**: Relatório de campo.
- **EnvironmentalPhoto**: Banco de imagens geotagueadas (`location_coords`), vinculadas a um Processo e, opcionalmente, a uma Inspeção específica.

## Dinâmica (Checklist)
- **ChecklistTemplate** e **ChecklistAnswer**: Permitem que os administradores criem itens exigidos globalmente, enquanto o sistema armazena o status de *check* por processo individualmente.
