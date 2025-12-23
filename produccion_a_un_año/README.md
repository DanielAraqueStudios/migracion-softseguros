# Producción a Un Año - SoftSeguros

## Descripción
Módulo completo para el procesamiento, migración, validación y corrección de pólizas con vigencia de un año, trasladando datos desde CELER hacia la plantilla Maviso. Incluye herramientas profesionales con interfaz gráfica para comparación automática, corrección de discrepancias, validación de NITs y más.

## Estructura de Carpetas

```
produccion_a_un_año/
├── Copy of Maviso.xlsx                    # Plantilla destino (estructura y formato)
├── Copy of polizas vigentes celer.xlsx    # Archivo fuente CELER
├── llenar_maviso.py                       # Script CLI de migración
├── llenar_maviso_gui.py                   # 🎨 GUI para llenado de Maviso
├── calcular_dv_maviso.py                  # Script CLI para cálculo de DV
├── calcular_dv_maviso_gui.py              # 🎨 GUI para cálculo de DV con API DIAN
├── comparador_archivos/                   # 📊 Herramientas de comparación
│   ├── comparar_archivos_gui.py           # GUI principal de comparación
│   ├── comparar_maviso_celer.py           # Motor de comparación
│   ├── estilos.py                         # Tema dark profesional
│   └── output/                            # Reportes de comparación
├── mapeo_ramos.py                         # Mapeo de ramos CELER → Maviso
├── conciliar_ramos.py                     # Conciliación de ramos
├── analizar_ramos_subramos.py             # Análisis de ramos/subramos
├── README.md                              # Esta documentación
├── COMPARACION_RAMOS_SUBRAMOS.md          # Documentación de mapeos
├── logs/                                  # Logs de ejecución
└── output/                                # Archivos generados
    └── Maviso_llenado_YYYYMMDD_HHMMSS.xlsx
```

## Archivos

### Entrada
- `Copy of polizas vigentes celer.xlsx` - Archivo fuente con datos de CELER (3,164 filas × 59 columnas, skiprows=3)
- `Copy of Maviso.xlsx` - Plantilla con estructura y formato a replicar (39 columnas)

### Salida
- `output/Maviso_llenado_YYYYMMDD_HHMMSS.xlsx` - Archivo generado con datos de CELER y formato de Maviso

---

## Mapeo de Columnas CELER → Maviso (por letra Excel)

| Maviso (Destino) | CELER (Fuente) | Descripción |
|------------------|----------------|-------------|
| A | U | NÚMERO DE PÓLIZA ← Póliza |
| B | AE | RIESGO ← Placa |
| C | R | ASEGURADORA ← Aseguradora |
| D | (vacío) | - |
| E | S | SUBRAMO ← Ramo |
| F | (vacío) | - |
| J | BE | FECHA INICIO ← F_Inicio |
| K | W | FECHA FIN ← F_Fin |
| L | X | PRIMA NETA ← prima sin iva |
| O | AQ | VALOR RIESGO ASEGURADO ← V_Asegurado |
| **W** | **Condicional AB** | **FORMA PAGO (ver lógica abajo)** |
| X | AP | - |
| AB | C | DOCUMENTO DEL CLIENTE ← Identificacion |
| AC | A | TIPO PERSONA ← Tipo_Persona |
| AD | B | NOMBRE DEL TOMADOR ← Tomador |
| AE | C | DOCUMENTO DEL TOMADOR ← Identificacion |
| AF | AS | NOMBRE DEL ASEGURADO ← Asegurado |
| AG | AT | DOCUMENTO DEL ASEGURADO ← Iden_Asegurado |
| AH | AW | NOMBRE DEL BENEFICIARIO ← Beneficiario |
| AI | AX | DOCUMENTO DEL BENEFICIARIO ← Iden_Beneficiario |

---

## Lógica Condicional - Columna W (FORMA PAGO)

La columna **W de Maviso** (FORMA PAGO) se llena con lógica condicional basada en la columna **AB de CELER** (Forma_Pago):

| CELER AB (Forma_Pago) | Maviso W (FORMA PAGO) |
|-----------------------|-----------------------|
| MENSUAL | **Fraccionado** |
| ANUAL | **Contado** |

```python
# Lógica en el script:
if forma_pago_celer == "MENSUAL":
    forma_pago_maviso = "Fraccionado"
elif forma_pago_celer == "ANUAL":
    forma_pago_maviso = "Contado"
```

---

## Estructura de Columnas - Archivos

### ARCHIVO DESTINO: Copy of Maviso.xlsx (SoftSeguros)
**3,166 filas × 39 columnas**

