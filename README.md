# Migración SoftSeguros

Sistema de migración de datos para Seguros Unión, especializado en procesamiento ETL de datos de seguros desde archivos Excel heredados.

## 📋 Descripción

Este proyecto automatiza la migración y validación de datos de pólizas de seguros, incluyendo:
- Extracción de datos desde archivos Excel (.xlsx, .xls)
- Transformación y limpieza de datos
- Validación de documentos NIT/CC con cálculo de dígito de verificación (API DIAN)
- Generación de reportes y plantillas estandarizadas
- Conciliación entre diferentes fuentes de datos (Celer → SoftSeguros)

## 🏗️ Arquitectura

```
migracion-softseguros/
├── backend/                  # API DIAN para cálculo de dígitos de verificación
│   ├── app.py               # FastAPI server
│   └── requirements.txt     # Dependencias del backend
├── conciliador_clientes/     # Scripts de conciliación y matching
├── NEW_ARCHIVE_TO_BE_SENT/   # Procesamiento de archivos de pólizas
├── src/                      # Código fuente principal
├── data/                     # Archivos de datos (input/output/samples)
├── config/                   # Configuraciones JSON/YAML
├── logs/                     # Logs de ejecución
├── docs/                     # Documentación y especificaciones
└── tests/                    # Pruebas unitarias e integración
```

---

## 🔢 Backend - API DIAN (Dígito de Verificación)

El directorio `backend/` contiene una API REST en **FastAPI** para calcular el dígito de verificación de NITs colombianos según la normativa oficial de la DIAN.

### Estructura del Backend

```
backend/
├── app.py              # Aplicación FastAPI principal
├── requirements.txt    # Dependencias Python (fastapi, uvicorn, pydantic)
├── README.md           # Documentación específica del backend
├── test_api.py         # Tests de la API
├── verificar_calculo.py # Script de verificación del algoritmo
├── src/                # Código fuente PHP original (referencia)
├── frontend/           # Interfaz web opcional
└── venv/               # Entorno virtual Python
```

### Iniciar el Servidor API

```powershell
# Desde la carpeta raíz del proyecto
cd backend

# Activar entorno virtual (si existe)
.\venv\Scripts\Activate.ps1

# Instalar dependencias
pip install -r requirements.txt

# Iniciar servidor en modo desarrollo
uvicorn app:app --reload

# O ejecutar directamente
python app.py
```

El servidor estará disponible en: `http://localhost:8000`

### Endpoints Disponibles

| Endpoint | Método | Descripción |
|----------|--------|-------------|
| `/` | GET | Información de la API |
| `/health` | GET | Health check del servidor |
| `/calcular` | POST | Calcula el DV de un NIT |
| `/ejemplo` | GET | NITs de ejemplo con DV calculado |
| `/docs` | GET | Documentación Swagger UI |
| `/redoc` | GET | Documentación ReDoc |

### Ejemplo de Uso

**PowerShell:**
```powershell
$body = @{nit="890981212"} | ConvertTo-Json
Invoke-RestMethod -Method POST -Uri "http://localhost:8000/calcular" -Body $body -ContentType "application/json"
```

**cURL:**
```bash
curl -X POST "http://localhost:8000/calcular" \
     -H "Content-Type: application/json" \
     -d '{"nit":"890981212"}'
```

**Response:**
```json
{
  "nit_original": "890981212",
  "digito_verificacion": 5,
  "nit_completo": "8909812125",
  "formato_display": "890981212-5"
}
```

### Algoritmo DIAN Implementado

El cálculo sigue la normativa oficial de la DIAN con los siguientes factores de ponderación:

```
Posición:  1   2   3   4   5   6   7   8   9  10  11  12  13  14  15
Factor:    3   7  13  17  19  23  29  37  41  43  47  53  59  67  71
```

**Fórmula:**
1. Multiplicar cada dígito por su factor de posición (de derecha a izquierda)
2. Sumar todos los productos
3. Calcular `residuo = suma % 11`
4. Si `residuo > 1`: DV = `11 - residuo`, sino: DV = `residuo`

### Características de la API

- ✅ Validación de entrada (solo números, máximo 15 dígitos)
- ✅ Algoritmo DIAN oficial implementado
- ✅ CORS habilitado para integraciones frontend
- ✅ Documentación automática (Swagger/ReDoc)
- ✅ Health check endpoint
- ✅ Manejo de errores robusto
- ✅ Formato de salida flexible (completo y con guión)

### Integración con Scripts del Proyecto

Los scripts interactivos (`calculador_nits_interactivo.py`) usan esta API automáticamente:

1. El script verifica si el servidor está corriendo
2. Si no está corriendo, lo inicia automáticamente en background
3. Envía requests a `http://localhost:8000/calcular`
4. Procesa las respuestas y genera los archivos Excel

---

## 🔄 Conciliador de Clientes

El directorio `conciliador_clientes/` contiene scripts para la conciliación y matching de datos de clientes entre diferentes fuentes (CELER vs SoftSeguros).

### Estructura del Conciliador

```
conciliador_clientes/
├── comparar_tomador_asegurado.py       # Compara TOMADOR vs ASEGURADO y genera JSON de diferencias
├── exportar_plantilla_coincidentes.py  # Genera template Excel con datos validados
├── estadisticas_match_json_excel.py    # Estadísticas de coincidencias
├── buscar_nit_sin_dv_y_cedula.py       # Detecta NITs sin dígito de verificación
├── llenar_plantilla_nombres_apellidos.py # Rellena plantilla con nombres separados
├── mostrar_columnas_informe.py         # Muestra estructura de columnas
├── mostrar_columnas_informe_personas.py # Estructura del informe de personas
├── comparar_identificaciones_informe_json.py # Compara IDs entre JSON e informe
├── leer_estructura_plantilla.py        # Lee estructura de plantilla Excel
│
├── clientes_activos/                   # Archivos de clientes activos
│   └── diferencias_tomador_asegurado.json  # Reporte de diferencias
├── data_celer/                         # Datos exportados de CELER
│   └── InformedePersonas CELER.xlsx   # Informe de personas
├── plantilla/                          # Templates de salida
│   └── PLANTILLA_COINCIDEN.xlsx       # Plantilla con coincidentes
├── ERRORES/                            # Registros con errores
│
├── logs_comparacion.log                # Log de comparaciones
└── logs_coincidencias_identificacion.txt # Log de coincidencias
```

