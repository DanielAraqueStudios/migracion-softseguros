import pandas as pd
import json
import os

# Rutas absolutas recomendadas para robustez
excel_path = os.path.join(os.path.dirname(__file__), 'data_celer', 'InformedePersonas CELER.xlsx')
json_path = os.path.join(os.path.dirname(__file__), 'clientes_activos', 'diferencias_tomador_asegurado.json')

def cargar_json(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"No se encontró el archivo JSON de mismatches en: {path}")
        return []
    except json.JSONDecodeError:
        print(f"Error al decodificar el archivo JSON: {path}")
        return []

def cargar_excel(path):
    try:
        return pd.read_excel(path)
    except FileNotFoundError:
        print(f"No se encontró el archivo Excel en: {path}")
        return pd.DataFrame()

def main():
    mismatches = cargar_json(json_path)
    df_excel = cargar_excel(excel_path)

    total_excel = len(df_excel)
    total_mismatches = len(mismatches)
    total_matches = total_excel - total_mismatches

    print("--- Estadísticas de comparación Tomador vs Asegurado ---")
    print(f"Total registros en Excel: {total_excel}")
    print(f"Total registros con mismatch (JSON): {total_mismatches}")
    print(f"Total registros coincidentes: {total_matches}")

    if total_excel > 0:
        porcentaje_match = (total_matches / total_excel) * 100
        print(f"Porcentaje de coincidencia: {porcentaje_match:.2f}%")
    else:
        print("No hay registros en el Excel para comparar.")

if __name__ == "__main__":
    main()
