# DIAN Colombia - Frontend

Interfaz web simple para probar el cálculo del dígito de verificación de NITs colombianos.

## Características

- ✨ Interfaz moderna y responsive
- 🎯 Validación de entrada en tiempo real
- 📱 Compatible con dispositivos móviles
- ⚡ Resultados instantáneos
- 🎨 Diseño limpio y profesional
- 🔌 Conexión automática con el backend

## Uso

### Opción 1: Abrir directamente (sin servidor)

1. Asegúrate de que el backend esté corriendo en `http://localhost:8000`
2. Abre `index.html` directamente en tu navegador

**Nota**: Si hay problemas de CORS, usa la Opción 2.

### Opción 2: Con servidor HTTP simple

```powershell
# Python HTTP Server
cd frontend
python -m http.server 3000

# O con PHP
php -S localhost:3000
```

Luego abre: `http://localhost:3000`

### Opción 3: Con VS Code Live Server

1. Instala la extensión "Live Server" en VS Code
2. Click derecho en `index.html`
3. Selecciona "Open with Live Server"

## Estructura

```
frontend/
├── index.html    # Aplicación web completa (HTML + CSS + JS)
└── README.md     # Este archivo
```

## Funcionalidades

### Validación de Entrada
- Solo acepta números
- Máximo 15 dígitos
- Limpieza automática de caracteres no válidos

### Ejemplos Predefinidos
Click en cualquier ejemplo para probarlo rápidamente:
- `1003618585`
- `890903938`
- `800197268`

### Resultados
Muestra claramente:
- NIT original
- Dígito de verificación (destacado)
- NIT completo
- Formato DIAN (con guión)

## Requisitos

- Backend corriendo en `http://localhost:8000`
- Navegador web moderno (Chrome, Firefox, Edge, Safari)

## Personalización

### Cambiar URL del Backend

Edita la línea 246 en `index.html`:

```javascript
const API_URL = 'http://localhost:8000';  // Cambia aquí
```

### Cambiar Colores

Modifica las variables CSS en el `<style>`:

```css
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
```

## Captura de Pantalla

La aplicación incluye:
- 🎨 Gradiente morado moderno
- 📊 Resultados con formato claro
- ✅ Indicador de estado de la API
- 💡 Ejemplos interactivos

## Solución de Problemas

### Error de CORS

Si ves errores de CORS en la consola del navegador:

1. Verifica que el backend tenga CORS habilitado (ya está configurado en `app.py`)
2. Usa un servidor HTTP local (Opción 2 o 3)

### API no conectada

Asegúrate de que el backend esté corriendo:

```powershell
cd backend
uvicorn app:app --reload
```

## Licencia

MIT License - Ver LICENSE.md en el directorio raíz
