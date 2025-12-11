import pandas as pd
import sys

poliza_buscar = '900001203798'

# Cargar Maviso
df_maviso = pd.read_excel('../Copy of Maviso.xlsx')
poliza_maviso = df_maviso[df_maviso.iloc[:, 0].astype(str).str.strip() == poliza_buscar]

print('=' * 60)
print(f'VERIFICACIÓN DE PÓLIZA: {poliza_buscar}')
print('=' * 60)

print('\n=== DATOS EN MAVISO ===')
if len(poliza_maviso) > 0:
    print(f'Póliza: {poliza_maviso.iloc[0, 0]}')
    print(f'Prima Neta (col 14): {poliza_maviso.iloc[0, 14]}')
    print(f'  Tipo: {type(poliza_maviso.iloc[0, 14])}')
    print(f'  Valor absoluto: {abs(float(poliza_maviso.iloc[0, 14]))}')
    print(f'Fecha Inicio (col 10): {poliza_maviso.iloc[0, 10]}')
    print(f'Fecha Fin (col 11): {poliza_maviso.iloc[0, 11]}')
else:
    print('NO ENCONTRADA en Maviso')

# Cargar CELER
df_celer = pd.read_excel('../Copy of polizas vigentes celer.xlsx', skiprows=3, header=0)
poliza_celer = df_celer[df_celer.iloc[:, 20].astype(str).str.strip() == poliza_buscar]

print('\n=== DATOS EN CELER ===')
if len(poliza_celer) > 0:
    print(f'Póliza (col 20): {poliza_celer.iloc[0, 20]}')
    print(f'Prima sin IVA (col 42): {poliza_celer.iloc[0, 42]}')
    print(f'  Tipo: {type(poliza_celer.iloc[0, 42])}')
    print(f'  Valor absoluto: {abs(float(poliza_celer.iloc[0, 42]))}')
    print(f'F_Inicio (col 22): {poliza_celer.iloc[0, 22]}')
    print(f'F_Fin (col 23): {poliza_celer.iloc[0, 23]}')
else:
    print('NO ENCONTRADA en CELER')

# Comparar
if len(poliza_maviso) > 0 and len(poliza_celer) > 0:
    print('\n=== COMPARACIÓN ===')
    
    # Prima
    prima_maviso = abs(round(float(poliza_maviso.iloc[0, 14]), 2))
    prima_celer = abs(round(float(poliza_celer.iloc[0, 42]), 2))
    print(f'Prima Maviso |{prima_maviso:.2f}| vs CELER |{prima_celer:.2f}|')
    print(f'  ¿Coincide? {prima_maviso == prima_celer}')
    
    # Fechas
    fecha_ini_m = str(poliza_maviso.iloc[0, 10])
    fecha_ini_c = str(poliza_celer.iloc[0, 22])
    print(f'Fecha Inicio: Maviso "{fecha_ini_m}" vs CELER "{fecha_ini_c}"')
    print(f'  ¿Coincide? {fecha_ini_m == fecha_ini_c}')
    
    fecha_fin_m = str(poliza_maviso.iloc[0, 11])
    fecha_fin_c = str(poliza_celer.iloc[0, 23])
    print(f'Fecha Fin: Maviso "{fecha_fin_m}" vs CELER "{fecha_fin_c}"')
    print(f'  ¿Coincide? {fecha_fin_m == fecha_fin_c}')
