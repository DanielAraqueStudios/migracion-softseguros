import pandas as pd
import os

informe_path = os.path.join(os.path.dirname(__file__), 'data_celer', 'InformedePersonas CELER.xlsx')

preview = pd.read_excel(informe_path, header=None, nrows=10)
print('Vista previa de las primeras 10 filas:')
print(preview)