### Scripts Principales

#### 1. Comparar TOMADOR vs ASEGURADO
Compara los campos TOMADOR y ASEGURADO en registros con tipo NIT, detectando inconsistencias.

```powershell
cd conciliador_clientes
python comparar_tomador_asegurado.py
```

**Funcionalidades:**
- Filtra registros con tipo documento NIT
- Normaliza nombres (mayúsculas, sin espacios)
- Detecta diferencias entre TOMADOR y ASEGURADO
- Calcula dígito de verificación DIAN
- Exporta diferencias a JSON

**Salida:** `clientes_activos/diferencias_tomador_asegurado.json`

#### 2. Exportar Plantilla de Coincidentes
Genera una plantilla Excel con datos validados y formateados.

```powershell
python exportar_plantilla_coincidentes.py
```

**Funcionalidades:**
- Lee identificaciones del JSON de diferencias
- Busca coincidencias en el informe de personas CELER
- Separa nombres y apellidos automáticamente
- Mapea tipos de documento (CC → Cédula, NIT → NIT, etc.)
- Calcula dígito de verificación para NITs
- Genera teléfonos móviles con tipo

**Salida:** `plantilla/PLANTILLA_COINCIDEN.xlsx`

#### 3. Estadísticas de Match
Muestra estadísticas de coincidencia entre el Excel y el JSON.

```powershell
python estadisticas_match_json_excel.py
```

**Salida en consola:**
```
--- Estadísticas de comparación Tomador vs Asegurado ---
Total registros en Excel: 1,370
Total registros con mismatch (JSON): 210
Total registros coincidentes: 1,160
Porcentaje de coincidencia: 84.67%
```

#### 4. Buscar NIT sin DV
Detecta NITs que no tienen dígito de verificación en los registros.

```powershell
python buscar_nit_sin_dv_y_cedula.py
```

**Detecta:**
- NITs con formato incompleto (7-10 dígitos sin DV)
- Registros con cédula válida asociada

### Mapeo de Tipos de Documento

| Valor Original | Valor Mapeado |
|----------------|---------------|
| CC, C.C, CEDULA, IND | Cédula |
| NIT | NIT |
| PSP, CE | Cédula de Extranjería |
| Vacío/NAN | (vacío) |

### Flujo de Conciliación

```
┌────────────────────────────────────────────────────────────────┐
│                    FLUJO DE CONCILIACIÓN                        │
└────────────────────────────────────────────────────────────────┘

1️⃣ COMPARACIÓN INICIAL
   └─> python comparar_tomador_asegurado.py
       ├─> Lee: clientes_activos/*.xlsx
       ├─> Filtra: Registros con tipo NIT
       ├─> Compara: TOMADOR vs ASEGURADO
       └─> Genera: diferencias_tomador_asegurado.json

2️⃣ ESTADÍSTICAS
   └─> python estadisticas_match_json_excel.py
       └─> Muestra: % coincidencia, totales

3️⃣ EXPORTAR PLANTILLA
   └─> python exportar_plantilla_coincidentes.py
       ├─> Lee: JSON de diferencias + Informe CELER
       ├─> Busca: Coincidencias por ID y nombre
       ├─> Procesa: Nombres, DV, teléfonos
       └─> Genera: PLANTILLA_COINCIDEN.xlsx

4️⃣ VALIDACIÓN ADICIONAL
   └─> python buscar_nit_sin_dv_y_cedula.py
       └─> Detecta: NITs incompletos para corrección
```

---

## 📦 Migrador de Clientes

El directorio `migrador_clientes/` contiene el pipeline completo para la migración y enriquecimiento de la base de clientes de SoftSeguros, usando CELER como fuente de verdad.

### Estructura del Migrador

```
migrador_clientes/
├── procesar_v2.py                     # Pipeline principal v2 (orquestador)
├── analisis_ids.py                    # Wrapper: análisis de IDs
├── corregir_nits.py                   # Wrapper: corrección de NITs
├── validar_nombres_documentos.py      # Wrapper: validación nombres
├── actualizar_desde_celer.py          # Wrapper: actualización desde CELER
├── asignar_generos.py                 # Wrapper: asignación de género
│
├── src/                               # Código fuente modular
│   ├── transformers/                  # Transformaciones de datos
│   │   ├── actualizar_desde_celer.py  # Sincroniza datos con CELER
│   │   ├── asignar_generos.py         # Asigna género por nombre
│   │   └── corregir_nits.py           # Corrige formato NITs DIAN
│   └── validators/                    # Validaciones
│       ├── analisis_ids.py            # Análisis de documentos
│       └── validar_nombres_documentos.py # Valida coincidencias
│
├── data/                              # Archivos de datos
│   ├── input/                         # Archivos fuente
│   ├── output/                        # Resultados por fase
│   │   ├── 01_analisis/
│   │   ├── 02_correcciones/
│   │   ├── 03_validaciones/
│   │   ├── 04_actualizaciones/
│   │   └── 05_finales/
│   ├── samples/                       # Datos de prueba
│   └── templates/                     # Plantillas Excel
│
├── config/                            # Configuraciones YAML/JSON
├── logs/                              # Logs de ejecución
├── docs/                              # Documentación técnica
├── tests/                             # Pruebas unitarias
│
├── CLIENTES SOFTSEGUROSv2.xlsx        # Base principal de clientes
├── CLIENTES VIGENTES CELER.xlsx       # Clientes y pólizas CELER
├── CLIENTES_SOFTSEGUROSv2_FINAL.xlsx  # ⭐ Archivo final migración
│
├── requirements.txt                   # Dependencias Python
├── INDEX.md                           # Índice de archivos
└── README.md                          # Documentación específica
```

### Scripts del Pipeline

#### 1. Análisis de Identificaciones
Analiza la calidad de números de documento en ambas bases.

```powershell
cd migrador_clientes
python analisis_ids.py
```

**Funcionalidades:**
- Detecta identificaciones vacías o nulas
- Identifica duplicados en cada base
- Valida formatos de NITs (con/sin DV)
- Compara IDs entre SOFTSEGUROS y CELER
- Genera distribución por tipo de documento

