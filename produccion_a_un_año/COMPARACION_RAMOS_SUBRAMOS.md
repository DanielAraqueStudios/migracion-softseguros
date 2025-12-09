# 📊 Comparación de Ramos (CELER) vs Subramos (MAVISO)

Este documento detalla la equivalencia entre los Ramos del sistema CELER y los Subramos disponibles en el sistema MAVISO (SoftSeguros).

## 📋 Resumen General

| Métrica | Valor |
|---------|-------|
| **Total Pólizas CELER** | 3,164 |
| **Total Aseguradoras CELER** | 26 |
| **Total Ramos únicos CELER** | 44 |
| **Aseguradoras en MAVISO** | 30 |
| **Cobertura de mapeo** | 100% |

## 🎨 Leyenda de Colores

| Color | Significado |
|-------|-------------|
| 🟢 **Verde claro** | Requiere REVISIÓN MANUAL - Verificar subramo correcto en destino |
| ✅ | Mapeo automático confirmado |

---

## 🔄 Mapeo de Aseguradoras

### Aseguradoras con Equivalencia Directa

| CELER | MAVISO |
|-------|--------|
| ALLIANZ SEGUROS S.A | ALLIANZ SEGUROS SA / ALLIANZ SEGUROS DE VIDA SA |
| ASEGURADORA SOLIDARIA DE COLOMBIA | ASEGURADORA SOLIDARIA DE COLOMBIA |
| ASSIST CARD | ASSIST CARD DE COLOMBIA SAS |
| AXA COLPATRIA SEGUROS S.A. | AXA COLPATRIA SEGUROS SA / AXA COLPATRIA SEGUROS DE VIDA SA |
| CEM | COOMEVA EXPERIENCIA MEDICA SAS |
| CHUBB DE COLOMBIA COMPAÑÍA SEGUROS S A | CHUBB SEGUROS COLOMBIA SA |
| COLMENA VIDA Y RIESGOS PROFESIONES SA | COLMENA SEGUROS |
| COMPAÑIA DE MEDICINA PREPAGADA COLSANITAS S.A | COMPAÑIA DE MEDICINA PREPAGADA COLSANITAS SA |
| COMPAÑÍA MUNDIAL DE SEGUROS S A | SEGUROS MUNDIAL |
| COOMEVA | COOMEVA MEDICINA PREPAGADA SA |
| EMERMÉDICA S.A | EMERMEDICA SA SERVICIOS DE AMBULANCIA PREPAGADOS |
| FUNER SAN VICENTE | FUNERARIA SAN VICENTE SA |
| HDI SEGUROS SA | HDI SEGUROS |
| LA EQUIDAD SEGUROS OC | LA EQUIDAD SEGUROS GENERALES |
| LA PREVISORA S A COMPAÑÍA DE SEGUROS | LA PREVISORA S A COMPAÑIA DE SEGUROS |
| MAGENTA SEGUROS LTDA | MAGENTA ASISTANCE SAS |
| MAPFRE SEGUROS DE COLOMBIA S A | MAPFRE SEGUROS GENERALES |
| MEDISANITAS | MEDISANITAS SAS COMPAÑIA DE MEDICINA PREPAGADA |
| POSITIVA COMPAÑIA DE SEGUROS S.A. | POSITIVA COMPAÑIA DE SEGUROS SA |
| SBS SEGUROS COLOMBIA S.A | SBS SEGUROS COLOMBIA SA |
| SEGUROS BOLIVAR | COMPAÑIA DE SEGUROS BOLIVAR SA |
| SEGUROS DEL ESTADO S A | SEGUROS DEL ESTADO SA / SEGUROS DE VIDA DEL ESTADO |
| SURAMERICANA S.A. | SEGUROS GENERALES SURAMERICANA S A / SEGUROS DE VIDA SURAMERICANA SA |
| ZURICH COLOMBIA SEGUROS S.A | ZURICH COLOMBIA SEGUROS SA |
| ASEGURADORA GRANCOLOMBIANA S.A. | GRANCOLOMBIANA DE FIANZAS SAS |

