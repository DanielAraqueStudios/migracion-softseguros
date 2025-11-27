import pandas as pd
from pathlib import Path

# Ruta del archivo plantilla
archivo_plantilla = Path(__file__).parent / 'plantilla' / 'PLANTILLA DE SOTSEGUROS.xlsx'

try:
    df = pd.read_excel(archivo_plantilla)
    print(f'Archivo leído: {archivo_plantilla}')
    print('Columnas:', df.columns.tolist())
    print('Tipos de datos:', df.dtypes)
except Exception as e:
    print(f'Error al leer el archivo Excel: {e}')
