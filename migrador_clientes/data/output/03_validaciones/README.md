# ✅ Validaciones de Calidad

Esta carpeta contiene los reportes de validación de coincidencia entre bases.

## Archivos

### VALIDACION_NOMBRES_DOCUMENTOS_YYYYMMDD_HHMMSS.xlsx
**Descripción:** Validación de coincidencia nombre-documento entre SOFTSEGUROS y CELER.

**Hojas:**
- **Resumen**: Estadísticas de coincidencias
- **Inconsistencias**: Casos donde los nombres no coinciden

**Algoritmo:**
- Normalización de texto (mayúsculas, sin tildes)
- Cálculo de similitud (SequenceMatcher)
- Umbral: 85% de similitud

**Resultados:**
- 99.7% de coincidencia exacta
- 1 inconsistencia detectada (Ferney Antonio)
- Código de colores:
  - 🔴 Rojo: < 30% similitud (crítico)
  - 🟠 Naranja: 30-50% (significativo)
  - 🟡 Amarillo: 50-85% (menor)
