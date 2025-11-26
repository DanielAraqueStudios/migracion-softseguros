import json
from pathlib import Path
import re

# Ruta del JSON a analizar
json_path = Path(__file__).parent / 'clientes_activos' / 'diferencias_tomador_asegurado_con_dv.json'

with open(json_path, encoding='utf-8') as f:
    data = json.load(f)

# Función para detectar NIT sin dígito de verificación
nit_sin_dv = lambda x: bool(re.fullmatch(r'\d{7,10}', str(x)))
# Función para detectar cédula válida (Colombia: 6-10 dígitos, no NIT)
cedula_valida = lambda x: bool(re.fullmatch(r'\d{6,10}', str(x))) and not nit_sin_dv(x)

resultados = []
for registro in data:
    # Buscar NIT sin DV en los campos relevantes
    for campo in ['Identificacion', 'Iden_Asegurado', 'Iden_Beneficiario']:
        valor = registro.get(campo)
        if valor and nit_sin_dv(valor):
            # Buscar cédula válida en el mismo registro
            cedula = registro.get('Identificacion')
            if cedula and cedula_valida(cedula):
                resultados.append({
                    'registro': registro,
                    'campo_nit_sin_dv': campo,
                    'nit_sin_dv': valor,
                    'cedula': cedula
                })

print(f"Registros con NIT sin DV y cédula válida:")
for r in resultados:
    print(f"NIT sin DV en campo {r['campo_nit_sin_dv']}: {r['nit_sin_dv']}, cédula: {r['cedula']}")
