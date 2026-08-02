# Arquitetura do Módulo Ambiental

O Módulo Ambiental gerencia os processos de licenciamento, Áreas de Preservação e inspeções. Ele foi projetado para atuar em conjunto com o `GISModule` (Sprint 5) e o `TerritorialModule` (Sprint 6).

## Camadas e Componentes

1. **EnvironmentalController**: Atua como maestro. Quando o usuário abre um "Processo Ambiental", ele coordena o carregamento dos dados, das licenças, condicionantes, APPs e fotos.
2. **JobManager & ComplianceService**: A inovação técnica desta sprint. Ao invés de travar a UI iterando sobre centenas de condicionantes para descobrir quais estão vencidas, o `Controller` lança uma *Task Assíncrona* (`calculate_compliance`) no Job Manager. O resultado volta via `Signal` e pinta os painéis do Dashboard de Verde, Amarelo ou Vermelho.
3. **Eventos**:
   - `AppSelectedEvent`: Transita pelo Event Bus. Quando a UI Ambiental quer focar numa reserva legal, emite este evento. O motor GIS (se estiver aberto na janela) fará Pan/Zoom na área.
