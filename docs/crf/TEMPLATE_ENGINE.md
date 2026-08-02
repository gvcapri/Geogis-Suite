# Motor de Templates (Template Engine)

A geração documental automatizada baseia-se na entidade `CRFTemplate`.

## Como Funciona

1. **Armazenamento:** Os textos-base das minutas, declarações e ofícios são salvos no banco de dados com marcações no padrão Jinja2 `{{Variavel}}`.
2. **Resolução:** O módulo CRF recebe o pedido de geração e consulta o `TerritorialRepository` ou o `ProjectRepository`.
3. **Geração:** O `DocumentGenerator` pega o dicionário `{ 'Variavel': 'Valor Real' }`, injeta no texto base, e expele o resultado final.

Conforme a decisão arquitetural da Sprint 8, o foco primário será renderização via HTML -> PDF interno (não requer instalação do MS Word).
