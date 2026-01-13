# Conciliador de Clientes

Scripts para conciliación y matching de datos de clientes entre diferentes fuentes (CELER vs archivos activos).

## 📋 Descripción

Sistema de validación y conciliación de datos de clientes que:
- Compara datos entre TOMADOR y ASEGURADO para identificar discrepancias
- Genera reportes de diferencias en formato JSON con logs detallados
- Realiza matching entre múltiples fuentes de datos (JSON + CELER)
- Calcula y valida dígitos de verificación NIT según normativa DIAN
- Exporta plantillas Excel con datos limpios y estandarizados para migración

## 🎯 Objetivo

Validar y conciliar datos de clientes identificando inconsistencias entre TOMADOR y ASEGURADO, realizar matching con base de datos CELER, y generar plantillas limpias con datos validados listos para proceso de migración a SoftSeguros.

## � FLUJO COMPLETO DEL PROCESO

### **Flujo de 3 Etapas con Entrada/Salida**

```
┌─────────────────────────────────────────────────────────────────────┐
│ ETAPA 1: Comparación TOMADOR vs ASEGURADO                          │
│ Script: comparar_tomador_asegurado.py                              │
└─────────────────────────────────────────────────────────────────────┘
📂 ENTRADA:
   • clientes_activos/*.xlsx (detectado automáticamente)
   • Lee desde fila 5 (skiprows=3)

🔧 PROCESO:
   1. Filtrado inicial: Solo registros con Tipo_Doc = NIT
   2. Normalización: Quita espacios, convierte a mayúsculas
   3. Comparación: Verifica si Tomador ≠ Asegurado (ambos no vacíos)
   4. Exclusión: Ignora registros donde algún campo está vacío

📤 SALIDA:
   • clientes_activos/diferencias_tomador_asegurado.json
   • logs_comparacion.log

         ↓ JSON con discrepancias ↓

┌─────────────────────────────────────────────────────────────────────┐
│ ETAPA 2: Matching y Generación de Plantilla                        │
│ Script: exportar_plantilla_coincidentes.py                         │
└─────────────────────────────────────────────────────────────────────┘
📂 ENTRADA:
   • data_celer/InformedePersonas CELER.xlsx (35 columnas)
   • clientes_activos/diferencias_tomador_asegurado.json (Etapa 1)

🔧 PROCESO:
   1. Búsqueda doble criterio:
      - Por número: Identificacion ∈ Iden_Beneficiario (JSON)
      - Por nombre: Nombre ∈ Nombre_Beneficiario (JSON)
      - Une resultados y elimina duplicados
   
   2. Separación nombres/apellidos:
      - < 3 palabras → últimas = apellido, resto = nombre
      - ≥ 3 palabras → últimas 2 = apellido, resto = nombre
   
   3. Mapeo de campos:
      • Tipo Doc: CC/IND→Cédula, NIT→NIT, CE/PSP→Cédula Extranjería
      • Género: M→MASCULINO, F→FEMENINO
      • Teléfonos: Prioriza Celular_Personal > Tel_Personal > Laboral
      • Email: Prioriza Mail_Personal > Mail_Laboral
   
   4. Cálculo DV NIT (solo para NIT):
      - Algoritmo DIAN con factores [71,67,59,53,47,43,41,37,29,23,19,17,13,7,3]
      - Suma = Σ(dígito[i] × factor[i]), Resto = Suma % 11
      - DV = 0 si resto ≤ 1, sino (1 - resto)

📤 SALIDA:
   • plantilla/PLANTILLA_COINCIDEN.xlsx (11 columnas limpias)
     Columnas: NOMBRES | APELLIDOS | NÚMERO DE DOCUMENTO | 
               TIPO DE DOCUMENTO | GÉNERO | TELÉFONO MÓVIL | 
               TIPO TELÉFONO MÓVIL | EMAIL | TIPO EMAIL | 
               DIRECCIÓN PRINCIPAL | DV_NIT

         ↓ Plantilla limpia ↓

┌─────────────────────────────────────────────────────────────────────┐
│ ETAPA 3: Estadísticas y Validación                                 │
│ Script: estadisticas_match_json_excel.py                           │
└─────────────────────────────────────────────────────────────────────┘
📂 ENTRADA:
   • data_celer/InformedePersonas CELER.xlsx
   • clientes_activos/diferencias_tomador_asegurado.json

🔧 PROCESO:
   • Total Coincidentes = Total Excel - Total JSON
   • Porcentaje = (Coincidentes / Total Excel) × 100

📤 SALIDA (consola):
   Total registros en Excel: 5000
   Total registros con mismatch (JSON): 150
   Total registros coincidentes: 4850
   Porcentaje de coincidencia: 97.00%
```

## 🚀 Ejecución Secuencial

```powershell
# Paso 1: Comparar TOMADOR vs ASEGURADO
python comparar_tomador_asegurado.py

# Paso 2: Generar plantilla con coincidentes
python exportar_plantilla_coincidentes.py

# Paso 3: Ver estadísticas de conciliación
python estadisticas_match_json_excel.py
```