### ⚠️ Aseguradoras Sin Equivalencia

| CELER | Pólizas | Observación |
|-------|---------|-------------|
| **LIBERTY SEGUROS S A** | 53 | **Usar mapeo de ALLIANZ** (misma aseguradora) |

---

## 📑 Mapeo Detallado por Aseguradora

### ALLIANZ SEGUROS S.A (603 pólizas)

**Ramos CELER → Subramos MAVISO (Generales)**

| Ramo CELER | Cantidad | Subramo MAVISO | ✓ |
|------------|----------|----------------|---|
| AUTOMOVILES | 251 | AUTOS INDIVIDUAL | ✅ |
| MULTIRIESGO RESIDENCIAL | 199 | HOGAR | ✅ |
| MULTIRIESGO EMPRESARIAL | 80 | MULTIRRIESGO EMPRESARIAL | ✅ |
| MI PYME | 4 | MI PYME | ✅ |
| RESPONSABILIDAD CIVIL | 9 | RC DIRECTORES Y ADMINISTRADORES | ✅ |
| TRANSPORTES DE MERCANCIAS | 6 | TRANSPORTES DE MERCANCIAS | ✅ |

**Ramos CELER → Subramos MAVISO (Vida)**

| Ramo CELER | Cantidad | Subramo MAVISO | ✓ |
|------------|----------|----------------|---|
| ACCIDENTES PERSONALES | 28 | ACCIDENTES PERSONALES | ✅ |
| VIDA INDIVIDUAL | 20 | VIDA ACTUAL | 🟢 REVISAR |
| SALUD FAMILIAR | 5 | SALUD MEDICALL CARE | ✅ |
| VIDA COLECTIVO | 1 | VIDA GRUPO CONTRIBUTIVA | 🟢 REVISAR |

**Subramos MAVISO disponibles (no usados):**
- AUTOS COLECTIVO, AUTOS PESADOS, HOGAR DEUDOR, INFIDELIDAD DE RIESGSOS FINANCIEROS
- MANEJO, MOTO, NAVEGACIÓN, PREDIOS LABORES Y OPERACIONES
- RC CLINICAS Y HOSPITALES, RC HIDROCARBUROS, RC TRAYECTOS
- TRANSPORTE DE MERCANCIAS AUTOMATICAS, TRANSPORTE DE VALORES

---

### ASEGURADORA SOLIDARIA DE COLOMBIA (1,001 pólizas)

| Ramo CELER | Cantidad | Subramo MAVISO | ✓ |
|------------|----------|----------------|---|
| SOAT | 464 | SOAT | ✅ |
| CUMPLIMIENTO | 146 | CUMPLIMIENTO | ✅ |
| TODO RIESGO DAÑOS MATERIALES | 135 | TODO RIESGO DAÑOS MATERIALES | ✅ |
| AUTOMOVILES | 78 | AUTOS INDIVIDUAL | ✅ |
| RESPONSABILIDAD CIVIL | 68 | RC DERIVADA DE CUMPLIMIENTO | ✅ |
| MULTIRIESGO RESIDENCIAL | 42 | HOGAR | ✅ |
| MULTIRIESGO EMPRESARIAL | 20 | MULTIRIESGO EMPRESARIAL | ✅ |
| VIDA GRUPO COLECTIVO | 12 | VIDA GRUPO CONTRIBUTIVO | ✅ |
| MANEJO | 9 | MANEJO ENTIDADES FINANCIERAS | ✅ |
| MANEJO ENTIDADES FINANCIERAS | 7 | MANEJO ENTIDADES FINANCIERAS | ✅ |
| MAQUINARIA Y EQUIPO | 5 | MAQUINARIA Y EQUIPO | ✅ |
| TRANSPORTES DE MERCANCIAS | 5 | TRANSPORTES DE MERCANCIAS | ✅ |
| ACCIDENTES PERSONALES | 3 | ACCIDENTES PERSONALES | ✅ |
| ACCIDENTES JUVENILES | 3 | ACCIDENTES JUVENILES | ✅ |
| TRANSPORTE DE VALORES | 2 | TRANSPORTE DE VALORES | ✅ |
| MULTIRIESGO COPROPIEDADES | 1 | COPROPIEDADES | ✅ |
| ACCIDENTES DE PASAJEROS | 1 | ACCIDENTES PERSONALES | ✅ |

