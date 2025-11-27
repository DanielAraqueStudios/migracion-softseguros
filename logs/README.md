# Logs de Ejecución

Archivos de log generados durante la ejecución de los scripts de migración.

## 📋 Descripción

Esta carpeta contiene todos los logs de ejecución con:
- Trazabilidad completa de procesos
- Errores y warnings encontrados
- Estadísticas de procesamiento
- Cambios realizados por fila

## 📁 Archivos

### Logs Principales
- `clasificacion_tomador.log` - Log del procesamiento de pólizas
- `exportar_plantilla.log` - Log de generación de templates
- `comparacion_tomador.log` - Log de conciliación

### Formato
```
2025-11-27 15:45:31,225 - INFO - Fila 7: Asegurado='RUBER ALBERTO ESCUDERO RINCON' -> Tipo=PERSONA, Documento='98571752.0' -> '98571752.0'
```

## 🚀 Uso

```bash
# Revisar logs recientes
tail -f logs/clasificacion_tomador.log

# Buscar errores
grep "ERROR" logs/*.log

# Contar procesamientos
grep "Fila" logs/clasificacion_tomador.log | wc -l
```

## 📊 Información Registrada

### Por Script
- **clasificar_tomador.py**: Clasificaciones y ajustes de documentos
- **exportar_plantilla.py**: Mapeos y validaciones realizadas
- **comparar_tomador.py**: Comparaciones y diferencias encontradas

### Niveles de Log
- **INFO**: Procesos normales y cambios realizados
- **WARNING**: Situaciones que requieren atención
- **ERROR**: Errores que impiden el procesamiento

## ⚠️ Notas Importantes

- Los logs se rotan automáticamente
- No contienen datos sensibles
- Útiles para debugging y auditoría
- Mantener histórico para trazabilidad