## 🔑 Conceptos Clave

| Término | Significado |
|---------|-------------|
| **TOMADOR** | Persona/empresa que contrata la póliza |
| **ASEGURADO** | Persona/objeto cubierto por la póliza |
| **Match** | Tomador y Asegurado son iguales (común en seguros personales) |
| **Mismatch** | Tomador ≠ Asegurado (común en seguros empresariales) |
| **Conciliación** | Buscar registro en CELER para completar datos faltantes |
| **DV NIT** | Dígito de verificación DIAN (obligatorio para NITs Colombia) |

## 📂 Estructura de Carpetas

```
conciliador_clientes/
├── clientes_activos/              # ← ENTRADA: Excel fuente
│   ├── *.xlsx                     # Detectado automáticamente
│   └── diferencias_tomador_asegurado.json  # ← Generado Etapa 1
├── data_celer/                    # ← ENTRADA: Informe CELER
│   └── InformedePersonas CELER.xlsx
├── plantilla/                     # ← SALIDA: Template limpio
│   └── PLANTILLA_COINCIDEN.xlsx
├── ERRORES/                       # Registros problemáticos
├── comparar_tomador_asegurado.py       # Etapa 1: Comparación
├── exportar_plantilla_coincidentes.py  # Etapa 2: Matching
├── estadisticas_match_json_excel.py    # Etapa 3: Stats
├── buscar_nit_sin_dv_y_cedula.py      # Auxiliar: Detectar NITs sin DV
└── logs_comparacion.log           # Logs detallados del proceso
```

## �📁 Archivos

### Scripts Principales

#### 🔄 Etapa 1: `comparar_tomador_asegurado.py`
**Función:** Identifica registros NIT donde TOMADOR ≠ ASEGURADO
- Lee Excel desde `clientes_activos/` (auto-detecta primer .xlsx/.xls)
- Filtra solo registros con Tipo_Doc = NIT
- Normaliza texto (sin espacios, mayúsculas)
- Exporta discrepancias a JSON
- Genera logs detallados con timestamps

**Criterios de exportación:**
- Ambos campos (Tomador y Asegurado) deben tener valor
- Ignora diferencias de espacios y mayúsculas/minúsculas
- Solo exporta cuando realmente son diferentes

#### ✅ Etapa 2: `exportar_plantilla_coincidentes.py`
**Función:** Genera plantilla Excel con datos validados y enriquecidos
- Matching doble: por identificación Y por nombre completo
- Calcula DV NIT automáticamente con algoritmo DIAN
- Prioriza datos de contacto (Personal > Laboral)
- Mapea tipos de documento a nomenclatura estándar
- Separa nombres/apellidos inteligentemente

**Validaciones incluidas:**
- Tipo documento: normaliza CC/C.C/IND/CEDULA → "Cédula"
- Género: M → "MASCULINO", F → "FEMENINO"
- Teléfonos: concatena múltiples con tipo (PERSONAL/OFICINA)
- Emails: selecciona primero disponible con tipo

#### 📊 Etapa 3: `estadisticas_match_json_excel.py`
**Función:** Calcula métricas de calidad del proceso
- Total registros procesados
- Cantidad de mismatches detectados
- Porcentaje de coincidencia
- Sirve para validar efectividad del proceso

### Scripts Auxiliares

#### 🔍 `buscar_nit_sin_dv_y_cedula.py`
Detecta registros con NIT sin dígito de verificación
- Busca patrones: 7-10 dígitos consecutivos
- Identifica si hay cédula válida en mismo registro
- Útil para corrección manual de NITs problemáticos

#### 📋 `comparar_identificaciones_informe_json.py`
Cruza identificaciones entre informe CELER y JSON de diferencias

#### 🏗️ `leer_estructura_plantilla.py`
Analiza estructura de plantillas Excel para debugging

#### 👤 `llenar_plantilla_nombres_apellidos.py`
Procesa separación de nombres completos en campos individuales

### Archivos de Salida

#### 📄 `PLANTILLA_COINCIDEN.xlsx` (Etapa 2)
Template final con datos limpios y validados

**Estructura (11 columnas):**
1. NOMBRES - Separados de nombre completo
2. APELLIDOS - Últimas 1-2 palabras del nombre completo
3. NÚMERO DE DOCUMENTO - ID sin formato
4. TIPO DE DOCUMENTO - Normalizado (Cédula/NIT/Cédula de Extranjería)
5. GÉNERO - MASCULINO/FEMENINO
6. TELÉFONO MÓVIL - Prioridad: Celular_Personal, Tel_Personal, Celular_Laboral, Tel_Laboral
7. TIPO TELÉFONO MÓVIL - PERSONAL o OFICINA
8. EMAIL - Prioridad: Mail_Personal, Mail_Laboral
9. TIPO EMAIL - PERSONAL o OFICINA
10. DIRECCIÓN PRINCIPAL - De campo Direccion_Personal
11. DV_NIT - Dígito verificación (solo para NIT)

