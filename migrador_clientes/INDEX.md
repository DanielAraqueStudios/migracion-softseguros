# Índice de Archivos Migrador de Clientes

Este índice enumera los principales archivos del proceso de migración y enriquecimiento de clientes SoftSeguros v2.

## Scripts ETL
- `analisis_ids.py` — Análisis de IDs y documentos
- `corregir_nits.py` — Corrección y validación de NITs
- `validar_nombres_documentos.py` — Validación de nombres y documentos
- `actualizar_desde_celer.py` — Sincronización y enriquecimiento desde CELER
- `asignar_generos.py` — Asignación automática de género
- `procesar_v2.py` — Pipeline principal v2

## Archivos de Entrada
- `CLIENTES SOFTSEGUROSv2.xlsx` — Base principal de clientes
- `CLIENTES VIGENTES CELER.xlsx` — Clientes y pólizas CELER

## Archivos de Salida y Reportes
- `CLIENTES_SOFTSEGUROS_CORREGIDO_*.xlsx` — Correcciones NITs
- `CLIENTES_SOFTSEGUROS_ACTUALIZADO_*.xlsx` — Actualizaciones desde CELER
- `CLIENTES_SOFTSEGUROSv2_FINAL.xlsx` — Archivo final listo para migración
- `REPORTE_CORRECCIONES_NITS_*.xlsx` — Reportes de NITs
- `REPORTE_ACTUALIZACIONES_*.xlsx` — Reportes de actualizaciones

## Documentación
- `README.md` — Descripción general y glosario
- `INDEX.md` — Índice de archivos y scripts
