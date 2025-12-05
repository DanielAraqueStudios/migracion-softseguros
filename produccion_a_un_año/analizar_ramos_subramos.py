"""
Analizar Ramos y Subramos
=========================
Script para analizar las combinaciones de Aseguradora + Ramo en CELER
y los dropdowns de Subramo disponibles en SoftSeguros (Maviso).
"""

import pandas as pd
from openpyxl import load_workbook
from pathlib import Path
from collections import defaultdict

# Rutas
CARPETA_BASE = Path(__file__).parent
ARCHIVO_MAVISO = CARPETA_BASE / 'Copy of Maviso.xlsx'
ARCHIVO_CELER = CARPETA_BASE / 'Copy of polizas vigentes celer.xlsx'


def analizar_celer():
    """Analiza las combinaciones Aseguradora + Ramo en CELER"""
    print("=" * 80)
    print("ANÁLISIS DE RAMOS EN CELER")
    print("=" * 80)
    
    df = pd.read_excel(ARCHIVO_CELER, skiprows=3)
    
    # Columnas: R = Aseguradora (índice 17), S = Ramo (índice 18)
    col_aseguradora = df.columns[17]  # R = Aseguradora
    col_ramo = df.columns[18]         # S = Ramo
    
    print(f"\nColumna Aseguradora: {col_aseguradora}")
    print(f"Columna Ramo: {col_ramo}")
    
    # Agrupar por Aseguradora y contar Ramos
    combinaciones = defaultdict(lambda: defaultdict(int))
    
    for _, row in df.iterrows():
        aseguradora = str(row[col_aseguradora]).strip() if pd.notna(row[col_aseguradora]) else 'SIN ASEGURADORA'
        ramo = str(row[col_ramo]).strip() if pd.notna(row[col_ramo]) else 'SIN RAMO'
        combinaciones[aseguradora][ramo] += 1
    
    # Imprimir resultados organizados
    print("\n" + "-" * 80)
    print("ASEGURADORAS Y SUS RAMOS (con cantidad de pólizas):")
    print("-" * 80)
    
    for aseguradora in sorted(combinaciones.keys()):
        ramos = combinaciones[aseguradora]
        total_polizas = sum(ramos.values())
        print(f"\n📋 {aseguradora} ({total_polizas} pólizas)")
        print("   " + "-" * 50)
        for ramo in sorted(ramos.keys()):
            cantidad = ramos[ramo]
            print(f"   └── {ramo}: {cantidad}")
    
    # Resumen
    print("\n" + "=" * 80)
    print("RESUMEN CELER:")
    print(f"  Total Aseguradoras: {len(combinaciones)}")
    print(f"  Total Ramos únicos: {len(set(ramo for ramos in combinaciones.values() for ramo in ramos))}")
    print(f"  Total Pólizas: {len(df)}")
    
    return combinaciones


def analizar_maviso_dropdowns():
    """Analiza los dropdowns (validaciones) en el archivo Maviso"""
    print("\n" + "=" * 80)
    print("ANÁLISIS DE DROPDOWNS EN MAVISO (SoftSeguros)")
    print("=" * 80)
    
    wb = load_workbook(ARCHIVO_MAVISO)
    ws = wb.active
    
    # Buscar validaciones de datos (dropdowns)
    print("\n📋 Validaciones de datos encontradas:")
    print("-" * 80)
    
    if ws.data_validations:
        for dv in ws.data_validations.dataValidation:
            print(f"\n  Tipo: {dv.type}")
            print(f"  Rango: {dv.sqref}")
            if dv.formula1:
                print(f"  Fórmula/Lista: {dv.formula1}")
            if dv.formula2:
                print(f"  Fórmula2: {dv.formula2}")
    else:
        print("  No se encontraron validaciones de datos directas.")
    
    # Leer también los valores únicos actuales en columnas relevantes
    print("\n" + "-" * 80)
    print("VALORES ÚNICOS EN COLUMNAS DE MAVISO:")
    print("-" * 80)
    
    df = pd.read_excel(ARCHIVO_MAVISO)
    
    # Columnas de interés: C/D = Aseguradora, E/F = Subramo
    columnas_interes = {
        'ASEGURADORA (Col D)': df.columns[3] if len(df.columns) > 3 else None,  # D
        'SUBRAMO (Col F)': df.columns[5] if len(df.columns) > 5 else None,       # F
        'CELER Aseg (Col C)': df.columns[2] if len(df.columns) > 2 else None,   # C
        'CELER Ramo (Col E)': df.columns[4] if len(df.columns) > 4 else None,   # E
    }
    
    for nombre, col in columnas_interes.items():
        if col and col in df.columns:
            valores = df[col].dropna().unique()
            print(f"\n📋 {nombre} - Columna: '{col}'")
            print(f"   Valores únicos ({len(valores)}):")
            for v in sorted(set(str(x).strip() for x in valores if str(x).strip())):
                count = len(df[df[col].astype(str).str.strip() == v])
                print(f"   └── {v}: {count}")
    
    return wb