**Ejemplo de registro:**
```
NOMBRES: JUAN CARLOS
APELLIDOS: PÉREZ GÓMEZ
NÚMERO DE DOCUMENTO: 900123456
TIPO DE DOCUMENTO: NIT
GÉNERO: MASCULINO
TELÉFONO MÓVIL: 3001234567, 6012345678
TIPO TELÉFONO MÓVIL: PERSONAL, OFICINA
EMAIL: juan.perez@empresa.com
TIPO EMAIL: OFICINA
DIRECCIÓN PRINCIPAL: CALLE 100 # 20-30
DV_NIT: 7
```

#### 🗂️ `diferencias_tomador_asegurado.json` (Etapa 1)
Reporte de discrepancias entre TOMADOR y ASEGURADO

**Contiene:**
- Todos los campos del registro original
- Solo registros NIT donde Tomador ≠ Asegurado
- Formato JSON para procesamiento posterior

**Ejemplo:**
```json
{
  "Tipo_Doc": "NIT",
  "Tomador": "EMPRESA ABC S.A.",
  "Asegurado": "EMPRESA ABC S.A.S.",
  "Iden_Beneficiario": "900123456",
  "Nombre_Beneficiario": "EMPRESA ABC SOCIEDAD ANONIMA"
}
```

#### 📊 `estadisticas_conciliacion.json` (Etapa 3)
Métricas del proceso de conciliación

**Contiene:**
```json
{
  "total_excel": 5000,
  "total_mismatches": 150,
  "total_coincidentes": 4850,
  "porcentaje_coincidencia": 97.00
}
```

## 🚀 Uso

### Ejecución Completa (Recomendada)

```powershell
# Navegar a la carpeta
cd "C:\Users\danie\Documents\EMPRESA\SEGUROS UNIÓN\AUTOMATIZACIONES\migraciones\migracion-softseguros\conciliador_clientes"

# Paso 1: Identificar discrepancias TOMADOR vs ASEGURADO
python comparar_tomador_asegurado.py
# ✅ Genera: clientes_activos/diferencias_tomador_asegurado.json

# Paso 2: Generar plantilla con datos validados
python exportar_plantilla_coincidentes.py
# ✅ Genera: plantilla/PLANTILLA_COINCIDEN.xlsx

# Paso 3: Verificar estadísticas
python estadisticas_match_json_excel.py
# ✅ Muestra: Porcentaje de coincidencia en consola
```

### Ejecución Individual

```powershell
# Solo comparar TOMADOR vs ASEGURADO
python comparar_tomador_asegurado.py

# Solo generar plantilla (requiere JSON previo)
python exportar_plantilla_coincidentes.py

# Solo ver estadísticas
python estadisticas_match_json_excel.py

# Buscar NITs problemáticos
python buscar_nit_sin_dv_y_cedula.py
```

## 📊 Funcionalidades Detalladas

### 🔍 Comparación TOMADOR vs ASEGURADO

**Algoritmo de detección:**

1. **Normalización de texto:**
   ```python
   def normalizar(texto):
       return str(texto).replace(' ', '').upper()
   ```
   - Elimina espacios
   - Convierte a mayúsculas
   - Ignora valores vacíos/NaN

2. **Criterio de diferencia:**
   - Ambos campos deben tener valor
   - Después de normalizar, deben ser diferentes
   - Solo aplica a registros con Tipo_Doc = NIT

3. **Casos excluidos:**
   - Uno o ambos campos vacíos
   - Valores idénticos después de normalizar
   - Tipos de documento diferentes a NIT

**Ejemplo de detección:**
```
✅ DETECTADO (exporta a JSON):
Tomador: "EMPRESA ABC S.A."
Asegurado: "EMPRESA ABC S.A.S."
→ Normalizado: "EMPRESAABCS.A." ≠ "EMPRESAABCS.A.S."

❌ NO DETECTADO (no exporta):
Tomador: "EMPRESA ABC S.A."
Asegurado: "EMPRESA ABC  S. A."
→ Normalizado: "EMPRESAABCS.A." = "EMPRESAABCS.A."
```

### ✅ Validación de NIT

**Algoritmo DIAN (Resolución 12487 de 2018):**
```python
def calcular_dv(nit):
    factores = [71, 67, 59, 53, 47, 43, 41, 37, 29, 23, 19, 17, 13, 7, 3]
    nit_padded = nit.zfill(15)[-15:]  # Rellena con ceros a 15 dígitos
    
    suma = 0
    for i in range(15):
        suma += int(nit_padded[i]) * factores[i]
    
    resto = suma % 11
    
    if resto <= 1:
        return 0
    else:
        return 11 - resto
```

**Ejemplo de cálculo:**
```
NIT: 900123456
Suma ponderada: 900123456 × factores
Resto: suma % 11 = 7
DV: 11 - 7 = 4
→ NIT completo: 900123456-4
```