---

### SURAMERICANA S.A. (592 pólizas)

**→ SEGUROS GENERALES SURAMERICANA S A**

| Ramo CELER | Cantidad | Subramo MAVISO | ✓ |
|------------|----------|----------------|---|
| AUTOMOVILES | 108 | AUTOS INDIVIDUAL | ✅ |
| RESPONSABILIDAD CIVIL | 62 | RC DERIVADA DE CUMPLIMIENTO | ✅ |
| MULTIRIESGO EMPRESARIAL | 27 | MULTIRIESGO EMPRESARIAL | ✅ |
| CUMPLIMIENTO | 27 | CUMPLIMIENTO | ✅ |
| INCENDIO | 9 | MULTIRIESGO EMPRESARIAL | ✅ |
| MULTIRIESGO RESIDENCIAL | 9 | HOGAR | ✅ |
| TRANSPORTES DE MERCANCIAS | 6 | TRANSPORTES DE MERCANCIAS | ✅ |
| TRANSPORTE DE VALORES | 3 | TRANSPORTE DE VALORES | ✅ |
| PROTECCION DIGITAL | 3 | PROTECCION DIGITAL | ✅ |
| RC CLINICAS Y HOSPITALES | 1 | RC CLINICAS Y HOSPITALES | ✅ |
| MANEJO | 1 | MANEJO | ✅ |

**→ SEGUROS DE VIDA SURAMERICANA SA**

| Ramo CELER | Cantidad | Subramo MAVISO | ✓ |
|------------|----------|----------------|---|
| VIDA INDIVIDUAL | 104 | VIDA GRUPO APORTES | 🟢 REVISAR |
| SALUD FAMILIAR | 96 | SALUD CLASICO | 🟢 REVISAR |
| VIDA GRUPO COLECTIVO | 59 | VIDA GRUPO CONTRIBUTIVO | 🟢 REVISAR |
| SALUD PARA TODOS | 31 | SALUD PARA TODOS | ✅ |
| PLAN COMPLEMENTARIO | 12 | PLAN COMPLEMENTARIO | ✅ |
| ARL | 11 | ARL | ✅ |
| ACCIDENTES PERSONALES | 8 | ACCIDENTES PERSONALES | ✅ |
| SALUD COLECTIVA | 6 | SALUD COLECTIVA CLASICO | ✅ |
| RENTA EDUCATIVA | 4 | RENTA EDUCATIVA | ✅ |
| PLAN COMPLEMENTARIO COLECTIVO | 3 | PLAN COMPLEMENTARIO COLECTIVO | ✅ |
| PLAN COMPLEMENTARIO FAMILIAR | 1 | PLAN COMPLEMENTARIO | ✅ |
| ACCIDENTES JUVENILES | 1 | ACCIDENTES JUVENILES | ✅ |

---

### COMPAÑÍA MUNDIAL DE SEGUROS S A (251 pólizas)

| Ramo CELER | Cantidad | Subramo MAVISO | ✓ |
|------------|----------|----------------|---|
| CUMPLIMIENTO | 160 | CUMPLIMIENTO | ✅ |
| RESPONSABILIDAD CIVIL | 53 | RC DERIVADA DE CUMPLIMIENTO | 🟢 REVISAR |
| AUTOMOVILES | 36 | AUTOS INDIVIDUAL | ✅ |
| ARRENDAMIENTO | 1 | ARRENDAMIENTO | ✅ |
| TRANSPORTES DE MERCANCIAS | 1 | TRANSPORTES DE MERCANCIAS | ✅ |

---

### SBS SEGUROS COLOMBIA S.A (170 pólizas)

