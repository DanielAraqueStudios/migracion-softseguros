# DIAN Colombia - Backend API

API REST en Python/FastAPI para calcular el dígito de verificación de NITs colombianos según las normas de la DIAN.

## Instalación

### 1. Crear entorno virtual

```bash
# Windows PowerShell
python -m venv venv
.\venv\Scripts\Activate.ps1

# Linux/Mac
python -m venv venv
source venv/bin/activate
```

### 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

## Uso

### Iniciar servidor

```bash
# Modo desarrollo (auto-reload)
uvicorn app:app --reload

# Modo producción
python app.py
```

El servidor estará disponible en: `http://localhost:8000`

### Endpoints

#### 1. Calcular dígito de verificación

```bash
# PowerShell
$body = @{nit="1003618585"} | ConvertTo-Json
Invoke-RestMethod -Method POST -Uri "http://localhost:8000/calcular" -Body $body -ContentType "application/json"

# curl
curl -X POST "http://localhost:8000/calcular" -H "Content-Type: application/json" -d "{\"nit\":\"1003618585\"}"
```

**Response:**
```json
{
  "nit_original": "1003618585",
  "digito_verificacion": 1,
  "nit_completo": "10036185851",
  "formato_display": "1003618585-1"
}
```

#### 2. Ver ejemplos

```bash
# PowerShell
Invoke-RestMethod -Method GET -Uri "http://localhost:8000/ejemplo"

# curl
curl http://localhost:8000/ejemplo
```

#### 3. Documentación interactiva

Abre en tu navegador:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Estructura del Proyecto

```
backend/
├── app.py              # Aplicación FastAPI principal
├── requirements.txt    # Dependencias Python
└── README.md          # Este archivo
```

## Características

- ✅ Validación de entrada (solo números, máximo 15 dígitos)
- ✅ Algoritmo DIAN oficial implementado
- ✅ CORS habilitado para integraciones frontend
- ✅ Documentación automática (Swagger/ReDoc)
- ✅ Health check endpoint
- ✅ Manejo de errores robusto
- ✅ Formato de salida flexible (completo y con guión)

## Algoritmo DIAN

El cálculo sigue la resolución oficial de la DIAN:

1. Multiplica cada dígito del NIT por su factor de ponderación (posición 1-15)
2. Suma todos los productos
3. Calcula `residuo = suma % 11`
4. Dígito de verificación = `(11 - residuo)` si residuo > 1, sino `residuo`

### Factores de Ponderación

| Posición | Factor | Posición | Factor | Posición | Factor |
|----------|--------|----------|--------|----------|--------|
| 1        | 3      | 6        | 23     | 11       | 47     |
| 2        | 7      | 7        | 29     | 12       | 53     |
| 3        | 13     | 8        | 37     | 13       | 59     |
| 4        | 17     | 9        | 41     | 14       | 67     |
| 5        | 19     | 10       | 43     | 15       | 71     |

## Testing

```bash
# Ejecutar pruebas de endpoints
python -m pytest tests/

# Probar manualmente
python -c "from app import DIANCalculator; print(DIANCalculator.calcular_digito('1003618585'))"
```

## Despliegue

### Docker (opcional)

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app.py .
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
```

```bash
docker build -t dian-api .
docker run -p 8000:8000 dian-api
```

## Licencia

MIT License - Ver LICENSE.md en el directorio raíz
