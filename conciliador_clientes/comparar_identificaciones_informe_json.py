import pandas as pd
import json
import os

# Rutas de archivos
informe_path = os.path.join(os.path.dirname(__file__), 'data_celer', 'InformedePersonas CELER.xlsx')
json_path = os.path.join(os.path.dirname(__file__), 'clientes_activos', 'diferencias_tomador_asegurado.json')

# Leer informe de personas usando la fila 3 como encabezado
informe_df = pd.read_excel(informe_path, header=3)


# Leer identificaciones del JSON usando 'Iden_Beneficiario'
with open(json_path, 'r', encoding='utf-8') as f:
    json_data = json.load(f)
identificaciones_json = set(str(item['Iden_Beneficiario']) for item in json_data if 'Iden_Beneficiario' in item)

# Columna C es la tercera columna (índice 2) en pandas
if 'NÚMERO DE DOCUMENTO' in informe_df.columns:
    identificaciones_informe = informe_df['NÚMERO DE DOCUMENTO'].astype(str)
else:
    identificaciones_informe = informe_df.iloc[:,2].astype(str)

# Comparar y marcar coincidencias
coincidencias = identificaciones_informe.isin(identificaciones_json)

# Resultados
total = len(identificaciones_informe)
total_coinciden = coincidencias.sum()
total_no_coinciden = total - total_coinciden

print(f'Total registros en informe: {total}')
print(f'Coinciden con JSON: {total_coinciden}')
print(f'No coinciden con JSON: {total_no_coinciden}')

# Opcional: exportar resultados
resultado_df = informe_df.copy()
resultado_df['Coincide_JSON'] = coincidencias
resultado_df.to_excel(os.path.join(os.path.dirname(__file__), 'data_celer', 'informe_comparado_con_json.xlsx'), index=False)
print('Archivo de comparación exportado a data_celer/informe_comparado_con_json.xlsx')