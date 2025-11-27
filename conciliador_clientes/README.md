# Conciliador de Clientes - Migración SoftSeguros

Este módulo automatiza la conciliación y migración de datos de clientes entre sistemas de seguros, con enfoque en validación, limpieza y generación de plantillas para importación.

## ¿Cómo funciona?

1. **Input principal:**
   - `data_celer/InformedePersonas CELER.xlsx`: Base de datos de personas (CELER).
   - `clientes_activos/diferencias_tomador_asegurado.json`: Registros a comparar (campo `Iden_Beneficiario`).

2. **Comparación y filtrado:**
   - Se buscan coincidencias por número de documento (`Identificacion`) y por nombre (`Nombre_Beneficiario`).
   - Solo se exportan los datos que aparecen en ambos archivos.

3. **Transformación y mapeo:**
   - Nombres y apellidos se separan y se asignan a columnas A y B de la plantilla.
   - Tipo de documento se normaliza: "CC", "C.C", "IND" → "Cédula"; "NIT" → "NIT"; "PSP", "CE" → "Cédula de Extranjería".
   - Teléfonos móviles y tipos se extraen de columnas personales/laborales y se asignan en la plantilla, permitiendo múltiples valores.
   - Email y tipo de email se extraen de columnas personales/laborales y se asignan en la plantilla.
   - Dirección principal se toma de la columna S del informe.
   - Si el tipo de documento es NIT, se calcula y agrega el dígito de verificación en la columna Z.

4. **Exportación:**
   - El archivo final se genera en `plantilla/PLANTILLA_COINCIDEN.xlsx` listo para importación o revisión.

## Scripts principales
- `exportar_plantilla_coincidentes.py`: Genera la plantilla con todos los mapeos y validaciones.
- `comparar_identificaciones_informe_json.py`: Estadísticas y comparación por identificaciones.
- `llenar_plantilla_nombres_apellidos.py`: Ejemplo de llenado básico de plantilla.

## Personalización
- Puedes modificar los scripts para agregar más campos, cambiar reglas de mapeo o ajustar la lógica de validación según tus necesidades.

## Recomendaciones
- Mantén los archivos Excel cerrados antes de ejecutar los scripts para evitar errores de escritura.
- Revisa los logs generados para validar el proceso y depurar posibles inconsistencias.

---

Para más detalles, consulta el README general en la raíz del proyecto.
