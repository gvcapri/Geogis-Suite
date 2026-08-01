# Event Bus

Toda comunicação entre módulos ocorre via Event Bus para evitar acoplamento (imports diretos).

## Como funciona
1. Módulo A (Projetos) publica um evento:
```python
event_bus.publish("PROJECT_CREATED", {"id": 1})
```
2. Módulo B (Notificações) reage:
```python
event_bus.subscribe("PROJECT_CREATED", notify_user)
```
