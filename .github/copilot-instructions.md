# Copilot Instructions - Migración SoftSeguros

## Project Overview
Python-based data migration system for SoftSeguros insurance data, specializing in Excel file processing, transformation, and automated report generation. Focus on robust data extraction from legacy Excel formats, validation, and loading into target systems.

## Technology Stack
- **Core**: Python 3.x with pandas, openpyxl, xlsxwriter, xlrd, xlwings
- **Data Processing**: pandas DataFrames for ETL operations
- **Excel Operations**: openpyxl for advanced formatting, pandas for data manipulation
- **Validation**: Custom validators with detailed logging

## Language & Localization
- **Business Terms**: Spanish domain terminology (`poliza`, `asegurado`, `prima`, `siniestro`)
- **Code**: Spanish variable names for domain concepts, English for technical operations
- **Comments**: Spanish for business logic explanations, clear docstrings in Spanish

## Project Structure
```
/src
  /extractors        # Excel file readers (.xlsx, .xls, .xlsm)
  /transformers      # pandas-based data transformation pipelines
  /validators        # Data quality checks and validation rules
  /loaders          # Export to target formats (DB, Excel, CSV)
  /formatters       # openpyxl styling and report generation
  /utils            # Shared helpers (file handling, logging)
/data
  /input            # Source Excel files (gitignored)
  /output           # Generated reports and exports (gitignored)
  /samples          # Sample/test data files (committed)
  /templates        # Excel templates for report generation
/config             # Connection configs, field mappings (JSON/YAML)
/logs               # Execution logs (gitignored)
/docs               # Migration specs, field mappings, data dictionaries
/tests              # Unit tests and integration tests
requirements.txt    # Python dependencies
.env.example        # Environment variable template
```

## Development Guidelines

### Excel Processing Pattern
Standard workflow for all migration scripts:
```python
# 1. EXTRACT - Read Excel with proper engine selection
df = pd.read_excel('polizas.xlsx', engine='openpyxl')  # .xlsx
df = pd.read_excel('legacy.xls', engine='xlrd')        # .xls

# 2. TRANSFORM - Apply business rules using pandas
df_limpio = df.dropna(subset=['numero_poliza'])
df_limpio['prima'] = pd.to_numeric(df_limpio['prima'], errors='coerce')

# 3. VALIDATE - Check data quality
errores = df_limpio[df_limpio['prima'].isna()]
log_errores(errores, 'primas_invalidas.xlsx')

# 4. LOAD - Export with formatting
with pd.ExcelWriter('salida.xlsx', engine='openpyxl') as writer:
    df_limpio.to_excel(writer, sheet_name='Datos', index=False)
    aplicar_formato(writer.book['Datos'])

# 5. LOG - Record execution details
logger.info(f"Procesados: {len(df)}, Válidos: {len(df_limpio)}, Errores: {len(errores)}")
```

### Library Selection Guide
- **pandas**: Bulk data reading, filtering, aggregation, transformations
- **openpyxl**: Cell formatting, styling, charts, formulas (.xlsx only)
- **xlrd**: Reading legacy .xls files (pre-2007 Excel)
- **xlsxwriter**: Write-only performance for large exports with formatting
- **xlwings**: COM automation for Excel interaction (Windows only, use sparingly)

### Data Handling Standards
```python
# Always use context managers for file operations
with pd.ExcelWriter('output.xlsx', engine='openpyxl') as writer:
    df.to_excel(writer, sheet_name='Datos')

# Handle missing values explicitly
df['asegurado'] = df['asegurado'].fillna('NO ESPECIFICADO')
df['prima'] = df['prima'].fillna(0)

# Preserve data types when reading
dtype_map = {'numero_poliza': str, 'cedula': str}
df = pd.read_excel('file.xlsx', dtype=dtype_map)

# Keep audit trail - never modify source files
df['_archivo_origen'] = 'polizas_2024.xlsx'
df['_fecha_proceso'] = datetime.now()
```

### Error Handling
```python
# Wrap file operations with proper exception handling
try:
    df = pd.read_excel(archivo_entrada, sheet_name='Polizas')
except FileNotFoundError:
    logger.error(f"Archivo no encontrado: {archivo_entrada}")
    return
except ValueError as e:
    logger.error(f"Error en estructura de Excel: {e}")
    return

# Continue processing valid records, log failures
for idx, row in df.iterrows():
    try:
        procesar_poliza(row)
    except ValidationError as e:
        errores.append({'fila': idx, 'error': str(e), 'datos': row.to_dict()})
        continue

# Export errors to separate Excel for review
if errores:
    df_errores = pd.DataFrame(errores)
    df_errores.to_excel(f'errores_{timestamp}.xlsx', index=False)
```

### Excel Formatting Standards
```python
# Use openpyxl for professional output styling
from openpyxl.styles import Font, PatternFill, Border, Side, Alignment

def aplicar_formato_header(worksheet):
    """Aplica formato estándar a encabezados"""
    header_fill = PatternFill(start_color="366092", end_color="366092", fill_type="solid")
    header_font = Font(bold=True, color="FFFFFF", size=11)
    
    for cell in worksheet[1]:
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = Alignment(horizontal="center", vertical="center")
    
    # Auto-ajustar ancho de columnas
    for column in worksheet.columns:
        max_length = 0
        column_letter = column[0].column_letter
        for cell in column:
            if cell.value:
                max_length = max(max_length, len(str(cell.value)))
        worksheet.column_dimensions[column_letter].width = min(max_length + 2, 50)

# Conditional formatting for amounts
from openpyxl.formatting.rule import CellIsRule

def resaltar_primas_altas(worksheet, columna='E', umbral=10000):
    """Resalta primas superiores al umbral en amarillo"""
    yellow_fill = PatternFill(start_color="FFFF00", end_color="FFFF00", fill_type="solid")
    worksheet.conditional_formatting.add(
        f'{columna}2:{columna}1000',
        CellIsRule(operator='greaterThan', formula=[umbral], fill=yellow_fill)
    )
```

### Configuration Management
```python
# config/config.yaml
rutas:
  entrada: "data/input"
  salida: "data/output"
  logs: "logs"
  templates: "data/templates"

formatos:
  fecha: "%d/%m/%Y"
  moneda: "es_CO"  # Colombia locale for currency

validaciones:
  numero_poliza_regex: "^[A-Z]{2}\\d{6}$"
  prima_min: 0
  prima_max: 1000000000

# Load in scripts with pyyaml
import yaml
with open('config/config.yaml') as f:
    config = yaml.safe_load(f)
```

## Insurance Domain Terms
Common terms you'll encounter:
- `poliza` - insurance policy
- `asegurado` - insured person/entity
- `prima` - premium
- `siniestro` - claim/incident
- `cobertura` - coverage
- `endoso` - endorsement
- `vigencia` - validity period

## Commands & Workflows
(To be documented as scripts are developed)

## Testing Strategy
- Test with small data samples before full migration
- Validate record counts match between source and target
- Perform spot checks on critical fields (amounts, dates, IDs)
- Test rollback procedures

## Git Workflow
- Commit frequently with descriptive Spanish messages
- Create branches for each migration phase or entity type
- Tag successful migration milestones
