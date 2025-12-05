"""
Verificar Mapeo de Ramos
========================
Script para verificar qué tan completo está el mapeo CELER → MAVISO
y mostrar los casos que faltan por mapear.
"""

import pandas as pd
from pathlib import Path
from collections import defaultdict
from mapeo_ramos import (
    obtener_aseguradora_maviso, 
    obtener_subramo_maviso,
    SUBRAMOS_VALIDOS
)

# Rutas
CARPETA_BASE = Path(__file__).parent
ARCHIVO_CELER = CARPETA_BASE / 'Copy of polizas vigentes celer.xlsx'


def verificar_mapeo():
    """Verifica el mapeo para todos los registros de CELER"""
    print("=" * 80)
    print("VERIFICACIÓN DE MAPEO CELER → MAVISO")
    print("=" * 80)
    
    df = pd.read_excel(ARCHIVO_CELER, skiprows=3)
    
    # Columnas: R = Aseguradora (índice 17), S = Ramo (índice 18)
    col_aseguradora = df.columns[17]  # R = Aseguradora
    col_ramo = df.columns[18]         # S = Ramo
    
    # Contadores
    mapeados = 0
    sin_aseguradora = 0
    sin_subramo = 0
    
    # Registrar casos sin mapeo
    casos_sin_aseguradora = defaultdict(int)
    casos_sin_subramo = defaultdict(lambda: defaultdict(int))
    casos_mapeados = defaultdict(lambda: defaultdict(int))
    
    for _, row in df.iterrows():
        aseg_celer = str(row[col_aseguradora]).strip() if pd.notna(row[col_aseguradora]) else ''
        ramo_celer = str(row[col_ramo]).strip() if pd.notna(row[col_ramo]) else ''
        
        if not aseg_celer or not ramo_celer:
            continue
        
        # Obtener aseguradora MAVISO
        aseg_maviso = obtener_aseguradora_maviso(aseg_celer, ramo_celer)
        
        if aseg_maviso is None:
            sin_aseguradora += 1
            casos_sin_aseguradora[aseg_celer] += 1
            continue
        
        # Obtener subramo MAVISO
        subramo_maviso = obtener_subramo_maviso(aseg_maviso, ramo_celer)
        
        if subramo_maviso is None:
            sin_subramo += 1
            casos_sin_subramo[aseg_maviso][ramo_celer] += 1
        else:
            # Verificar que el subramo sea válido
            if aseg_maviso in SUBRAMOS_VALIDOS:
                if subramo_maviso in SUBRAMOS_VALIDOS[aseg_maviso]:
                    mapeados += 1
                    casos_mapeados[aseg_maviso][subramo_maviso] += 1
                else:
                    # Subramo mapeado pero no es válido en el dropdown
                    sin_subramo += 1
                    casos_sin_subramo[aseg_maviso][f"{ramo_celer} → {subramo_maviso} (INVÁLIDO)"] += 1
            else:
                mapeados += 1
                casos_mapeados[aseg_maviso][subramo_maviso] += 1
    
    # Resumen
    total = mapeados + sin_aseguradora + sin_subramo
    print(f"\n📊 RESUMEN:")
    print(f"   Total registros: {total}")
    print(f"   ✅ Mapeados correctamente: {mapeados} ({100*mapeados/total:.1f}%)")
    print(f"   ⚠️  Sin aseguradora en MAVISO: {sin_aseguradora} ({100*sin_aseguradora/total:.1f}%)")
    print(f"   ⚠️  Sin subramo mapeado: {sin_subramo} ({100*sin_subramo/total:.1f}%)")
    
    # Detalle de casos sin aseguradora
    if casos_sin_aseguradora:
        print("\n" + "-" * 80)
        print("❌ ASEGURADORAS SIN MAPEO EN MAVISO:")
        print("-" * 80)
        for aseg, count in sorted(casos_sin_aseguradora.items(), key=lambda x: -x[1]):
            print(f"   {aseg}: {count} pólizas")
    
    # Detalle de casos sin subramo
    if casos_sin_subramo:
        print("\n" + "-" * 80)
        print("❌ RAMOS SIN MAPEO A SUBRAMO:")
        print("-" * 80)
        for aseg_maviso in sorted(casos_sin_subramo.keys()):
            ramos = casos_sin_subramo[aseg_maviso]
            total_aseg = sum(ramos.values())
            print(f"\n   📋 {aseg_maviso} ({total_aseg} pólizas)")
            for ramo, count in sorted(ramos.items(), key=lambda x: -x[1]):
                # Mostrar subramos válidos como sugerencia
                print(f"      └── {ramo}: {count}")
            
            # Sugerir subramos válidos
            if aseg_maviso in SUBRAMOS_VALIDOS:
                print(f"      📝 Subramos válidos disponibles:")
                for s in SUBRAMOS_VALIDOS[aseg_maviso][:5]:
                    print(f"         - {s}")
                if len(SUBRAMOS_VALIDOS[aseg_maviso]) > 5:
                    print(f"         ... y {len(SUBRAMOS_VALIDOS[aseg_maviso])-5} más")
    
    # Resumen de mapeos exitosos
    print("\n" + "-" * 80)
    print("✅ MAPEOS EXITOSOS POR ASEGURADORA:")
    print("-" * 80)
    for aseg_maviso in sorted(casos_mapeados.keys()):
        subramos = casos_mapeados[aseg_maviso]
        total_aseg = sum(subramos.values())
        print(f"\n   📋 {aseg_maviso} ({total_aseg} pólizas)")
        for subramo, count in sorted(subramos.items(), key=lambda x: -x[1]):
            print(f"      └── {subramo}: {count}")


def main():
    print("\n" + "█" * 80)
    print("  VERIFICACIÓN DE MAPEO RAMOS CELER → SUBRAMOS MAVISO")
    print("█" * 80)
    
    verificar_mapeo()
    
    print("\n" + "█" * 80)
    print("  FIN DE LA VERIFICACIÓN")
    print("█" * 80)


if __name__ == "__main__":
    main()
