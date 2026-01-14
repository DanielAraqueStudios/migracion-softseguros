#!/usr/bin/env python3
"""
Programa para llenar la plantilla de SoftSeguros con datos de Celer.

Busca los NITs/cédulas en el archivo de Celer y llena la plantilla de SoftSeguros.
"""

import pandas as pd
import re
import os
from datetime import datetime


def separar_nombre_apellidos(nombre_completo):
    """
    Separa el nombre completo en nombres y apellidos.
    Asume formato: APELLIDO1 APELLIDO2 NOMBRE1 NOMBRE2
    o: APELLIDO1 APELLIDO2, NOMBRE1 NOMBRE2 (con coma)
    """
    if pd.isna(nombre_completo) or not str(nombre_completo).strip():
        return "", ""
    
    nombre_str = str(nombre_completo).strip().upper()
    
    # Si tiene coma, separar por coma (APELLIDOS, NOMBRES)
    if ',' in nombre_str:
        partes = nombre_str.split(',', 1)
        apellidos = partes[0].strip()
        nombres = partes[1].strip() if len(partes) > 1 else ""
        return nombres, apellidos
    
    # Sin coma: asumir primeras 2 palabras son apellidos, resto son nombres
    palabras = nombre_str.split()
    if len(palabras) <= 2:
        # Solo 1-2 palabras: todo como apellido
        return "", nombre_str
    elif len(palabras) == 3:
        # 3 palabras: 2 apellidos, 1 nombre
        apellidos = " ".join(palabras[:2])
        nombres = palabras[2]
        return nombres, apellidos
    else:
        # 4+ palabras: 2 apellidos, resto nombres
        apellidos = " ".join(palabras[:2])
        nombres = " ".join(palabras[2:])
        return nombres, apellidos


def mapear_tipo_documento(tipo_celer):
    """Mapea el tipo de documento de Celer a SoftSeguros"""
    if pd.isna(tipo_celer):
        return ""
    
    tipo = str(tipo_celer).upper().strip()
    
    mapeo = {
        'CC': 'Cédula de ciudadanía',
        'CEDULA': 'Cédula de ciudadanía',
        'CEDULA DE CIUDADANIA': 'Cédula de ciudadanía',
        'NIT': 'NIT',
        'CE': 'Cédula de extranjería',
        'CEDULA DE EXTRANJERIA': 'Cédula de extranjería',
        'TI': 'Tarjeta de identidad',
        'TARJETA DE IDENTIDAD': 'Tarjeta de identidad',
        'PA': 'Pasaporte',
        'PASAPORTE': 'Pasaporte',
        'RC': 'Registro civil',
        'REGISTRO CIVIL': 'Registro civil',
    }
    
    return mapeo.get(tipo, tipo)


def mapear_genero(genero_celer):
    """Mapea el género de Celer a SoftSeguros"""
    if pd.isna(genero_celer):
        return ""
    
    genero = str(genero_celer).upper().strip()
    
    if genero in ['M', 'MASCULINO', 'HOMBRE']:
        return 'Masculino'
    elif genero in ['F', 'FEMENINO', 'MUJER']:
        return 'Femenino'
    
    return genero


def mapear_estado_civil(estado_celer):
    """Mapea el estado civil de Celer a SoftSeguros"""
    if pd.isna(estado_celer):
        return ""
    
    estado = str(estado_celer).upper().strip()
    
    mapeo = {
        'S': 'Soltero(a)',
        'SOLTERO': 'Soltero(a)',
        'SOLTERA': 'Soltero(a)',
        'C': 'Casado(a)',
        'CASADO': 'Casado(a)',
        'CASADA': 'Casado(a)',
        'U': 'Unión libre',
        'UNION LIBRE': 'Unión libre',
        'D': 'Divorciado(a)',
        'DIVORCIADO': 'Divorciado(a)',
        'DIVORCIADA': 'Divorciado(a)',
        'V': 'Viudo(a)',
        'VIUDO': 'Viudo(a)',
        'VIUDA': 'Viudo(a)',
    }
    
    return mapeo.get(estado, estado)


def limpiar_identificacion(valor):
    """Limpia la identificación para comparación (solo números)"""
    if pd.isna(valor):
        return ""
    return re.sub(r'\D', '', str(valor))


def limpiar_nit_sin_dv(valor):
    """Limpia NIT y remueve dígito de verificación si existe"""
    if pd.isna(valor):
        return ""
    limpio = re.sub(r'\D', '', str(valor))
    # Si tiene más de 9 dígitos, quitar último (posible DV)
    if len(limpio) > 9:
        return limpio[:-1]
    return limpio


def obtener_columna(df, posibles_nombres):
    """
    Busca y retorna el nombre de la primera columna que coincida con la lista de posibles nombres.
    Retorna None si no encuentra ninguna.
    """
    for nombre in posibles_nombres:
        if nombre in df.columns:
            return nombre
    return None


