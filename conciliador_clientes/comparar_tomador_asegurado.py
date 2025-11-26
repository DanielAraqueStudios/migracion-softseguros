import sys
sys.path.append(r"c:\Users\danie\Documents\EMPRESA\SEGUROS UNIÓN\AUTOMATIZACIONES\migraciones\migracion-softseguros\produccion_a_un_mes\src\dian_utils")
from dian_verificacion import calcular_digito_verificacion
import pandas as pd
import json
import logging
from pathlib import Path

# Configuración de logs
logging.basicConfig(
    filename=Path(__file__).parent / 'logs_comparacion.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s: %(message)s'
)


CARPETA_CLIENTES_ACTIVOS = Path(__file__).parent / 'clientes_activos'

# Detectar archivo Excel en clientes_activos
archivo_clientes = None
for f in CARPETA_CLIENTES_ACTIVOS.iterdir():
    if f.suffix in ['.xlsx', '.xls']:
        archivo_clientes = f
        break
if archivo_clientes is None:
    logging.error('No se encontró archivo Excel en clientes_activos.')
    print('No se encontró archivo Excel en clientes_activos.')
    exit(1)

try:
    # Leer desde la fila 5 (skiprows=4)
    df = pd.read_excel(archivo_clientes, skiprows=3)
    logging.info(f'Archivo leído: {archivo_clientes}')
    print(f'Archivo leído: {archivo_clientes}')
except Exception as e:
    logging.error(f'Error al leer el archivo: {e}')
    print(f'Error al leer el archivo: {e}')
    exit(1)

# Mostrar estructura de columnas y tipos
logging.info(f'Columnas: {df.columns.tolist()}')
logging.info(f'Tipos: {df.dtypes}')
print('Estructura de columnas:', df.columns.tolist())
print('Tipos de datos:', df.dtypes)


# Buscar columnas por nombre (coincidencia parcial, sin importar mayúsculas)

# Usar nombres exactos de columnas
col_tipo_doc = 'Tipo_Doc'
col_tomador = 'Tomador'
col_asegurado = 'Asegurado'

for col in [col_tipo_doc, col_tomador, col_asegurado]:
    if col not in df.columns:
        logging.error(f'No se encontró la columna: {col}')
        print(f'No se encontró la columna: {col}')
        exit(1)

# Filtrar solo NIT
df_nit = df[df[col_tipo_doc].astype(str).str.upper().str.contains('NIT', na=False)]
logging.info(f'Registros con tipo NIT: {len(df_nit)}')


# Comparar tomador vs asegurado ignorando mayúsculas y espacios y excluyendo vacíos
def normalizar(texto):
    if pd.isna(texto):
        return ''
    return str(texto).replace(' ', '').upper()

def es_diferente(row):
    t = normalizar(row[col_tomador])
    a = normalizar(row[col_asegurado])
    return bool(t and a and t != a)

mascara = df_nit.apply(es_diferente, axis=1)
diferentes = df_nit.loc[mascara]
logging.info(f'Registros con tomador distinto a asegurado y ambos no vacíos: {len(diferentes)}')

# Agregar dígito de verificación DIAN si corresponde
data = diferentes.to_dict(orient='records')
for registro in data:
    # Identificacion principal
    nit = registro.get('Identificacion')
    tipo_doc = registro.get('Tipo_Doc', '').upper()
    if tipo_doc == 'NIT' and nit and str(nit).isdigit():
        dv = calcular_digito_verificacion(str(nit))
        if dv is not None:
            registro['Identificacion'] = f"{nit}-{dv}"

    # Iden_Asegurado
    nit_aseg = registro.get('Iden_Asegurado')
    if nit_aseg and str(nit_aseg).isdigit():
        dv_aseg = calcular_digito_verificacion(str(nit_aseg))
        if dv_aseg is not None:
            registro['Iden_Asegurado'] = f"{nit_aseg}-{dv_aseg}"

    # Iden_Beneficiario
    nit_bene = registro.get('Iden_Beneficiario')
    if nit_bene and str(nit_bene).isdigit():
        dv_bene = calcular_digito_verificacion(str(nit_bene))
        if dv_bene is not None:
            registro['Iden_Beneficiario'] = f"{nit_bene}-{dv_bene}"

# Exportar a JSON con dígito de verificación
output_json = CARPETA_CLIENTES_ACTIVOS / 'diferencias_tomador_asegurado_con_dv.json'
try:
    with open(output_json, 'w', encoding='utf-8') as f:
        import json
        json.dump(data, f, ensure_ascii=False, indent=2)
    logging.info(f'Archivo JSON exportado: {output_json}')
    print(f'Archivo JSON exportado: {output_json}')
except Exception as e:
    logging.error(f'Error al exportar JSON: {e}')
    print(f'Error al exportar JSON: {e}')