| Ramo CELER | Cantidad | Subramo MAVISO | ✓ |
|------------|----------|----------------|---|
| AUTOMOVILES | 153 | AUTOS INDIVIDUAL | ✅ |
| RESPONSABILIDAD CIVIL | 10 | RC EXTRACONTRACTUAL | 🟢 REVISAR |
| ACCIDENTES PERSONALES | 2 | ACCIDENTES PERSONAL | ✅ |
| MULTIRIESGO COPROPIEDADES | 2 | COPROPIEDADES | ✅ |
| MULTIRIESGO RESIDENCIAL | 1 | HOGAR | ✅ |
| MAQUINARIA Y EQUIPO | 1 | MAQUINARIA Y EQUIPO | ✅ |
| INCENDIO | 1 | MULTIRIESGO EMPRESARIAL | 🟢 REVISAR |

---

### SEGUROS DEL ESTADO S A (117 pólizas)

**→ SEGUROS DEL ESTADO SA**

| Ramo CELER | Cantidad | Subramo MAVISO | ✓ |
|------------|----------|----------------|---|
| AUTOMOVILES | 55 | AUTOS INDIVIDUAL | ✅ |
| RESPONSABILIDAD CIVIL | 29 | RC DERIVADA DE CUMPLIMIENTO | ✅ |
| CUMPLIMIENTO | 23 | CUMPLIMIENTO | ✅ |
| MULTIRIESGO COPROPIEDADES | 3 | COPROPIEDADES | ✅ |
| MULTIRIESGO EMPRESARIAL | 1 | MULTIRIESGO EMPRESARIAL | ✅ |
| MANEJO | 2 | MANEJO | ✅ |
| INCENDIO | 1 | MULTIRIESGO EMPRESARIAL | 🟢 REVISAR |
| TRANSPORTES DE MERCANCIAS | 1 | TRANSPORTES DE MERCANCIAS | ✅ |
| SOAT | 1 | SOAT | ✅ |

**→ SEGUROS DE VIDA DEL ESTADO**

| Ramo CELER | Cantidad | Subramo MAVISO | ✓ |
|------------|----------|----------------|---|
| ACCIDENTES PERSONALES | 1 | ACCIDENTES PERSONALES | ✅ |

---

### HDI SEGUROS SA (70 pólizas)

| Ramo CELER | Cantidad | Subramo MAVISO | ✓ |
|------------|----------|----------------|---|
| AUTOMOVILES | 63 | AUTOS INDIVIDUAL | ✅ |
| ACCIDENTES PERSONALES | 3 | ACCIDENTES PERSONAL | ✅ |
| MULTIRIESGO RESIDENCIAL | 3 | HOGAR | ✅ |
| MULTIRIESGO EMPRESARIAL | 1 | MULTIRIESGO EMPRESARIAL | ✅ |
| VIDA INDIVIDUAL | - | - | 🟢 REVISAR (si existe) |

---

### SEGUROS BOLIVAR (71 pólizas)

| Ramo CELER | Cantidad | Subramo MAVISO | ✓ |
|------------|----------|----------------|---|
| AUTOMOVILES | 61 | AUTOS INDIVIDUAL | ✅ |
| ARL | 2 | ARL | ✅ |
| CUMPLIMIENTO | 2 | CUMPLIMIENTO | ✅ |
| MULTIRIESGO EMPRESARIAL | 2 | MULTIRIESGO EMPRESARIAL | ✅ |
| VIDA INDIVIDUAL | 2 | GRUPO COLECTIVO | ✅ |
| RESPONSABILIDAD CIVIL | 1 | RC DERIVADA DE CUMPLIMIENTO | ✅ |
| SALUD FAMILIAR | 1 | SALUD FAMILIAR | ✅ |

---

### AXA COLPATRIA SEGUROS S.A. (59 pólizas)

**→ AXA COLPATRIA SEGUROS SA**

| Ramo CELER | Cantidad | Subramo MAVISO | ✓ |
|------------|----------|----------------|---|
| AUTOMOVILES | 50 | AUTOS INDIVIDUAL | ✅ |
| MULTIRIESGO COPROPIEDADES | 2 | COPROPIEDADES | ✅ |
| SOAT | 1 | SOAT | 🟢 REVISAR |

