# data - Archivos de Entrada y Salida

Este directorio almacena los archivos de datos utilizados y generados durante la migración y procesamiento de información de seguros.

## Subcarpetas
- `input/` : Archivos fuente originales (Excel, CSV) para migración. No se versionan en git.
- `output/` : Archivos generados por los scripts (reportes, exportaciones, logs). No se versionan en git.
- `samples/` : Datos de ejemplo y pruebas, incluidos en el repositorio.
- `templates/` : Plantillas Excel para generación de reportes y migraciones.

## Recomendaciones
- No modificar los archivos fuente originales; siempre trabajar con copias en `input/`.
- Los resultados y reportes se guardan en `output/`.
- Utiliza los archivos de `samples/` para pruebas antes de procesar datos reales.
- Las plantillas en `templates/` deben usarse para exportaciones con formato profesional.

---
Actualizado: 25/11/2025