**Salida:** `data/output/01_analisis/analisis_ids_*.xlsx`

#### 2. Corrección de NITs
Corrige automáticamente el formato de NITs según algoritmo DIAN.

```powershell
python corregir_nits.py
```

**Funcionalidades:**
- Detecta NITs sin formato correcto
- Calcula dígito de verificación DIAN
- Aplica formato `XXXXXXXX-X`
- Preserva estructura original de 41 columnas

**Salida:** `data/output/02_correcciones/CLIENTES_SOFTSEGUROS_CORREGIDO_*.xlsx`

#### 3. Validación de Nombres
Valida coincidencia de nombres asociados a documentos entre bases.

```powershell
python validar_nombres_documentos.py
```

**Funcionalidades:**
- Normaliza texto (mayúsculas, sin tildes, sin espacios extras)
- Calcula similitud con SequenceMatcher
- Clasifica por severidad (crítico, significativo, menor)
- Detecta IDs con múltiples nombres

**Salida:** `data/output/03_validaciones/VALIDACION_NOMBRES_DOCUMENTOS_*.xlsx`

#### 4. Actualización desde CELER
Sincroniza y enriquece SOFTSEGUROS usando CELER como fuente de verdad.

```powershell
python actualizar_desde_celer.py
```

**Funcionalidades:**
- Actualiza nombres y apellidos
- Sincroniza fechas de nacimiento
- Actualiza teléfonos móviles
- Actualiza emails
- Actualiza direcciones

**Lógica:**
```
SI campo_celer tiene valor:
    SI campo_soft está vacío → Actualizar
    SI campo_soft tiene valor diferente → Actualizar (CELER prevalece)
SINO:
    → Mantener valor de SOFTSEGUROS
```

**Salida:** `data/output/04_actualizaciones/CLIENTES_SOFTSEGUROS_ACTUALIZADO_*.xlsx`

#### 5. Asignación de Géneros
Asigna automáticamente género (M/F) basándose en el primer nombre.

```powershell
python asignar_generos.py
```

**Funcionalidades:**
- Base de datos de +150 nombres colombianos comunes
- Detecta nombres masculinos y femeninos
- Marca como 'REVISAR' los ambiguos
- Excluye NITs (empresas) del proceso

**Salida:** `data/output/05_finales/CLIENTES_SOFTSEGUROSv2_FINAL.xlsx`

### Estado del Pipeline

| Fase | Script | Estado | Resultado |
|------|--------|--------|-----------|
| 1. Análisis | `analisis_ids.py` | ✅ | 99.3% coincidencia |
| 2. NITs | `corregir_nits.py` | ✅ | 217 corregidos |
| 3. Validación | `validar_nombres_documentos.py` | ✅ | 99.7% exactitud |
| 4. Actualización | `actualizar_desde_celer.py` | ✅ | 3,449 cambios |
| 5. Género | `asignar_generos.py` | ✅ | 77.3% asignados |

### Flujo del Pipeline

```
┌────────────────────────────────────────────────────────────────┐
│                    PIPELINE MIGRADOR v2                         │
└────────────────────────────────────────────────────────────────┘

         CLIENTES SOFTSEGUROS.xlsx    CLIENTES VIGENTES CELER.xlsx
                    │                            │
                    └──────────┬─────────────────┘
                               │
                    ┌──────────▼──────────┐
              1️⃣   │   analisis_ids.py   │  → Análisis de calidad
                    └──────────┬──────────┘
                               │
                    ┌──────────▼──────────┐
              2️⃣   │   corregir_nits.py  │  → Formato DIAN
                    └──────────┬──────────┘
                               │
                    ┌──────────▼──────────┐
              3️⃣   │ validar_nombres.py  │  → Validar coincidencias
                    └──────────┬──────────┘
                               │
                    ┌──────────▼──────────┐
              4️⃣   │ actualizar_celer.py │  → Sincronizar datos
                    └──────────┬──────────┘
                               │
                    ┌──────────▼──────────┐
              5️⃣   │ asignar_generos.py  │  → Asignar M/F
                    └──────────┬──────────┘
                               │
                    ┌──────────▼──────────┐
                    │  ARCHIVO FINAL v2   │
                    │  1,370 registros    │
                    │  ✅ LISTO MIGRACIÓN │
                    └─────────────────────┘
```

### Archivos de Entrada/Salida

| Archivo | Tipo | Descripción |
|---------|------|-------------|
| `CLIENTES SOFTSEGUROSv2.xlsx` | Entrada | Base principal (1,370 registros) |
| `CLIENTES VIGENTES CELER.xlsx` | Entrada | Fuente de verdad CELER |
| `CLIENTES_SOFTSEGUROSv2_FINAL.xlsx` | Salida | ⭐ Archivo final para migración |
| `REPORTE_CORRECCIONES_NITS_*.xlsx` | Reporte | Detalle de NITs corregidos |
| `REPORTE_ACTUALIZACIONES_*.xlsx` | Reporte | Trazabilidad de cambios |

---

## 📋 Procesamiento de Pólizas (NEW_ARCHIVE_TO_BE_SENT)

El directorio `NEW_ARCHIVE_TO_BE_SENT/` contiene scripts para clasificación automática de entidades y ajuste de documentos en archivos de pólizas.

### Estructura del Directorio

```
NEW_ARCHIVE_TO_BE_SENT/
├── clasificar_tomador.py              # Script principal de clasificación
├── clasificacion_tomador.log          # Log detallado de cambios
│
├── Plantilla POLIZAS Actulizada.xlsx  # Archivo fuente de pólizas
├── Plantilla POLIZAS_Clasificada.xlsx # Versión procesada v1
├── Plantilla POLIZAS_Clasificada_v2.xlsx
├── Plantilla POLIZAS_Clasificada_v3.xlsx
├── Plantilla POLIZAS_Clasificada_v4.xlsx # ⭐ Última versión procesada
│
├── Copy of Copia de errores.xlsx      # Archivo de errores original
├── Copy of Copia de errores_corregido.xlsx # Errores corregidos
│
└── README.md                          # Documentación específica
```

### Script Principal: clasificar_tomador.py

Clasifica automáticamente entidades (PERSONA/EMPRESA) y ajusta documentos.

