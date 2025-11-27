# Archivos de Datos

Repositorio de datos de entrada, salida y ejemplos para el sistema de migración.

## 📋 Descripción

Esta carpeta contiene todos los archivos de datos organizados por tipo:
- Input: Archivos fuente para procesamiento
- Output: Resultados generados por los scripts
- Samples: Ejemplos y datos de prueba
- Templates: Plantillas Excel para reportes

## 📁 Estructura

```
data/
├── input/          # Archivos Excel de entrada (gitignored)
├── output/         # Resultados de procesamiento (gitignored)
├── samples/        # Datos de ejemplo y prueba
└── templates/      # Plantillas Excel base
```

## 📊 Contenido

### Input
- `Plantilla POLIZAS Actulizada.xlsx` - Archivo principal de pólizas
- Archivos Excel heredados (.xls, .xlsx)
- Datos JSON de conciliación

### Output
- `PLANTILLA_COINCIDEN.xlsx` - Template validado
- `Plantilla POLIZAS_Clasificada_*.xlsx` - Archivos procesados
- Reportes JSON con estadísticas
- Logs de procesamiento

### Samples
- Archivos de ejemplo para testing
- Datos anonimizados
- Casos edge para validación

### Templates
- Estructuras Excel base
- Formatos predefinidos
- Headers estandarizados

## 🚀 Uso

```bash
# Colocar archivos fuente en input/
# Los scripts generan resultados en output/
# Usar samples/ para pruebas
```

## ⚠️ Notas Importantes

- Las carpetas `input/` y `output/` están en `.gitignore`
- Mantener `samples/` y `templates/` versionados
- No subir datos sensibles o personales
