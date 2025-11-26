import pandas as pd
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parent.parent.parent / 'src' / 'dian_utils'))
from dian_verificacion import calcular_digito_verificacion

# Rutas de los archivos
CARPETA_CLIENTS = Path(__file__).parent.parent.parent / 'data' / 'clients_input'
CARPETA_OUTPUT = Path(__file__).parent.parent.parent / 'output'

# Detectar archivo en clients_input
archivo_clients = None
for f in CARPETA_CLIENTS.iterdir():
    if f.suffix in ['.xlsx', '.xls']:
        archivo_clients = f
        break
if archivo_clients is None:
    print('No se encontró archivo en clients_input.')
    exit(1)

# Detectar archivo generado con fecha fin
archivo_fecha_fin = None
for f in CARPETA_OUTPUT.iterdir():
    if f.name.endswith('_con_fecha_fin.xlsx'):
        archivo_fecha_fin = f
        break
if archivo_fecha_fin is None:
    print('No se encontró archivo generado con fecha fin.')
    exit(1)

# Leer ambos archivos
clientes_df = pd.read_excel(archivo_clients)
fecha_fin_df = pd.read_excel(archivo_fecha_fin)

# Extraer columnas relevantes
col_doc_clients = clientes_df.columns[3]  # Columna D
col_tipo_clients = clientes_df.columns[4] # Columna E
col_nit_fecha_fin = 'DOCUMENTO DEL CLIENTE'  # Confirmado por análisis

# Filtrar solo los que son NIT en clients_input

# Filtrar solo los que son NIT en clients_input
nits_clients = clientes_df[clientes_df[col_tipo_clients].str.upper().str.contains('NIT', na=False)]
# Extraer solo el número base del NIT (antes del guion) en clients_input
nits_clients_base = nits_clients[col_doc_clients].astype(str).str.extract(r'(\d{7,10})')[0]
# Extraer solo el número base del NIT en archivo fecha fin
nits_fecha_fin_base = fecha_fin_df[col_nit_fecha_fin].astype(str).str.extract(r'(\d{7,10})')[0]
# Reportar coincidencias y diferencias

coincidentes = nits_clients_base[nits_clients_base.isin(nits_fecha_fin_base)]
diferentes = nits_clients_base[~nits_clients_base.isin(nits_fecha_fin_base)]
print(f"Total NITs en clients_input: {len(nits_clients_base)}")
print(f"Coinciden con archivo fecha fin: {len(coincidentes)}")
print(f"No encontrados en archivo fecha fin: {len(diferentes)}")
if len(diferentes) > 0:
    print("NITs no encontrados (con dígito calculado si falta):")
    resultado = []
    for nit in diferentes:
        if nit and nit.isdigit():
            digito = calcular_digito_verificacion(nit)
            resultado.append({"NIT": nit, "NIT con dígito": f"{nit}-{digito}"})
        else:
            resultado.append({"NIT": nit, "NIT con dígito": nit})
    print([r["NIT con dígito"] for r in resultado])
    # Exportar a Excel
    import pandas as pd
    df_resultado = pd.DataFrame(resultado)
    output_path = Path(__file__).parent.parent.parent / 'output' / 'nits_no_encontrados_con_digito.xlsx'
    df_resultado.to_excel(output_path, index=False)
    print(f"Archivo exportado: {output_path}")
