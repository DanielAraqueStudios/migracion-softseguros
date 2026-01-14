import pandas as pd
from datetime import datetime
import re

def limpiar_identificacion(valor):
    """Elimina caracteres no numéricos de una identificación"""
    if pd.isna(valor) or valor == '':
        return ''
    return re.sub(r'\D', '', str(valor))

def limpiar_nit_sin_dv(valor):
    """Elimina caracteres no numéricos Y el último dígito si es NIT (>9 dígitos)"""
    if pd.isna(valor) or valor == '':
        return ''
    limpio = re.sub(r'\D', '', str(valor))
    if len(limpio) > 9:
        return limpio[:-1]
    return limpio

def obtener_columna(df, posibles_nombres):
    """Busca la primera columna que coincida con los nombres posibles"""
    for nombre in posibles_nombres:
        if nombre in df.columns:
            return nombre
    return None

def obtener_valor(row, posibles_nombres, default=''):
    """Obtiene el primer valor no vacío de las columnas posibles"""
    for nombre in posibles_nombres:
        if nombre in row.index and pd.notna(row[nombre]) and str(row[nombre]).strip() != '':
            return str(row[nombre]).strip()
    return default

def separar_nombre_apellidos(nombre_completo):
    """Separa nombre completo en nombres y apellidos"""
    if not nombre_completo or nombre_completo.strip() == '':
        return '', ''
    
    nombre_str = nombre_completo.strip()
    
    # Si tiene coma, formato es "APELLIDOS, NOMBRES"
    if ',' in nombre_str:
        partes = nombre_str.split(',', 1)
        apellidos = partes[0].strip()
        nombres = partes[1].strip() if len(partes) > 1 else ''
        return nombres, apellidos
    
    # Sin coma: asumir primeras 2 palabras son apellidos, resto son nombres
    palabras = nombre_str.split()
    if len(palabras) <= 2:
        return "", nombre_str
    elif len(palabras) == 3:
        apellidos = " ".join(palabras[:2])
        nombres = palabras[2]
        return nombres, apellidos
    else:
        apellidos = " ".join(palabras[:2])
        nombres = " ".join(palabras[2:])
        return nombres, apellidos

def mapear_tipo_documento(tipo_doc):
    """Mapea tipos de documento a formato SoftSeguros"""
    tipo_limpio = str(tipo_doc).strip().upper()
    mapeo = {
        'CC': 'Cédula de ciudadanía',
        'CE': 'Cédula de extranjería',
        'NIT': 'NIT',
        'TI': 'Tarjeta de identidad',
        'PA': 'Pasaporte',
        'RC': 'Registro civil'
    }
    return mapeo.get(tipo_limpio, tipo_limpio)

def mapear_genero(genero):
    """Mapea género a formato SoftSeguros"""
    genero_limpio = str(genero).strip().upper()
    if genero_limpio in ['M', 'MASCULINO', 'HOMBRE']:
        return 'Masculino'
    elif genero_limpio in ['F', 'FEMENINO', 'MUJER']:
        return 'Femenino'
    return genero_limpio

def mapear_estado_civil(estado):
    """Mapea estado civil a formato SoftSeguros"""
    estado_limpio = str(estado).strip().upper()
    mapeo = {
        'S': 'Soltero',
        'C': 'Casado',
        'U': 'Unión libre',
        'V': 'Viudo',
        'D': 'Divorciado'
    }
    return mapeo.get(estado_limpio, estado_limpio)

