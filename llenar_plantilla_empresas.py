#!/usr/bin/env python3
"""
Programa para llenar la plantilla de SoftSeguros con empresas desde Clientes Activos.

Busca los NITs no encontrados en Celer y los busca en el archivo de Clientes Activos.
"""

import pandas as pd
import re
import os
from datetime import datetime


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


def main():
    print("=" * 70)
    print("  LLENAR PLANTILLA SOFTSEGUROS - EMPRESAS (CLIENTES ACTIVOS)")
    print("=" * 70)
    
    # Rutas de archivos
    base_path = "c:/Users/danie/Documents/EMPRESA/SEGUROS UNIÓN/AUTOMATIZACIONES/migraciones/migracion-softseguros"
    
    # Usar archivo más reciente de NITs no encontrados
    archivo_no_encontrados = f"{base_path}/conciliador_clientes/ERRORES/nits_no_encontrados_20260114_121927.xlsx"
    archivo_clientes = f"{base_path}/conciliador_clientes/clientes_activos/CLIENTES ACTIVOS.xlsx"
    archivo_plantilla = f"{base_path}/conciliador_clientes/plantilla/PLANTILLA DE SOTSEGUROS.xlsx"
    
    # 1. Leer NITs no encontrados
    print("\n[1] LEYENDO NITs NO ENCONTRADOS EN CELER")
    print("-" * 50)
    
    df_nits = pd.read_excel(archivo_no_encontrados, dtype=str)
    nits_buscar = df_nits.iloc[:, 0].dropna().apply(limpiar_identificacion).unique().tolist()
    nits_buscar = [n for n in nits_buscar if n]
    
    print(f"  [OK] NITs a buscar: {len(nits_buscar)}")
    print(f"  Ejemplos: {nits_buscar[:5]}")
    
    # 2. Leer archivo de Clientes Activos
    print("\n[2] LEYENDO CLIENTES ACTIVOS")
    print("-" * 50)
    
    df_clientes = pd.read_excel(archivo_clientes, header=3, dtype=str)
    print(f"  [OK] Registros en Clientes Activos: {len(df_clientes)}")
    
    # Crear columnas de identificación limpia (con y sin DV)
    df_clientes['_id_limpia'] = df_clientes['Identificacion'].apply(limpiar_identificacion)
    df_clientes['_id_sin_dv'] = df_clientes['Identificacion'].apply(limpiar_nit_sin_dv)
    
    # Debug: mostrar ejemplos
    print(f"\n[DEBUG] Ejemplos de limpieza en Clientes Activos:")
    for idx, row in df_clientes.head(3).iterrows():
        print(f"  Original: '{row['Identificacion']}' → Limpia: '{row['_id_limpia']}' → Sin DV: '{row['_id_sin_dv']}'")
    print()
    
    # 3. Leer estructura de plantilla
    print("\n[3] PREPARANDO PLANTILLA SOFTSEGUROS")
    print("-" * 50)
    
    df_plantilla = pd.read_excel(archivo_plantilla, nrows=0)
    columnas_plantilla = list(df_plantilla.columns)
    print(f"  [OK] Columnas en plantilla: {len(columnas_plantilla)}")
    
    # 4. Buscar y mapear datos
    print("\n[4] BUSCANDO EMPRESAS EN CLIENTES ACTIVOS")
    print("-" * 50)
    
    registros_encontrados = []
    no_encontrados = []
    nits_ya_agregados = set()  # Para evitar duplicados
    
    for nit in nits_buscar:
        # Buscar en Clientes Activos (con y sin DV)
        match = df_clientes[(df_clientes['_id_limpia'] == nit) | (df_clientes['_id_sin_dv'] == nit)]
        
        if len(match) == 0:
            no_encontrados.append(nit)
            print(f"  [X] {nit}: No encontrado")
            continue
        
        # Evitar duplicados
        if nit in nits_ya_agregados:
            continue
        nits_ya_agregados.add(nit)
        
        # Tomar primer match
        row = match.iloc[0]
        
        # Para empresas: el nombre va en NOMBRES, APELLIDOS queda vacío
        nombre_empresa = str(row.get('Tomador', '')).strip()
        
        print(f"  [OK] {nit}: {nombre_empresa}")
        
        # Obtener identificación con formato original (puede tener DV)
        identificacion = row.get('Identificacion', '')
        
        # Crear registro para plantilla (solo con nombre de empresa)
        registro = {
            'NOMBRES': nombre_empresa,
            'APELLIDOS': '',
            'SOBRENOMBRE (ALIAS)': '',
            'NÚMERO DE DOCUMENTO': identificacion,
            'TIPO DE DOCUMENTO': 'NIT',
            'GÉNERO': '',
            'ESTADO CIVIL': '',
            'FECHA DE NACIMIENTO': '',
            'TELÉFONO MÓVIL': row.get('Celular_Pers', '') or row.get('Celular_Lab', ''),
            'TIPO TELÉFONO MÓVIL': 'Laboral',
            'TELÉFONO PRINCIPAL': row.get('Telefono_Pers', '') or row.get('Telefono_Lab', ''),
            'TIPO DE TELÉFONO PRINCIPAL': 'Laboral',
            'TELÉFONO SECUNDARIO': '',
            'TIPO DE TELÉFONO SECUNDARIO': '',
            'EMAIL': row.get('Mail_Pers', '') or row.get('Mail_Lab', ''),
            'TIPO EMAIL': 'Laboral',
            'EMAIL SECUNDARIO': '',
            'TIPO EMAIL SECUNDARIO': '',
            'DIRECCIÓN PRINCIPAL': row.get('Direccion_Lab', ''),
            'TIPO DIRECCIÓN': 'Laboral',
            'DIRECCIÓN SECUNDARIA': '',
            'TIPO DIRECCIÓN SECUNDARIA': '',
            'PAÍS': 'Colombia',
            'ESTADO': '',
            'CIUDAD': row.get('Ciudad_Lab', ''),
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
            'CARGADO POR': 'Migración Automática - Empresas'
        }
        
        registros_encontrados.append(registro)
        print(f"  [OK] {nit}: {nombre_empresa}")
    
    print(f"\n  Encontrados: {len(registros_encontrados)}")
    print(f"  No encontrados: {len(no_encontrados)}")
    
    if no_encontrados:
        print(f"\n  NITs no encontrados en Clientes Activos:")
        for nit in no_encontrados[:10]:
            print(f"    - {nit}")
        if len(no_encontrados) > 10:
            print(f"    ... y {len(no_encontrados) - 10} más")
    
    # 5. Crear DataFrame y guardar
    print("\n[5] GUARDANDO PLANTILLA LLENA (EMPRESAS)")
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
        archivo_salida = f"{base_path}/conciliador_clientes/plantilla/PLANTILLA_EMPRESAS_{timestamp}.xlsx"
        
        df_resultado.to_excel(archivo_salida, index=False, engine='openpyxl')
        
        print(f"  [OK] Archivo guardado: {os.path.basename(archivo_salida)}")
        print(f"  [OK] Registros: {len(df_resultado)}")
        print(f"  [OK] Ruta: {archivo_salida}")
    else:
        print("  [WARN] No se encontraron registros para guardar")
    
    # 6. Guardar los que aún no se encontraron
    if no_encontrados:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        archivo_no_enc = f"{base_path}/conciliador_clientes/ERRORES/nits_sin_datos_{timestamp}.xlsx"
        df_no_enc = pd.DataFrame({'NIT_SIN_DATOS': no_encontrados})
        df_no_enc.to_excel(archivo_no_enc, index=False)
        print(f"\n  [INFO] NITs sin datos guardados en: {os.path.basename(archivo_no_enc)}")
    
    print("\n" + "=" * 70)
    print("  PROCESO COMPLETADO")
    print("=" * 70)


if __name__ == "__main__":
    main()
