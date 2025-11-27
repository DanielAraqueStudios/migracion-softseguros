# Conciliador de Clientes

Scripts para conciliación y matching de datos de clientes entre diferentes fuentes.

## 📋 Descripción

Esta carpeta contiene los scripts principales para:
- Comparación de datos entre TOMADOR y ASEGURADO
- Generación de reportes de diferencias en formato JSON
- Estadísticas de coincidencias y discrepancias
- Exportación de plantillas con datos validados

## 📁 Archivos

### Scripts Principales
- `exportar_plantilla_coincidentes.py` - Genera template Excel con datos validados y NIT corregidos
- `comparar_tomador_asegurado.py` - Compara columnas y exporta diferencias JSON

### Archivos de Salida
- `PLANTILLA_COINCIDEN.xlsx` - Template final con datos limpios
- `diferencias_tomador_asegurado.json` - Reporte de diferencias
- `estadisticas_conciliacion.json` - Estadísticas del proceso

## 🚀 Uso

```bash
# Ejecutar conciliación completa
python comparar_tomador_asegurado.py

# Generar template validado
python exportar_plantilla_coincidentes.py
```

## 📊 Funcionalidades

### Comparación TOMADOR vs ASEGURADO
- Análisis de similitud entre nombres
- Validación cruzada de documentos
- Detección de inconsistencias

### Validación de NIT
- Cálculo automático de dígito de verificación
- Corrección de formatos inválidos
- Reporte de errores encontrados

### Generación de Templates
- Mapeo de campos estandarizados
- Inclusión de campos calculados (género, teléfonos, etc.)
- Formato Excel profesional

## 📝 Logs

Los procesos generan logs detallados en `../logs/` con:
- Cambios realizados por fila
- Errores encontrados
- Estadísticas de procesamiento

## 🔗 Dependencias

Requiere acceso a:
- Archivo fuente de datos
- Scripts de utilidad compartidos
- Configuraciones de validación
