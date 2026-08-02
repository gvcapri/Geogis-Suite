# Guia de Templates de Relatórios

O sistema deve automatizar as peças técnicas entregues aos órgãos ambientais. 

## Como funciona (Implementação Futura)
Os relatórios (`reports/`) consumirão os dados do SQLAlchemy formatando-os em PDF usando uma engine (ex: `reportlab` ou `jinja2` para HTML -> PDF).

## Tipos de Relatórios
1. **Relatório Fotográfico:** Lê todas as `EnvironmentalPhoto` de uma `Inspection` e plota em grid de 2x2 com a descrição embaixo.
2. **Relatório de Conformidade:** Exportação do Dashboard (Painel de Conformidade). Exibe em gráfico pizza quantas APPs estão regulares vs invadidas, e lista as condicionantes que estouraram o prazo.
3. **Memorial Descritivo:** Puxa os dados espaciais (Área e Perímetro) do `gis_feature_id` e a titularidade do Cadastro Territorial, unindo tudo num Word/PDF.
