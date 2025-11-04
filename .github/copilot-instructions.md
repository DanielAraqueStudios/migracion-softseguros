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

## Project Structure (To Be Established)
As this project develops, maintain this structure:
```
/src                 # Source code for migration scripts
  /extractors        # Data extraction from legacy system
  /transformers      # Data transformation logic
  /loaders          # Data loading to new system
/data               # Sample and test data files
/config             # Configuration files for connections and mappings
/docs               # Migration documentation and field mappings
/tests              # Test scripts and validation
```

## Development Guidelines

### Migration Pattern
When building migration scripts:
1. **Extract** - Pull data from source system with error handling
2. **Transform** - Apply business rules and data mapping
3. **Validate** - Check data integrity before loading
4. **Load** - Insert into target system with transaction control
5. **Log** - Record all operations with timestamps and row counts

### Data Handling
- Always validate data before transformation
- Log discrepancies and data quality issues separately
- Keep audit trail of all migrations (source record → target record mapping)
- Handle null values and missing data explicitly
- Preserve original data in staging tables before transformation

### Error Handling
- Wrap database operations in transactions
- Implement retry logic for transient failures
- Create detailed error logs with: timestamp, operation, record ID, error message
- Continue processing valid records when individual records fail

### Configuration
- Store connection strings and credentials in `.env` files (never commit)
- Use separate configs for development, testing, and production environments
- Document all configuration parameters with examples

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
