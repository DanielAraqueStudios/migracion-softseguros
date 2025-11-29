#!/usr/bin/env python3
"""
Script de prueba para validar el algoritmo de cálculo de dígito verificador DIAN
usando la API REST del repositorio https://github.com/DanielAraqueStudios/DIAN
"""

import sys
import os
import requests
import json

# Configuración de la API
API_URL = "http://localhost:8000"
CALCULAR_ENDPOINT = f"{API_URL}/calcular"

def verificar_conexion_api():
    """Verifica que la API esté corriendo"""
    try:
        response = requests.get(f"{API_URL}/health", timeout=5)
        if response.status_code == 200:
            print("API conectada correctamente")
            return True
        else:
            print(f"API responde con status {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("No se puede conectar a la API")
        print("Asegúrate de que el servidor esté corriendo:")
        print("  cd backend && python -m uvicorn app:app --host 127.0.0.1 --port 8000")
        return False
    except Exception as e:
        print(f"Error al verificar conexión: {e}")
        return False

def calcular_digito_api(nit_sin_dv):
    """Calcula el dígito verificador usando la API"""
    try:
        response = requests.post(CALCULAR_ENDPOINT, json={"nit": nit_sin_dv}, timeout=10)
        if response.status_code == 200:
            data = response.json()
            return data["digito_verificacion"]
        else:
            print(f"Error en API: {response.status_code} - {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error de conexión con API: {e}")
        return None

def probar_algoritmo_dian():
    """Prueba el algoritmo de cálculo de dígito verificador"""

    # Verificar conexión primero
    if not verificar_conexion_api():
        print("No se puede continuar sin conexión a la API")
        return False

    # Casos de prueba conocidos
    nits_prueba = [
        ("1003618585", 2),  # Caso de ejemplo - dígito correcto es 2
        ("890903938", 8),   # NIT empresarial - dígito correcto es 8
        ("800197268", 4),   # Otro NIT común - dígito correcto es 4
        ("123456789", 6),   # Caso de prueba - dígito correcto es 6
    ]

    print("\n=== PRUEBA ALGORITMO DIAN ===\n")

    todos_correctos = True

    for nit_base, dv_esperado in nits_prueba:
        dv_calculado = calcular_digito_api(nit_base)

        if dv_calculado == dv_esperado:
            print(f"PASS | {nit_base} -> {dv_calculado} (correcto)")
        else:
            print(f"FAIL | {nit_base} -> {dv_calculado} (esperado: {dv_esperado})")
            todos_correctos = False

    print(f"\n{'TODOS LOS TESTS PASARON' if todos_correctos else 'ALGUNOS TESTS FALLARON'}")

    return todos_correctos

def probar_correccion_formato():
    """Prueba la corrección de formato de NITs usando la API"""

    # Casos de prueba
    casos_prueba = [
        # (NIT original, tipo, esperado, debe_cambiar)
        ("900310074", "NIT", "90031007-1", True),    # DV incorrecto (4->1)
        ("90031007-4", "NIT", "90031007-1", True),   # DV incorrecto
        ("90031007-1", "NIT", "90031007-1", False),  # Ya correcto
        ("123456789", "NIT", "12345678-8", True),    # DV incorrecto (9->8)
        ("123456", "CC", "123456", False),          # No es NIT
    ]

    print("\n=== PRUEBA CORRECCIÓN FORMATO NIT ===\n")

    todos_correctos = True

    for nit_orig, tipo, esperado, debe_cambiar in casos_prueba:
        try:
            if tipo == "CC":
                # Para cédulas, no hacer corrección
                resultado = nit_orig
                cambiado = False
            else:
                # Para NITs, calcular el dígito correcto
                # Extraer la base del NIT (sin dígito verificador)
                if "-" in nit_orig:
                    base = nit_orig.split("-")[0]
                else:
                    # Si no tiene guión, asumir que el último dígito es el DV
                    base = nit_orig[:-1] if len(nit_orig) > 1 else nit_orig

                # Calcular dígito correcto
                response = requests.post(CALCULAR_ENDPOINT, json={"nit": base}, timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    dv_correcto = data["digito_verificacion"]
                    resultado = f"{base}-{dv_correcto}"
                    cambiado = (resultado != nit_orig)
                else:
                    print(f"FAIL | Error API ({response.status_code}): {nit_orig}")
                    todos_correctos = False
                    continue

            if resultado == esperado and cambiado == debe_cambiar:
                status = "PASS"
            else:
                status = "FAIL"
                todos_correctos = False

            print(f"{status} | {nit_orig} ({tipo}) -> {resultado} (cambiado: {cambiado})")

        except requests.exceptions.RequestException as e:
            print(f"FAIL | Error conexión API: {nit_orig} - {e}")
            todos_correctos = False

    print(f"\n{'TODOS LOS TESTS PASARON' if todos_correctos else 'ALGUNOS TESTS FALLARON'}")

    return todos_correctos

if __name__ == "__main__":
    print("Probando algoritmo de dígito verificador DIAN usando API REST...\n")

    # Verificar conexión a la API
    if not verificar_conexion_api():
        print("\nNo se puede conectar a la API. Asegúrate de que el servidor esté corriendo en localhost:8000")
        sys.exit(1)

    print("Conexión a la API establecida\n")

    test1_ok = probar_algoritmo_dian()
    test2_ok = probar_correccion_formato()

    if test1_ok and test2_ok:
        print("\nTODAS LAS PRUEBAS PASARON - Algoritmo DIAN implementado correctamente")
        sys.exit(0)
    else:
        print("\nALGUNAS PRUEBAS FALLARON - Revisar implementación")
        sys.exit(1)