#!/usr/bin/env python3
"""
Script para iniciar la API DIAN
Ejecutar: python run_api.py
"""
import subprocess
import sys
import os

def main():
    backend_dir = os.path.join(os.path.dirname(__file__), 'backend')
    venv_python = os.path.join(backend_dir, 'venv', 'Scripts', 'python.exe')

    print('🚀 Iniciando API DIAN...')
    print('📍 URL: http://127.0.0.1:8000')
    print('📋 Documentación: http://127.0.0.1:8000/docs')
    print('🔄 Presiona Ctrl+C para detener')
    print()

    try:
        subprocess.run([
            venv_python, '-m', 'uvicorn', 'app:app',
            '--host', '127.0.0.1', '--port', '8000', '--reload'
        ], cwd=backend_dir, check=True)
    except KeyboardInterrupt:
        print('\n🛑 API detenida')
    except subprocess.CalledProcessError as e:
        print(f'❌ Error al iniciar API: {e}')

if __name__ == '__main__':
    main()