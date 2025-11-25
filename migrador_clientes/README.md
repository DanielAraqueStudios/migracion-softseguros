
# Migrador de Clientes - SoftSeguros v2

Este módulo contiene el pipeline completo para la migración y enriquecimiento de la base de clientes de SoftSeguros, usando CELER como fuente de verdad y agregando asignación automática de género.

## Estructura de Carpetas

```
/migrador_clientes
    /src
        /extractors        # Lectores de Excel
        /transformers      # Transformaciones pandas
        /validators        # Validaciones y reglas
        /loaders           # Exportación
        /formatters        # Formato y reportes
        /utils             # Utilidades
    /data
        /input             # Archivos fuente
        /output            # Resultados y reportes
            /01_analisis
            /02_correcciones
            /03_validaciones
            /04_actualizaciones
            /05_finales
        /samples           # Datos de prueba
        /templates         # Plantillas Excel
    /config              # Configuración YAML/JSON
    /logs                # Logs de ejecución
    /docs                # Especificaciones y diccionarios
    /tests               # Pruebas unitarias
    requirements.txt     # Dependencias
    .env.example         # Variables de entorno
    README.md            # Documentación principal
    INDEX.md             # Índice de archivos
```

## Archivos Clave
- `CLIENTES SOFTSEGUROSv2.xlsx` — Base principal de clientes
- `CLIENTES VIGENTES CELER.xlsx` — Clientes y pólizas CELER
- `CLIENTES_SOFTSEGUROSv2_FINAL.xlsx` — Archivo final listo para migración

## Estado del Proyecto

| Fase | Estado | Registros | Resultado |
|------|--------|-----------|-----------|
| 1. Análisis | ✅ Completado | 1,370 | 99.3% coincidencia |
| 2. Corrección NITs | ✅ Completado | 217 corregidos | 100% con formato DIAN |
| 3. Validación | ✅ Completado | 1,170 comparados | 99.7% exactitud |
| 4. Actualización | ✅ Completado | 3,449 cambios | 1,261 registros enriquecidos |
| 5. Género | ✅ Completado | 1,370 | 77.3% asignados automáticamente |
| 6. Archivo Final v2 | ✅ Listo | 1,370 | **LISTO PARA REVISIÓN** |

## Siguiente Paso

1. Revisar archivo final: `data/output/05_finales/CLIENTES_SOFTSEGUROSv2_FINAL.xlsx`
2. Validar con área de negocio los pendientes en `05_finales/README.md`
3. Revisar columna GÉNERO y corregir manualmente los 84 casos marcados como 'REVISAR' (ver `REPORTE_GENEROS_*.xlsx`)
4. Resolver manualmente el NIT duplicado `900437270-3`
5. Verificar los 200 registros únicos de SOFTSEGUROS
6. Aprobar para carga en sistema de producción

## Glosario de Términos

| Término | Significado |
|---------|-------------|
| NIT | Número de Identificación Tributaria |
| C.C | Cédula de Ciudadanía |
| C.E | Cédula de Extranjería |
| PSP | Pasaporte |
| NUIP/DIPL | Número Único de Identificación Personal |
| Dígito Verificador | Dígito de control del NIT (DIAN) |
| Póliza | Contrato de seguro |
| Tomador | Cliente/titular de la póliza |
| Prima | Monto pagado por el seguro |
| Vigencia | Periodo de validez de la póliza |
| Ramo | Tipo de seguro |
| CELER | Sistema nuevo |
| SoftSeguros | Sistema legacy |

## Tecnologías Utilizadas
- Python 3.x
- pandas
- openpyxl
- xlrd
- xlsxwriter
- xlwings
- pyyaml

## Soporte
Para dudas o problemas, contactar al equipo de desarrollo.