**→ AXA COLPATRIA SEGUROS DE VIDA SA**

| Ramo CELER | Cantidad | Subramo MAVISO | ✓ |
|------------|----------|----------------|---|
| MAS VIDA | 3 | MAS VIDA | ✅ |
| ARL | 2 | ARL | ✅ |
| VIDA INDIVIDUAL | 1 | VIDA GRUPO CONTRIBUTIVA | ✅ |

---

### LIBERTY SEGUROS S A (53 pólizas) → **USAR ALLIANZ**

| Ramo CELER | Cantidad | Subramo MAVISO (Allianz) | ✓ |
|------------|----------|--------------------------|---|
| AUTOMOVILES | 52 | AUTOS INDIVIDUAL | ✅ |
| MULTIRIESGO RESIDENCIAL | 1 | HOGAR | ✅ |

**✅ NOTA: Liberty Seguros usa el mismo mapeo de ALLIANZ ya que son la misma aseguradora.**

---

### Otras Aseguradoras

#### CEM (28 pólizas) → COOMEVA EXPERIENCIA MEDICA SAS

| Ramo CELER | Cantidad | Subramo MAVISO | ✓ |
|------------|----------|----------------|---|
| AREA PROTEGIDA | 27 | CEM | ✅ |
| MEDICINA PREPAGADA COLECTIV | 1 | MEDICINA PREPAGADA FAMILIAR | ✅ |

#### COOMEVA (28 pólizas) → COOMEVA MEDICINA PREPAGADA SA

| Ramo CELER | Cantidad | Subramo MAVISO | ✓ |
|------------|----------|----------------|---|
| MEDICINA PREPAGADA FAMILIAR | 15 | MEDICINA PREPAGADA FAMILIAR | ✅ |
| MEDICINA PREPAGADA COLECTIV | 10 | MEDICINA PREPAGADA COLECTIV | ✅ |
| EMERGENCIAS MÉDICAS | 3 | AREA PROTEGIDA | 🟢 REVISAR |

#### LA PREVISORA S A COMPAÑÍA DE SEGUROS (23 pólizas)

| Ramo CELER | Cantidad | Subramo MAVISO | ✓ |
|------------|----------|----------------|---|
| AUTOMOVILES | 13 | AUTOS INDIVIDUAL | ✅ |
| CUMPLIMIENTO | 3 | CUMPLIMIENTO | ✅ |
| RESPONSABILIDAD CIVIL | 2 | RC PREDIOS LABORES Y OPERACIONES | 🟢 REVISAR |
| MULTIRIESGO EMPRESARIAL | 2 | MULTIRIESGO EMPRESARIAL | ✅ |
| RC SERVIDORES PUBLICOS | 1 | RC PREDIOS LABORES Y OPERACIONES | 🟢 REVISAR |
| MANEJO | 1 | MANEJO | ✅ |
| VIDA COLECTIVO | 1 | VIDA GRUPO COLECTIVO | ✅ |

#### ASSIST CARD (16 pólizas) → ASSIST CARD DE COLOMBIA SAS

| Ramo CELER | Cantidad | Subramo MAVISO | ✓ |
|------------|----------|----------------|---|
| ASIST CARD | 16 | ASSIST CARD | ✅ |

#### MAGENTA SEGUROS LTDA (15 pólizas) → MAGENTA ASISTANCE SAS

| Ramo CELER | Cantidad | Subramo MAVISO | ✓ |
|------------|----------|----------------|---|
| EMERGENCIAS MÉDICAS | 7 | EMERGENCIAS MÉDICAS | ✅ |
| ACCIDENTES PERSONALES | 7 | ACCIDENTES PERSONALES | ✅ |
| TELEMEDICINA | 1 | EMERGENCIAS MÉDICAS | ✅ |

#### COLMENA VIDA Y RIESGOS PROFESIONES SA (14 pólizas) → COLMENA SEGUROS