def obtener_valor(row, posibles_nombres, default=''):
    """
    Obtiene el valor de una columna usando una lista de posibles nombres.
    Retorna el primer valor no vacío encontrado o el valor default.
    """
    for nombre in posibles_nombres:
        if nombre in row.index:
            valor = row.get(nombre)
            if pd.notna(valor) and str(valor).strip():
                return valor
    return default


def main():
    print("=" * 70)
    print("  LLENAR PLANTILLA SOFTSEGUROS CON DATOS DE CELER")
    print("=" * 70)
    
    # Rutas de archivos
    base_path = "c:/Users/danie/Documents/EMPRESA/SEGUROS UNIÓN/AUTOMATIZACIONES/migraciones/migracion-softseguros"
    
    archivo_nits = f"{base_path}/conciliador_clientes/ERRORES/errores_sin_dv_20251202_102025.xlsx"
    archivo_celer = f"{base_path}/conciliador_clientes/data_celer/InformedePersonas CELER.xlsx"
    archivo_plantilla = f"{base_path}/conciliador_clientes/plantilla/PLANTILLA DE SOTSEGUROS.xlsx"
    
    # 1. Leer NITs sin DV (columna A)
    print("\n[1] LEYENDO NITs A BUSCAR")
    print("-" * 50)
    
    df_nits = pd.read_excel(archivo_nits, dtype=str)
    columna_nits = df_nits.columns[0]  # Primera columna (A)
    
    # Obtener lista de NITs únicos (limpios, solo números)
    nits_buscar = df_nits[columna_nits].dropna().apply(limpiar_identificacion).unique().tolist()
    nits_buscar = [n for n in nits_buscar if n]  # Quitar vacíos
    
    print(f"  [OK] NITs a buscar: {len(nits_buscar)}")
    print(f"  Ejemplos: {nits_buscar[:5]}")
    
    # 2. Leer archivo de Celer
    print("\n[2] LEYENDO DATOS DE CELER")
    print("-" * 50)
    
    # Leer con header correcto (fila 4 = índice 3, saltar primeras 3 filas)
    df_celer = pd.read_excel(archivo_celer, header=3, dtype=str)
    print(f"  [OK] Registros en Celer: {len(df_celer)}")
    
    # MOSTRAR COLUMNAS DISPONIBLES
    print(f"\n  [DEBUG] Total de columnas: {len(df_celer.columns)}")
    print(f"  [DEBUG] Columnas disponibles en Celer:")
    for i, col in enumerate(df_celer.columns, 1):
        print(f"    {i:2d}. {col}")
    
    # Detectar columna de identificación automáticamente
    posibles_id = ['Identificacion', 'IDENTIFICACION', 'Identificación', 'NÚMERO DE DOCUMENTO', 
                   'Numero_Documento', 'Documento', 'Cedula', 'NIT']
    
    col_identificacion = None
    for nombre in posibles_id:
        if nombre in df_celer.columns:
            col_identificacion = nombre
            break
    
    # Si no encuentra, usar columna índice 2 (columna C típicamente es ID)
    if col_identificacion is None:
        if len(df_celer.columns) > 2:
            col_identificacion = df_celer.columns[2]
            print(f"\n  [WARN] Columna 'Identificacion' no encontrada, usando columna índice 2: '{col_identificacion}'")
        else:
            print(f"\n  [ERROR] No se puede detectar columna de identificación")
            return
    else:
        print(f"\n  [OK] Columna de identificación detectada: '{col_identificacion}'")
    
    # Crear columnas de identificación limpia para búsqueda (con y sin DV)
    df_celer['_id_limpia'] = df_celer[col_identificacion].apply(limpiar_identificacion)
    df_celer['_id_sin_dv'] = df_celer[col_identificacion].apply(limpiar_nit_sin_dv)
    
    print(f"  [INFO] Ejemplos de limpieza:")
    for i in range(min(3, len(df_celer))):
        orig = df_celer[col_identificacion].iloc[i]
        limpia = df_celer['_id_limpia'].iloc[i]
        sin_dv = df_celer['_id_sin_dv'].iloc[i]
        print(f"    Original: '{orig}' → Limpia: '{limpia}' → Sin DV: '{sin_dv}'")
    
    # 3. Leer estructura de plantilla
    print("\n[3] PREPARANDO PLANTILLA SOFTSEGUROS")
    print("-" * 50)
    
    df_plantilla = pd.read_excel(archivo_plantilla, nrows=0)  # Solo columnas
    columnas_plantilla = list(df_plantilla.columns)
    print(f"  [OK] Columnas en plantilla: {len(columnas_plantilla)}")
    
    # 4. Buscar y mapear datos
    print("\n[4] BUSCANDO Y MAPEANDO DATOS")
    print("-" * 50)
    
    registros_encontrados = []
    no_encontrados = []
    
    for nit in nits_buscar:
        # Buscar en Celer (intentar con identificación completa y sin DV)
        match = df_celer[
            (df_celer['_id_limpia'] == nit) | 
            (df_celer['_id_sin_dv'] == nit)
        ]
        
        if len(match) == 0:
            no_encontrados.append(nit)
            continue
        
        # Tomar primer match
        row = match.iloc[0]
        
        # Separar nombre en nombres y apellidos
        nombres, apellidos = separar_nombre_apellidos(
            obtener_valor(row, ['Nombre', 'NOMBRE', 'Nombre_Completo'])
        )
        
        # Obtener valores con fallback de múltiples posibles nombres de columnas
        identificacion = obtener_valor(row, [col_identificacion, 'Identificacion', 'IDENTIFICACION', 'Identificación'])
        tipo_doc = obtener_valor(row, ['Tipo_Doc', 'TIPO_DOC', 'TipoDoc', 'Tipo_Documento'])
        genero = obtener_valor(row, ['Genero', 'GENERO', 'Género', 'GÉNERO', 'Sexo'])
        estado_civil = obtener_valor(row, ['Estado_civil', 'ESTADO_CIVIL', 'EstadoCivil'])
        f_nacimiento = obtener_valor(row, ['F_Nacimiento', 'FECHA_NACIMIENTO', 'Fecha_Nacimiento'])
        cel_personal = obtener_valor(row, ['Celular_Personal', 'CELULAR_PERSONAL', 'Cel_Pers'])
        tel_personal = obtener_valor(row, ['Tel_Personal', 'TEL_PERSONAL', 'Telefono_Pers'])
        tel_laboral = obtener_valor(row, ['Tel_Laboral', 'TEL_LABORAL', 'Telefono_Lab'])
        mail_personal = obtener_valor(row, ['Mail_Personal', 'MAIL_PERSONAL', 'Email_Personal'])
        mail_laboral = obtener_valor(row, ['Mail_Laboral', 'MAIL_LABORAL', 'Email_Laboral'])
        dir_personal = obtener_valor(row, ['Direccion_Personal', 'DIRECCION_PERSONAL', 'Dir_Pers'])
        dir_laboral = obtener_valor(row, ['Direccion_Laboral', 'DIRECCION_LABORAL', 'Dir_Lab'])
        ciudad = obtener_valor(row, ['Ciudad_Personal', 'CIUDAD_PERSONAL', 'Ciudad'])
        ocupacion = obtener_valor(row, ['Ocupacion', 'OCUPACION', 'Ocupación', 'Profesion'])
        observaciones = obtener_valor(row, ['Observaciones', 'OBSERVACIONES', 'Obs'])
        
        # Crear registro para plantilla
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
        print(f"  [OK] {nit}: {nombres} {apellidos}")
    
    print(f"\n  Encontrados: {len(registros_encontrados)}")
    print(f"  No encontrados: {len(no_encontrados)}")
    
    if no_encontrados:
        print(f"\n  NITs no encontrados en Celer:")
        for nit in no_encontrados[:10]:
            print(f"    - {nit}")
        if len(no_encontrados) > 10:
            print(f"    ... y {len(no_encontrados) - 10} más")
    
    # 5. Crear DataFrame y guardar
    print("\n[5] GUARDANDO PLANTILLA LLENA")
    print("-" * 50)
    
    if registros_encontrados:
        df_resultado = pd.DataFrame(registros_encontrados)
        
        # Asegurar que tenga todas las columnas de la plantilla
        for col in columnas_plantilla:
            if col not in df_resultado.columns:
                df_resultado[col] = ''
        
        # Reordenar columnas según plantilla
        df_resultado = df_resultado[columnas_plantilla]
        
        # Guardar
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        archivo_salida = f"{base_path}/conciliador_clientes/plantilla/PLANTILLA_LLENA_{timestamp}.xlsx"
        
        df_resultado.to_excel(archivo_salida, index=False, engine='openpyxl')
        
        print(f"  [OK] Archivo guardado: {os.path.basename(archivo_salida)}")
        print(f"  [OK] Registros: {len(df_resultado)}")
        print(f"  [OK] Ruta: {archivo_salida}")
    else:
        print("  [WARN] No se encontraron registros para guardar")
    
    # 6. Guardar no encontrados
    if no_encontrados:
        archivo_no_encontrados = f"{base_path}/conciliador_clientes/ERRORES/nits_no_encontrados_{timestamp}.xlsx"
        df_no_enc = pd.DataFrame({'NIT_NO_ENCONTRADO': no_encontrados})
        df_no_enc.to_excel(archivo_no_encontrados, index=False)
        print(f"\n  [INFO] NITs no encontrados guardados en: {os.path.basename(archivo_no_encontrados)}")
    
    print("\n" + "=" * 70)
    print("  PROCESO COMPLETADO")
    print("=" * 70)


if __name__ == "__main__":
    main()
