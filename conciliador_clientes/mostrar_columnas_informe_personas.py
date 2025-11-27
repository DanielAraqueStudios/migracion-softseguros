import pandas as pd
import os

informe_path = os.path.join(os.path.dirname(__file__), 'data_celer', 'InformedePersonas CELER.xlsx')

df = pd.read_excel(informe_path, header=3)
print('Columnas encontradas en el informe de personas:')
for col in df.columns:
    print(f'- {col}')