```powershell
cd NEW_ARCHIVE_TO_BE_SENT
python clasificar_tomador.py
```

### Funcionalidades

#### 1. Clasificación Automática de Entidades

| Tipo | Criterio |
|------|----------|
| **PERSONA** | Nombres propios con 2-4 palabras, sin términos empresariales |
| **EMPRESA** | Contiene términos empresariales o >4 palabras |
| **DESCONOCIDO** | Campo vacío o nulo |

#### 2. Términos Empresariales Detectados

```
COOPERATIVA, FONDO, S.A., LTDA., SAS, CIA, LIMITADA,
SOCIEDAD, ASOCIADOS, GRUPO, CORPORACION, DEPARTAMENTO,
EMPLEADOS, SENA, AFROAMERICANA, PARROQUIAL, COLEGIO,
INSTITUTO, VICARIAL, ACINPRO, COOSANROQUE
```

#### 3. Ajuste de Documentos

| Tipo | Acción |
|------|--------|
| **PERSONA** | Quita dígito de verificación si existe (`890981212-5` → `890981212`) |
| **EMPRESA** | Calcula y agrega DV si falta (`890981212` → `890981212-5`) |

### Columnas Procesadas

| Columna Excel | Campo | Basado en |
|---------------|-------|-----------|
| AB | DOCUMENTO DEL TOMADOR | AA (NOMBRE DEL TOMADOR) |
| AD | DOCUMENTO DEL ASEGURADO | AC (NOMBRE DEL ASEGURADO) |
| Z | DOCUMENTO DEL CLIENTE | AA (mismo tipo que tomador) |

### Algoritmo de Decisión

```
┌─────────────────────────────────────────────────────────────┐
│                  CLASIFICACIÓN DE ENTIDAD                    │
└─────────────────────────────────────────────────────────────┘

                    ┌─────────────────┐
                    │  Leer Nombre    │
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │ ¿Está vacío?    │───SI──→ DESCONOCIDO
                    └────────┬────────┘
                             │ NO
                    ┌────────▼────────┐
                    │ ¿Contiene       │
                    │ términos        │───SI──→ EMPRESA
                    │ empresariales?  │
                    └────────┬────────┘
                             │ NO
                    ┌────────▼────────┐
                    │ ¿Tiene >4       │───SI──→ EMPRESA
                    │ palabras?       │
                    └────────┬────────┘
                             │ NO
                    ┌────────▼────────┐
                    │ ¿Tiene 2-4      │───SI──→ PERSONA
                    │ palabras?       │
                    └────────┬────────┘
                             │ NO
                    ┌────────▼────────┐
                    │ ¿Mayúsculas     │
                    │ >2 palabras?    │───SI──→ EMPRESA
                    └────────┬────────┘
                             │ NO
                             ▼
                          PERSONA
```

### Logs Generados

El archivo `clasificacion_tomador.log` registra:
- Clasificación por fila y columna
- Cambios realizados en documentos (antes/después)
- Estadísticas de procesamiento
- Errores encontrados

---

## 📅 Producción a Un Mes

El directorio `produccion_a_un_mes/` contiene scripts para el procesamiento de pólizas con vigencia de un mes, incluyendo análisis de estructura Excel y generación de fechas.

### Estructura del Directorio

```
produccion_a_un_mes/
├── src/
│   ├── dian_utils/                    # Utilidades DIAN
│   │   ├── dian_verificacion.py       # Cálculo de DV (módulo reutilizable)
│   │   └── DIAN/                      # Recursos DIAN adicionales
│   └── utils/                         # Scripts de procesamiento
│       ├── analizar_estructura_excel.py  # Análisis de columnas y tipos
│       ├── generar_fecha_fin.py          # Genera fecha fin (+1 año)
│       └── comparar_nits.py              # Comparación de NITs
│
├── data/
│   ├── input/                         # Archivos Excel a procesar
│   └── clients_input/                 # Datos de clientes
│
├── output/                            # Archivos procesados
│
├── conciliador_clientes/              # Sub-módulo de conciliación
│   ├── carpeta_1/
│   ├── carpeta_2/
│   └── carpeta_3/
│
├── tests/                             # Pruebas unitarias
└── README.md                          # Documentación específica
```

### Scripts Disponibles

#### 1. Módulo DIAN (dian_verificacion.py)
Módulo reutilizable para cálculo de dígito de verificación DIAN.

```python
from src.dian_utils.dian_verificacion import calcular_digito_verificacion

nit = "900437270"
dv = calcular_digito_verificacion(nit)
print(f"NIT: {nit}-{dv}")  # NIT: 900437270-3
```

**Algoritmo:**
- Pesos oficiales DIAN: `[71, 67, 59, 53, 47, 43, 41, 37, 29, 23, 19, 17, 13, 7, 3]`
- Aplicados de derecha a izquierda
- Fórmula: `DV = (11 - (suma % 11))` si residuo > 1, sino residuo

#### 2. Analizar Estructura Excel
Analiza columnas, tipos y formatos de archivos Excel.

```powershell
cd produccion_a_un_mes
python src/utils/analizar_estructura_excel.py
```

**Detecta:**
- Tipos de datos por columna (datetime, object, float, int)
- Formato de fechas (con/sin hora)
- Fechas en formato texto
- Muestra de valores por columna

**Salida en consola:**
```
Archivo: data/input/polizas.xlsx
Filas: 1500, Columnas: 25
Columnas, tipos y formato detectado:
  - NÚMERO DE PÓLIZA: object | Formato: Texto | Ejemplo: ['1527934', '101092379']
  - FECHA INICIO: datetime64[ns] | Formato: Solo fecha | Ejemplo: [...]
```

#### 3. Generar Fecha Fin
Genera la columna de fecha fin sumando un año a la fecha de inicio.

```powershell
python src/utils/generar_fecha_fin.py
```

**Funcionalidades:**
- Lee archivos Excel de `data/input/`
- Detecta columna de fecha inicio (columna I)
- Calcula fecha fin (+1 año)
- Limpia formatos de fecha inconsistentes
- Exporta a `output/` con sufijo `_con_fecha_fin.xlsx`

**Manejo de fechas:**
- Formato esperado: `dd/mm/yyyy`
- Convierte datetime a string formateado
- Marca fechas inválidas como `FECHA_FALTANTE`

