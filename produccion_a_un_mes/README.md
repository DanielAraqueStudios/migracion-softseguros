# Producción a Un Mes - SoftSeguros

## Descripción
Este entorno contiene los scripts y archivos para el procesamiento y migración de datos de pólizas de seguros, siguiendo el estándar profesional de ETL y validación para la empresa SEGUROS UNIÓN.

## Estructura de Carpetas
- `data/input/` : Archivos Excel originales para procesar.
- `output/` : Archivos generados y resultados finales.
- `src/utils/` : Scripts Python para análisis y transformación de datos.

## Scripts Clave
- `analizar_estructura_excel.py` : Analiza columnas, tipos y formatos de los archivos Excel.
- `generar_fecha_fin.py` : Genera la columna de fecha fin sumando un año a la fecha inicio.

## Ejemplo de Datos (primeras 4 columnas)
| NÚMERO DE PÓLIZA | RIESGO | ASEGURADORA | SUBRAMO |
|------------------|--------|-------------|---------|
| 1527934          | DFU947 | SEGUROS DE VIDA SURAMERICANA S.A. | VIDA GRUPO APORTES |
| 101092379        | SNX880 | SEGUROS DE VIDA SURAMERICANA S.A. | PLAN COMPLEMENTARIO COLECTIVO |
| 900315447-6      | FXR853 | COOMEVA MEDICINA PREPAGADA S.A.   | AREA PROTEGIDA |

## Procesos Realizados
- Análisis de estructura y tipos de datos de los archivos Excel.
- Generación automática de columna de fecha fin.
- Validación de formatos y advertencia sobre fechas con hora.

## Recomendaciones
- Coloca los archivos Excel a procesar en `data/input/`.
- Ejecuta los scripts desde la carpeta principal para asegurar rutas correctas.
- Los resultados y archivos procesados se guardan en `output/`.

---
Actualizado: 25/11/2025
