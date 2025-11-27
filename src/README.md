# src - Scripts y Módulos de Migración

Este directorio contiene el código fuente principal para la migración, transformación y validación de datos de seguros en SoftSeguros.

## Subcarpetas
- `extractors/` : Lectores de archivos Excel (.xlsx, .xls, .xlsm) usando pandas y openpyxl.
- `transformers/` : Pipelines de transformación de datos con pandas.
- `validators/` : Reglas de validación y chequeo de calidad de datos.
- `loaders/` : Exportación de datos a formatos destino (Excel, CSV, DB).
- `formatters/` : Scripts para formateo profesional de reportes y archivos Excel.
- `utils/` : Utilidades compartidas (manejo de archivos, logging, helpers).

## Estándares de Desarrollo
- Scripts en Python 3.x siguiendo patrones ETL.
- Uso de pandas para manipulación masiva de datos.
- openpyxl para formato avanzado de Excel.
- Validaciones y logs detallados para trazabilidad.

## Recomendaciones
- Mantener los scripts organizados por función.
- Documentar cada módulo con docstrings y comentarios en español para lógica de negocio.
- Usar los templates de Excel desde `data/templates/` para reportes.

---
Actualizado: 25/11/2025