| Col | # | Columna | Ejemplo |
|-----|---|---------|---------|
| A | 1 | NÚMERO DE PÓLIZA | 1338293 |
| B | 2 | RIESGO | CJG82H |
| C | 3 | CELER | SBS SEGUROS COLOMBIA S.A |
| D | 4 | ASEGURADORA | SBS SEGUROS COLOMBIA S.A |
| E | 5 | CELER | AUTOMOVILES |
| F | 6 | SUBRAMO | AUTOS INDIVIDUAL |
| G | 7 | TIPO DE PÓLIZA | individual |
| H | 8 | ESTADO DE PÓLIZA | Vigente |
| I | 9 | RENOVABLE | Si |
| J | 10 | NOMBRE DEL VENDEDOR | YEISON LEON PUERTA CADAVID |
| K | 11 | FECHA INICIO | 17/07/2025 |
| L | 12 | FECHA FIN | 17/07/2026 |
| M | 13 | FECHA DE RECEPCIÓN | (vacío) |
| N | 14 | FECHA DE EXPEDICIÓN | (vacío) |
| O | 15 | PRIMA NETA | 597729.0 |
| P | 16 | GASTOS DE EXPEDICIÓN | (vacío) |
| Q | 17 | IVA | 19 |
| R | 18 | TOTAL | (vacío) |
| S | 19 | PORCENTAJE DE COMISIÓN | (vacío) |
| T | 20 | PARTICIPACIÓN | (vacío) |
| U | 21 | COMISIÓN | (vacío) |
| V | 22 | CELER.1 | ANUAL |
| W | 23 | FORMA PAGO | Fraccionado/Contado |
| X | 24 | VALOR RIESGO ASEGURADO | 11600000 |
| Y | 25 | FECHA CANCELACIÓN | (vacío) |
| Z | 26 | ES RENOVACIÓN | Si |
| AA | 27 | PÓLIZA PADRE AGRUPADORA | (vacío) |
| AB | 28 | DOCUMENTO DEL CLIENTE | 98700799 |
| AC | 29 | (Tipo Persona) | N |
| AD | 30 | NOMBRE DEL TOMADOR | ADRIAN FELIPE ARROYAVE |
| AE | 31 | DOCUMENTO DEL TOMADOR | 98700799 |
| AF | 32 | NOMBRE DEL ASEGURADO | ADRIAN FELIPE ARROYAVE |
| AG | 33 | DOCUMENTO DEL ASEGURADO | 98700799 |
| AH | 34 | NOMBRE DEL BENEFICIARIO | ADRIAN FELIPE ARROYAVE |
| AI | 35 | DOCUMENTO DEL BENEFICIARIO | 98700799 |
| AJ | 36 | OBSERVACIONES INTERNAS | (vacío) |
| AK | 37 | OBSERVACIONES | (vacío) |
| AL | 38 | CARGADA POR | (vacío) |
| AM | 39 | CATEGORÍAS | (vacío) |

---

### ARCHIVO FUENTE: Copy of polizas vigentes celer.xlsx
**3,164 filas × 59 columnas** (skiprows=3)

