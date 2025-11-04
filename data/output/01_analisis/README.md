# 📊 Análisis Inicial

Esta carpeta contiene los reportes de análisis inicial de la calidad de datos.

## Archivos

### analisis_ids_YYYYMMDD_HHMMSS.xlsx
**Descripción:** Análisis completo de números de identificación en ambos archivos.

**Hojas:**
- **Resumen**: Estadísticas generales de IDs
- **Duplicados_SoftSeguros**: IDs duplicados encontrados
- **Duplicados_Celer**: IDs duplicados en CELER (múltiples pólizas)
- **Problemas_Formato**: NITs con formato incorrecto
- **Sin_ID_SoftSeguros**: Registros sin identificación

**Hallazgos clave:**
- 1 NIT duplicado detectado
- 217 NITs sin formato correcto (sin guión verificador)
- 99.3% de coincidencia entre bases
