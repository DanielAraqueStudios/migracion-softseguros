#!/usr/bin/env python3
"""
Script para iniciar y probar la API DIAN
"""
import subprocess
import sys
import time
import requests
import os

def main():
    backend_dir = os.path.join(os.path.dirname(__file__), 'backend')
    venv_python = os.path.join(backend_dir, 'venv', 'Scripts', 'python.exe')

    print('🚀 Iniciando API DIAN...')

    # Iniciar servidor
    server = subprocess.Popen([
        venv_python, '-m', 'uvicorn', 'app:app',
        '--host', '127.0.0.1', '--port', '8000', '--log-level', 'info'
    ], cwd=backend_dir, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Esperar a que inicie
    time.sleep(3)

    try:
        # Probar health check
        response = requests.get('http://127.0.0.1:8000/health', timeout=5)
        print('✅ API conectada!')
        print(f'Status: {response.status_code}')
        print(f'Response: {response.json()}')

        # Probar cálculo
        calc_response = requests.post('http://127.0.0.1:8000/calcular',
                                    json={'nit': '1003618585'}, timeout=5)
        print(f'\n✅ Endpoint /calcular funciona!')
        print(f'Status: {calc_response.status_code}')
        data = calc_response.json()
        print(f'NIT: {data["nit_original"]}')
        print(f'Dígito: {data["digito_verificacion"]}')
        print(f'Completo: {data["nit_completo"]}')

        print('\n🎉 ¡API DIAN funcionando correctamente!')
        print('Ahora puedes ejecutar: python test_dian_algorithm.py')

    except requests.exceptions.RequestException as e:
        print(f'❌ Error de conexión: {e}')
        print('\nLogs del servidor:')
        stdout, stderr = server.communicate()
        print('STDOUT:', stdout.decode() if stdout else 'None')
        print('STDERR:', stderr.decode() if stderr else 'None')

    finally:
        print('\n🛑 Deteniendo servidor...')
        server.terminate()
        server.wait()

if __name__ == '__main__':
    main()