import pandas as pd
import os
from pathlib import Path

# Carpeta de entrada de archivos Excel
CARPETA_INPUT = Path(__file__).parent.parent.parent / 'data' / 'input'


def analizar_archivo_excel(ruta_archivo):
    """
    Analiza las columnas y tipos de datos de un archivo Excel.
    """
    try:
        df = pd.read_excel(ruta_archivo)
    except Exception as e:
        print(f"Error al leer el archivo {ruta_archivo}: {e}")
        return

    print(f"\nArchivo: {ruta_archivo}")
    print(f"Filas: {df.shape[0]}, Columnas: {df.shape[1]}")
    print("Columnas, tipos y formato detectado:")
    for col in df.columns:
        serie = df[col].dropna()
        tipo = df[col].dtype
        muestra = serie.iloc[:3].to_list()
        formato = ""
        if tipo == 'datetime64[ns]':
            # Verificar si hay hora en los datos
            tiene_hora = any(pd.to_datetime(val).hour != 0 or pd.to_datetime(val).minute != 0 for val in serie if pd.notnull(val))
            formato = "Fecha con hora" if tiene_hora else "Solo fecha"
        elif tipo == 'object':
            # Intentar detectar si son fechas en texto
            fechas_detectadas = 0
            for val in muestra:
                try:
                    dt = pd.to_datetime(val, errors='raise')
                    fechas_detectadas += 1
                except Exception:
                    pass
            if fechas_detectadas:
                formato = f"Texto con formato de fecha ({fechas_detectadas} de 3 muestras)"
        elif tipo == 'float64' or tipo == 'int64':
            formato = "Numérico"
        else:
            formato = str(tipo)
        print(f"  - {col}: {tipo} | Formato: {formato} | Ejemplo: {muestra}")
    print("\nResumen de tipos:")
    print(df.dtypes)


def main():
    print(f"Analizando archivos en: {CARPETA_INPUT}\n")
    archivos = [f for f in os.listdir(CARPETA_INPUT) if f.endswith('.xlsx') or f.endswith('.xls')]
    if not archivos:
        print("No se encontraron archivos Excel en la carpeta de entrada.")
        return
    for archivo in archivos:
        ruta = CARPETA_INPUT / archivo
        analizar_archivo_excel(ruta)

if __name__ == "__main__":
    main()
