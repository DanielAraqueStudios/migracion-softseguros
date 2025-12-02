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
    
    df_celer = pd.read_excel(archivo_celer, dtype=str)
    print(f"  [OK] Registros en Celer: {len(df_celer)}")
    
    # Crear columna de identificación limpia para búsqueda
    df_celer['_id_limpia'] = df_celer['Identificacion'].apply(limpiar_identificacion)
    
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
        # Buscar en Celer
        match = df_celer[df_celer['_id_limpia'] == nit]
        
        if len(match) == 0:
            no_encontrados.append(nit)
            continue
        
        # Tomar primer match
        row = match.iloc[0]
        
        # Separar nombre en nombres y apellidos
        nombres, apellidos = separar_nombre_apellidos(row.get('Nombre', ''))
        
        # Crear registro para plantilla
        registro = {
            'NOMBRES': nombres,
            'APELLIDOS': apellidos,
            'SOBRENOMBRE (ALIAS)': '',
            'NÚMERO DE DOCUMENTO': row.get('Identificacion', ''),
            'TIPO DE DOCUMENTO': mapear_tipo_documento(row.get('Tipo_Doc', '')),
            'GÉNERO': mapear_genero(row.get('Genero', '')),
            'ESTADO CIVIL': mapear_estado_civil(row.get('Estado_civil', '')),
            'FECHA DE NACIMIENTO': row.get('F_Nacimiento', ''),
            'TELÉFONO MÓVIL': row.get('Celular_Personal', ''),
            'TIPO TELÉFONO MÓVIL': 'Personal' if pd.notna(row.get('Celular_Personal')) and row.get('Celular_Personal') else '',
            'TELÉFONO PRINCIPAL': row.get('Tel_Personal', ''),
            'TIPO DE TELÉFONO PRINCIPAL': 'Personal' if pd.notna(row.get('Tel_Personal')) and row.get('Tel_Personal') else '',
            'TELÉFONO SECUNDARIO': row.get('Tel_Laboral', ''),
            'TIPO DE TELÉFONO SECUNDARIO': 'Laboral' if pd.notna(row.get('Tel_Laboral')) and row.get('Tel_Laboral') else '',
            'EMAIL': row.get('Mail_Personal', ''),
            'TIPO EMAIL': 'Personal' if pd.notna(row.get('Mail_Personal')) and row.get('Mail_Personal') else '',
            'EMAIL SECUNDARIO': row.get('Mail_Laboral', ''),
            'TIPO EMAIL SECUNDARIO': 'Laboral' if pd.notna(row.get('Mail_Laboral')) and row.get('Mail_Laboral') else '',
            'DIRECCIÓN PRINCIPAL': row.get('Direccion_Personal', ''),
            'TIPO DIRECCIÓN': 'Personal' if pd.notna(row.get('Direccion_Personal')) and row.get('Direccion_Personal') else '',
            'DIRECCIÓN SECUNDARIA': row.get('Direccion_Laboral', ''),
            'TIPO DIRECCIÓN SECUNDARIA': 'Laboral' if pd.notna(row.get('Direccion_Laboral')) and row.get('Direccion_Laboral') else '',
            'PAÍS': 'Colombia',
            'ESTADO': '',
            'CIUDAD': row.get('Ciudad_Personal', ''),
            'OCUPACIÓN': row.get('Ocupacion', ''),
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
            'OBSERVACIONES': row.get('Observaciones', ''),
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
