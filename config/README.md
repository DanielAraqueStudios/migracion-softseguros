# Configuraciones

Archivos de configuración para parámetros del sistema de migración.

## 📋 Descripción

Esta carpeta contiene configuraciones JSON/YAML que controlan:
- Mapeos de campos entre sistemas
- Reglas de validación
- Parámetros de conexión
- Configuraciones de procesamiento

## 📁 Archivos

### Configuraciones Principales
- `mapeos.json` - Mapeo de campos entre fuentes
- `validaciones.yaml` - Reglas de validación
- `conexion.yaml` - Parámetros de conexión a BD

### Ejemplos
- `config.example.yaml` - Template de configuración

## 🚀 Uso

```python
import yaml
with open('config/validaciones.yaml') as f:
    config = yaml.safe_load(f)
```

## 📊 Estructura Típica

```yaml
# validaciones.yaml
nit:
  formato: '^\d+-\d$'
  algoritmo: 'dian'

campos:
  nombre_completo: 'NOMBRE_DEL_CLIENTE'
  documento: 'DOCUMENTO_DEL_CLIENTE'

reglas:
  persona_max_palabras: 4
  empresa_terminos: ['S.A.', 'LTDA.', 'COOPERATIVA']
```

## ⚠️ Notas Importantes

- No incluir credenciales reales
- Usar variables de entorno para datos sensibles
- Mantener versionado para trazabilidad