### 📋 Generación de Templates

**Lógica de campos calculados:**

#### 1. Separación Nombres/Apellidos
```python
nombre_completo = "JUAN CARLOS PÉREZ GÓMEZ"

Si len(palabras) < 3:
    nombres = palabras[:-1]      # "JUAN CARLOS"
    apellidos = palabras[-1]     # "PÉREZ"

Si len(palabras) ≥ 3:
    nombres = palabras[:-2]      # "JUAN CARLOS"
    apellidos = palabras[-2:]    # "PÉREZ GÓMEZ"
```

#### 2. Prioridad de Contacto

**Teléfonos:**
```
1º Celular_Personal  → PERSONAL
2º Tel_Personal      → PERSONAL
3º Celular_Laboral   → OFICINA
4º Tel_Laboral       → OFICINA
```
Concatena todos disponibles: `"3001234567, 6012345678"`

**Emails:**
```
1º Mail_Personal  → PERSONAL
2º Mail_Laboral   → OFICINA
```
Solo selecciona el primero disponible

#### 3. Mapeo de Documentos
```python
'CC', 'C.C', 'CEDULA', 'CÉDULA', 'IND' → 'Cédula'
'NIT'                                   → 'NIT'
'PSP', 'CE', 'CEDULA DE EXTRANJERIA'   → 'Cédula de Extranjería'
```

#### 4. Mapeo de Género
```python
'M' → 'MASCULINO'
'F' → 'FEMENINO'
Otro → '' (vacío)
```

### 🔄 Matching de Datos

**Criterios de búsqueda (doble coincidencia):**

1. **Por número de documento:**
   ```python
   informe_df['Identificacion'].isin(json_data['Iden_Beneficiario'])
   ```

2. **Por nombre completo:**
   ```python
   informe_df['Nombre'].upper().isin(json_data['Nombre_Beneficiario'].upper())
   ```

3. **Unión de resultados:**
   - Combina ambas búsquedas
   - Elimina duplicados con `drop_duplicates()`
   - Maximiza posibilidades de encontrar coincidencias

**Ventaja del doble criterio:**
- Si el documento cambió pero el nombre no → Encuentra por nombre
- Si el nombre cambió pero el documento no → Encuentra por documento
- Mayor tasa de éxito en conciliación

## 📝 Logs

Los procesos generan logs detallados en:
- `logs_comparacion.log` - Logs de comparación TOMADOR vs ASEGURADO
- `logs_coincidencias_identificacion.txt` - Detalles de matching

**Información registrada:**
- Timestamp de cada operación
- Archivos procesados
- Cantidad de registros
- Errores encontrados
- Estadísticas de procesamiento
- Cambios realizados por fila

## 🔗 Dependencias

### Librerías Python
```python
pandas         # Lectura/escritura Excel, manipulación de datos
openpyxl       # Motor para archivos .xlsx
json           # Manejo de archivos JSON
logging        # Sistema de logs
pathlib        # Manejo de rutas multiplataforma
```

### Módulos Externos
```python
# Desde produccion_a_un_mes/src/dian_utils/
from dian_verificacion import calcular_digito_verificacion
```

### Archivos Requeridos

**Entrada obligatoria:**
- `clientes_activos/*.xlsx` - Archivo Excel con datos fuente (detectado automáticamente)
- `data_celer/InformedePersonas CELER.xlsx` - Informe de personas CELER (35 columnas)

**Columnas esperadas en archivo fuente:**
- `Tipo_Doc` - Tipo de documento (NIT/CC/CE/PSP)
- `Tomador` - Nombre del tomador de la póliza
- `Asegurado` - Nombre del asegurado
- `Iden_Beneficiario` - Número de identificación
- `Nombre_Beneficiario` - Nombre completo del beneficiario

**Columnas esperadas en InformedePersonas CELER:**
```
Nombre, Tipo_Doc, Identificacion, F_Nacimiento, Edad, Genero, Prefijo, 
Estado_civil, Estrato_social, Peso, Estatura, Fallecido, Profesion, 
Ocupacion, Tel_Personal, Celular_Personal, Tel_Laboral, Celular_Laboral, 
Direccion_Personal, Ciudad_Personal, Direccion_Laboral, Ciudad_Laboral, 
Mail_Personal, Mail_Laboral, F_Exp_Iden, Unidad, F_Creacion, 
F_Modificacion, Apartado_Aereo, Lugar_Exp_Iden, Lugar_Nacimiento, 
Calidades_Activas, Ejecutivo_Principal, Info_Confidencial, Observaciones
```

## ⚠️ Consideraciones Importantes

### Formato de Datos
- **skiprows=3**: El Excel se lee desde la fila 5 (salta header de 3 filas)
- **Normalización**: Todos los textos se normalizan (sin espacios, mayúsculas)
- **NITs**: Solo se procesan registros con Tipo_Doc = NIT en comparación
- **Valores vacíos**: Se ignoran en comparaciones (no se exportan diferencias)