| Col | # | Columna CELER | Ejemplo |
|-----|---|---------------|---------|
| A | 1 | Tipo_Persona | N |
| B | 2 | Tomador | ADRIAN FELIPE ARROYAVE |
| C | 3 | Identificacion | 98700799 |
| D | 4 | Tipo_Doc | C.C |
| E | 5 | Telefono_Lab | 322-92-23 |
| F | 6 | Telefono_Pers | 8515708 |
| G | 7 | Celular_Lab | 3218003673 |
| H | 8 | Celular_Pers | 3015556155 |
| I | 9 | Mail_Lab | avcolombiasas@gmail.com |
| J | 10 | Mail_Pers | arrofeli@gmail.com |
| K | 11 | Direccion_Lab | CR 6 62 B 32 OFICINA 305 |
| L | 12 | Ciudad_Lab | MEDELLIN |
| M | 13 | Direccion_Pers | CALLE 57# 69-27 |
| N | 14 | Ciudad_Pers | MEDELLIN |
| O | 15 | F_Nac_Tomador | 21/07/1984 |
| P | 16 | Edad_Tomador | 41 |
| Q | 17 | Cod_Aseguradora | 78 |
| R | 18 | Aseguradora | SBS SEGUROS COLOMBIA S.A |
| S | 19 | Ramo | AUTOMOVILES |
| T | 20 | Cod_Ramo | 40 |
| U | 21 | Póliza | 1338293 |
| V | 22 | F_Inicio_Primera_Vig | 17/07/2024 |
| W | 23 | F_Inicio | 17/07/2025 |
| X | 24 | F_Fin | 17/07/2026 |
| Y | 25 | Plan_Cod | 0 |
| Z | 26 | Plan | TRADICIONAL |
| AA | 27 | Modalidad | I |
| AB | 28 | Forma_Pago | ANUAL |
| AC | 29 | Cuotas | 1 |
| AD | 30 | Dsc_Riesgo | CJG82H *AEROX 155 |
| AE | 31 | Placa | CJG82H |
| AF | 32 | Modelo_Vehiculo | 2025 |
| AG | 33 | Marca_Vehiculo | YAMAHA |
| AH | 34 | Tipo_Vehiculo | MOTOCICLE |
| AI | 35 | Linea | AEROX 155 AT 155CC ABS |
| AJ | 36 | Servicio | Particular |
| AK | 37 | Fasecolda | 09817232 |
| AL | 38 | Motor | G3P4E0235439 |
| AM | 39 | Chasis | 9FKSG8715S2235439 |
| AN | 40 | Venci_TecnicoMecanica | 15/07/2025 |
| AO | 41 | Circulacion | MEDELLIN |
| AP | 42 | V_Asegurado | 11600000 |
| AQ | 43 | prima sin iva | 597729.0 |
| AR | 44 | Prima_Anualizada | 597729.0 |
| AS | 45 | Asegurado | ADRIAN FELIPE ARROYAVE |
| AT | 46 | Iden_Asegurado | 98700799 |
| AU | 47 | F_Nac_Asegurado | 21/07/1984 |
| AV | 48 | Edad_Asegurado | 41 |
| AW | 49 | Beneficiario | ADRIAN FELIPE ARROYAVE |
| AX | 50 | Iden_Beneficiario | 98700799 |
| AY | 51 | F_Nac_Beneficiario | 21/07/1984 |
| AZ | 52 | Edad_Beneficiario | 41 |
| BA | 53 | Con_Bene_Oneroso | S |
| BB | 54 | Bene_Oneroso | COMPAÑÍA SURAMERICANA |
| BC | 55 | Sucursal | SUCURSAL MEDELLIN |
| BD | 56 | Unidad | LILIANA LOPEZ BENJUMEA |
| BE | 57 | Ejecutivos | YEISON LEON PUERTA |
| BF | 58 | F_Creacion | 17/07/2024 9:31 a.m. |
| BG | 59 | F_Modificacion | 21/07/2025 11:21 a.m. |

---

## 🚀 Herramientas Principales


### 1. 🎨 Comparador de Archivos (GUI)
**Archivo**: `comparador_archivos/comparar_archivos_gui.py`

Interfaz gráfica profesional para comparar MAVISO vs CELER, detectar discrepancias, aplicar correcciones automáticas y realizar operaciones avanzadas sobre los archivos de pólizas.

#### Funcionalidades:

**📊 Comparación Automática**
- Compara ambos archivos póliza por póliza
- Detecta discrepancias en: Modalidad, Prima, Fechas (Inicio/Fin)
- Identifica pólizas solo en MAVISO o solo en CELER
- Equivalencia especial: CELER "UNICA" = MAVISO "ANUAL"
- Genera estadísticas en tiempo real

**🔍 Búsqueda de Póliza**
- Busca póliza específica en ambos archivos
- Muestra todos los campos (prima, fechas, modalidad)
- Indica en qué archivo existe
- Proporciona conclusiones sobre discrepancias

**📥 Agregar Faltantes desde CELER**
- Detecta pólizas que están solo en CELER
- Las agrega automáticamente a MAVISO
- Mapea todos los campos según especificación
- Genera archivo nuevo con timestamp

**🔧 Corregir Modalidades**
- Actualiza modalidades en MAVISO con datos de CELER
- Preserva formato y colores Excel
- Recompara automáticamente después de corrección
- Abre archivo actualizado

**💰 Corregir Primas**
- Actualiza primas en MAVISO con datos de CELER
- Mantiene formatos numéricos
- Recompara automáticamente
- Log detallado de cambios

**🔄 Primas Mensuales a Cero**
- Pone en 0 las primas de todas las pólizas MENSUALES
- Útil para ajustes de facturación
- Confirmación antes de aplicar

**📅 Corregir Vigencias**
- Actualiza fechas de inicio y fin desde CELER
- Toma CELER como fuente de verdad
- Preserva formato de fechas

**📝 Llenar Riesgos Vacíos**
- Si columna B (RIESGO) está vacía, copia columna F (SUBRAMO)
- Útil para completar datos faltantes

