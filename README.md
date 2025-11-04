# Migración SoftSeguros

Sistema completo de migración y validación de datos para clientes de seguros, especializado en procesamiento de archivos Excel, limpieza de datos, sincronización entre sistemas y generación de reportes automatizados.

## 📋 Descripción del Proyecto

Este proyecto automatiza la migración de datos de clientes entre el sistema legacy **SoftSeguros** y el nuevo sistema **Celer**. Implementa un flujo completo de ETL (Extract, Transform, Load) con validaciones de calidad, corrección automática de formatos y sincronización de datos usando **CELER como fuente de verdad**.

## 🎯 Características Principales

- ✅ **Análisis de calidad de datos**: Identificación de duplicados, IDs inválidos y problemas de formato
- ✅ **Corrección automática de NITs**: Cálculo y aplicación de dígito verificador según algoritmo DIAN
- ✅ **Validación nombre-documento**: Algoritmo de similitud de texto para detectar inconsistencias
- ✅ **Sincronización de datos**: Actualización automática desde CELER (fuente confiable)
- ✅ **Trazabilidad completa**: Reportes detallados de cada cambio con valor anterior/nuevo
- ✅ **Organización profesional**: Estructura de carpetas por etapas del proceso
- ✅ **Documentación exhaustiva**: README en cada carpeta explicando contenido y resultados

## 📁 Estructura del Proyecto

```
migracion-softseguros/
├── src/
│   ├── validators/              # Scripts de validación de datos
│   │   ├── analisis_ids.py                 # Análisis de identificaciones
│   │   └── validar_nombres_documentos.py   # Validación nombre-documento
│   ├── transformers/            # Scripts de transformación de datos
│   │   ├── corregir_nits.py                # Corrección de NITs
│   │   └── actualizar_desde_celer.py       # Sincronización con CELER ⭐
│   ├── extractors/              # Lectores de datos fuente
│   ├── loaders/                 # Exportadores de datos
│   └── utils/                   # Utilidades compartidas
├── data/
│   ├── input/                   # Archivos Excel de entrada (gitignored)
│   └── output/                  # Estructura organizada por etapas ⭐
│       ├── INDEX.md                 # Índice general de archivos
│       ├── 01_analisis/             # Reportes de análisis inicial
│       ├── 02_correcciones/         # NITs corregidos
│       ├── 03_validaciones/         # Validaciones de calidad
│       ├── 04_actualizaciones/      # Actualizaciones desde CELER
│       └── 05_finales/              # Archivo final listo ✅
├── .github/
│   └── copilot-instructions.md  # Guía para agentes de IA
├── config/                      # Configuraciones
├── logs/                        # Logs de ejecución (gitignored)
├── docs/                        # Documentación adicional
└── tests/                       # Tests unitarios
```

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
900310074   → 900310074-1
900438817   → 900438817-6
900771432   → 900771432-0
900004949   → 900004949-7
811030395   → 811030395-4
```

**Algoritmo DIAN:**
```python
# NIT: 900310074
# Multiplicadores: [71, 67, 59, 53, 47, 43, 41, 37, 29]
# Suma: 9×71 + 0×67 + 0×59 + 3×53 + 1×47 + 0×43 + 0×41 + 7×37 + 4×29
# Residuo: suma % 11
# DV: si residuo ≤ 1 → residuo, sino → 11 - residuo
```

---

### 3. Validación Nombre-Documento

**Archivo:** `src/validators/validar_nombres_documentos.py`

**Descripción:** Valida que los nombres asociados a cada documento coincidan entre ambas bases, detectando errores de escritura.

**Ejecutar:**
```powershell
python src\validators\validar_nombres_documentos.py
```

**Características:**
- ✅ Normalización de texto (mayúsculas, sin tildes)
- ✅ Algoritmo de similitud de texto (SequenceMatcher)
- ✅ Umbral configurable (default: 85%)
- ✅ Detección de inconsistencias internas
- ✅ Clasificación de problemas por severidad

**Archivos generados:**
- `VALIDACION_NOMBRES_DOCUMENTOS_YYYYMMDD_HHMMSS.xlsx`
  - Hoja "Resumen": Estadísticas generales
  - Hoja "Inconsistencias": Casos problemáticos con colores

**Resultados típicos:**
- ✅ 99.7% coincidencia exacta (1,167 de 1,170)
- ⚠️ 2 similitudes altas (>85%)
- ❌ 1 inconsistencia detectada

**Código de colores en reporte:**
- 🔴 Rojo: Similitud < 30% (crítico)
- 🟠 Naranja: Similitud 30-50% (significativo)
- 🟡 Amarillo: Similitud 50-85% (menor)

---

## 📈 Flujo de Trabajo Recomendado

```
1. Análisis Inicial
   └─> python src\validators\analisis_ids.py
       └─> Revisa: data/output/analisis_ids_*.xlsx

2. Corrección de NITs
   └─> python src\transformers\corregir_nits.py
       └─> Obtiene: CLIENTES_SOFTSEGUROS_CORREGIDO_*.xlsx

3. Validación de Nombres
   └─> python src\validators\validar_nombres_documentos.py
       └─> Revisa: VALIDACION_NOMBRES_DOCUMENTOS_*.xlsx

4. Correcciones Manuales
   └─> Corrige inconsistencias críticas en Excel

5. Migración Final
   └─> Ejecuta scripts de carga a sistema destino
```

## 🐛 Problemas Conocidos y Soluciones

### Problema 1: NIT Duplicado
**ID:** `900437270-3`
**Empresas:**
- A.V COLOMBIA S.A.S
- AB & C LOGISTICA S.A.S.

**Solución:** Verificar documentos legales y corregir manualmente el NIT incorrecto.

---

### Problema 2: Nombre Duplicado
**ID:** `70137592`
**SOFTSEGUROS:** `FERNEY ANTONIO   FERNEY ANTONIO` (error)
**CELER:** `FERNEY ANTONIO RAMIREZ RODRIGUEZ` (correcto)

**Solución:** Actualizar SOFTSEGUROS con nombre completo de CELER.

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

## 📚 Glosario de Términos

| Término | Significado |
|---------|-------------|
| **NIT** | Número de Identificación Tributaria (empresas) |
| **C.C** | Cédula de Ciudadanía (personas naturales) |
| **C.E** | Cédula de Extranjería |
| **PSP** | Pasaporte |
| **Póliza** | Contrato de seguro |
| **Tomador** | Cliente/titular de la póliza |
| **Prima** | Monto pagado por el seguro |
| **Vigencia** | Periodo de validez de la póliza |
| **Ramo** | Tipo de seguro (automóviles, hogar, vida, etc.) |

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

## 📄 Licencia

Uso interno - SEGUROS UNIÓN

---

**Última actualización:** Noviembre 2025  
**Versión:** 1.0  
**Estado:** Producción
