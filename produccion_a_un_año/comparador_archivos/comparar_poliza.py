"""
Script sencillo para comparar datos de una póliza específica entre CELER y MAVISO
"""
import pandas as pd
import sys

# Configuración de columnas
CELER_COL_POLIZA = 20
CELER_COL_PRIMA = 42
CELER_COL_FECHA_INICIO = 22
CELER_COL_FECHA_FIN = 23
CELER_COL_MODALIDAD = 27  # Forma_Pago (col AB)

MAVISO_COL_POLIZA = 0
MAVISO_COL_PRIMA = 14
MAVISO_COL_FECHA_INICIO = 10
MAVISO_COL_FECHA_FIN = 11
MAVISO_COL_MODALIDAD = 21  # CELER.1 (col V)

def comparar_poliza(numero_poliza: str):
    """Compara una póliza específica entre CELER y MAVISO"""
    
    print("=" * 80)
    print(f"COMPARANDO PÓLIZA: {numero_poliza}")
    print("=" * 80)
    
    # Cargar CELER
    print("\n📂 Cargando CELER...")
    df_celer = pd.read_excel('../Copy of polizas vigentes celer.xlsx', skiprows=3)
    print(f"   Total registros: {len(df_celer)}")
    
    # Buscar en CELER - Match exacto
    print(f"\n🔍 Buscando póliza '{numero_poliza}' (longitud: {len(numero_poliza)}) en CELER...")
    
    # Convertir columna a string y comparar exactamente
    celer_polizas_str = df_celer.iloc[:, CELER_COL_POLIZA].astype(str).str.strip()
    mask_celer = celer_polizas_str == numero_poliza
    indices_celer = df_celer.index[mask_celer].tolist()
    
    if len(indices_celer) == 0:
        print(f"❌ Póliza {numero_poliza} NO encontrada en CELER")
        # Buscar coincidencias similares
        similares = celer_polizas_str[celer_polizas_str.str.contains(numero_poliza[-6:], na=False)]
        if len(similares) > 0:
            print(f"   Pólizas similares encontradas (últimos 6 dígitos): {len(similares)}")
        return
    
    print(f"✅ Encontrada en CELER:")
    for idx in indices_celer:
        valor_celda = df_celer.iloc[idx, CELER_COL_POLIZA]
        fila_excel = idx + 5  # skiprows=3 + header + 1-based
        print(f"   Índice DataFrame: {idx} → Fila Excel: {fila_excel}")
        print(f"   Valor en celda: '{valor_celda}' (tipo: {type(valor_celda).__name__}, longitud: {len(str(valor_celda).strip())})")
    
    poliza_celer = df_celer.loc[indices_celer[0:1]]
    
    # Cargar MAVISO
    print("\n📂 Cargando MAVISO...")
    df_maviso = pd.read_excel('../output/MASIVO_NO_TERMINADO_YULIANA.xlsx')
    print(f"   Total registros: {len(df_maviso)}")
    
    # Buscar en MAVISO - Match exacto
    print(f"\n🔍 Buscando póliza '{numero_poliza}' (longitud: {len(numero_poliza)}) en MAVISO...")
    
    # Convertir columna a string y comparar exactamente
    maviso_polizas_str = df_maviso.iloc[:, MAVISO_COL_POLIZA].astype(str).str.strip()
    mask_maviso = maviso_polizas_str == numero_poliza
    indices_maviso = df_maviso.index[mask_maviso].tolist()
    
    if len(indices_maviso) == 0:
        print(f"❌ Póliza {numero_poliza} NO encontrada en MAVISO")
        # Buscar coincidencias similares
        similares = maviso_polizas_str[maviso_polizas_str.str.contains(numero_poliza[-6:], na=False)]
        if len(similares) > 0:
            print(f"   Pólizas similares encontradas (últimos 6 dígitos): {len(similares)}")
        return
    
    print(f"✅ Encontrada en MAVISO:")
    for idx in indices_maviso:
        valor_celda = df_maviso.iloc[idx, MAVISO_COL_POLIZA]
        fila_excel = idx + 2  # header + 1-based
        print(f"   Índice DataFrame: {idx} → Fila Excel: {fila_excel}")
        print(f"   Valor en celda: '{valor_celda}' (tipo: {type(valor_celda).__name__}, longitud: {len(str(valor_celda).strip())})")
    
    poliza_maviso = df_maviso.loc[indices_maviso[0:1]]
    
    # Verificar múltiples coincidencias
    if len(indices_maviso) > 1:
        print(f"\n⚠️ ADVERTENCIA: Se encontraron {len(indices_maviso)} pólizas con el número {numero_poliza}")
        print(f"   Usando la primera coincidencia (índice {indices_maviso[0]})")
    
    # Obtener índices de fila (posición en el DataFrame)
    idx_celer = poliza_celer.index[0]
    idx_maviso = poliza_maviso.index[0]
    
    # Calcular fila en Excel (1-based, con header)
    fila_excel_celer = idx_celer + 5  # skiprows=3 + 1 header + 1 (1-based)
    fila_excel_maviso = idx_maviso + 2  # 1 header + 1 (1-based)
    
    print(f"\n📍 UBICACIÓN EN EXCEL:")
    print(f"   CELER:  Fila {fila_excel_celer} (DataFrame índice: {idx_celer})")
    print(f"   MAVISO: Fila {fila_excel_maviso} (DataFrame índice: {idx_maviso})")
    
    # Extraer datos CELER
    celer_prima = poliza_celer.iloc[0, CELER_COL_PRIMA]
    celer_fecha_inicio = poliza_celer.iloc[0, CELER_COL_FECHA_INICIO]
    celer_fecha_fin = poliza_celer.iloc[0, CELER_COL_FECHA_FIN]
    celer_modalidad = poliza_celer.iloc[0, CELER_COL_MODALIDAD]
    
    # Extraer datos MAVISO
    maviso_prima = poliza_maviso.iloc[0, MAVISO_COL_PRIMA]
    maviso_fecha_inicio = poliza_maviso.iloc[0, MAVISO_COL_FECHA_INICIO]
    maviso_fecha_fin = poliza_maviso.iloc[0, MAVISO_COL_FECHA_FIN]
    maviso_modalidad = poliza_maviso.iloc[0, MAVISO_COL_MODALIDAD]
    
    # Mostrar todas las columnas de MAVISO para verificar
    print(f"\n🔍 VERIFICACIÓN - Todas las columnas de MAVISO (fila {idx_maviso}):")
    for i, valor in enumerate(poliza_maviso.iloc[0]):
        print(f"   Col {i:2d}: {valor}")
    
    # Mostrar comparación
    print("\n" + "=" * 80)
    print("DATOS EN CELER:")
    print("=" * 80)
    print(f"  Póliza:        {numero_poliza}")
    print(f"  Prima:         {celer_prima}")
    print(f"  Tipo Prima:    {type(celer_prima)}")
    print(f"  Fecha Inicio:  {celer_fecha_inicio}")
    print(f"  Fecha Fin:     {celer_fecha_fin}")
    print(f"  Modalidad:     {celer_modalidad}")
    
    print("\n" + "=" * 80)
    print("DATOS EN MAVISO:")
    print("=" * 80)
    print(f"  Póliza:        {numero_poliza}")
    print(f"  Prima:         {maviso_prima}")
    print(f"  Tipo Prima:    {type(maviso_prima)}")
    print(f"  Fecha Inicio:  {maviso_fecha_inicio}")
    print(f"  Fecha Fin:     {maviso_fecha_fin}")
    print(f"  Modalidad:     {maviso_modalidad}")
    
    # Comparar
    print("\n" + "=" * 80)
    print("ANÁLISIS DE COMPARACIÓN:")
    print("=" * 80)
    
    # Prima
    try:
        celer_prima_abs = abs(round(float(celer_prima), 2))
        maviso_prima_abs = abs(round(float(maviso_prima), 2))
        prima_coincide = celer_prima_abs == maviso_prima_abs
        
        print(f"\n📊 PRIMA:")
        print(f"   CELER:  {celer_prima} → |{celer_prima_abs}|")
        print(f"   MAVISO: {maviso_prima} → |{maviso_prima_abs}|")
        print(f"   Diferencia: {abs(celer_prima_abs - maviso_prima_abs)}")
        if prima_coincide:
            print(f"   ✅ COINCIDEN (valor absoluto)")
        else:
            print(f"   ❌ DISCREPANCIA")
    except Exception as e:
        print(f"   ⚠️ Error comparando prima: {e}")
    
    # Fechas
    print(f"\n📅 FECHA INICIO:")
    print(f"   CELER:  {celer_fecha_inicio}")
    print(f"   MAVISO: {maviso_fecha_inicio}")
    if str(celer_fecha_inicio).strip() == str(maviso_fecha_inicio).strip():
        print(f"   ✅ COINCIDEN")
    else:
        print(f"   ❌ DISCREPANCIA")
    
    print(f"\n📅 FECHA FIN:")
    print(f"   CELER:  {celer_fecha_fin}")
    print(f"   MAVISO: {maviso_fecha_fin}")
    if str(celer_fecha_fin).strip() == str(maviso_fecha_fin).strip():
        print(f"   ✅ COINCIDEN")
    else:
        print(f"   ❌ DISCREPANCIA")
    
    print(f"\n🔄 MODALIDAD:")
    print(f"   CELER:  {celer_modalidad}")
    print(f"   MAVISO: {maviso_modalidad}")
    if str(celer_modalidad).strip().upper() == str(maviso_modalidad).strip().upper():
        print(f"   ✅ COINCIDEN")
    else:
        print(f"   ❌ DISCREPANCIA")
    
    print("\n" + "=" * 80)


if __name__ == "__main__":
    # Por defecto buscar la póliza 900001203798
    poliza = "900001203798"
    
    # O recibir como argumento
    if len(sys.argv) > 1:
        poliza = sys.argv[1]
    
    comparar_poliza(poliza)