**🔧 Colocar NITs Completos**
- Calcula y agrega DV a NITs de personas jurídicas
- Usa API DIAN para validación
- Solo actualiza si no tiene DV

**📊 Exportar Reporte**
- Genera Excel con pestañas: Coincidencias, Discrepancias, Solo Maviso, Solo CELER
- Abre automáticamente el reporte
- Timestamp en nombre de archivo

**🆕 Copiar Unidades desde CELER**
- Nueva pestaña dedicada para copiar la columna **Unidad** desde el archivo CELER hacia otro archivo Excel destino, emparejando por número de póliza.
- Solo requiere seleccionar el archivo CELER y el archivo DESTINO (no requiere archivo MAVISO para esta función).
- Permite elegir la columna de destino donde pegar las unidades.
- Busca automáticamente las pólizas en la **columna B** del archivo destino.
- Lee las unidades desde la **columna BD (índice 55)** del archivo CELER (con skiprows=3).
- Empata las pólizas desde la **columna U (índice 20)** de CELER con la columna B del destino.
- Copia el valor de la columna **Unidad** a la columna seleccionada en el archivo destino, según coincidencia de número de póliza.
- Si la póliza no se encuentra en CELER, toda la fila se marca en **rojo** en el archivo de salida.
- Genera un archivo Excel de salida con timestamp y un log detallado de la operación.
- Proceso asíncrono con barra de progreso y estadísticas en tiempo real.

**Ejecutar**:
```powershell
cd produccion_a_un_año/comparador_archivos
python comparar_archivos_gui.py
```

---

### 2. 🧮 Calculadora de DV (GUI)
**Archivo**: `calcular_dv_maviso_gui.py`

Interfaz para calcular y agregar Dígitos de Verificación a NITs de personas jurídicas usando la API DIAN.

#### Funcionalidades:

**🚀 Gestión de API DIAN**
- Inicia/detiene API FastAPI automáticamente
- Puerto 8000 (localhost)
- Verificación de salud de API
- Botón de reinicio con limpieza de puerto

**🔢 Cálculo Masivo de DV**
- Procesa todo el archivo MAVISO
- Solo actualiza NITs de personas jurídicas (tipo "J")
- Solo agrega DV si no existe (no tiene "-")
- Preserva formato Excel original

**📊 Monitoreo en Tiempo Real**
- Barra de progreso visual
- Log detallado de operaciones
- Contador de NITs procesados
- Errores y advertencias

**Ejecutar**:
```powershell
cd produccion_a_un_año
python calcular_dv_maviso_gui.py
```

---

### 3. 📋 Llenado de Maviso (GUI)
**Archivo**: `llenar_maviso_gui.py`

Interfaz gráfica para migración inicial de datos CELER → Maviso.

#### Funcionalidades:

**📤 Migración Completa**
- Lee CELER con skiprows=3
- Aplica mapeo según especificación
- Copia formato y estilos de plantilla
- Lógica condicional para FORMA PAGO

**📊 Validaciones**
- Verifica estructura de archivos
- Valida columnas requeridas
- Log detallado de proceso

**Ejecutar**:
```powershell
cd produccion_a_un_año
python llenar_maviso_gui.py
```

---

## 📖 Workflow Recomendado

### Migración Completa Paso a Paso

1. **🏁 Llenado Inicial**
   ```powershell
   python llenar_maviso_gui.py
   ```
   - Selecciona archivo CELER fuente
   - Selecciona plantilla Maviso
   - Ejecuta migración
   - Genera `output/Maviso_llenado_TIMESTAMP.xlsx`

2. **🔍 Comparación y Validación**
   ```powershell
   cd comparador_archivos
   python comparar_archivos_gui.py
   ```
   - Carga MAVISO generado
   - Carga archivo CELER original
   - Ejecuta comparación
   - Revisa estadísticas y discrepancias

3. **🔧 Correcciones Automáticas**
   En orden recomendado:
   - **📥 Agregar Faltantes**: Si hay pólizas solo en CELER
   - **📅 Corregir Vigencias**: Actualizar fechas desde CELER
   - **🔧 Corregir Modalidades**: Sincronizar modalidades
   - **💰 Corregir Primas**: Actualizar valores
   - **📝 Llenar Riesgos Vacíos**: Completar datos faltantes

4. **🔢 Cálculo de DV**
   ```powershell
   python calcular_dv_maviso_gui.py
   ```
   - Inicia API DIAN
   - Carga archivo MAVISO
   - Ejecuta cálculo masivo
   - Verifica NITs actualizados

5. **📊 Exportar Reporte Final**
   - Click en "📊 Exportar Reporte"
   - Revisa pestañas del reporte Excel
   - Valida coincidencias vs discrepancias