def analizar_combinaciones_maviso():
    """Analiza las combinaciones Aseguradora + Subramo en Maviso"""
    print("\n" + "=" * 80)
    print("COMBINACIONES ASEGURADORA + SUBRAMO EN MAVISO")
    print("=" * 80)
    
    df = pd.read_excel(ARCHIVO_MAVISO)
    
    # D = Aseguradora (índice 3), F = Subramo (índice 5)
    col_aseguradora = df.columns[3]  # D
    col_subramo = df.columns[5]      # F
    
    combinaciones = defaultdict(lambda: defaultdict(int))
    
    for _, row in df.iterrows():
        aseguradora = str(row[col_aseguradora]).strip() if pd.notna(row[col_aseguradora]) else 'SIN ASEGURADORA'
        subramo = str(row[col_subramo]).strip() if pd.notna(row[col_subramo]) else 'SIN SUBRAMO'
        if aseguradora and subramo:
            combinaciones[aseguradora][subramo] += 1
    
    print("\n" + "-" * 80)
    print("ASEGURADORAS Y SUS SUBRAMOS EN MAVISO:")
    print("-" * 80)
    
    for aseguradora in sorted(combinaciones.keys()):
        subramos = combinaciones[aseguradora]
        if aseguradora and aseguradora != 'nan':
            total = sum(subramos.values())
            print(f"\n📋 {aseguradora} ({total} registros)")
            print("   " + "-" * 50)
            for subramo in sorted(subramos.keys()):
                if subramo and subramo != 'nan':
                    cantidad = subramos[subramo]
                    print(f"   └── {subramo}: {cantidad}")
    
    return combinaciones


def main():
    print("\n" + "█" * 80)
    print("  ANÁLISIS DE RAMOS Y SUBRAMOS - CELER vs MAVISO")
    print("█" * 80)
    
    # 1. Analizar CELER
    comb_celer = analizar_celer()
    
    # 2. Analizar dropdowns en Maviso
    analizar_maviso_dropdowns()
    
    # 3. Analizar combinaciones en Maviso
    comb_maviso = analizar_combinaciones_maviso()
    
    # 4. Comparación
    print("\n" + "=" * 80)
    print("COMPARACIÓN CELER vs MAVISO")
    print("=" * 80)
    
    aseg_celer = set(comb_celer.keys())
    aseg_maviso = set(k for k in comb_maviso.keys() if k and k != 'nan')
    
    print(f"\nAseguradoras en CELER: {len(aseg_celer)}")
    print(f"Aseguradoras en MAVISO: {len(aseg_maviso)}")
    
    # Aseguradoras en común
    comunes = aseg_celer & aseg_maviso
    print(f"\nAseguradoras en común: {len(comunes)}")
    
    # Solo en CELER
    solo_celer = aseg_celer - aseg_maviso
    if solo_celer:
        print(f"\n⚠️  Solo en CELER ({len(solo_celer)}):")
        for a in sorted(solo_celer):
            print(f"   - {a}")
    
    # Solo en MAVISO
    solo_maviso = aseg_maviso - aseg_celer
    if solo_maviso:
        print(f"\n⚠️  Solo en MAVISO ({len(solo_maviso)}):")
        for a in sorted(solo_maviso):
            print(f"   - {a}")
    
    print("\n" + "█" * 80)
    print("  FIN DEL ANÁLISIS")
    print("█" * 80)


if __name__ == "__main__":
    main()