### Flujo de Trabajo

```
┌────────────────────────────────────────────────────────────────┐
│              PRODUCCIÓN A UN MES - FLUJO                        │
└────────────────────────────────────────────────────────────────┘

         data/input/*.xlsx
               │
    ┌──────────▼──────────┐
    │ analizar_estructura │  → Ver columnas y tipos
    │      _excel.py      │
    └──────────┬──────────┘
               │
    ┌──────────▼──────────┐
    │ generar_fecha_fin   │  → Crear columna FECHA FIN
    │        .py          │
    └──────────┬──────────┘
               │
               ▼
    output/*_con_fecha_fin.xlsx
```

### Ejemplo de Datos Procesados

| NÚMERO DE PÓLIZA | RIESGO | ASEGURADORA | FECHA INICIO | FECHA FIN |
|------------------|--------|-------------|--------------|-----------|
| 1527934 | DFU947 | SEGUROS DE VIDA SURAMERICANA | 01/01/2025 | 01/01/2026 |
| 101092379 | SNX880 | SEGUROS DE VIDA SURAMERICANA | 15/03/2025 | 15/03/2026 |

---

## 🚀 Inicio Rápido

### Prerrequisitos
- Python 3.8+
- pip para gestión de dependencias

### Instalación
```bash
# Clonar repositorio
git clone <url-del-repo>
cd migracion-softseguros

# Crear entorno virtual
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# o
.venv\Scripts\activate     # Windows

# Instalar dependencias
pip install -r requirements.txt
pip install pandas openpyxl requests fastapi uvicorn
```

## 🔧 Herramientas de NITs

### Calculador Interactivo de Dígitos de Verificación
Calcula y corrige el dígito de verificación de NITs usando la API DIAN.

```bash
python calculador_nits_interactivo.py
```

**Características:**
- Selección interactiva de archivo Excel y columna
- Solo procesa NITs con formato `número-dígito` (ej: 890981212-5)
- Usa API DIAN para cálculo preciso
- Genera archivo con NITs corregidos

### Quitar Dígito de Verificación
Convierte NITs con DV a solo el número base.

```bash
python quitar_dv_interactivo.py
```

**Ejemplo:** `890981212-5` → `890981212`

### Llenar Plantilla SoftSeguros
Busca NITs en Celer y llena la plantilla de SoftSeguros automáticamente.

```bash
python llenar_plantilla_softseguros.py
```

**Mapeo de campos Celer → SoftSeguros:**
| CELER | SOFTSEGUROS |
|-------|-------------|
| Nombre | NOMBRES + APELLIDOS |
| Identificacion | NÚMERO DE DOCUMENTO |
| Tipo_Doc | TIPO DE DOCUMENTO |
| Genero | GÉNERO |
| Estado_civil | ESTADO CIVIL |
| F_Nacimiento | FECHA DE NACIMIENTO |
| Celular_Personal | TELÉFONO MÓVIL |
| Mail_Personal | EMAIL |
| Direccion_Personal | DIRECCIÓN PRINCIPAL |
| Ciudad_Personal | CIUDAD |
| Ocupacion | OCUPACIÓN |

## 📊 Funcionalidades Principales

### 1. Conciliación de Clientes
- Comparación entre TOMADOR y ASEGURADO
- Generación de reportes JSON con diferencias
- Estadísticas de matching

### 2. Clasificación de Entidades
- Automatización PERSONA vs EMPRESA basada en nombres
- Ajuste automático de documentos NIT/CC
- Cálculo de dígito de verificación DIAN

### 3. Procesamiento de Pólizas
- Limpieza y estandarización de datos
- Validación de formatos
- Generación de plantillas Excel

## 🛠️ Tecnologías

- **Python 3.x** - Lenguaje principal
- **pandas** - Manipulación de datos
- **openpyxl** - Procesamiento Excel avanzado
- **xlrd** - Lectura archivos .xls legacy
- **FastAPI** - API para cálculo DIAN
- **requests** - Cliente HTTP
- **logging** - Sistema de logs

## 📁 Estructura de Datos

### Archivos de Entrada
- `Plantilla POLIZAS Actulizada.xlsx` - Archivo principal de pólizas
- `InformedePersonas CELER.xlsx` - Datos de clientes desde Celer
- Archivos JSON de conciliación
- Templates Excel para reportes

### Archivos de Salida
- `PLANTILLA_COINCIDEN.xlsx` - Template con datos validados
- `PLANTILLA_LLENA_*.xlsx` - Plantilla SoftSeguros con datos de Celer
- `*_nits_calculados_*.xlsx` - NITs con DV corregido
- `*_sin_dv_*.xlsx` - NITs sin dígito de verificación
- `clasificacion_tomador.log` - Log de procesamiento

## 🔧 Configuración

Los archivos de configuración están en `config/`:
- Mapeos de campos
- Reglas de validación
- Parámetros de conexión

## 📝 Documentación

Ver carpeta `docs/` para:
- Especificaciones de campos
- Diagramas de flujo
- Manuales de usuario

## 🧪 Testing

```bash
# Ejecutar pruebas
python -m pytest tests/

# Ejecutar pruebas específicas
python -m pytest tests/test_validaciones.py
```

## 🤝 Contribución

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📞 Soporte

Para soporte técnico contactar al equipo de desarrollo.

## 📄 Licencia

Este proyecto es propiedad de Seguros Unión.

> **Nota:** Todos los scripts, archivos de entrada y reportes ahora se encuentran bajo la carpeta `migrador_clientes/` siguiendo la misma estructura profesional y rutas relativas. Ejecuta los scripts desde esa carpeta para asegurar que los outputs y logs se generen correctamente.

## 🚀 Instalación

### Requisitos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)

### Instalar Dependencias

```powershell
pip install pandas openpyxl xlrd xlsxwriter pyyaml
```

O crear un archivo `requirements.txt`:

```txt
pandas>=2.0.0
openpyxl>=3.1.0
xlrd>=2.0.0
xlsxwriter>=3.0.0
pyyaml>=6.0
```

E instalar con:

```powershell
pip install -r requirements.txt
```

## 📊 Archivos de Entrada

### 1. CLIENTES SOFTSEGUROS.xlsx
Archivo con información de clientes del sistema legacy.