---

## 🎨 Características de las GUI

### Tema Dark Profesional
- Colores: Fondo #1e1e1e, Texto #d4d4d4
- Botones con gradientes y hover effects
- Logs con colores por tipo (success, error, warning, info)
- Iconos emoji para mejor UX

### Operaciones Asíncronas
- Comparaciones en threads separados
- No bloquea la interfaz
- Barras de progreso en tiempo real

### Preservación de Formato
- Usa openpyxl para mantener estilos
- Colores, fuentes, bordes originales
- Formatos numéricos y de fecha

---

## Uso CLI (Scripts Originales)

### Migración básica
```powershell
cd produccion_a_un_año
python llenar_maviso.py
```

### Cálculo de DV por consola
### Cálculo de DV por consola
```powershell
python calcular_dv_maviso.py
```

---

## ⚙️ Configuración de API DIAN

### Backend FastAPI
Ubicación: `backend/app.py` (dos niveles arriba)

**Endpoints**:
- `GET /health` - Verificar estado de API
- `POST /calcular` - Calcular DV para un NIT

**Puerto**: 8000 (localhost)

### Inicio Manual de API
```powershell
cd ../../backend
uvicorn app:app --host 127.0.0.1 --port 8000
```

### Reinicio con Limpieza de Puerto
Si el puerto 8000 está ocupado:
1. Usa el botón "🔄 REINICIAR API" en la GUI
2. O manualmente:
   ```powershell
   netstat -ano | findstr :8000
   taskkill /F /PID <PID_NUMBER>
   ```

---

## 📋 Reglas de Negocio

### Equivalencias de Modalidad
- **CELER "UNICA"** = **MAVISO "ANUAL"** (no se marca como discrepancia)

### Forma de Pago (Lógica Condicional)
- CELER "MENSUAL" → MAVISO "Fraccionado"
- CELER "ANUAL" → MAVISO "Contado"

### Personas Jurídicas (Cálculo DV)
- Solo se procesa si Tipo Persona = "J"
- Solo se agrega DV si NIT no contiene "-"
- Formato: `NIT-DV` (ej: 890906852-7)

### Llenado de Riesgos
- Si columna B (RIESGO) vacía → copiar columna F (SUBRAMO)

---

## 🏢 Mapeo de Aseguradoras y Ramos/Subramos

### Resumen de Cobertura
- **Total Pólizas CELER**: 3,164
- **Aseguradoras CELER**: 26
- **Ramos únicos CELER**: 44
- **Cobertura de mapeo**: 100% ✅ (todos los ramos están mapeados)

### Lógica de Aseguradoras con Versión Generales/Vida

Algunas aseguradoras tienen dos versiones en MAVISO: una para seguros **Generales** y otra para seguros de **Vida**. El sistema determina automáticamente cuál usar según el tipo de ramo:

**Ramos que van a compañía de VIDA:**
- VIDA INDIVIDUAL, VIDA COLECTIVO, VIDA GRUPO COLECTIVO
- ACCIDENTES PERSONALES, ACCIDENTES DE PASAJEROS, ACCIDENTES JUVENILES, ACCIDENTES ESCOLARES
- SALUD FAMILIAR, SALUD PARA TODOS, SALUD COLECTIVA
- PLAN COMPLEMENTARIO, PLAN COMPLEMENTARIO COLECTIVO, PLAN COMPLEMENTARIO FAMILIAR
- RENTA EDUCATIVA, MAS VIDA, ARL, SEGURO EXEQUIAL, SEGUROS EXEQUIALES

**Aseguradoras con doble versión (Generales/Vida):**

| CELER | MAVISO Generales | MAVISO Vida |
|-------|------------------|-------------|
| SURAMERICANA S.A. | SEGUROS GENERALES SURAMERICANA S.A | SEGUROS DE VIDA SURAMERICANA S.A |
| ALLIANZ SEGUROS S.A | ALLIANZ SEGUROS S.A | ALLIANZ SEGUROS DE VIDA S.A |
| LIBERTY SEGUROS S A* | ALLIANZ SEGUROS S.A | ALLIANZ SEGUROS DE VIDA S.A |
| AXA COLPATRIA SEGUROS S.A. | AXA COLPATRIA SEGUROS S.A | AXA COLPATRIA SEGUROS DE VIDA S.A |
| SEGUROS DEL ESTADO S A | SEGUROS DEL ESTADO S.A | SEGUROS DE VIDA DEL ESTADO |

> *LIBERTY y ALLIANZ son la misma compañía en MAVISO

