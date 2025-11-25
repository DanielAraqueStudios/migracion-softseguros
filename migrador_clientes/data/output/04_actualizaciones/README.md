# 🔄 Actualizaciones desde CELER

Esta carpeta contiene los archivos con datos actualizados desde CELER.

## Archivos

### CLIENTES_SOFTSEGUROS_ACTUALIZADO_YYYYMMDD_HHMMSS.xlsx
**Descripción:** Archivo SOFTSEGUROS enriquecido con datos de CELER.

**Campos actualizados:**
- ✅ Nombres y apellidos (corregidos)
- ✅ Fechas de nacimiento (866 actualizaciones)
- ✅ Teléfonos móviles (1,019 actualizaciones)
- ✅ Emails (1,005 actualizaciones)
- ✅ Direcciones (61 actualizaciones)

**Total de cambios:** 2,957 actualizaciones en 1,082 registros

**Criterio de actualización:**
- CELER es la fuente de verdad
- Si CELER tiene dato y SOFTSEGUROS no, se actualiza
- Si ambos tienen datos diferentes, prevalece CELER
- Si CELER está vacío, se mantiene SOFTSEGUROS

### REPORTE_ACTUALIZACIONES_YYYYMMDD_HHMMSS.xlsx
**Descripción:** Detalle completo de todas las actualizaciones realizadas.

**Hojas:**
- **Resumen**: Estadísticas por campo actualizado
- **Detalle_Cambios**: Los 2,957 cambios con valor anterior y nuevo

**Incluye:**
- ID del cliente
- Nombre del cliente
- Campo modificado
- Valor anterior (SOFTSEGUROS)
- Valor nuevo (CELER)
