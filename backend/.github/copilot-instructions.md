# DIAN Colombia - Copilot Instructions

## Project Overview
PHP library for calculating verification digits (dígito de verificación) for Colombian tax identification numbers (NIT/Cédula) according to DIAN regulations. Single-purpose utility following DIAN's official algorithm.

## Architecture Pattern

### Static Facade + Trait Composition
- **Entry Point**: `DIAN::digitoVerificacion($nit)` static method in `BaseDian.php`
- **Core Logic**: `DIAN` class extends `BaseDian`, composes `Utilities` and `Validacion` traits
- **Data Flow**: Static call → Constructor with NIT → `digito()` method → Algorithm execution

```php
// Usage pattern - always static entry point
$digito = DIAN::digitoVerificacion(1003618585); // Returns int verification digit
```

### Trait Separation Strategy
- **`Utilities`**: Pure calculation logic (factors, length, digit extraction, residue)
- **`Validacion`**: Input validation (numeric check only)
- **Purpose**: Logical separation without inheritance complexity

## DIAN Algorithm Implementation

### Weighting Factors (Key Pattern)
The `factores()` method in `Utilities` trait uses **position-indexed array** (1-15), not zero-indexed:
```php
[1 => 3, 2 => 7, 3 => 13, 4 => 17, ...] // Positions 1-15
```

### Calculation Flow in `digito()` method:
1. Validate input with `inputValido()` (returns false on invalid, despite int return type - known bug)
2. Multiply each NIT digit by corresponding factor: `$digito * $factores[$longitudNit - $i]`
3. Sum all weighted values
4. Calculate residue: `($suma % 11)`, then apply transformation: `(residuo > 1) ? (11 - residuo) : residuo`

**Critical**: Loop iterates from position 0, but accesses factors using `$longitudNit - $i` to map correctly.

## Code Conventions

### Naming (Spanish)
- Variables/methods use Spanish: `$cedula`, `digito()`, `factores()`, `longitud()`
- Comments and documentation in Spanish
- Maintain this convention - do NOT translate to English

### Type Handling
- Constructor accepts `int $cedula` only
- Return type `int` declared on `digito()`, but returns `false` on validation failure (inconsistency)
- When adding validation, return `null` or throw exception instead of `false`

### Namespace Structure
`Rmunate\DianColombia\` root with subdirectories:
- `Bases\` - Abstract base classes
- `Traits\` - Reusable trait components

## Development Workflow

### Testing
No test suite currently exists. When adding tests:
- Use PHPUnit (not configured yet)
- Test cases should include: valid NITs (various lengths), non-numeric input, edge cases (single digit, max length 15)
- Expected verification digits from official DIAN examples

### Dependencies
- PHP ^7.4|^8.0 (composer.json requirement)
- PSR-4 autoloading: `Rmunate\\DianColombia\\` → `src/`
- No external dependencies

### Installation & Usage
```bash
composer require rmunate/dian-colombia
```

## Extension Points

### Adding New Validation Rules
Extend `Validacion` trait or create new trait. Current validation only checks `is_numeric()`.

### Supporting Additional DIAN Calculations
Follow the static facade pattern in `BaseDian`. Create new methods that instantiate and call internal logic.

### Error Handling
Currently returns `false` on invalid input. Consider throwing custom exceptions for better error reporting:
```php
throw new \InvalidArgumentException("El NIT debe ser numérico");
```

## Known Issues
- `digito()` returns `false` despite `int` return type declaration (line 36-39 in DIAN.php)
- No validation for NIT length constraints (DIAN NITs typically 9-10 digits)