### Mapeo Completo de Ramos CELER → Subramos MAVISO

#### 🟦 Seguros Generales

| Ramo CELER | Subramo MAVISO | Aseguradoras que lo usan |
|------------|----------------|--------------------------|
| AUTOMOVILES | AUTOS INDIVIDUAL | Todas las principales |
| SOAT | SOAT | Solidaria, Seg. Estado, AXA |
| CUMPLIMIENTO | CUMPLIMIENTO | Solidaria, Mundial, Suramericana, Seg. Estado |
| MULTIRIESGO RESIDENCIAL | HOGAR | Allianz, Suramericana, HDI |
| MULTIRIESGO EMPRESARIAL | MULTIRRIESGO EMPRESARIAL | Todas las principales |
| MI PYME | MI PYME | Allianz |
| RESPONSABILIDAD CIVIL | RC DERIVADA DE CUMPLIMIENTO | Solidaria, Mundial, Suramericana |
| RC SERVIDORES PUBLICOS | RC PREDIOS LABORES Y OPERACIONES | La Previsora |
| RC CLINICAS Y HOSPITALES | RC CLINICAS Y HOSPITALES | Suramericana |
| TRANSPORTES DE MERCANCIAS | TRANSPORTES DE MERCANCIAS | Allianz, Solidaria, Suramericana |
| TRANSPORTE DE VALORES | TRANSPORTE DE VALORES | Solidaria, Suramericana |
| TODO RIESGO DAÑOS MATERIALES | TODO RIESGO DAÑOS MATERIALES | Solidaria |
| MANEJO | MANEJO ENTIDADES FINANCIERAS | Solidaria, Suramericana, Seg. Estado |
| MANEJO ENTIDADES FINANCIERAS | MANEJO ENTIDADES FINANCIERAS | Solidaria |
| MAQUINARIA Y EQUIPO | MAQUINARIA Y EQUIPO | Solidaria, SBS |
| MULTIRIESGO COPROPIEDADES | COPROPIEDADES | Solidaria, SBS, Seg. Estado |
| INCENDIO | MULTIRRIESGO EMPRESARIAL | Suramericana, SBS |
| ARRENDAMIENTO | ARRENDAMIENTO | Mundial |
| PROTECCION DIGITAL | PROTECCION DIGITAL | Suramericana |
| AERONAVES CASCO | AERONAVES CASCO | Zurich |

#### 🟩 Seguros de Vida

| Ramo CELER | Subramo MAVISO | Aseguradoras que lo usan |
|------------|----------------|--------------------------|
| VIDA INDIVIDUAL | VIDA ACTUAL | Allianz, Suramericana, HDI |
| VIDA COLECTIVO | VIDA GRUPO CONTRIBUTIVA | Allianz, Suramericana, La Previsora |
| VIDA GRUPO COLECTIVO | VIDA GRUPO CONTRIBUTIVO | Solidaria, Suramericana, Colmena |
| ACCIDENTES PERSONALES | ACCIDENTES PERSONALES | Todas las principales |
| ACCIDENTES DE PASAJEROS | ACCIDENTES PERSONALES | Solidaria |
| ACCIDENTES JUVENILES | ACCIDENTES JUVENILES | Solidaria, Suramericana |
| ACCIDENTES ESCOLARES | ACCIDENTES ESCOLARES | Positiva |
| SALUD FAMILIAR | SALUD CLASICO | Allianz, Suramericana, Bolívar |
| SALUD PARA TODOS | SALUD PARA TODOS | Suramericana |
| SALUD COLECTIVA | SALUD COLECTIVA CLASICO | Suramericana |
| PLAN COMPLEMENTARIO | PLAN COMPLEMENTARIO | Suramericana |
| PLAN COMPLEMENTARIO COLECTIVO | PLAN COMPLEMENTARIO COLECTIVO | Suramericana |
| PLAN COMPLEMENTARIO FAMILIAR | PLAN COMPLEMENTARIO | Suramericana |
| ARL | ARL | Suramericana, Bolívar, AXA, Colmena |
| RENTA EDUCATIVA | RENTA EDUCATIVA | Suramericana |
| MAS VIDA | MAS VIDA | AXA Colpatria |
| SEGURO EXEQUIAL | SEGUROS EXEQUIALES | Colmena, Funer San Vicente |
| SEGUROS EXEQUIALES | SEGUROS EXEQUIALES | Funer San Vicente |

#### 🟪 Medicina Prepagada y Asistencias

