# Procesamiento de Pólizas

Scripts para clasificación automática de entidades y ajuste de documentos en archivos de pólizas.

## 📋 Descripción

Esta carpeta contiene el procesamiento principal de archivos de pólizas, incluyendo:
- Clasificación automática PERSONA vs EMPRESA basada en nombres
- Ajuste automático de documentos NIT/CC
- Cálculo de dígito de verificación DIAN
- Procesamiento de múltiples columnas de documentos

## 📁 Archivos

### Scripts Principales
- `clasificar_tomador.py` - Clasifica entidades y ajusta documentos en columnas AB, AD y Z

### Archivos de Entrada
- `Plantilla POLIZAS Actulizada.xlsx` - Archivo principal de pólizas a procesar

### Archivos de Salida
- `Plantilla POLIZAS_Clasificada_v4.xlsx` - Archivo procesado con documentos ajustados
- `clasificacion_tomador.log` - Log detallado de todos los cambios realizados

## 🚀 Uso

```bash
# Procesar archivo de pólizas completo
python clasificar_tomador.py
```

## 📊 Funcionalidades

### Clasificación Automática
- **PERSONA**: Nombres propios de 2-4 palabras sin términos empresariales
- **EMPRESA**: Contiene términos como COOPERATIVA, S.A., LTDA., FONDO, etc.

### Ajuste de Documentos
- **PERSONA**: Quita dígito de verificación si existe
- **EMPRESA**: Calcula y agrega dígito de verificación si falta

### Columnas Procesadas
- **AB (DOCUMENTO DEL TOMADOR)**: Basado en AA (NOMBRE DEL TOMADOR)
- **AD (DOCUMENTO DEL ASEGURADO)**: Basado en AC (NOMBRE DEL ASEGURADO)
- **Z (DOCUMENTO DEL CLIENTE)**: Basado en AA (mismo tipo que tomador)

## 🔧 Algoritmo de Clasificación

### Términos Empresariales
```
COOPERATIVA, FONDO, S.A., LTDA., SOCIEDAD, ASOCIADOS,
GRUPO, CORPORACION, DEPARTAMENTO, EMPLEADOS, SENA,
AFROAMERICANA, PARROQUIAL, COLEGIO, INSTITUTO, VICARIAL
```

### Reglas de Decisión
1. Si contiene términos empresariales → EMPRESA
2. Si tiene más de 4 palabras → EMPRESA
3. Si tiene 2-4 palabras → PERSONA
4. Si es mayúsculas con >2 palabras → EMPRESA

## 📝 Logs

Archivo `clasificacion_tomador.log` incluye:
- Clasificación por fila y columna
- Cambios realizados en documentos
- Estadísticas de procesamiento

## 🔗 Dependencias

- Requiere pandas, openpyxl, re, logging
- Acceso al archivo fuente Excel
- Función `calcular_dv()` integrada

## ⚠️ Notas Importantes

- Mantener archivos Excel cerrados durante ejecución
- Revisar logs para validar cambios
- Los documentos float (.0) se limpian automáticamente