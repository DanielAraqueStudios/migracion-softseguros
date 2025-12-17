"""
Test para verificar búsqueda de Unidades en CELER
"""
import pandas as pd
import sys
from pathlib import Path

# Constantes
CELER_COL_POLIZA = 20  # Columna U (después de skiprows=3)
CELER_COL_UNIDAD = 55  # Columna BD

# Tests esperados
TESTS = [
    {
        'poliza': '1338293',
        'unidad_esperada': 'LILIANA LOPEZ BENJUMEA'
    },
    {
        'poliza': '02196072300489',
        'unidad_esperada': 'LUCIA BEATRIZ HERRERA ARCINIEGAS'
    }
]

def buscar_unidad_en_celer(archivo_celer: str, numero_poliza: str) -> tuple:
    """
    Busca una póliza en CELER y retorna su Unidad
    
    Returns:
        tuple: (encontrada: bool, unidad: str, fila: int)
    """
    try:
        # Leer CELER
        df_celer = pd.read_excel(archivo_celer, skiprows=3, dtype=str)
        
        print(f"\n📂 Archivo CELER cargado: {len(df_celer)} registros")
        print(f"🔍 Buscando póliza: {numero_poliza}")
        
        # Normalizar y buscar
        for idx, row in df_celer.iterrows():
            poliza_celer = str(row.iloc[CELER_COL_POLIZA]).strip().upper()
            
            if poliza_celer == numero_poliza.upper():
                unidad = row.iloc[CELER_COL_UNIDAD]
                fila_excel = idx + 5  # +5 por skiprows=3 + header + 0-index
                return True, unidad, fila_excel
        
        return False, None, None
        
    except Exception as e:
        print(f"❌ Error al leer archivo: {e}")
        return False, None, None


def ejecutar_tests(archivo_celer: str):
    """Ejecuta todos los tests"""
    print("="*70)
    print("🧪 TEST: BÚSQUEDA DE UNIDADES EN CELER")
    print("="*70)
    print(f"\n📄 Archivo: {Path(archivo_celer).name}")
    
    resultados = []
    
    for i, test in enumerate(TESTS, 1):
        print(f"\n{'='*70}")
        print(f"TEST {i}/{len(TESTS)}")
        print(f"{'='*70}")
        
        poliza = test['poliza']
        unidad_esperada = test['unidad_esperada']
        
        print(f"Póliza: {poliza}")
        print(f"Unidad esperada: {unidad_esperada}")
        
        encontrada, unidad_obtenida, fila = buscar_unidad_en_celer(archivo_celer, poliza)
        
        if encontrada:
            print(f"✅ Póliza ENCONTRADA en fila {fila}")
            print(f"📋 Unidad obtenida: {unidad_obtenida}")
            
            # Verificar si coincide
            if str(unidad_obtenida).strip().upper() == str(unidad_esperada).strip().upper():
                print("✅ ✅ ✅ TEST PASADO - Los valores coinciden")
                resultados.append(True)
            else:
                print("❌ ❌ ❌ TEST FALLIDO - Los valores NO coinciden")
                print(f"   Esperado: '{unidad_esperada}'")
                print(f"   Obtenido: '{unidad_obtenida}'")
                resultados.append(False)
        else:
            print(f"❌ Póliza NO encontrada en CELER")
            print("❌ ❌ ❌ TEST FALLIDO")
            resultados.append(False)
    
    # Resumen final
    print(f"\n{'='*70}")
    print("📊 RESUMEN DE TESTS")
    print(f"{'='*70}")
    print(f"Total tests: {len(TESTS)}")
    print(f"✅ Pasados: {sum(resultados)}")
    print(f"❌ Fallidos: {len(resultados) - sum(resultados)}")
    
    if all(resultados):
        print("\n🎉 🎉 🎉 TODOS LOS TESTS PASARON 🎉 🎉 🎉")
        return 0
    else:
        print("\n⚠️ ALGUNOS TESTS FALLARON")
        return 1


if __name__ == "__main__":
    # Solicitar archivo CELER
    print("\n" + "="*70)
    print("SCRIPT DE TEST - BÚSQUEDA DE UNIDADES")
    print("="*70)
    
    if len(sys.argv) > 1:
        archivo_celer = sys.argv[1]
    else:
        print("\n❓ Por favor ingrese la ruta del archivo CELER:")
        archivo_celer = input(">>> ").strip()
    
    # Verificar que existe
    if not Path(archivo_celer).exists():
        print(f"\n❌ Error: El archivo no existe: {archivo_celer}")
        sys.exit(1)
    
    # Ejecutar tests
    exit_code = ejecutar_tests(archivo_celer)
    
    print("\n" + "="*70)
    input("\nPresione ENTER para salir...")
    sys.exit(exit_code)