| Ramo CELER | Subramo MAVISO | Aseguradoras que lo usan |
|------------|----------------|--------------------------|
| MEDICINA PREPAGADA FAMILIAR | MEDICINA PREPAGADA FAMILIAR | Coomeva, CEM |
| MEDICINA PREPAGADA COLECTIV | MEDICINA PREPAGADA COLECTIV | Coomeva, Colsanitas, Medisanitas |
| EMERGENCIAS MÉDICAS | EMERGENCIAS MÉDICAS | Coomeva, Magenta, Emermedica |
| AREA PROTEGIDA | CEM | CEM |
| TELEMEDICINA | EMERGENCIAS MÉDICAS | Magenta |
| ASIST CARD | ASSIST CARD | Assist Card |

### Principales Aseguradoras por Volumen

1. **ASEGURADORA SOLIDARIA DE COLOMBIA** (1,001 pólizas)
   - Principal ramo: SOAT (464), Cumplimiento (146), Todo Riesgo (135)

2. **ALLIANZ SEGUROS S.A / LIBERTY** (656 pólizas combinadas)
   - Principal ramo: Automóviles (303), Multiriesgo Residencial (200)

3. **SURAMERICANA S.A.** (592 pólizas)
   - Ramos diversos: Automóviles (108), Vida Individual (104), Salud Familiar (96)

4. **COMPAÑÍA MUNDIAL DE SEGUROS** (251 pólizas)
   - Principal ramo: Cumplimiento (160), RC (53)

5. **SBS SEGUROS COLOMBIA S.A** (170 pólizas)
   - Principal ramo: Automóviles (153)

### Notas Importantes

1. **LIBERTY = ALLIANZ**: Son la misma compañía, todos los mapeos de LIBERTY usan las reglas de ALLIANZ.

2. **Aseguradoras con nombre idéntico**: Las siguientes mantienen el mismo nombre en CELER y MAVISO:
   - ASEGURADORA SOLIDARIA DE COLOMBIA
   - POSITIVA COMPANIA DE SEGUROS S.A
   - SBS SEGUROS COLOMBIA S.A
   - ZURICH COLOMBIA SEGUROS S.A
   - LA PREVISORA S A COMPAÑÍA DE SEGUROS

3. **100% de cobertura**: Todos los 44 ramos únicos de CELER tienen su correspondiente subramo en MAVISO.

4. **Documentación detallada**: Consultar `COMPARACION_RAMOS_SUBRAMOS.md` para el mapeo completo con ejemplos y casos especiales por aseguradora.

---

## 🗂️ Estructura de Archivos

### Archivos de Entrada

---

## 🗂️ Estructura de Archivos

### Archivos de Entrada
- **MAVISO**: 3,140+ filas × 39 columnas (sin skiprows)
- **CELER**: 3,164+ filas × 59 columnas (skiprows=3)

### Archivos Generados
- `output/Maviso_llenado_YYYYMMDD_HHMMSS.xlsx` - Migración inicial
- `output/MAVISO_con_faltantes_YYYYMMDD_HHMMSS.xlsx` - Con pólizas agregadas
- `comparador_archivos/output/reporte_comparacion_YYYYMMDD_HHMMSS.xlsx` - Reportes
- `logs/` - Logs de ejecución

---

## 🔍 Mapeo de Columnas Detallado

### Migración CELER → Maviso

| MAVISO | Col# | CELER | Col# | Descripción | Notas |
|--------|------|-------|------|-------------|-------|
| A | 0 | U | 20 | NÚMERO DE PÓLIZA | - |
| B | 1 | AE | 30 | RIESGO | Placa del vehículo |
| C | 2 | R | 17 | ASEGURADORA | - |
| D | 3 | - | - | - | Vacío |
| E | 4 | S | 18 | SUBRAMO | Ramo de CELER |
| F | 5 | - | - | SUBRAMO | Puede copiarse a B si B vacío |
| J | 9 | BE | 56 | FECHA INICIO | - |
| K | 10 | W | 22 | FECHA INICIO | F_Inicio |
| L | 11 | X | 23 | FECHA FIN | F_Fin |
| O | 14 | AQ | 42 | PRIMA NETA | Prima sin IVA |
| V | 21 | AB | 27 | MODALIDAD | Forma_Pago |
| W | 22 | AB | 27 | FORMA PAGO | Condicional (ver arriba) |
| X | 23 | AP | 41 | VALOR ASEGURADO | V_Asegurado |
| AB | 27 | C | 2 | DOCUMENTO CLIENTE | Identificacion |
| AC | 28 | A | 0 | TIPO PERSONA | N=Natural, J=Jurídica |
| AD | 29 | B | 1 | NOMBRE TOMADOR | - |
| AE | 30 | C | 2 | DOC TOMADOR | Identificacion |
| AF | 31 | AS | 44 | NOMBRE ASEGURADO | - |
| AG | 32 | AT | 45 | DOC ASEGURADO | Iden_Asegurado |
| AH | 33 | AW | 48 | NOMBRE BENEFICIARIO | - |
| AI | 34 | AX | 49 | DOC BENEFICIARIO | Iden_Beneficiario |

