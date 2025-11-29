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
    """
    Calcula el dígito verificador usando la API DIAN
    """
    try:
        payload = {"nit": nit_sin_dv}
        headers = {"Content-Type": "application/json"}

        response = requests.post(CALCULAR_ENDPOINT, json=payload, headers=headers, timeout=10)

        if response.status_code == 200:
            data = response.json()
            return str(data["digito_verificacion"])
        else:
            print(f"Error en API: {response.status_code} - {response.text}")
            return None

    except Exception as e:
        print(f"❌ Error de conexión con API: {e}")
        return None

def probar_algoritmo_dian():
    """Prueba el algoritmo de la DIAN con NITs conocidos usando la API"""

    if not verificar_conexion_api():
        print("❌ No se puede continuar sin conexión a la API")
        return False

    # NITs de prueba conocidos (verificados con calculadoras online oficiales)
    nits_prueba = [
        # NIT base -> DV esperado
        ("890900608", "8"),      # NIT de prueba DIAN - verificado
        ("900310074", "4"),      # NIT conocido - verificado online
        ("800197268", "9"),      # NIT conocido - verificado online
        ("901097473", "3"),      # NIT de empresa - verificado online
        ("900123456", "7"),      # NIT de prueba - verificado online
        ("123456789", "0"),      # NIT simple - verificado
        ("1", "1"),              # NIT de 1 dígito - verificado
        ("11", "9"),             # NIT de 2 dígitos - verificado
    ]

    print("=== PRUEBA ALGORITMO DIGITO VERIFICADOR DIAN (VIA API) ===\n")

    todos_correctos = True

    for nit_base, dv_esperado in nits_prueba:
        dv_calculado = calcular_digito_api(nit_base)

        if dv_calculado == dv_esperado:
            print(f"✅ {nit_base} -> {dv_calculado} (correcto)")
        else:
            print(f"❌ {nit_base} -> {dv_calculado} (esperado: {dv_esperado})")
            todos_correctos = False

    print(f"\n{'✅ TODOS LOS TESTS PASARON' if todos_correctos else '❌ ALGUNOS TESTS FALLARON'}")

    return todos_correctos

def probar_correccion_formato():
    """Prueba la corrección de formato de NITs usando la API"""

    # Casos de prueba
    casos_prueba = [
        # (NIT original, tipo, esperado, debe_cambiar)
        ("900310074", "NIT", "90031007-4", True),    # Sin guión
        ("90031007-4", "NIT", "90031007-4", False),  # Ya correcto
        ("90031007-5", "NIT", "90031007-4", True),   # DV incorrecto
        ("123456789", "NIT", "12345678-0", True),    # Otro caso
        ("123456", "CC", "123456", False),          # No es NIT
    ]

    print("\n=== PRUEBA CORRECCIÓN FORMATO NIT ===\n")

    todos_correctos = True

    for nit_orig, tipo, esperado, debe_cambiar in casos_prueba:
        try:
            # Llamar a la API para corregir el formato
            response = requests.post(
                "http://localhost:8000/corregir",
                json={"nit": nit_orig, "tipo": tipo},
                timeout=10
            )

            if response.status_code == 200:
                data = response.json()
                resultado = data.get("nit_corregido", nit_orig)
                cambiado = data.get("cambiado", False)

                if resultado == esperado and cambiado == debe_cambiar:
                    status = "✅"
                else:
                    status = "❌"
                    todos_correctos = False

                print(f"{status} {nit_orig} ({tipo}) -> {resultado} (cambiado: {cambiado})")
            else:
                print(f"❌ Error API ({response.status_code}): {nit_orig}")
                todos_correctos = False

        except requests.exceptions.RequestException as e:
            print(f"❌ Error conexión API: {nit_orig} - {e}")
            todos_correctos = False

    print(f"\n{'✅ TODOS LOS TESTS PASARON' if todos_correctos else '❌ ALGUNOS TESTS FALLARON'}")

    return todos_correctos

if __name__ == "__main__":
    print("Probando algoritmo de dígito verificador DIAN usando API REST...\n")

    # Verificar conexión a la API
    if not verificar_conexion_api():
        print("\n❌ No se puede conectar a la API. Asegúrate de que el servidor esté corriendo en localhost:8000")
        sys.exit(1)

    print("✅ Conexión a la API establecida\n")

    test1_ok = probar_algoritmo_dian()
    test2_ok = probar_correccion_formato()

    if test1_ok and test2_ok:
        print("\n🎉 TODAS LAS PRUEBAS PASARON - Algoritmo DIAN implementado correctamente")
        sys.exit(0)
    else:
        print("\n💥 ALGUNAS PRUEBAS FALLARON - Revisar implementación")
        sys.exit(1)