### Calidad de Datos
- **Nombres duplicados**: El matching por nombre puede devolver múltiples coincidencias
- **Documentos sin DV**: NITs sin dígito de verificación requieren validación manual
- **Formatos inconsistentes**: Se normalizan automáticamente (espacios, mayúsculas)

### Performance
- **Archivos grandes**: Usa pandas para eficiencia en memoria
- **Logs**: Los logs pueden crecer considerablemente con archivos grandes
- **JSON**: Los archivos JSON son legibles pero pueden ser pesados

## 🔧 Troubleshooting

### Error: "No se encontró archivo Excel en clientes_activos"
**Solución:** Coloca un archivo .xlsx o .xls en la carpeta `clientes_activos/`

### Error: "No se encontró la columna: Tipo_Doc"
**Solución:** Verifica que el Excel tenga las columnas exactas esperadas (case-sensitive)

### Error al calcular DV NIT
**Solución:** Verifica que el NIT contenga solo dígitos (sin puntos, guiones o letras)

### Matching bajo (< 80%)
**Solución:** 
- Revisa normalización de nombres en JSON
- Verifica que los documentos estén correctos
- Considera búsqueda por nombre como alternativa

### JSON vacío después de comparación
**Posibles causas:**
- Todos los tomadores coinciden con asegurados (caso normal)
- Filtro de NIT muy restrictivo
- Columnas mal configuradas

## 📈 Métricas de Calidad

### Indicadores Esperados
- **Porcentaje de coincidencia**: > 95% (excelente), 80-95% (bueno), < 80% (revisar)
- **Mismatches detectados**: Varía según tipo de negocio (seguros personales vs empresariales)
- **NITs sin DV**: < 5% del total

### Validación de Resultados
```powershell
# Verificar cantidad de registros
python estadisticas_match_json_excel.py

# Revisar logs para errores
cat logs_comparacion.log

# Inspeccionar JSON de diferencias
python -m json.tool clientes_activos/diferencias_tomador_asegurado.json
```

---

## 🏗️ PROCESO COMPLETO: LLENADO DE PLANTILLA SOFTSEGUROS

Esta sección documenta el proceso completo de llenado de la plantilla de SoftSeguros con datos desde múltiples fuentes (CELER + Clientes Activos).

### 📊 Objetivo del Proceso

Llenar la plantilla oficial de SoftSeguros (`PLANTILLA DE SOTSEGUROS.xlsx`) con datos de clientes desde 2 fuentes:
1. **InformedePersonas CELER.xlsx** → Personas naturales (datos completos)
2. **CLIENTES ACTIVOS.xlsx** → Empresas/NITs (datos corporativos)

### 🗂️ Estructura Completa de Archivos

```
migracion-softseguros/
│
├── conciliador_clientes/
│   │
│   ├── clientes_activos/                    # FUENTE 2: Datos empresas
│   │   ├── CLIENTES ACTIVOS.xlsx           # ← Excel principal con empresas
│   │   └── diferencias_tomador_asegurado.json
│   │
│   ├── data_celer/                          # FUENTE 1: Datos personas
│   │   ├── InformedePersonas CELER.xlsx    # ← Excel principal con personas
│   │   └── informe_comparado_con_json.xlsx
│   │
│   ├── plantilla/                           # DESTINO: Plantillas llenas
│   │   ├── PLANTILLA DE SOTSEGUROS.xlsx    # ← Template vacío (estructura)
│   │   ├── PLANTILLA_LLENA_*.xlsx          # Personas (desde Celer)
│   │   ├── PLANTILLA_EMPRESAS_*.xlsx       # Empresas (desde Clientes)
│   │   ├── PLANTILLA_COINCIDEN.xlsx        # Coincidencias (proceso conciliación)
│   │   └── PAra enviar definitivo.xlsx     # Archivo final unificado
│   │
│   ├── ERRORES/                             # NITs problemáticos
│   │   ├── errores_sin_dv_*.xlsx           # NITs sin dígito verificación
│   │   ├── nits_no_encontrados_*.xlsx      # No encontrados en Celer
│   │   └── nits_sin_datos_*.xlsx           # No en ninguna fuente
│   │
│   └── [scripts comparación .py]           # Scripts etapas 1-3
│
├── llenar_plantilla_softseguros.py         # PROGRAMA PRINCIPAL 1
└── llenar_plantilla_empresas.py            # PROGRAMA PRINCIPAL 2
```

### 🔄 Flujo de Llenado (3 Pasos)

