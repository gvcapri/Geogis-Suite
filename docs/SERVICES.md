# Serviços e Infraestrutura

## File Services
Local: `services/files/`
Todo acesso a PDF, Shapefile, Imagens passa por aqui.
```python
pdf_service.extract_text(file_path)
```

## GIS Services
Local: `services/gis/`
Operações espaciais (GeoPandas, Shapely) encapsuladas.
```python
geometry_service.calculate_area(polygon)
```

## Job Manager
Local: `core/jobs/`
```python
job_manager.submit(long_running_task, callback=update_ui)
```
