# Sistema de Plugins

Novos módulos podem ser adicionados dinamicamente copiando uma pasta para `src/modules/`.

## Estrutura de um Plugin
```text
meu_modulo/
  __init__.py      # Registra o plugin no PluginLoader
  views.py         # Interface UI
  controllers.py   # Lógica local
```

O `PluginLoader` varre essas pastas, injeta as dependências (DI) e acopla a view no `MainWindow`.
