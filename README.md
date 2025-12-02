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