def main():
    print("=" * 70)
    print("  CORREGIR ERRORES SOFTSEGUROS - DUAL SOURCE (CELER + CLIENTES)")
    print("=" * 70)
    
    # Rutas de archivos
    base_path = "c:/Users/danie/Documents/EMPRESA/SEGUROS UNIÓN/AUTOMATIZACIONES/migraciones/migracion-softseguros"
    
    archivo_errores = f"{base_path}/produccion_a_un_año/DESCARGA ENERO 07 DE SOFTSEGUROS/errores softseguros/errores.xlsx"
    archivo_celer = f"{base_path}/conciliador_clientes/data_celer/InformedePersonas CELER.xlsx"
    archivo_clientes = f"{base_path}/conciliador_clientes/clientes_activos/CLIENTES ACTIVOS.xlsx"
    archivo_plantilla = f"{base_path}/conciliador_clientes/plantilla/PLANTILLA DE SOTSEGUROS.xlsx"
    
    # 1. Leer documentos del archivo de errores
    print("\n[1] LEYENDO DOCUMENTOS DE ERRORES.XLSX")
    print("-" * 50)
    
    df_errores = pd.read_excel(archivo_errores, header=0, dtype=str)
    print(f"  [OK] Registros en errores: {len(df_errores)}")
    print(f"  [DEBUG] Columnas detectadas: {list(df_errores.columns)}")
    
    # Verificar que existe la columna
    if 'DOCUMENTO DEL CLIENTE' not in df_errores.columns:
        print(f"  [ERROR] No se encontró la columna 'DOCUMENTO DEL CLIENTE'")
        print(f"  Columnas disponibles: {list(df_errores.columns)}")
        return
    
    # Extraer documentos únicos
    documentos_buscar = df_errores['DOCUMENTO DEL CLIENTE'].dropna().apply(limpiar_identificacion).unique().tolist()
    documentos_buscar = [d for d in documentos_buscar if d]
    
    print(f"  [OK] Documentos únicos a buscar: {len(documentos_buscar)}")
    print(f"  Ejemplos: {documentos_buscar[:5]}")
    
    # 2. Leer archivo de CELER
    print("\n[2] LEYENDO DATOS DE CELER")
    print("-" * 50)
    
    df_celer = pd.read_excel(archivo_celer, header=3, dtype=str)
    print(f"  [OK] Registros en Celer: {len(df_celer)}")
    
    # Detectar columna de identificación en Celer
    col_id_celer = obtener_columna(df_celer, ['Identificacion', 'Identificación', 'IDENTIFICACION'])
    if not col_id_celer:
        print("  [ERROR] No se encontró columna de identificación en Celer")
        return
    
    # Crear columnas de búsqueda en Celer (con y sin DV)
    df_celer['_id_limpia'] = df_celer[col_id_celer].apply(limpiar_identificacion)
    df_celer['_id_sin_dv'] = df_celer[col_id_celer].apply(limpiar_nit_sin_dv)
    df_celer['_id_original'] = df_celer[col_id_celer]  # Conservar con DV
    
    print(f"  [DEBUG] Ejemplos Celer:")
    for idx, row in df_celer.head(3).iterrows():
        print(f"    Original: '{row['_id_original']}' -> Limpia: '{row['_id_limpia']}' -> Sin DV: '{row['_id_sin_dv']}'")
    
    # 3. Leer archivo de Clientes Activos
    print("\n[3] LEYENDO CLIENTES ACTIVOS")
    print("-" * 50)
    
    df_clientes = pd.read_excel(archivo_clientes, header=3, dtype=str)
    print(f"  [OK] Registros en Clientes Activos: {len(df_clientes)}")
    
    # Crear columnas de búsqueda en Clientes (con y sin DV)
    df_clientes['_id_limpia'] = df_clientes['Identificacion'].apply(limpiar_identificacion)
    df_clientes['_id_sin_dv'] = df_clientes['Identificacion'].apply(limpiar_nit_sin_dv)
    df_clientes['_id_original'] = df_clientes['Identificacion']  # Conservar con DV
    
    print(f"  [DEBUG] Ejemplos Clientes:")
    for idx, row in df_clientes.head(3).iterrows():
        print(f"    Original: '{row['_id_original']}' -> Limpia: '{row['_id_limpia']}' -> Sin DV: '{row['_id_sin_dv']}'")
    
    # 4. Leer estructura de plantilla
    print("\n[4] PREPARANDO PLANTILLA SOFTSEGUROS")
    print("-" * 50)
    
    df_plantilla = pd.read_excel(archivo_plantilla, nrows=0)
    columnas_plantilla = list(df_plantilla.columns)
    print(f"  [OK] Columnas en plantilla: {len(columnas_plantilla)}")
    
    # 5. Buscar y mapear datos (primero Celer, luego Clientes)
    print("\n[5] BUSCANDO Y MAPEANDO DATOS")
    print("-" * 50)
    
    registros_encontrados = []
    no_encontrados = []
    docs_ya_agregados = set()
    
    for doc in documentos_buscar:
        # Buscar primero en CELER
        match_celer = df_celer[(df_celer['_id_limpia'] == doc) | (df_celer['_id_sin_dv'] == doc)]
        
        if len(match_celer) > 0:
            # Encontrado en CELER
            if doc in docs_ya_agregados:
                continue
            docs_ya_agregados.add(doc)
            
            row = match_celer.iloc[0]
            
            # Obtener tipo de documento primero para decidir si separar nombre
            tipo_doc = obtener_valor(row, ['Tipo_Doc', 'TIPO_DOC', 'TipoDoc', 'Tipo_Documento'])
            nombre_completo = obtener_valor(row, ['Nombre', 'NOMBRE', 'Nombre_Completo'])
            
            # Solo separar nombres/apellidos si NO es NIT
            if tipo_doc.upper() == 'NIT':
                nombres = nombre_completo
                apellidos = ''
            else:
                nombres, apellidos = separar_nombre_apellidos(nombre_completo)
            
            # Obtener todos los valores de Celer
            identificacion = str(row['_id_original']).strip()
            genero = obtener_valor(row, ['Genero', 'GENERO', 'Género', 'GÉNERO', 'Sexo'])
            estado_civil = obtener_valor(row, ['Estado_civil', 'ESTADO_CIVIL', 'EstadoCivil'])
            f_nacimiento = obtener_valor(row, ['F_Nacimiento', 'FECHA_NACIMIENTO', 'Fecha_Nacimiento'])
            cel_personal = obtener_valor(row, ['Celular_Personal', 'CELULAR_PERSONAL', 'Cel_Pers', 'Celular'])
            tel_personal = obtener_valor(row, ['Tel_Personal', 'TEL_PERSONAL', 'Telefono_Pers', 'Telefono'])
            tel_laboral = obtener_valor(row, ['Tel_Laboral', 'TEL_LABORAL', 'Telefono_Lab'])
            mail_personal = obtener_valor(row, ['Mail_Personal', 'MAIL_PERSONAL', 'Email_Personal', 'Email', 'Correo'])
            mail_laboral = obtener_valor(row, ['Mail_Laboral', 'MAIL_LABORAL', 'Email_Laboral'])
            dir_personal = obtener_valor(row, ['Direccion_Personal', 'DIRECCION_PERSONAL', 'Dir_Pers', 'Direccion'])
            dir_laboral = obtener_valor(row, ['Direccion_Laboral', 'DIRECCION_LABORAL', 'Dir_Lab'])
            ciudad = obtener_valor(row, ['Ciudad_Personal', 'CIUDAD_PERSONAL', 'Ciudad'])
            ocupacion = obtener_valor(row, ['Ocupacion', 'OCUPACION', 'Ocupación', 'Profesion'])
            observaciones = obtener_valor(row, ['Observaciones', 'OBSERVACIONES', 'Obs'])
            
            # Mostrar en consola
            if tipo_doc.upper() == 'NIT':
                print(f"  [CELER] {doc}: {nombres}")
            else:
                print(f"  [CELER] {doc}: {apellidos} {nombres}")
            
            registro = {
                'NOMBRES': nombres,
                'APELLIDOS': apellidos,
                'SOBRENOMBRE (ALIAS)': '',
                'NÚMERO DE DOCUMENTO': identificacion,
                'TIPO DE DOCUMENTO': mapear_tipo_documento(tipo_doc),
                'GÉNERO': mapear_genero(genero),
                'ESTADO CIVIL': mapear_estado_civil(estado_civil),
                'FECHA DE NACIMIENTO': f_nacimiento,
                'TELÉFONO MÓVIL': cel_personal,
                'TIPO TELÉFONO MÓVIL': 'Personal' if cel_personal else '',
                'TELÉFONO PRINCIPAL': tel_personal,
                'TIPO DE TELÉFONO PRINCIPAL': 'Personal' if tel_personal else '',
                'TELÉFONO SECUNDARIO': tel_laboral,
                'TIPO DE TELÉFONO SECUNDARIO': 'Laboral' if tel_laboral else '',
                'EMAIL': mail_personal,
                'TIPO EMAIL': 'Personal' if mail_personal else '',
                'EMAIL SECUNDARIO': mail_laboral,
                'TIPO EMAIL SECUNDARIO': 'Laboral' if mail_laboral else '',
                'DIRECCIÓN PRINCIPAL': dir_personal,
                'TIPO DIRECCIÓN': 'Personal' if dir_personal else '',
                'DIRECCIÓN SECUNDARIA': dir_laboral,
                'TIPO DIRECCIÓN SECUNDARIA': 'Laboral' if dir_laboral else '',
                'PAÍS': 'Colombia',
                'ESTADO': '',
                'CIUDAD': ciudad,
                'OCUPACIÓN': ocupacion,
                'INGRESO MENSUAL': '',
                'PATRIMONIO': '',
                'CASA PROPIA': '',
                'NÚMERO DE CASAS': '',
                'HIJOS': '',
                'NÚMERO DE HIJOS': '',
                'VEHÍCULOS': '',
                'NÚMERO DE VEHÍCULOS': '',
                'PAGINA WEB': '',
                'REDES SOCIALES': '',
                'NOMBRE DE CONTACTO': '',
                'CATEGORÍAS': '',
                'OBSERVACIONES': observaciones,
                'CARGADO POR': 'Migración Automática'
            }
            registros_encontrados.append(registro)
            continue
        
        # Si no está en CELER, buscar en CLIENTES ACTIVOS
        match_clientes = df_clientes[(df_clientes['_id_limpia'] == doc) | (df_clientes['_id_sin_dv'] == doc)]
        
        if len(match_clientes) > 0:
            # Encontrado en CLIENTES ACTIVOS
            if doc in docs_ya_agregados:
                continue
            docs_ya_agregados.add(doc)
            
            row = match_clientes.iloc[0]
            
            # Para empresas: nombre en NOMBRES, APELLIDOS vacío
            nombre_empresa = obtener_valor(row, ['Tomador', 'Nombre', 'NOMBRE'])
            identificacion = str(row['_id_original']).strip()
            telefono = obtener_valor(row, ['Telefono', 'TELEFONO', 'Celular'])
            email = obtener_valor(row, ['Email', 'Correo', 'EMAIL'])
            direccion = obtener_valor(row, ['Direccion', 'DIRECCION'])
            ciudad = obtener_valor(row, ['Ciudad', 'CIUDAD'])
            
            print(f"  [CLIENTES] {doc}: {nombre_empresa}")
            
            registro = {
                'NOMBRES': nombre_empresa,
                'APELLIDOS': '',
                'SOBRENOMBRE (ALIAS)': '',
                'NÚMERO DE DOCUMENTO': identificacion,
                'TIPO DE DOCUMENTO': 'NIT',
                'GÉNERO': '',
                'ESTADO CIVIL': '',
                'FECHA DE NACIMIENTO': '',
                'TELÉFONO MÓVIL': telefono,
                'TIPO TELÉFONO MÓVIL': 'Principal' if telefono else '',
                'TELÉFONO PRINCIPAL': '',
                'TIPO DE TELÉFONO PRINCIPAL': '',
                'TELÉFONO SECUNDARIO': '',
                'TIPO DE TELÉFONO SECUNDARIO': '',
                'EMAIL': email,
                'TIPO EMAIL': 'Principal' if email else '',
                'EMAIL SECUNDARIO': '',
                'TIPO EMAIL SECUNDARIO': '',
                'DIRECCIÓN PRINCIPAL': direccion,
                'TIPO DIRECCIÓN': 'Principal' if direccion else '',
                'DIRECCIÓN SECUNDARIA': '',
                'TIPO DIRECCIÓN SECUNDARIA': '',
                'PAÍS': 'Colombia',
                'ESTADO': '',
                'CIUDAD': ciudad,
                'OCUPACIÓN': '',
                'INGRESO MENSUAL': '',
                'PATRIMONIO': '',
                'CASA PROPIA': '',
                'NÚMERO DE CASAS': '',
                'HIJOS': '',
                'NÚMERO DE HIJOS': '',
                'VEHÍCULOS': '',
                'NÚMERO DE VEHÍCULOS': '',
                'PAGINA WEB': '',
                'REDES SOCIALES': '',
                'NOMBRE DE CONTACTO': '',
                'CATEGORÍAS': '',
                'OBSERVACIONES': '',
                'CARGADO POR': 'Migración Automática'
            }
            registros_encontrados.append(registro)
            continue
        
        # No encontrado en ninguna fuente
        no_encontrados.append(doc)
        print(f"  [X] {doc}: No encontrado")
    
    print(f"\n  Encontrados: {len(registros_encontrados)}")
    print(f"  No encontrados: {len(no_encontrados)}")
    
    # 6. Crear DataFrame con estructura de plantilla
    print("\n[6] GENERANDO PLANTILLA CORREGIDA")
    print("-" * 50)
    
    df_salida = pd.DataFrame(registros_encontrados)
    
    # Agregar columnas faltantes de la plantilla
    for col in columnas_plantilla:
        if col not in df_salida.columns:
            df_salida[col] = ''
    
    # Reordenar según plantilla
    df_salida = df_salida[columnas_plantilla]
    
    # 7. Guardar archivos
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    archivo_salida = f"{base_path}/conciliador_clientes/plantilla/PLANTILLA_CORREGIDA_{timestamp}.xlsx"
    archivo_no_encontrados = f"{base_path}/conciliador_clientes/ERRORES/documentos_no_encontrados_{timestamp}.xlsx"
    
    # Guardar plantilla corregida
    df_salida.to_excel(archivo_salida, index=False, engine='openpyxl')
    print(f"  [OK] Plantilla guardada: PLANTILLA_CORREGIDA_{timestamp}.xlsx")
    print(f"  [OK] Registros: {len(df_salida)}")
    print(f"  [OK] Ruta: {archivo_salida}")
    
    # Guardar no encontrados
    if no_encontrados:
        df_no_encontrados = pd.DataFrame({'Documento': no_encontrados})
        df_no_encontrados.to_excel(archivo_no_encontrados, index=False, engine='openpyxl')
        print(f"  [INFO] Documentos no encontrados guardados en: documentos_no_encontrados_{timestamp}.xlsx")
    
    print("\n" + "=" * 70)
    print("  PROCESO COMPLETADO")
    print("=" * 70)

if __name__ == '__main__':
    main()