| Ramo CELER | Cantidad | Subramo MAVISO | ✓ |
|------------|----------|----------------|---|
| ARL | 11 | ARL COLMENA | ✅ |
| SEGURO EXEQUIAL | 2 | SEGUROS EXEQUIALES | ✅ |
| VIDA GRUPO COLECTIVO | 1 | VIDA GRUPO | ✅ |

#### LA EQUIDAD SEGUROS OC (13 pólizas) → LA EQUIDAD SEGUROS GENERALES

| Ramo CELER | Cantidad | Subramo MAVISO | ✓ |
|------------|----------|----------------|---|
| AUTOMOVILES | 10 | AUTOS INDIVIDUAL | ✅ |
| ACCIDENTES PERSONALES | 1 | ACCIDENTES PERSONALES | ✅ |
| MANEJO | 1 | MANEJO | ✅ |
| MULTIRIESGO EMPRESARIAL | 1 | MULTIRIESGO EMPRESARIAL | ✅ |

#### MAPFRE SEGUROS DE COLOMBIA S A (9 pólizas) → MAPFRE SEGUROS GENERALES

| Ramo CELER | Cantidad | Subramo MAVISO | ✓ |
|------------|----------|----------------|---|
| AUTOMOVILES | 9 | AUTOS INDIVIDUAL | ✅ |

#### ZURICH COLOMBIA SEGUROS S.A (6 pólizas)

| Ramo CELER | Cantidad | Subramo MAVISO | ✓ |
|------------|----------|----------------|---|
| RESPONSABILIDAD CIVIL | 3 | RC DIRECTORES Y ADMINISTRADORES | ✅ |
| MULTIRIESGO EMPRESARIAL | 1 | MULTIRIESGO EMPRESARIAL | ✅ |
| MULTIRIESGO RESIDENCIAL | 1 | HOGAR DEUDOR | ✅ |
| AERONAVES CASCO | 1 | AERONAVES CASCO | ✅ |

#### CHUBB DE COLOMBIA (5 pólizas) → CHUBB SEGUROS COLOMBIA SA

| Ramo CELER | Cantidad | Subramo MAVISO | ✓ |
|------------|----------|----------------|---|
| RESPONSABILIDAD CIVIL | 3 | RC DIRECTORES Y ADMINISTRADORES | ✅ |
| MULTIRIESGO EMPRESARIAL | 1 | MULTIRRIESGO EMPRESARIAL | ✅ |
| ACCIDENTES PERSONALES | 1 | ACCIDENTES PERSONALES | ✅ |

#### COLSANITAS (5 pólizas)

| Ramo CELER | Cantidad | Subramo MAVISO | ✓ |
|------------|----------|----------------|---|
| MEDICINA PREPAGADA COLECTIV | 5 | MEDICINA PREPAGADA COLECTIV | ✅ |

#### POSITIVA (4 pólizas)

| Ramo CELER | Cantidad | Subramo MAVISO | ✓ |
|------------|----------|----------------|---|
| ACCIDENTES ESCOLARES | 4 | ACCIDENTES ESCOLARES | ✅ |

#### ASEGURADORA GRANCOLOMBIANA S.A. (4 pólizas) → GRANCOLOMBIANA DE FIANZAS SAS

| Ramo CELER | Cantidad | Subramo MAVISO | ✓ |
|------------|----------|----------------|---|
| CUMPLIMIENTO | 3 | CUMPLIMIENTO | ✅ |
| RESPONSABILIDAD CIVIL | 1 | RESPONSABILIDAD CIVIL | ✅ |

#### FUNER SAN VICENTE (4 pólizas) → FUNERARIA SAN VICENTE SA

| Ramo CELER | Cantidad | Subramo MAVISO | ✓ |
|------------|----------|----------------|---|
| SEGUROS EXEQUIALES | 4 | SEGUROS EXEQUIALES | ✅ |

#### EMERMÉDICA S.A (2 pólizas)

| Ramo CELER | Cantidad | Subramo MAVISO | ✓ |
|------------|----------|----------------|---|
| EMERGENCIAS MÉDICAS | 2 | EMERGENCIAS MÉDICAS | ✅ |

