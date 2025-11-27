# Código Fuente Principal

Scripts y módulos principales del sistema de migración.

## 📋 Descripción

Esta carpeta contiene el código fuente organizado por funcionalidad:
- Extractors: Lectores de datos desde diferentes fuentes
- Transformers: Scripts de transformación y limpieza
- Validators: Validaciones de calidad de datos
- Loaders: Exportadores a diferentes formatos
- Utils: Utilidades compartidas

## 📁 Estructura

```
src/
├── extractors/     # Lectores de archivos Excel, JSON, etc.
├── transformers/   # Scripts de transformación de datos
├── validators/     # Validaciones de formato y calidad
├── loaders/        # Exportadores Excel, CSV, DB
└── utils/          # Funciones auxiliares compartidas
```

## 🚀 Uso

Los scripts en `src/` son módulos reutilizables que pueden ser importados por los scripts principales en otras carpetas.

## 📊 Funcionalidades

### Extractors
- Lectura de archivos Excel (.xlsx, .xls)
- Parsing de archivos JSON
- Conexión a bases de datos

### Transformers
- Limpieza de datos
- Normalización de formatos
- Cálculos automáticos (NIT, fechas)

### Validators
- Validación de NIT/CC
- Chequeo de formatos
- Reglas de negocio

### Loaders
- Exportación Excel con formato
- Generación CSV
- Inserción en bases de datos

### Utils
- Funciones de logging
- Helpers de string
- Utilidades de fecha
