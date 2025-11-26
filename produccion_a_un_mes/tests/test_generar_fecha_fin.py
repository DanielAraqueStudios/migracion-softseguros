import pandas as pd
import re
from pathlib import Path

def test_formato_fechas():
    output_path = Path(__file__).parent.parent / 'output' / 'Plantilla Enero Softseguros_con_fecha_fin.xlsx'
    input_path = Path(__file__).parent.parent / 'data' / 'input' / 'Plantilla Enero Softseguros.xlsx'
    df_out = pd.read_excel(output_path)
    df_in = pd.read_excel(input_path)
    # Validar columnas
    assert list(df_out.columns) == list(df_in.columns), f"Las columnas no coinciden:\nOriginal: {df_in.columns.tolist()}\nProcesado: {df_out.columns.tolist()}"
    # Validar formato fechas
    col_inicio = df_out.columns[8]
    col_fin = df_out.columns[9]
    formato_fecha = re.compile(r'^\d{1,2}/\d{1,2}/\d{4}$')
    for i in range(min(10, len(df_out))):
        fecha_inicio = str(df_out.iloc[i][col_inicio])
        fecha_fin = str(df_out.iloc[i][col_fin])
        assert formato_fecha.match(fecha_inicio), f"Fecha inicio mal formateada en fila {i}: {fecha_inicio}"
        assert formato_fecha.match(fecha_fin), f"Fecha fin mal formateada en fila {i}: {fecha_fin}"
    print("Test columnas y formato de fechas: OK")

if __name__ == "__main__":
    test_formato_fechas()
