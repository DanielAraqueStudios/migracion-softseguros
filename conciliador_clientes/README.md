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

## 📚 Referencias

- **Algoritmo DV NIT**: Resolución DIAN 12487 de 2018
- **Formatos de documento Colombia**: CC (Cédula), CE (Cédula Extranjería), NIT (Registro Tributario)
- **Nomenclatura seguros**: TOMADOR = Contratante, ASEGURADO = Persona/bien cubierto

---

**Última actualización:** Enero 2026  
**Versión:** 2.0  
**Autor:** Equipo Migración SoftSeguros
