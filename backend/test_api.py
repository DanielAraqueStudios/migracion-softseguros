"""
Script de prueba para validar el funcionamiento de la API DIAN.
"""
import requests
import json

BASE_URL = "http://localhost:8000"

def test_calcular_digito():
    """Prueba el endpoint de cálculo de dígito."""
    print("\n=== Prueba: Calcular Dígito de Verificación ===")
    
    test_cases = [
        ("1003618585", 1),  # Caso de ejemplo del README
        ("890903938", 5),   # NIT empresarial típico
        ("800197268", 2),   # Otro NIT común
        ("123456789", 4),   # Caso de prueba
    ]
    
    for nit, expected_digit in test_cases:
        try:
            response = requests.post(
                f"{BASE_URL}/calcular",
                json={"nit": nit}
            )
            
            if response.status_code == 200:
                data = response.json()
                digito = data["digito_verificacion"]
                completo = data["formato_display"]
                
                status = "✅ PASS" if digito == expected_digit else f"❌ FAIL (esperado: {expected_digit})"
                print(f"{status} | NIT: {nit} | Dígito: {digito} | Completo: {completo}")
            else:
                print(f"❌ ERROR | NIT: {nit} | Status: {response.status_code}")
                
        except Exception as e:
            print(f"❌ EXCEPTION | NIT: {nit} | Error: {str(e)}")


def test_validaciones():
    """Prueba las validaciones de entrada."""
    print("\n=== Prueba: Validaciones de Entrada ===")
    
    invalid_cases = [
        ("", "NIT vacío"),
        ("abc123", "Caracteres no numéricos"),
        ("12345678901234567890", "NIT demasiado largo (>15)"),
    ]
    
    for nit, descripcion in invalid_cases:
        try:
            response = requests.post(
                f"{BASE_URL}/calcular",
                json={"nit": nit}
            )
            
            if response.status_code == 400:
                error = response.json()
                print(f"✅ PASS | {descripcion} | Error: {error['detail']}")
            else:
                print(f"❌ FAIL | {descripcion} | Debería retornar 400, retornó {response.status_code}")
                
        except Exception as e:
            print(f"❌ EXCEPTION | {descripcion} | Error: {str(e)}")


def test_health_check():
    """Prueba el endpoint de health check."""
    print("\n=== Prueba: Health Check ===")
    
    try:
        response = requests.get(f"{BASE_URL}/health")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ PASS | Status: {data['status']}")
        else:
            print(f"❌ FAIL | Status code: {response.status_code}")
            
    except Exception as e:
        print(f"❌ EXCEPTION | Error: {str(e)}")


def test_ejemplo():
    """Prueba el endpoint de ejemplos."""
    print("\n=== Prueba: Endpoint de Ejemplos ===")
    
    try:
        response = requests.get(f"{BASE_URL}/ejemplo")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ PASS | Ejemplos obtenidos: {len(data['ejemplos'])}")
            
            for ejemplo in data['ejemplos']:
                print(f"  - NIT: {ejemplo['nit']} | Dígito: {ejemplo['digito']} | Completo: {ejemplo['completo']}")
        else:
            print(f"❌ FAIL | Status code: {response.status_code}")
            
    except Exception as e:
        print(f"❌ EXCEPTION | Error: {str(e)}")


def test_formato_con_guiones():
    """Prueba que la API acepte NITs con guiones y espacios."""
    print("\n=== Prueba: Formatos con Guiones/Espacios ===")
    
    test_cases = [
        "1003618585",
        "1.003.618.585",
        "1-003-618-585",
        "1 003 618 585",
    ]
    
    for nit_input in test_cases:
        try:
            response = requests.post(
                f"{BASE_URL}/calcular",
                json={"nit": nit_input}
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ PASS | Input: '{nit_input}' | NIT procesado: {data['nit_original']}")
            else:
                print(f"❌ FAIL | Input: '{nit_input}' | Status: {response.status_code}")
                
        except Exception as e:
            print(f"❌ EXCEPTION | Input: '{nit_input}' | Error: {str(e)}")


if __name__ == "__main__":
    print("=" * 60)
    print("PRUEBAS DE API - DIAN Colombia")
    print("=" * 60)
    print(f"\nAsegúrate de que el servidor esté corriendo en {BASE_URL}")
    print("Ejecuta: uvicorn app:app --reload")
    
    try:
        # Verificar que el servidor esté corriendo
        response = requests.get(BASE_URL, timeout=2)
        print("\n✅ Servidor detectado. Iniciando pruebas...\n")
        
        # Ejecutar todas las pruebas
        test_health_check()
        test_calcular_digito()
        test_validaciones()
        test_ejemplo()
        test_formato_con_guiones()
        
        print("\n" + "=" * 60)
        print("PRUEBAS COMPLETADAS")
        print("=" * 60 + "\n")
        
    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: No se puede conectar al servidor")
        print(f"Asegúrate de que el servidor esté corriendo en {BASE_URL}")
        print("Ejecuta: uvicorn app:app --reload\n")
    except Exception as e:
        print(f"\n❌ ERROR INESPERADO: {str(e)}\n")
