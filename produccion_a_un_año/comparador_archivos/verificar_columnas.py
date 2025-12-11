"""
Script para verificar columnas de CELER y MAVISO
"""
import pandas as pd

print("=" * 80)
print("VERIFICACIÓN DE COLUMNAS")
print("=" * 80)

# CELER
print("\n=== CELER ===")
df_celer = pd.read_excel('../Copy of polizas vigentes celer.xlsx', skiprows=3)
print(f"Total columnas: {len(df_celer.columns)}")
print("\nColumnas relevantes:")
for i in range(20, 30):
    if i < len(df_celer.columns):
        letra = chr(65 + i) if i < 26 else f"{chr(65 + (i // 26) - 1)}{chr(65 + (i % 26))}"
        print(f"  {i:2d} ({letra:2s}): {df_celer.columns[i]}")

# MAVISO
print("\n=== MAVISO (MASIVO_NO_TERMINADO_YULIANA) ===")
df_maviso = pd.read_excel('../output/MASIVO_NO_TERMINADO_YULIANA.xlsx')
print(f"Total columnas: {len(df_maviso.columns)}")
print("\nColumnas relevantes:")
for i in range(18, 26):
    if i < len(df_maviso.columns):
        letra = chr(65 + i)
        print(f"  {i:2d} ({letra}): {df_maviso.columns[i]}")

# Verificar con una póliza
print("\n" + "=" * 80)
print("VERIFICACIÓN CON PÓLIZA 900001203798")
print("=" * 80)

poliza_celer = df_celer[df_celer.iloc[:, 20].astype(str).str.strip() == '900001203798']
if len(poliza_celer) > 0:
    print("\nCELER - Valores de modalidad:")
    print(f"  Col 26 (AA): '{poliza_celer.iloc[0, 26]}'")
    print(f"  Col 27 (AB): '{poliza_celer.iloc[0, 27]}'")

poliza_maviso = df_maviso[df_maviso.iloc[:, 0].astype(str).str.strip() == '900001203798']
if len(poliza_maviso) > 0:
    print("\nMAVISO - Valores de modalidad:")
    print(f"  Col 21 (V): '{poliza_maviso.iloc[0, 21]}'")
    print(f"  Col 22 (W): '{poliza_maviso.iloc[0, 22]}'")
