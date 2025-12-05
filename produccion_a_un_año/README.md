# Producción a Un Año - SoftSeguros

## Descripción
Módulo para el procesamiento y migración de pólizas con vigencia de un año, trasladando datos desde CELER hacia la plantilla Maviso.

## Estructura de Carpetas

```
produccion_a_un_año/
├── Copy of Maviso.xlsx                    # Plantilla destino (estructura y formato)
├── Copy of polizas vigentes celer.xlsx    # Archivo fuente CELER
├── llenar_maviso.py                       # Script de migración
├── README.md                              # Esta documentación
└── output/                                # Carpeta de salida
    └── Maviso_llenado_YYYYMMDD_HHMMSS.xlsx  # Archivo generado
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

## Uso

```powershell
cd produccion_a_un_año
python llenar_maviso.py
```

## Características del Script

- ✅ Lee archivo CELER con skiprows=3
- ✅ Copia formato y estilos de Maviso original (colores, fuentes, bordes)
- ✅ Aplica mapeo de columnas según especificación
- ✅ Lógica condicional para FORMA PAGO (MENSUAL→Fraccionado, ANUAL→Contado)
- ✅ Genera archivo en `output/` con timestamp

---

Actualizado: 05/12/2025
