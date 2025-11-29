# Migración SoftSeguros - API DIAN

Sistema de migración de datos para SoftSeguros que incluye integración con la API DIAN para validación de NITs.

## 🚀 Inicio Rápido

### 1. Iniciar la API DIAN
```bash
python run_api.py
```

La API estará disponible en: http://127.0.0.1:8000

### 2. Probar la API
```bash
python test_dian_algorithm_simple.py
```

### 3. Ejecutar migración de Excel
```bash
python corregir_nits_columna_x.py
```

## 📋 API Endpoints

- `GET /health` - Verificar estado de la API
- `POST /calcular` - Calcular dígito verificador de NIT
- `GET /docs` - Documentación interactiva (Swagger)

### Ejemplo de uso:
```python
import requests

# Calcular dígito verificador
response = requests.post('http://127.0.0.1:8000/calcular',
                        json={'nit': '1003618585'})
data = response.json()
print(f"NIT completo: {data['nit_completo']}")  # 1003618585-2
```

## 🧪 Tests

- ✅ Algoritmo DIAN validado con múltiples casos de prueba
- ✅ Cálculo correcto de dígitos verificadores
- ✅ Corrección automática de NITs con DV incorrecto
- ✅ Integración completa con API REST

## 📁 Estructura del Proyecto

```
/
├── backend/              # API FastAPI DIAN
│   ├── app.py           # Servidor API
│   └── requirements.txt # Dependencias
├── src/                 # Código fuente
├── data/                # Archivos de datos
├── test_dian_algorithm_simple.py  # Tests de validación
├── corregir_nits_columna_x.py     # Script de migración
└── run_api.py          # Script para iniciar API
```