# SPRINT 06 REPORT: Cadastro Territorial

**Status:** Concluído
**Data:** Agosto 2026

## Objetivos Alcançados
- **Modelagem Relacional (Entidades):** Foram incluídas as 8 tabelas centrais (`Municipality`, `Neighborhood`, `Subdivision`, `Block`, `Lot`, `Owner`, `Registry`, `Address`).
- **Data Quality:** Módulo acoplado com sucesso. Capaz de sinalizar divergências espaciais e faltas documentais.
- **Integração Desacoplada (Event Bus):** Implementado `LotSelectedEvent` no Controller. O módulo Territorial e GIS agora interagem bidirecionalmente sem dependerem fortemente do código um do outro.
- **Interface Profissional:** Layout com Árvore de Hierarquia à Esquerda, Formulário de Cadastro Detalhado no Centro e a Barra de Busca Global unificada. Tudo instanciado na `main_window.py` sob o ícone de "Cadastro Territorial".

## Resolução das Questões Abertas (Decisões)
Conforme discutido no Plano de Implementação:
1. **Lote-Proprietário:** Foi implementado `Many-to-Many` (`lot_owners`) para suportar perfeitamente heranças e frações ideais (vários donos pro mesmo lote, ou vários lotes pro mesmo dono).
2. **Divergência de Área:** A área calculada pelo GIS **não sobrescreve** a área nominal da matrícula (`nominal_area_sqm`). O Módulo de `DataQuality` foi construído apenas para *avisar* se as áreas diferem muito (ajudando em retificações), mantendo a integridade legal da matrícula intacta.

## Próximos Passos
O GEOGIS Suite agora é completamente funcional tanto geograficamente (Sprint 05) quanto cadastralmente (Sprint 06). 
As próximas sprints (Ambiental, Workflow, Cotação) se basearão inteiramente nessa base sólida. 
A infraestrutura está pronta.
