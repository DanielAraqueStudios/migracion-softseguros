# Función para calcular dígito de verificación NIT (DIAN)
def calcular_dv(nit):
    nit = str(nit).strip()
    if not nit.isdigit():
        return ''
    factores = [71, 67, 59, 53, 47, 43, 41, 37, 29, 23, 19, 17, 13, 7, 3]
    nit = nit.zfill(15)[-15:]
    suma = sum(int(nit[i]) * factores[i] for i in range(15))
    resto = suma % 11
    dv = 0 if resto > 1 else 1 - resto
    return str(dv)
import pandas as pd
import json
import os

def map_tipo_doc(valor):
    valor = str(valor).strip().upper()
    if valor in ['CC', 'C.C', 'CEDULA', 'CÉDULA', 'IND']:
        return 'Cédula'
    elif valor == 'NIT':
        return 'NIT'
    elif valor in ['PSP', 'CE', 'CEDULA DE EXTRANJERIA', 'CÉDULA DE EXTRANJERÍA']:
        return 'Cédula de Extranjería'
    elif valor == 'NAN' or valor == '' or valor is None:
        return ''
    else:
        return ''  # Dejar en blanco si no corresponde

# Rutas de archivos
informe_path = os.path.join(os.path.dirname(__file__), 'data_celer', 'InformedePersonas CELER.xlsx')
json_path = os.path.join(os.path.dirname(__file__), 'clientes_activos', 'diferencias_tomador_asegurado.json')
salida_path = os.path.join(os.path.dirname(__file__), 'plantilla', 'PLANTILLA_COINCIDEN.xlsx')


# Leer informe de personas desde la primera fila y asignar nombres de columna manualmente
columnas_informe = [
    'Nombre', 'Tipo_Doc', 'Identificacion', 'F_Nacimiento', 'Edad', 'Genero', 'Prefijo', 'Estado_civil',
    'Estrato_social', 'Peso', 'Estatura', 'Fallecido', 'Profesion', 'Ocupacion', 'Tel_Personal', 'Celular_Personal',
    'Tel_Laboral', 'Celular_Laboral', 'Direccion_Personal', 'Ciudad_Personal', 'Direccion_Laboral', 'Ciudad_Laboral',
    'Mail_Personal', 'Mail_Laboral', 'F_Exp_Iden', 'Unidad', 'F_Creacion', 'F_Modificacion', 'Apartado_Aereo',
    'Lugar_Exp_Iden', 'Lugar_Nacimiento', 'Calidades_Activas', 'Ejecutivo_Principal', 'Info_Confidencial', 'Observaciones'
]
informe_df = pd.read_excel(informe_path, header=None, names=columnas_informe)

# Leer identificaciones del JSON usando 'Iden_Beneficiario'
with open(json_path, 'r', encoding='utf-8') as f:
    json_data = json.load(f)
identificaciones_json = set(str(item['Iden_Beneficiario']) for item in json_data if 'Iden_Beneficiario' in item)


# Buscar coincidencias por número de documento y por nombre
coincidentes_num = informe_df[informe_df['Identificacion'].astype(str).isin(identificaciones_json)]

# Extraer nombres del JSON para buscar por nombre
nombres_json = set(str(item.get('Nombre_Beneficiario', '')).strip().upper() for item in json_data if 'Nombre_Beneficiario' in item)
coincidentes_nom = informe_df[informe_df['Nombre'].str.strip().str.upper().isin(nombres_json)]

# Unir ambos resultados y eliminar duplicados
coincidentes = pd.concat([coincidentes_num, coincidentes_nom]).drop_duplicates()

# Separar nombres y apellidos
nombres = []
apellidos = []
for nombre_completo in coincidentes['Nombre']:
    partes = str(nombre_completo).strip().split()
    if len(partes) < 3:
        nombres.append(' '.join(partes[:-1]))
        apellidos.append(partes[-1] if partes else '')
    else:
        nombres.append(' '.join(partes[:-2]))
        apellidos.append(' '.join(partes[-2:]))



# Lógica para TELÉFONO MÓVIL y TIPO TELÉFONO MÓVIL
telefonos = []
tipos_telefono = []
for idx, row in coincidentes.iterrows():
    tel_list = []
    tipo_list = []
    # Personal
    if pd.notna(row['Celular_Personal']) and str(row['Celular_Personal']).strip():
        tel_list.append(str(row['Celular_Personal']))
        tipo_list.append('PERSONAL')
    elif pd.notna(row['Tel_Personal']) and str(row['Tel_Personal']).strip():
        tel_list.append(str(row['Tel_Personal']))
        tipo_list.append('PERSONAL')
    # Oficina
    if pd.notna(row['Celular_Laboral']) and str(row['Celular_Laboral']).strip():
        tel_list.append(str(row['Celular_Laboral']))
        tipo_list.append('OFICINA')
    if pd.notna(row['Tel_Laboral']) and str(row['Tel_Laboral']).strip():
        tel_list.append(str(row['Tel_Laboral']))
        tipo_list.append('OFICINA')
    # Unir resultados
    telefonos.append(', '.join(tel_list) if tel_list else '')
    tipos_telefono.append(', '.join(tipo_list) if tipo_list else '')


# Lógica para EMAIL y TIPO EMAIL
emails = []
tipos_email = []
for idx, row in coincidentes.iterrows():
    email = ''
    tipo = ''
    if pd.notna(row['Mail_Personal']) and str(row['Mail_Personal']).strip():
        email = str(row['Mail_Personal'])
        tipo = 'PERSONAL'
    elif pd.notna(row['Mail_Laboral']) and str(row['Mail_Laboral']).strip():
        email = str(row['Mail_Laboral'])
        tipo = 'OFICINA'
    emails.append(email)
    tipos_email.append(tipo)

# Calcular dígito de verificación para NIT en columna Z
dv_list = []
for tipo, doc in zip(coincidentes['Tipo_Doc'], coincidentes['Identificacion']):
    tipo_mapeado = map_tipo_doc(tipo)
    if tipo_mapeado == 'NIT':
        dv_list.append(calcular_dv(doc))
    else:
        dv_list.append('')

# Construir DataFrame para plantilla incluyendo Género, teléfonos, email, dirección y DV NIT
def map_genero(valor):
    valor = str(valor).strip().upper()
    if valor == 'M':
        return 'MASCULINO'
    elif valor == 'F':
        return 'FEMENINO'
    else:
        return ''

plantilla_df = pd.DataFrame({
    'NOMBRES': nombres,
    'APELLIDOS': apellidos,
    'NÚMERO DE DOCUMENTO': coincidentes['Identificacion'],
    'TIPO DE DOCUMENTO': coincidentes['Tipo_Doc'].apply(map_tipo_doc),
    'GÉNERO': coincidentes['Genero'].apply(map_genero),
    'TELÉFONO MÓVIL': telefonos,
    'TIPO TELÉFONO MÓVIL': tipos_telefono,
    'EMAIL': emails,
    'TIPO EMAIL': tipos_email,
    'DIRECCIÓN PRINCIPAL': coincidentes['Direccion_Personal'],
    'DV_NIT': dv_list
})

# Exportar a Excel
plantilla_df.to_excel(salida_path, index=False)
print(f'Archivo de plantilla exportado con coincidencias en: {salida_path}')