```
┌─────────────────────────────────────────────────────────────────────┐
│ PASO 1: Identificar NITs sin Dígito de Verificación                │
└─────────────────────────────────────────────────────────────────────┘

📂 Entrada: CLIENTES ACTIVOS.xlsx
    ↓
🔧 Proceso: Detectar NITs sin DV (7-10 dígitos sin guión)
    ↓
📤 Salida: ERRORES/errores_sin_dv_20251202_102025.xlsx


┌─────────────────────────────────────────────────────────────────────┐
│ PASO 2: Buscar Personas Naturales en CELER                         │
│ Script: llenar_plantilla_softseguros.py                            │
└─────────────────────────────────────────────────────────────────────┘

📂 ENTRADAS:
   • ERRORES/errores_sin_dv_*.xlsx           (Lista de NITs a buscar)
   • data_celer/InformedePersonas CELER.xlsx (Base datos personas)
   • plantilla/PLANTILLA DE SOTSEGUROS.xlsx  (Estructura columnas)

🔧 PROCESO:
   [1] Leer lista NITs → limpiar (solo números)
   
   [2] Leer InformedePersonas CELER.xlsx
       • 35 columnas con datos completos
       • Crear columna _id_limpia para búsqueda
   
   [3] Por cada NIT:
       ✅ SI ENCUENTRA en Celer:
          ├─ Separar Nombre → NOMBRES + APELLIDOS
          │  "PÉREZ GÓMEZ JUAN CARLOS"
          │  → APELLIDOS: "PÉREZ GÓMEZ" (primeras 2 palabras)
          │  → NOMBRES: "JUAN CARLOS" (resto)
          │
          ├─ Mapear Tipo_Doc:
          │  CC/CEDULA → "Cédula de ciudadanía"
          │  NIT → "NIT"
          │  CE → "Cédula de extranjería"
          │
          ├─ Mapear Género:
          │  M → "Masculino"
          │  F → "Femenino"
          │
          ├─ Mapear Estado_civil:
          │  S → "Soltero(a)"
          │  C → "Casado(a)"
          │  U → "Unión libre"
          │
          ├─ Extraer contactos con prioridad:
          │  Teléfono: Celular_Personal > Tel_Personal > Tel_Laboral
          │  Email: Mail_Personal > Mail_Laboral
          │  Dirección: Direccion_Personal > Direccion_Laboral
          │
          └─ Completar 44 campos de plantilla SoftSeguros
       
       ❌ SI NO ENCUENTRA:
          → Agregar a lista "no_encontrados"

📤 SALIDAS:
   ✅ plantilla/PLANTILLA_LLENA_20251202_103414.xlsx
      (Personas encontradas con datos completos)
   
   ⚠️  ERRORES/nits_no_encontrados_20251202_103414.xlsx
      (NITs no encontrados en Celer → posibles empresas)


┌─────────────────────────────────────────────────────────────────────┐
│ PASO 3: Buscar Empresas en CLIENTES ACTIVOS                        │
│ Script: llenar_plantilla_empresas.py                               │
└─────────────────────────────────────────────────────────────────────┘

📂 ENTRADAS:
   • ERRORES/nits_no_encontrados_*.xlsx      (Del paso anterior)
   • clientes_activos/CLIENTES ACTIVOS.xlsx  (Base datos empresas)
   • plantilla/PLANTILLA DE SOTSEGUROS.xlsx  (Estructura columnas)

🔧 PROCESO:
   [1] Leer NITs no encontrados en Celer (son empresas)
   
   [2] Leer CLIENTES ACTIVOS.xlsx
       • Lee desde fila 4 (header=3)
       • Crear columna _id_limpia para búsqueda
   
   [3] Por cada NIT:
       ✅ SI ENCUENTRA en Clientes Activos:
          ├─ NOMBRES = campo "Tomador" (nombre completo empresa)
          ├─ APELLIDOS = "" (empresas no tienen apellidos)
          ├─ TIPO DE DOCUMENTO = "NIT" (forzado)
          ├─ GÉNERO = "" (vacío)
          ├─ ESTADO CIVIL = "" (vacío)
          ├─ Teléfonos: Celular_Lab, Telefono_Lab
          ├─ Email: Mail_Lab
          ├─ Dirección: Direccion_Lab
          ├─ Ciudad: Ciudad_Lab
          └─ Marca: "CARGADO POR: Migración Automática - Empresas"
       
       ❌ SI NO ENCUENTRA:
          → Agregar a "nits_sin_datos" (requieren revisión manual)

📤 SALIDAS:
   ✅ plantilla/PLANTILLA_EMPRESAS_20251202_104937.xlsx
      (Empresas encontradas)
   
   ⚠️  ERRORES/nits_sin_datos_*.xlsx
      (NITs sin datos en ninguna fuente → revisión manual)
```

### 📋 Estructura de PLANTILLA DE SOTSEGUROS (44 columnas)