**Columnas principales:**
- `NOMBRES`, `APELLIDOS`
- `NÚMERO DE DOCUMENTO`, `TIPO DE DOCUMENTO`
- `TELÉFONO MÓVIL`, `EMAIL`
- `DIRECCIÓN PRINCIPAL`, `CIUDAD`, `PAÍS`
- `OCUPACIÓN`, `OBSERVACIONES`

Total: 41 columnas, ~1,370 registros

### 2. CLIENTES VIGENTES CELER.xlsx
Archivo con información de clientes y pólizas del nuevo sistema.

**Columnas principales:**
- `Tomador`, `Identificacion`, `Tipo_Doc`
- `Celular_Pers`, `Mail_Pers`
- `Aseguradora`, `Ramo`, `Póliza`
- `F_Inicio`, `F_Fin`

Total: 19 columnas, ~1,370 registros

## 🔧 Scripts Disponibles

### 1️⃣ Análisis de Identificaciones

**Archivo:** `src/validators/analisis_ids.py`

**Descripción:** Analiza la calidad de los números de documento en ambos archivos.

**Ejecutar:**
```powershell
python src\validators\analisis_ids.py
```

**Salida:** `data/output/01_analisis/analisis_ids_YYYYMMDD_HHMMSS.xlsx`

**Resultados obtenidos:**
- ✅ Detecta identificaciones vacías o nulas: **0 encontradas**
- ✅ Identifica duplicados: **1 NIT duplicado** (`900437270-3`)
- ✅ Valida formatos: **217 NITs sin formato correcto**
- ✅ Compara IDs entre bases: **99.3% de coincidencia** (1,360 de 1,369)
- ✅ Distribución por tipo de documento (Cédulas: 1,132, NITs: 227, etc.)

**Hojas del reporte:**
- Resumen general
- Duplicados SoftSeguros
- Duplicados Celer
- Problemas de formato
- Registros sin ID

---

### 2️⃣ Corrección de NITs

**Archivo:** `src/transformers/corregir_nits.py`

**Descripción:** Corrige automáticamente el formato de NITs agregando guión y dígito verificador según algoritmo oficial DIAN.

**Ejecutar:**
```powershell
python src\transformers\corregir_nits.py
```

**Salida:** `data/output/02_correcciones/`
- `CLIENTES_SOFTSEGUROS_CORREGIDO_YYYYMMDD_HHMMSS.xlsx` - Archivo completo
- `REPORTE_CORRECCIONES_NITS_YYYYMMDD_HHMMSS.xlsx` - Detalle de cambios

**Resultados obtenidos:**
- ✅ **217 NITs corregidos** con formato `XXXXXXXXX-X`
- ✅ **10 NITs sin corrección** (ya tenían formato correcto)
- ✅ Dígito verificador calculado según algoritmo DIAN
- ✅ Preserva estructura original de 41 columnas
- ✅ Formato profesional aplicado

**Ejemplos de correcciones:**
```
900310074   → 90031007-4
900438817   → 90043881-7
900771432   → 90077143-2
900004949   → 90000494-9
811030395   → 81103039-5
```

**Formato NIT:**
```python
# NIT original: 900310074
# El último dígito (4) es el dígito verificador
# Formato correcto: 90031007-4
# 
# Regla: Separar todos los dígitos menos el último - último dígito
# Estructura: [BASE]-[DV]
# Donde BASE = primeros N-1 dígitos, DV = último dígito
```

---

### 3️⃣ Validación Nombre-Documento

**Archivo:** `src/validators/validar_nombres_documentos.py`

**Descripción:** Valida que los nombres asociados a cada documento coincidan entre SOFTSEGUROS y CELER, detectando errores de escritura mediante algoritmos de similitud.

**Ejecutar:**
```powershell
python src\validators\validar_nombres_documentos.py
```

**Salida:** `data/output/03_validaciones/VALIDACION_NOMBRES_DOCUMENTOS_YYYYMMDD_HHMMSS.xlsx`

**Resultados obtenidos:**
- ✅ **1,170 IDs comparados** entre ambas bases
- ✅ **99.7% coincidencia exacta** (1,167 registros)
- ⚠️ **2 similitudes altas** (>85% - variaciones menores)
- ❌ **1 inconsistencia detectada** (0.09%)

**Algoritmo:**
1. Normalización de texto (MAYÚSCULAS, sin tildes, sin espacios extras)
2. Cálculo de similitud con `SequenceMatcher` (ratio 0.0 a 1.0)
3. Umbral configurable (default: 85%)
4. Clasificación automática por severidad

**Problema detectado:**
- **CC: 70137592** - FERNEY ANTONIO
  - SOFTSEGUROS: `FERNEY ANTONIO   FERNEY ANTONIO` (duplicado por error)
  - CELER: `FERNEY ANTONIO RAMIREZ RODRIGUEZ` (correcto) ✓
  - Similitud: 59% → **CORREGIDO en paso 4**

**Código de colores en reporte:**
- 🔴 Rojo: < 30% similitud (CRÍTICO - nombres completamente diferentes)
- 🟠 Naranja: 30-50% (SIGNIFICATIVO - diferencias importantes)
- 🟡 Amarillo: 50-85% (MENOR - errores de escritura)

**Validación interna:**
- ⚠️ 1 ID en SOFTSEGUROS con múltiples nombres (NIT duplicado)
- ✅ 0 IDs en CELER con múltiples nombres (correcto)

---

### 4️⃣ Actualización desde CELER ⭐ NUEVO

**Archivo:** `src/transformers/actualizar_desde_celer.py`

**Descripción:** Sincroniza y enriquece SOFTSEGUROS usando CELER como fuente de verdad. Actualiza nombres, fechas de nacimiento, teléfonos, emails y direcciones.

**Ejecutar:**
```powershell
python src\transformers\actualizar_desde_celer.py
```

**Salida:** `data/output/04_actualizaciones/`
- `CLIENTES_SOFTSEGUROS_ACTUALIZADO_YYYYMMDD_HHMMSS.xlsx` - Base actualizada
- `REPORTE_ACTUALIZACIONES_YYYYMMDD_HHMMSS.xlsx` - Trazabilidad completa

