# Roadmap - GEOGIS Suite

## Sprint 1: Autenticação e Segurança (Concluído)
- Login seguro, criptografia, e restrição de acesso a usuários autorizados.

## Sprint 2: Framework e Base (Concluído)
- Estrutura base da interface, componentes modulares (PySide6), gerenciamento de tema (Light/Dark).
- Configuração do Job Manager, Event Bus, e serviços centrais.

## Sprint 3: Comparativos (Concluído)
- Módulo assíncrono para SHP x Métrica, CRF, Ecoleta.
- Integração de projetos e resultados salvos no banco.

## Sprint 4: Documentos (Próximo)
**Objetivo:** Centralizar todos os documentos de um projeto.
- Biblioteca de documentos (Upload, Versionamento, Modelos).
- Geração automática, Preview (PDF/Word), Assinaturas, Histórico.
- Estrutura de pastas (Memorial, CRF, Relatórios, Licenças, Mapas, PDFs, Planilhas).

## Sprint 5: GIS (Geoprocessamento)
- Visualizador nativo integrado.
- Abrir SHP, GeoPackage, KML/KMZ, GeoJSON, DXF.
- Ferramentas: Camadas, Zoom, Pan, Medição, Seleção, Busca (lote/matrícula), Exportação/Impressão.
- Integrações base (GeoPandas, Shapely, GDAL, Fiona, Rasterio, PyProj).

## Sprint 6: Cadastro Urbano
- Gerenciamento de entidades: Município, Bairro, Quadra, Lote, Matrícula, Proprietário, Área, Perímetro, Coordenadas.
- Ferramentas de pesquisa, importação/exportação e controle de alterações (histórico).

## Sprint 7: Ambiental
- Relatórios Ambientais (APP, Reserva Legal, Vegetação, Recursos Hídricos).
- Licenças, Checklists, Documentação, Fotos, Mapas e Cronograma.

## Sprint 8: CRF
- Módulo de gestão: Cadastro, Modelos, Geração Automática, Aprovação e Revisão.
- Assinatura, PDF, Histórico e Versionamento.

## Sprint 9: Cotação
- Pesquisa de bairros, histórico de preços, cálculo automático, índices e comparações.
- Base histórica de avaliações, relatórios e dashboard com gráficos.

## Sprint 10: Workflow
- Interligação de todos os módulos.
- Pipeline do projeto: Cadastro -> GIS -> Ambiental -> Comparativos -> CRF -> Documentos -> Entrega.
- Definição de responsáveis, prazos, checklists e aprovações de cada etapa.

## Sprint 11: Agenda
- Tarefas, prazos, alertas de atrasos, calendário e pendências individuais por usuário.

## Sprint 12: Dashboard Executivo
- Visão gerencial (Projetos ativos/atrasados, Produção).
- Métricas: Tempo médio, Relatórios gerados, Comparativos, CRFs, Pendências e Gráficos avançados.

## Sprint 13: Administração
- Painel para gerenciamento de usuários (Criar, Editar, Bloquear), Setores e Permissões.
- Logs de Auditoria e Backup Automático.
- Configurações do sistema.

## Sprint 14: IA (Inteligência Artificial)
- Auxiliares inteligentes para validação e insights.
- Exemplos:
  - *"O Memorial possui informações incompatíveis com o SHP."*
  - *"Faltam fotografias da APP."*
  - *"Foram encontradas divergências semelhantes às do Projeto Vista Verde."*

## Sprint 15: Aplicativo Mobile (Opcional)
- Acesso remoto: Consulta de projetos, documentos, workflow, fotos e aprovações.

## Sprint 16: Integrações
- Ecosistema e Nuvem: Google Drive, OneDrive, SharePoint, E-mail, Assinatura Digital.
- Banco de dados em nuvem (PostgreSQL/PostGIS) e APIs Internas.

---

## Versão 1.0 (Lançamento Oficial)
Uma plataforma totalmente integrada conectando Engenharia, Cadastro, GIS, e Relatórios, tudo operando sobre o "GEOGIS Suite Dashboard". O sistema oferecerá valor imediato automatizando comparações, reduzindo dependência do QGIS para consultas simples, gerando laudos padronizados e organizando todo o workflow da equipe.

## Versão 2.0 (Visão de Futuro)
- **Portal do Cliente:** Uma área externa dedicada para que os clientes do GEOGIS Suite possam acompanhar os loteamentos e empreendimentos.
- **Funcionalidades:** Download de arquivos aprovados, visualização do workflow em tempo real, troca de mensagens com a equipe e transparência da evolução, transformando o GEOGIS Suite de uma ferramenta interna em uma plataforma completa de gestão de projetos.
