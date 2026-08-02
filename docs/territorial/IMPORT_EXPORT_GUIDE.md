# Guia de Importação e Exportação

O Módulo Territorial suporta interoperabilidade com outras ferramentas (como Excel ou cartórios).

## Importações de Planilhas (CSV/Excel)
- Será implementado nos serviços (`src/modules/territorial/imports/`).
- O usuário envia uma planilha com as colunas: `Quadra`, `Lote`, `Matrícula`, `Proprietário`.
- O importador deve ler a planilha e injetar os dados no banco usando as relações corretas, criando a Quadra, o Proprietário e o Lote em uma única transação atômica. Se um falhar, ocorre *rollback* (tudo é cancelado).

## Qualidade Automática durante a Importação
Assim que a importação termina (assíncrona no Job Manager), o `DataQualityService` varre os novos lotes e alerta se o Lote 12 da Quadra A já existia, prevenindo duplicações.

## Exportação (Relatórios)
- **Estatístico:** Resumo (qtd. Lotes, Área total do projeto vs Área vendável) exportado em PDF.
- O botão "Exportar" da UI chama o `territorial/exports` gerando as listagens em CSV para cruzamento contábil.
