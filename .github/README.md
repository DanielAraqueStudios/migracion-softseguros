# GitHub Configuration

Configuraciones específicas para el repositorio GitHub.

## 📋 Descripción

Esta carpeta contiene configuraciones para:
- Instrucciones para GitHub Copilot
- Workflows de GitHub Actions
- Templates de issues y PRs
- Configuraciones de branch protection

## 📁 Archivos

### Copilot Instructions
- `copilot-instructions.md` - Guía específica para GitHub Copilot en este proyecto

### Workflows (si existen)
- `ci.yml` - Continuous Integration
- `cd.yml` - Continuous Deployment
- `tests.yml` - Ejecución automática de tests

### Templates
- `ISSUE_TEMPLATE/` - Templates para reportar issues
- `PULL_REQUEST_TEMPLATE.md` - Template para pull requests

## 🚀 Uso

Los archivos en `.github/` son automáticamente reconocidos por GitHub:
- **Copilot**: Lee las instrucciones para contextualizar sugerencias
- **Actions**: Se ejecutan automáticamente en eventos del repo
- **Templates**: Aparecen cuando se crea un issue/PR

## 📊 Contenido Actual

### Copilot Instructions
Incluye información sobre:
- Arquitectura del proyecto
- Tecnologías utilizadas
- Patrones de código
- Reglas de negocio específicas

## 🤝 Mantenimiento

- Actualizar copilot-instructions.md con cambios importantes
- Revisar workflows periódicamente
- Mantener templates actualizados