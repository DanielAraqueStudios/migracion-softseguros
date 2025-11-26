import pandas as pd
from pathlib import Path
from datetime import datetime, timedelta
import sys
sys.path.append(str(Path(__file__).parent.parent.parent / 'src' / 'dian_utils'))
from dian_verificacion import calcular_digito_verificacion

# Carpeta de entrada y salida
CARPETA_INPUT = Path(__file__).parent.parent.parent / 'data' / 'input'
CARPETA_OUTPUT = Path(__file__).parent.parent.parent / 'output'

# Nombre del archivo a procesar (puedes cambiarlo si es necesario)
NOMBRE_ARCHIVO = None
for f in CARPETA_INPUT.iterdir():
    if f.suffix in ['.xlsx', '.xls']:
        NOMBRE_ARCHIVO = f.name
        break
if NOMBRE_ARCHIVO is None:
    print('No se encontró archivo Excel en la carpeta de entrada.')
    exit(1)

RUTA_ENTRADA = CARPETA_INPUT / NOMBRE_ARCHIVO
RUTA_SALIDA = CARPETA_OUTPUT / f"{NOMBRE_ARCHIVO.split('.')[0]}_con_fecha_fin.xlsx"

# Procesar archivo
try:
    df = pd.read_excel(RUTA_ENTRADA)
except Exception as e:
    print(f"Error al leer el archivo: {e}")
    exit(1)


# Asume que la columna I es la novena (índice 8) y la columna J es la décima (índice 9)
columna_inicio = df.columns[8]
columna_fin = df.columns[9]

def limpiar_fecha(fecha):
    if pd.isnull(fecha) or str(fecha).strip() == '':
        return 'FECHA_FALTANTE'
    # Si ya es datetime, convertir directamente
    if isinstance(fecha, datetime):
        return fecha.strftime('%d/%m/%Y')
    # Intentar primero el formato original d/m/yyyy
    try:
        fecha_dt = datetime.strptime(str(fecha).strip(), '%d/%m/%Y')
        return fecha_dt.strftime('%d/%m/%Y')
    except Exception:
        pass
    # Si falla, usar pandas
    try:
        fecha_dt = pd.to_datetime(fecha, dayfirst=True, errors='coerce')
        if pd.isnull(fecha_dt):
            return 'FECHA_FALTANTE'
        return fecha_dt.strftime('%d/%m/%Y')
    except Exception:
        return 'FECHA_FALTANTE'

def sumar_un_ano(fecha):
    if pd.isnull(fecha) or str(fecha).strip() == '' or fecha == 'FECHA_FALTANTE':
        return 'FECHA_FALTANTE'
    # Si ya es datetime, sumar un año y convertir
    if isinstance(fecha, datetime):
        fecha_fin = fecha.replace(year=fecha.year + 1)
        return fecha_fin.strftime('%d/%m/%Y')
    # Intentar primero el formato original d/m/yyyy
    try:
        fecha_dt = datetime.strptime(str(fecha).strip(), '%d/%m/%Y')
        fecha_fin = fecha_dt.replace(year=fecha_dt.year + 1)
        return fecha_fin.strftime('%d/%m/%Y')
    except Exception:
        pass
    # Si falla, usar pandas
    try:
        fecha_dt = pd.to_datetime(fecha, dayfirst=True, errors='coerce')
        if pd.isnull(fecha_dt):
            return 'FECHA_FALTANTE'
        fecha_fin = fecha_dt + pd.DateOffset(years=1)
        return fecha_fin.strftime('%d/%m/%Y')
    except Exception:
        return 'FECHA_FALTANTE'

# Alimentar columna J con fecha fin
if columna_inicio and columna_fin:
    # Agregar columna con dígito de verificación para DOCUMENTO DEL TOMADOR (columna AB)
    if 'DOCUMENTO DEL TOMADOR' in df.columns:
        def tomador_con_digito(val):
            val_str = str(val)
            base = val_str.split('-')[0]
            if base.isdigit() and len(base) >= 7:
                digito = calcular_digito_verificacion(base)
                return f"{base}-{digito}"
            return val_str
        df['DOCUMENTO DEL TOMADOR'] = df['DOCUMENTO DEL TOMADOR'].apply(tomador_con_digito)
    print(f"Valor original de la primera celda de fecha inicio: {df[columna_inicio].iloc[0]!r}")
    # Limpiar fecha inicio para que no tenga hora y asegurar que no queden vacíos
    df[columna_inicio] = df[columna_inicio].apply(limpiar_fecha)
    # Actualizar los valores de la columna fecha fin (J) sin modificar el título ni agregar/eliminar columnas
    df[columna_fin] = df[columna_inicio].apply(sumar_un_ano)
    # Agregar columna NIT con dígito de verificación calculado
    if 'DOCUMENTO DEL CLIENTE' in df.columns:
        def nit_con_digito(val):
            val_str = str(val)
            # Extraer solo el número base
            base = val_str.split('-')[0]
            if base.isdigit() and len(base) >= 7:
                digito = calcular_digito_verificacion(base)
                return f"{base}-{digito}"
            return val_str
        df['NIT CON DIGITO'] = df['DOCUMENTO DEL CLIENTE'].apply(nit_con_digito)
else:
    print('No se encontraron las columnas esperadas.')
    exit(1)

# Guardar archivo en iputput
try:
    df.to_excel(RUTA_SALIDA, index=False)
    print(f"Archivo procesado y guardado en: {RUTA_SALIDA}")
except Exception as e:
    print(f"Error al guardar el archivo: {e}")
    exit(1)
