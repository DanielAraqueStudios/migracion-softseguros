"""
Script para identificar pólizas MENSUALES con Prima en CERO
"""
import pandas as pd
from datetime import datetime

# Configuración de columnas
COL_POLIZA = 0
COL_PRIMA = 14
COL_MODALIDAD = 21

def validar_mensuales_sin_prima():
    """Identifica pólizas mensuales que tienen prima en cero"""
    
    print("=" * 80)
    print("VALIDACIÓN: PÓLIZAS MENSUALES SIN PRIMA")
    print("=" * 80)
    
    # Cargar archivo MAVISO
    print("\n📂 Cargando MASIVO_NO_TERMINADO_YULIANA.xlsx...")
    df = pd.read_excel('../output/MASIVO_NO_TERMINADO_YULIANA.xlsx')
    print(f"   Total registros: {len(df)}")
    
    # Filtrar pólizas MENSUALES
    print("\n🔍 Filtrando pólizas MENSUALES (Col 21)...")
    mask_mensual = df.iloc[:, COL_MODALIDAD].astype(str).str.strip().str.upper() == 'MENSUAL'
    df_mensuales = df[mask_mensual]
    print(f"   Pólizas MENSUALES encontradas: {len(df_mensuales)}")
    
    # De las mensuales, filtrar las que tienen prima en 0
    print("\n🔍 Filtrando pólizas con Prima = 0 (Col 14)...")
    mask_prima_cero = df_mensuales.iloc[:, COL_PRIMA].fillna(0) == 0
    df_problema = df_mensuales[mask_prima_cero]
    print(f"   Pólizas MENSUALES con Prima = 0: {len(df_problema)}")
    
    # Mostrar resultados
    print("\n" + "=" * 80)
    print("RESUMEN DE RESULTADOS:")
    print("=" * 80)
    print(f"Total pólizas en archivo:        {len(df)}")
    print(f"Pólizas MENSUALES:               {len(df_mensuales)}")
    print(f"MENSUALES con Prima = 0:         {len(df_problema)}")
    print(f"Porcentaje problemáticas:        {len(df_problema)/len(df_mensuales)*100:.1f}%")
    
    # Exportar a Excel
    if len(df_problema) > 0:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        archivo_salida = f'../output/mensuales_sin_prima_{timestamp}.xlsx'
        
        # Preparar datos para exportar
        resultado = pd.DataFrame({
            'Póliza': df_problema.iloc[:, COL_POLIZA],
            'Prima Neta': df_problema.iloc[:, COL_PRIMA],
            'Modalidad': df_problema.iloc[:, COL_MODALIDAD],
            'Fila Excel': df_problema.index + 2,  # +2 para contar header y base-1
            'Placa': df_problema.iloc[:, 1],
            'Asegurado': df_problema.iloc[:, 2],
            'Fecha Inicio': df_problema.iloc[:, 10],
            'Fecha Fin': df_problema.iloc[:, 11],
        })
        
        resultado.to_excel(archivo_salida, index=False)
        print(f"\n✅ Reporte exportado a: {archivo_salida}")
        
        # Mostrar primeros 10 registros
        print("\n" + "=" * 80)
        print("PRIMERAS 10 PÓLIZAS PROBLEMÁTICAS:")
        print("=" * 80)
        print(resultado.head(10).to_string(index=False))
    else:
        print("\n✅ No se encontraron pólizas mensuales con prima en cero")
    
    print("\n" + "=" * 80)
    
    return df_problema


if __name__ == "__main__":
    df_resultado = validar_mensuales_sin_prima()