```
┌─────────────────────────────────────────────────────────────────┐
│ SECCIÓN 1: IDENTIFICACIÓN (7 campos)                           │
└─────────────────────────────────────────────────────────────────┘
1.  NOMBRES
2.  APELLIDOS
3.  SOBRENOMBRE (ALIAS)
4.  NÚMERO DE DOCUMENTO
5.  TIPO DE DOCUMENTO
6.  GÉNERO
7.  ESTADO CIVIL

┌─────────────────────────────────────────────────────────────────┐
│ SECCIÓN 2: CONTACTOS (12 campos)                               │
└─────────────────────────────────────────────────────────────────┘
8.  FECHA DE NACIMIENTO
9.  TELÉFONO MÓVIL
10. TIPO TELÉFONO MÓVIL (Personal/Laboral)
11. TELÉFONO PRINCIPAL
12. TIPO DE TELÉFONO PRINCIPAL
13. TELÉFONO SECUNDARIO
14. TIPO DE TELÉFONO SECUNDARIO
15. EMAIL
16. TIPO EMAIL (Personal/Laboral)
17. EMAIL SECUNDARIO
18. TIPO EMAIL SECUNDARIO

┌─────────────────────────────────────────────────────────────────┐
│ SECCIÓN 3: DIRECCIONES (7 campos)                              │
└─────────────────────────────────────────────────────────────────┘
19. DIRECCIÓN PRINCIPAL
20. TIPO DIRECCIÓN (Personal/Laboral)
21. DIRECCIÓN SECUNDARIA
22. TIPO DIRECCIÓN SECUNDARIA
23. PAÍS
24. ESTADO
25. CIUDAD

┌─────────────────────────────────────────────────────────────────┐
│ SECCIÓN 4: INFORMACIÓN ADICIONAL (18 campos)                   │
└─────────────────────────────────────────────────────────────────┘
26. OCUPACIÓN
27. INGRESO MENSUAL
28. PATRIMONIO
29. CASA PROPIA
30. NÚMERO DE CASAS
31. HIJOS
32. NÚMERO DE HIJOS
33. VEHÍCULOS
34. NÚMERO DE VEHÍCULOS
35. PAGINA WEB
36. REDES SOCIALES
37. NOMBRE DE CONTACTO
38. CATEGORÍAS
39. OBSERVACIONES
40. CARGADO POR
41-44. (Campos adicionales)
```

### 🔑 Diferencias Clave: Personas vs Empresas

```
┌─────────────────────────────────────────────────────────────────┐
│ PERSONA NATURAL (desde Celer)                                  │
└─────────────────────────────────────────────────────────────────┘
NOMBRES:          "JUAN CARLOS"
APELLIDOS:        "PÉREZ GÓMEZ"
TIPO DOCUMENTO:   "Cédula de ciudadanía"
GÉNERO:           "Masculino"
ESTADO CIVIL:     "Casado(a)"
TELÉFONO:         Celular_Personal
EMAIL:            Mail_Personal
DIRECCIÓN:        Direccion_Personal
CARGADO POR:      "Migración Automática"

┌─────────────────────────────────────────────────────────────────┐
│ EMPRESA (desde Clientes Activos)                               │
└─────────────────────────────────────────────────────────────────┘
NOMBRES:          "SEGUROS BOLÍVAR S.A."
APELLIDOS:        "" (vacío)
TIPO DOCUMENTO:   "NIT"
GÉNERO:           "" (vacío)
ESTADO CIVIL:     "" (vacío)
TELÉFONO:         Celular_Lab o Telefono_Lab
EMAIL:            Mail_Lab
DIRECCIÓN:        Direccion_Lab
CARGADO POR:      "Migración Automática - Empresas"
```

### 🛠️ Scripts Principales de Llenado

#### 📄 `llenar_plantilla_softseguros.py`
**Propósito:** Llenar plantilla con personas naturales desde Celer

**Funciones clave:**
```python
separar_nombre_apellidos(nombre_completo)
  • Separa "APELLIDO1 APELLIDO2 NOMBRE1 NOMBRE2"
  • Detecta formato con coma: "APELLIDOS, NOMBRES"
  • Primeras 2 palabras = apellidos, resto = nombres

mapear_tipo_documento(tipo_celer)
  • CC/CEDULA → "Cédula de ciudadanía"
  • NIT → "NIT"
  • CE → "Cédula de extranjería"

mapear_genero(genero_celer)
  • M/MASCULINO → "Masculino"
  • F/FEMENINO → "Femenino"

mapear_estado_civil(estado_celer)
  • S/SOLTERO → "Soltero(a)"
  • C/CASADO → "Casado(a)"
  • U/UNION LIBRE → "Unión libre"

limpiar_identificacion(valor)
  • Elimina guiones, puntos, espacios
  • Deja solo números para comparación
```