**Resultados obtenidos:**
- ✅ **1,370 registros procesados**
- ✅ **1,170 registros encontrados** en CELER (85.4%)
- ✅ **1,082 registros actualizados** (92.5% de los encontrados)
- ✅ **2,957 cambios totales** aplicados
- ✅ **200 registros únicos** de SOFTSEGUROS preservados sin cambios

**Cambios por campo:**
| Campo | Actualizaciones |
|-------|----------------|
| 📅 Fechas de nacimiento | 866 |
| 📞 Teléfonos móviles | 1,019 |
| 📧 Emails | 1,005 |
| 🏠 Direcciones | 61 |
| 👤 Nombres/Apellidos | 3 |
| **TOTAL** | **2,957** |

**Lógica de actualización:**
```python
SI campo_celer tiene valor:
    SI campo_soft está vacío:
        → Actualizar (poblar desde CELER)
    SI campo_soft tiene valor diferente:
        → Actualizar (CELER prevalece como fuente de verdad)
    REGISTRAR cambio con valor anterior y nuevo
SINO (campo_celer vacío):
    → Mantener valor de SOFTSEGUROS sin cambios
```

**Casos corregidos:**
- ✅ Ferney Antonio: Apellidos actualizados de `FERNEY ANTONIO` → `RAMIREZ RODRIGUEZ`
- ✅ 866 fechas normalizadas: `1984-07-21 00:00:00` → `21/07/1984`
- ✅ 1,019 teléfonos sincronizados
- ✅ 1,005 emails actualizados
- ✅ 61 direcciones corregidas/completadas

---

## 📈 Flujo de Trabajo Completo

```
┌─────────────────────────────────────────────────────────────────┐
│                    FLUJO DE MIGRACIÓN                            │
└─────────────────────────────────────────────────────────────────┘

1️⃣ ANÁLISIS INICIAL
   └─> python src\validators\analisis_ids.py
       ├─> Salida: data/output/01_analisis/
       ├─> Detecta: 1 NIT duplicado, 217 NITs sin formato
       └─> Resultado: 99.3% coincidencia entre bases ✅

2️⃣ CORRECCIÓN DE NITs
   └─> python src\transformers\corregir_nits.py
       ├─> Salida: data/output/02_correcciones/
       ├─> Corrige: 217 NITs con algoritmo DIAN
       └─> Genera: CLIENTES_SOFTSEGUROS_CORREGIDO_*.xlsx ✅

3️⃣ VALIDACIÓN DE NOMBRES
   └─> python src\validators\validar_nombres_documentos.py
       ├─> Salida: data/output/03_validaciones/
       ├─> Compara: 1,170 IDs entre ambas bases
       └─> Resultado: 99.7% coincidencia exacta ✅

4️⃣ ACTUALIZACIÓN DESDE CELER ⭐
   └─> python src\transformers\actualizar_desde_celer.py
       ├─> Salida: data/output/04_actualizaciones/
       ├─> Actualiza: 2,957 campos desde CELER
       ├─> Sincroniza: Nombres, fechas, teléfonos, emails, direcciones
       └─> Genera: CLIENTES_SOFTSEGUROS_ACTUALIZADO_*.xlsx ✅

5️⃣ ARCHIVO FINAL
   └─> data/output/05_finales/CLIENTES_SOFTSEGUROS_FINAL.xlsx
       ├─> 1,370 registros procesados
       ├─> NITs corregidos con formato DIAN
       ├─> Datos sincronizados con CELER
       └─> ✅ LISTO PARA REVISIÓN Y CARGA

┌─────────────────────────────────────────────────────────────────┐
│  📊 RESULTADOS FINALES                                           │
├─────────────────────────────────────────────────────────────────┤
│  • 1,370 registros totales                                       │
│  • 217 NITs corregidos (100% con formato DIAN)                  │
│  • 2,957 actualizaciones aplicadas                              │
│  • 99.7% de calidad de datos                                    │
│  • 1,082 registros enriquecidos desde CELER                     │
└─────────────────────────────────────────────────────────────────┘
```

## 🐛 Problemas Detectados y Estado

### ✅ Problema 1: Nombre Duplicado - RESUELTO
**ID:** `70137592` (Cédula)
**Estado:** ✅ **CORREGIDO AUTOMÁTICAMENTE**

**Antes:**
- SOFTSEGUROS: `FERNEY ANTONIO   FERNEY ANTONIO` (error de captura)

**Después:**
- SOFTSEGUROS: `FERNEY ANTONIO RAMIREZ RODRIGUEZ` (sincronizado con CELER)

**Solución aplicada:** Script `actualizar_desde_celer.py` - Paso 4

---

### ⚠️ Problema 2: NIT Duplicado - REQUIERE ACCIÓN MANUAL
**ID:** `900437270-3` (NIT)
**Estado:** ⚠️ **PENDIENTE DE REVISIÓN**

**Empresas con el mismo NIT:**
1. A.V COLOMBIA S.A.S
2. AB & C LOGISTICA S.A.S.

**Impacto:** Una de las dos empresas tiene el NIT incorrecto

**Acción requerida:** 
1. Verificar documentos legales (RUT/Cámara de Comercio)
2. Identificar cuál empresa tiene el NIT correcto
3. Actualizar manualmente el NIT incorrecto
4. Re-ejecutar validaciones si se modifica

**Ubicación en reportes:**
- `01_analisis/analisis_ids_*.xlsx` → Hoja "Duplicados_SoftSeguros"
- `05_finales/README.md` → Sección "Pendientes"

---

### ℹ️ Registros Únicos - REVISIÓN RECOMENDADA
**Cantidad:** 200 registros
**Estado:** ℹ️ **INFORMATIVO**

**Descripción:** 200 clientes aparecen en SOFTSEGUROS pero no en CELER

**Posibles razones:**
- Clientes nuevos agregados recientemente
- Clientes sin pólizas vigentes
- Diferencias en criterios de inclusión

**Acción recomendada:**
1. Validar con área comercial si deben incluirse
2. Verificar si tienen pólizas activas
3. Confirmar criterios de migración

**Ubicación:** Los datos de estos clientes se mantuvieron intactos en el archivo final

---

## 🔍 Ejemplos de Uso

### Verificar solo un tipo de documento específico

