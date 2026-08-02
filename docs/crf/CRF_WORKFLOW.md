# Fluxo de Trabalho CRF (Workflow e Revisões)

A emissão de uma Regularização Fundiária não pode ser acidental e precisa de trilhas de auditoria (Histórico imutável).

## Fluxo Base

```
Rascunho -> Revisão Técnica -> Aprovado Gestor -> Emitido
```

## Regras de Transição
- O avanço só é permitido se a soma do Checklist e do *Assistente de Emissão* chegar a 100%.
- Se o gestor rejeitar, o `Status` retrocede, porém a versão enviada do arquivo (`CRFRevision`) é "congelada". É gerada uma Revisão 2 para as edições.
- Nunca um arquivo é sobrescrito no sistema (append-only na tabela `CRFRevision`).