**Ejemplo de mapeo completo:**
```python
# Registro en Celer:
{
  "Nombre": "PÉREZ GÓMEZ JUAN CARLOS",
  "Identificacion": "1234567890",
  "Tipo_Doc": "CC",
  "Genero": "M",
  "Estado_civil": "C",
  "Celular_Personal": "3001234567",
  "Mail_Personal": "juan@email.com",
  "Direccion_Personal": "CALLE 100 # 20-30"
}

# Se transforma a:
{
  "NOMBRES": "JUAN CARLOS",
  "APELLIDOS": "PÉREZ GÓMEZ",
  "NÚMERO DE DOCUMENTO": "1234567890",
  "TIPO DE DOCUMENTO": "Cédula de ciudadanía",
  "GÉNERO": "Masculino",
  "ESTADO CIVIL": "Casado(a)",
  "TELÉFONO MÓVIL": "3001234567",
  "TIPO TELÉFONO MÓVIL": "Personal",
  "EMAIL": "juan@email.com",
  "TIPO EMAIL": "Personal",
  "DIRECCIÓN PRINCIPAL": "CALLE 100 # 20-30",
  "TIPO DIRECCIÓN": "Personal",
  "PAÍS": "Colombia",
  "CARGADO POR": "Migración Automática"
}
```

#### 📄 `llenar_plantilla_empresas.py`
**Propósito:** Llenar plantilla con empresas desde Clientes Activos

**Características especiales:**
- Lee desde fila 4: `pd.read_excel(archivo, header=3)`
- Evita duplicados: `nits_ya_agregados = set()`
- Nombre completo va en campo NOMBRES
- APELLIDOS queda vacío
- Solo usa datos laborales (Lab)

**Ejemplo de mapeo empresa:**
```python
# Registro en Clientes Activos:
{
  "Tomador": "SEGUROS BOLÍVAR S.A.",
  "Identificacion": "860002503-4",
  "Telefono_Lab": "6012345678",
  "Mail_Lab": "info@bolivar.com",
  "Direccion_Lab": "AV. CARACAS # 100-20",
  "Ciudad_Lab": "BOGOTÁ"
}

# Se transforma a:
{
  "NOMBRES": "SEGUROS BOLÍVAR S.A.",
  "APELLIDOS": "",
  "NÚMERO DE DOCUMENTO": "860002503-4",
  "TIPO DE DOCUMENTO": "NIT",
  "GÉNERO": "",
  "ESTADO CIVIL": "",
  "TELÉFONO PRINCIPAL": "6012345678",
  "TIPO DE TELÉFONO PRINCIPAL": "Laboral",
  "EMAIL": "info@bolivar.com",
  "TIPO EMAIL": "Laboral",
  "DIRECCIÓN PRINCIPAL": "AV. CARACAS # 100-20",
  "TIPO DIRECCIÓN": "Laboral",
  "CIUDAD": "BOGOTÁ",
  "PAÍS": "Colombia",
  "CARGADO POR": "Migración Automática - Empresas"
}
```

### 📊 Scripts de Comparación y Análisis

#### `comparar_identificaciones_informe_json.py`
- Cruza identificaciones entre JSON de diferencias e InformedePersonas
- Genera: `informe_comparado_con_json.xlsx`
- Agrega columna `Coincide_JSON` (True/False)

#### `mostrar_columnas_informe.py`
- Vista previa de estructura de archivos
- Muestra primeras 10 filas sin encabezado

#### `mostrar_columnas_informe_personas.py`
- Lista todas las columnas de InformedePersonas CELER
- Útil para verificar nombres exactos de campos

#### `leer_estructura_plantilla.py`
- Analiza estructura de PLANTILLA DE SOTSEGUROS
- Muestra columnas y tipos de datos esperados

### 🎯 Resultado Final

```
PLANTILLA_LLENA_*.xlsx (Personas desde Celer)
           +
PLANTILLA_EMPRESAS_*.xlsx (Empresas desde Clientes)
           ↓
    Unir manualmente
           ↓
PAra enviar definitivo.xlsx
           ↓
    Subir a SoftSeguros
```

### ⚠️ Consideraciones Importantes

**Limpieza de identificaciones:**
- Todos los NITs se limpian antes de comparar (solo números)
- Esto permite encontrar coincidencias con diferentes formatos:
  - `900123456`
  - `900123456-4`
  - `900.123.456-4`

**Prioridad de datos de contacto:**
```
Teléfonos: Personal > Laboral
Emails: Personal > Laboral
Direcciones: Personal > Laboral
```

**Evitar duplicados:**
- `llenar_plantilla_empresas.py` usa `set()` para rastrear NITs ya agregados
- Si un NIT aparece múltiples veces, solo se agrega una vez

**Timestamp en archivos:**
- Todos los archivos generados incluyen timestamp: `YYYYMMDD_HHMMSS`
- Permite rastrear diferentes ejecuciones del proceso
- Ejemplo: `PLANTILLA_LLENA_20251202_103414.xlsx`

---

## 📚 Referencias

- **Algoritmo DV NIT**: Resolución DIAN 12487 de 2018
- **Formatos de documento Colombia**: CC (Cédula), CE (Cédula Extranjería), NIT (Registro Tributario)
- **Nomenclatura seguros**: TOMADOR = Contratante, ASEGURADO = Persona/bien cubierto

---

**Última actualización:** Enero 2026  
**Versión:** 2.1  
**Autor:** Equipo Migración SoftSeguros