Modificar el script `analisis_ids.py`:

```python
# Filtrar solo NITs
nits = df[df['TIPO DE DOCUMENTO'] == 'NIT']
```

### Cambiar umbral de similitud

En `validar_nombres_documentos.py`:

```python
# Más estricto (solo 95%+)
validador.validar_coincidencias(umbral_similitud=0.95)

# Más permisivo (80%+)
validador.validar_coincidencias(umbral_similitud=0.80)
```

### Procesar solo una muestra

```python
# Primeros 100 registros
df = df.head(100)
```

## � Estructura de Output Organizada

El directorio `data/output/` está organizado por etapas del proceso:

```
data/output/
├── INDEX.md                    # 📄 Índice general con trazabilidad completa
│
├── 01_analisis/               # 📊 Fase 1: Análisis de calidad
│   ├── README.md
│   └── analisis_ids_*.xlsx
│
├── 02_correcciones/           # 🔧 Fase 2: Corrección de NITs
│   ├── README.md
│   ├── CLIENTES_SOFTSEGUROS_CORREGIDO_*.xlsx
│   └── REPORTE_CORRECCIONES_NITS_*.xlsx
│
├── 03_validaciones/           # ✅ Fase 3: Validación de coincidencias
│   ├── README.md
│   └── VALIDACION_NOMBRES_DOCUMENTOS_*.xlsx
│
├── 04_actualizaciones/        # 🔄 Fase 4: Sincronización con CELER
│   ├── README.md
│   ├── CLIENTES_SOFTSEGUROS_ACTUALIZADO_*.xlsx
│   └── REPORTE_ACTUALIZACIONES_*.xlsx
│
└── 05_finales/                # 📦 Fase 5: Archivo listo para migración
    ├── README.md
    └── CLIENTES_SOFTSEGUROS_FINAL.xlsx ⭐ ARCHIVO PRINCIPAL
```

**Cada carpeta incluye:**
- ✅ README.md explicando el contenido
- ✅ Archivos de datos con timestamp
- ✅ Reportes con trazabilidad completa

**Navegación:**
1. Ver `INDEX.md` para resumen general
2. Revisar README.md de cada carpeta para detalles
3. Consultar reportes para análisis específicos

---

## �📚 Glosario de Términos

| Término | Significado |
|---------|-------------|
| **NIT** | Número de Identificación Tributaria (empresas colombianas) |
| **C.C** | Cédula de Ciudadanía (personas naturales colombianas) |
| **C.E** | Cédula de Extranjería |
| **PSP** | Pasaporte |
| **NUIP/DIPL** | Número Único de Identificación Personal |
| **Dígito Verificador** | Dígito de control del NIT calculado con algoritmo DIAN |
| **Póliza** | Contrato de seguro |
| **Tomador** | Cliente/titular de la póliza |
| **Prima** | Monto pagado por el seguro |
| **Vigencia** | Periodo de validez de la póliza |
| **Ramo** | Tipo de seguro (automóviles, hogar, vida, etc.) |
| **CELER** | Sistema nuevo (fuente de verdad) |
| **SoftSeguros** | Sistema legacy (a migrar) |

## 🛠️ Tecnologías Utilizadas

- **Python 3.x**: Lenguaje principal
- **pandas**: Manipulación de datos
- **openpyxl**: Lectura/escritura Excel con formato
- **xlrd**: Lectura de archivos .xls legacy
- **difflib.SequenceMatcher**: Cálculo de similitud de texto

## 📝 Logs

Los logs se generan automáticamente con nivel INFO mostrando:
- Archivos cargados y cantidad de registros
- Progreso de validaciones
- Correcciones aplicadas
- Errores y advertencias

Ejemplo:
```
2025-11-04 13:07:14 - INFO - ✅ 1370 registros cargados
2025-11-04 13:07:14 - INFO - ✅ NITs corregidos: 217
2025-11-04 13:07:14 - WARNING - ⚠️ DUPLICADOS ENCONTRADOS: ID 900437270-3
```

## 🤝 Contribución

Para agregar nuevos scripts de validación o transformación:

1. Crear archivo en `src/validators/` o `src/transformers/`
2. Seguir patrón de clase con métodos: `cargar_datos()`, `procesar()`, `generar_reporte()`
3. Usar logging para trazabilidad
4. Generar reportes en `data/output/` con timestamp
5. Documentar en este README

## 📞 Soporte

Para problemas o dudas sobre:
- Algoritmo de dígito verificador NIT
- Interpretación de reportes
- Correcciones manuales necesarias
- Nuevas validaciones requeridas

Contactar al equipo de desarrollo.

## ✅ Estado del Proyecto

| Fase | Estado | Registros | Resultado |
|------|--------|-----------|-----------|
| 1. Análisis | ✅ Completado | 1,370 | 99.3% coincidencia |
| 2. Corrección NITs | ✅ Completado | 217 corregidos | 100% con formato DIAN |
| 3. Validación | ✅ Completado | 1,170 comparados | 99.7% exactitud |
| 4. Actualización | ✅ Completado | 2,957 cambios | 1,082 registros enriquecidos |
| 5. Archivo Final | ✅ Listo | 1,370 | **LISTO PARA REVISIÓN** |

## 🎯 Siguiente Paso

1. **Revisar** archivo final: `data/output/05_finales/CLIENTES_SOFTSEGUROS_FINAL.xlsx`
2. **Validar** con área de negocio los pendientes en `05_finales/README.md`
3. **Resolver** manualmente el NIT duplicado `900437270-3`
4. **Verificar** los 200 registros únicos de SOFTSEGUROS
5. **Aprobar** para carga en sistema de producción

## 📞 Información del Proyecto

- **Organización:** SEGUROS UNIÓN
- **Proyecto:** Migración SoftSeguros → CELER
- **Repositorio:** [migracion-softseguros](https://github.com/DanielAraqueStudios/migracion-softseguros)
- **Documentación completa:** Ver `data/output/INDEX.md`

## 📄 Licencia

Uso interno - SEGUROS UNIÓN

---

**Fecha de procesamiento:** 4 de noviembre, 2025  
**Última actualización:** Noviembre 2025  
**Versión:** 1.0  
**Estado:** ✅ **PRODUCCIÓN - PROCESO COMPLETADO**
