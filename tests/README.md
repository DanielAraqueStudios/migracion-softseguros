# Pruebas

Suite de pruebas unitarias e integración para el sistema de migración.

## 📋 Descripción

Esta carpeta contiene todas las pruebas del sistema:
- Pruebas unitarias de funciones
- Pruebas de integración
- Tests de validación
- Datos de prueba

## 📁 Estructura

```
tests/
├── unit/           # Pruebas unitarias
├── integration/    # Pruebas de integración
├── fixtures/       # Datos de prueba
└── utils/          # Utilidades de testing
```

## 🚀 Ejecución

```bash
# Ejecutar todas las pruebas
python -m pytest tests/

# Ejecutar pruebas específicas
python -m pytest tests/unit/test_validaciones.py

# Con cobertura
python -m pytest --cov=src tests/

# Verbose
python -m pytest -v tests/
```

## 📊 Tipos de Pruebas

### Unitarias
- `test_calcular_dv.py` - Validación algoritmo DV
- `test_clasificar_tomador.py` - Lógica de clasificación
- `test_validar_nit.py` - Validaciones de formato

### Integración
- `test_proceso_completo.py` - Flujo ETL completo
- `test_conciliacion.py` - Proceso de matching
- `test_exportacion.py` - Generación de archivos

### Fixtures
- `datos_prueba.xlsx` - Datos de ejemplo
- `config_test.yaml` - Configuración de pruebas
- `resultados_esperados.json` - Resultados esperados

## 🛠️ Herramientas

- **pytest** - Framework de testing
- **pytest-cov** - Cobertura de código
- **fixtures** - Datos de prueba
- **mocks** - Simulación de dependencias

## 📝 Estructura de Prueba

```python
def test_calcular_dv():
    # Arrange
    nit = "890981212"

    # Act
    dv = calcular_dv(nit)

    # Assert
    assert dv == "2"

def test_clasificar_persona():
    # Arrange
    nombre = "JUAN PEREZ LOPEZ"

    # Act
    tipo = clasificar_tomador(nombre)

    # Assert
    assert tipo == "PERSONA"
```

## 🎯 Cobertura

- **Funciones críticas**: 100% cobertura
- **Lógica de negocio**: 95% cobertura mínima
- **Casos edge**: Cobertura completa

## 🤝 Contribución

- Agregar pruebas para nuevo código
- Mantener fixtures actualizados
- Revisar cobertura antes de merge
- Tests deben ser independientes y rápidos