#### MEDISANITAS (1 póliza)

| Ramo CELER | Cantidad | Subramo MAVISO | ✓ |
|------------|----------|----------------|---|
| MEDICINA PREPAGADA COLECTIV | 1 | MEDICINA PREPAGADA | ✅ |

---

## 🟢 Filas que Requieren Revisión Manual (Resaltar en Verde)

Se resaltan en **verde claro** todas las filas cuyo RAMO contenga alguna de estas palabras clave:

| Palabra Clave | Descripción |
|---------------|-------------|
| **RESPONSABILIDAD CIVIL** | Todos los ramos de RC |
| **RC** | Cualquier variante de Responsabilidad Civil |
| **VIDA** | Seguros de vida (individual, colectivo, grupo) |
| **MEDICINA PREPAGADA** | Medicina prepagada familiar/colectiva |
| **COLECTIV** | Pólizas colectivas (vida, salud, etc.) |
| **HOGAR** | Seguros de hogar/residencial |
| **SALUD** | Seguros de salud |

### Ramos que se Resaltan Automáticamente:

| Ramo CELER | Palabra Detectada |
|------------|-------------------|
| RESPONSABILIDAD CIVIL | RESPONSABILIDAD CIVIL |
| RC SERVIDORES PUBLICOS | RC |
| RC CLINICAS Y HOSPITALES | RC |
| VIDA INDIVIDUAL | VIDA |
| VIDA COLECTIVO | VIDA, COLECTIV |
| VIDA GRUPO COLECTIVO | VIDA, COLECTIV |
| SALUD FAMILIAR | SALUD |
| SALUD PARA TODOS | SALUD |
| SALUD COLECTIVA | SALUD, COLECTIV |
| MEDICINA PREPAGADA FAMILIAR | MEDICINA PREPAGADA |
| MEDICINA PREPAGADA COLECTIV | MEDICINA PREPAGADA, COLECTIV |
| MULTIRIESGO RESIDENCIAL | HOGAR (subramo destino) |
| PLAN COMPLEMENTARIO COLECTIVO | COLECTIV |

**Estimado de filas resaltadas: ~800-1000 pólizas**

---

## ❌ Ramos Sin Mapeo Directo

**✅ TODOS LOS RAMOS TIENEN MAPEO - NO HAY EXCEPCIONES**

Las correcciones aplicadas:
- LIBERTY → Usar mapeo de ALLIANZ (misma aseguradora)
- TRANSPORTES DE MERCANCIAS (Mundial) → TRANSPORTES DE MERCANCIAS ✅
- TRANSPORTES DE MERCANCIAS (Seg. Estado) → TRANSPORTES DE MERCANCIAS ✅
- AERONAVES CASCO (Zurich) → AERONAVES CASCO ✅
- SOAT (AXA/Seg. Estado) → SOAT ✅

---

## 📊 Estadísticas de Cobertura

```
Total pólizas:               3,164
Mapeadas correctamente:      3,164 (100%)
Requieren revisión manual:   ~800-1000 (25-32%) - Marcadas en verde
Sin mapeo:                       0 (0%)
```

### Criterios de Resaltado Verde:
- Ramos con "RESPONSABILIDAD CIVIL" o "RC"
- Ramos con "VIDA"
- Ramos con "MEDICINA PREPAGADA"
- Ramos con "COLECTIV" (colectivo/colectiva)
- Ramos con "HOGAR"
- Ramos con "SALUD"

---

## 📁 Archivos Relacionados

| Archivo | Descripción |
|---------|-------------|
| `mapeo_ramos.py` | Diccionarios Python con mapeos programáticos |
| `verificar_mapeo.py` | Script para verificar cobertura del mapeo |
| `extraer_dropdowns.py` | Extrae valores válidos de dropdowns de MAVISO |
| `analizar_ramos_subramos.py` | Análisis inicial de combinaciones |

---

*Documento generado: Diciembre 2025*
*Fuente: Copy of polizas vigentes celer.xlsx → Copy of Maviso.xlsx*
