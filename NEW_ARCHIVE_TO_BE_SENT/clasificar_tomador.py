import pandas as pd
import re
import logging
import os

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

# Configurar logging
logging.basicConfig(filename='clasificacion_tomador.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def clasificar_tomador(nombre):
    """
    Clasifica si el nombre del tomador es persona o empresa.
    - Persona: Nombres propios con 2-4 palabras, sin términos empresariales.
    - Empresa: Contiene términos empresariales o es todo mayúsculas con varias palabras.
    """
    if pd.isna(nombre) or str(nombre).strip() == '':
        return 'DESCONOCIDO'

    nombre_str = str(nombre).strip()
    nombre_upper = nombre_str.upper()
    palabras = nombre_upper.split()

    # Términos de empresa
    terminos_empresa = [
        'S.A.', 'LTDA.', 'SAS', 'CIA', 'LIMITADA',
        'SOCIEDAD', 'ASOCIADOS', 'GRUPO', 'CORPORACION',
        'COOPERATIVA', 'FONDO', 'DEPARTAMENTO', 'EMPLEADOS',
        'SENA', 'AFROAMERICANA', 'PARROQUIAL', 'COLEGIO',
        'INSTITUTO', 'VICARIAL', 'ACINPRO', 'COOSANROQUE'
    ]

    if any(termino in nombre_upper for termino in terminos_empresa):
        return 'EMPRESA'

    # Si tiene más de 4 palabras, probablemente empresa
    if len(palabras) > 4:
        return 'EMPRESA'

    # Si es 2-4 palabras y no contiene términos empresariales, persona
    if len(palabras) in [2, 3, 4]:
        return 'PERSONA'

    # Default: si es mayúsculas con más de 2 palabras, empresa; sino, persona
    if nombre_str == nombre_upper and len(palabras) > 2:
        return 'EMPRESA'
    else:
        return 'PERSONA'

def ajustar_documento(documento, tipo):
    """
    Ajusta el documento según el tipo.
    - Persona: Quitar dígito de verificación si lo tiene.
    - Empresa: Asegurar que tenga dígito de verificación (calcular si no lo tiene).
    """
    if pd.isna(documento) or str(documento).strip() == '':
        return documento, tipo  # Retornar también tipo por si cambia

    doc_str = str(documento).strip()

    # Limpiar formato float (.0)
    if doc_str.endswith('.0'):
        doc_str = doc_str[:-2]

    if tipo == 'PERSONA':
        # Quitar dígito si tiene formato NIT (número-guion-dígito)
        if re.match(r'^\d+-\d$', doc_str):
            return doc_str.split('-')[0], tipo
        return doc_str, tipo
    elif tipo == 'EMPRESA':
        # Si no tiene dígito, calcular y agregar
        if not re.match(r'^\d+-\d$', doc_str):
            dv = calcular_dv(doc_str)
            if dv:
                return f"{doc_str}-{dv}", tipo
            else:
                return doc_str, tipo  # Si no se puede calcular, dejar como está
        return doc_str, tipo
    return doc_str, tipo

# Ruta del archivo
archivo = 'Plantilla POLIZAS Actulizada.xlsx'

# Leer Excel
df = pd.read_excel(archivo)

# Columnas
col_aa = 'NOMBRE DEL TOMADOR'  # AA
col_ab = 'DOCUMENTO DEL TOMADOR'  # AB
col_ac = 'NOMBRE DEL ASEGURADO'  # AC
col_ad = 'DOCUMENTO DEL ASEGURADO'  # AD
col_z = 'DOCUMENTO DEL CLIENTE'  # Z

# Procesar cada fila
for i, (idx, row) in enumerate(df.iterrows()):
    fila_num = i + 1
    nombre_tomador = row[col_aa]
    documento_tomador = row[col_ab]
    nombre_asegurado = row[col_ac]
    documento_asegurado = row[col_ad]
    documento_cliente = row[col_z]

    # Clasificar y ajustar TOMADOR
    tipo_tomador = clasificar_tomador(nombre_tomador)
    nuevo_documento_tomador, tipo_final_tomador = ajustar_documento(documento_tomador, tipo_tomador)
    tipo_tomador = tipo_final_tomador

    # Clasificar y ajustar ASEGURADO
    tipo_asegurado = clasificar_tomador(nombre_asegurado)
    nuevo_documento_asegurado, tipo_final_asegurado = ajustar_documento(documento_asegurado, tipo_asegurado)
    tipo_asegurado = tipo_final_asegurado

    # Clasificar y ajustar CLIENTE (usando la misma clasificación que TOMADOR)
    nuevo_documento_cliente, _ = ajustar_documento(documento_cliente, tipo_tomador)

    # Log
    logging.info(f"Fila {fila_num}: Tomador='{nombre_tomador}' -> Tipo={tipo_tomador}, Documento='{documento_tomador}' -> '{nuevo_documento_tomador}'")
    logging.info(f"Fila {fila_num}: Asegurado='{nombre_asegurado}' -> Tipo={tipo_asegurado}, Documento='{documento_asegurado}' -> '{nuevo_documento_asegurado}'")
    logging.info(f"Fila {fila_num}: Cliente -> Tipo={tipo_tomador}, Documento='{documento_cliente}' -> '{nuevo_documento_cliente}'")

    # Actualizar DataFrame
    df.loc[i, col_ab] = str(nuevo_documento_tomador) if pd.notna(nuevo_documento_tomador) else ''
    df.loc[i, col_ad] = str(nuevo_documento_asegurado) if pd.notna(nuevo_documento_asegurado) else ''
    df.loc[i, col_z] = str(nuevo_documento_cliente) if pd.notna(nuevo_documento_cliente) else ''

# Guardar Excel modificado
df.to_excel('Plantilla POLIZAS_Clasificada_v4.xlsx', index=False)

print("Procesamiento completado. Archivo guardado como 'Plantilla POLIZAS_Clasificada_v4.xlsx'")
print("Se procesaron las columnas DOCUMENTO DEL TOMADOR (AB), DOCUMENTO DEL ASEGURADO (AD) y DOCUMENTO DEL CLIENTE (Z)")
print("Revisa 'clasificacion_tomador.log' para detalles.")