### Comparación (Campos Verificados)

La comparación automática verifica:
1. **Modalidad** (col V): Con equivalencia UNICA=ANUAL
2. **Prima** (col O): Valores numéricos
3. **Fecha Inicio** (col K): Formato fecha
4. **Fecha Fin** (col L): Formato fecha

---

## 📊 Formato de Reportes

### Reporte de Comparación (Excel)

**Pestaña: Coincidencias**
- Pólizas que coinciden en todos los campos
- Verde para validación positiva

**Pestaña: Discrepancias**
- Pólizas con diferencias en campos específicos
- Columnas: Póliza, Campo, Valor MAVISO, Valor CELER
- Amarillo para revisión

**Pestaña: Solo en MAVISO**
- Pólizas que no existen en CELER
- Posibles pólizas antiguas o erróneas

**Pestaña: Solo en CELER**
- Pólizas faltantes en MAVISO
- Usar botón "Agregar Faltantes" para incluirlas

---

## 🛠️ Dependencias

```python
PyQt6==6.7.0              # GUI framework
pandas==2.2.2             # Procesamiento de datos
openpyxl==3.1.2           # Manipulación Excel con formato
xlrd==2.0.1               # Lectura de .xls antiguos
requests==2.31.0          # Comunicación con API
fastapi==0.109.0          # Backend API DIAN
uvicorn==0.27.0           # Servidor ASGI
```

### Instalación
```powershell
pip install -r requirements.txt
```

---

## 🐛 Troubleshooting

### Error: "Puerto 8000 ocupado"
**Solución**: Click en botón "🔄 REINICIAR API" o ejecutar:
```powershell
netstat -ano | findstr :8000
taskkill /F /PID <PID>
```

### Error: "No se encuentra el archivo CELER"
**Solución**: Verificar que el archivo tenga exactamente 3 filas de encabezado para skiprows=3

### Error: "Discrepancias en modalidades"
**Solución**: 
1. Verificar equivalencia UNICA=ANUAL está activa
2. Usar botón "🔧 Corregir Modalidades"

### Error: "NITs sin DV"
**Solución**:
1. Iniciar API DIAN
2. Ejecutar calculadora de DV
3. Verificar que API esté en puerto 8000

### Pólizas no se agregan desde CELER
**Solución**:
1. Verificar normalización de números de póliza (uppercase, trim)
2. Revisar columna U en CELER (índice 20)
3. Check skiprows=3 en lectura

---

## 📝 Notas Técnicas


### Normalización de Pólizas
Todas las pólizas se normalizan para comparación:
```python
poliza_normalizada = str(poliza).strip().upper()
```

### Preservación de Formato Excel
- Usa `openpyxl.load_workbook()` en lugar de pandas para escritura
- Mantiene colores, fuentes, bordes, anchos de columna
- No altera celdas no modificadas

### Threads en GUI
- `ComparadorThread`: Ejecuta comparación asíncrona
- `CalculadorThread`: Procesa cálculo de DV
- `APIThread`: Inicia servidor FastAPI
- `CopiarUnidadesThread`: Copia la columna Unidad de CELER a destino de forma asíncrona

### Auto-Recomparación
Después de cada corrección se ejecuta automáticamente:
1. Recarga archivos
2. Ejecuta comparación
3. Actualiza estadísticas
4. Habilita botón de exportar

---

## 📄 Archivos de Soporte

- `COMPARACION_RAMOS_SUBRAMOS.md` - Mapeo detallado de ramos
- `estilos.py` - Definición de tema dark para PyQt6
- `mapeo_ramos.py` - Lógica de conciliación de ramos

---

Actualizado: 23/12/2025
- ✅ 100% de cobertura en mapeo de ramos y subramos confirmada
- ✅ Documentación completa de equivalencias CELER → MAVISO
- ✅ Todas las aseguradoras con mapeos verificados
- ✅ Copia formato y estilos de Maviso original (colores, fuentes, bordes)
- ✅ Aplica mapeo de columnas según especificación
- ✅ Lógica condicional para FORMA PAGO (MENSUAL→Fraccionado, ANUAL→Contado)
- ✅ Genera archivo en `output/` con timestamp
- ✅ Nueva funcionalidad: Copiar Unidades desde CELER a archivo destino

---
