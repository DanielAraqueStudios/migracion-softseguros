#!/usr/bin/env python3
"""
Programa interactivo para calcular dígitos de verificación de NITs
usando la API de DIAN.

Permite seleccionar un archivo Excel y la columna a procesar.
Verifica y corrige el dígito de verificación para NITs con formato número-dígito.
"""

import pandas as pd
import re
import os
import sys
import subprocess
import time
import requests
from pathlib import Path
from datetime import datetime

# URL de la API
API_URL = "http://localhost:8000"


class CalculadorNITsInteractivo:
    """Calculador interactivo de dígitos de verificación para NITs usando API DIAN"""

    def __init__(self):
        self.df = None
        self.archivo_entrada = None
        self.columna_seleccionada = None
        self.api_proceso = None
        self.modo_calcular_todos = False  # True = calcular DV para todos, False = solo corregir existentes

    def limpiar_pantalla(self):
        """Limpia la pantalla de la consola"""
        os.system('cls' if os.name == 'nt' else 'clear')

    def mostrar_banner(self):
        """Muestra el banner del programa"""
        print("=" * 60)
        print("  CALCULADOR DE DIGITOS DE VERIFICACION - API DIAN")
        print("=" * 60)
        print()

    def verificar_api(self):
        """Verifica si la API está corriendo"""
        try:
            response = requests.get(f"{API_URL}/health", timeout=2)
            return response.status_code == 200
        except:
            return False

    def matar_proceso_puerto(self, puerto=8000):
        """Mata cualquier proceso usando el puerto especificado (Windows)"""
        try:
            # Buscar el PID del proceso en el puerto
            resultado = subprocess.run(
                ["netstat", "-ano"],
                capture_output=True,
                text=True,
                creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
            )
            
            for linea in resultado.stdout.split('\n'):
                if f":{puerto}" in linea and "LISTENING" in linea:
                    partes = linea.split()
                    if partes:
                        pid = partes[-1]
                        if pid.isdigit():
                            subprocess.run(
                                ["taskkill", "/F", "/PID", pid],
                                capture_output=True,
                                creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
                            )
                            time.sleep(1)
                            return True
        except:
            pass
        return False

    def iniciar_api(self):
        """Inicia la API de DIAN en segundo plano"""
        print("\n[0] INICIANDO API DIAN")
        print("-" * 40)
        
        # Primero intentar matar cualquier proceso anterior en el puerto
        if self.verificar_api():
            print("  [INFO] Deteniendo API anterior...")
            self.matar_proceso_puerto(8000)
            time.sleep(1)
        
        print("  Iniciando servidor API...")
        
        # Ruta al directorio backend (usar ruta absoluta)
        script_dir = os.path.dirname(os.path.abspath(__file__))
        backend_dir = os.path.join(script_dir, 'backend')
        
        if not os.path.exists(backend_dir):
            print(f"  [ERROR] No se encuentra el directorio backend: {backend_dir}")
            return False
        
        try:
            # Iniciar uvicorn en segundo plano
            self.api_proceso = subprocess.Popen(
                [sys.executable, "-m", "uvicorn", "app:app", "--host", "127.0.0.1", "--port", "8000"],
                cwd=backend_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
            )
            
            # Esperar a que la API esté lista
            for i in range(10):
                time.sleep(1)
                if self.verificar_api():
                    print("  [OK] API iniciada correctamente")
                    return True
                print(f"  Esperando... ({i+1}/10)")
            
            print("  [ERROR] No se pudo iniciar la API")
            return False
            
        except Exception as e:
            print(f"  [ERROR] Error iniciando API: {e}")
            return False

    def detener_api(self):
        """Detiene la API si fue iniciada por este programa"""
        if self.api_proceso:
            self.api_proceso.terminate()
            print("\n  [INFO] API detenida")

    def calcular_digito_verificacion(self, nit_sin_dv):
        """
        Calcula el dígito de verificación usando la API de DIAN.
        
        Args:
            nit_sin_dv: NIT sin dígito de verificación (solo números)
            
        Returns:
            str: Dígito de verificación calculado (0-9)
        """
        try:
            # Limpiar el NIT - solo números
            nit_str = re.sub(r'\D', '', str(nit_sin_dv))
            
            if not nit_str or len(nit_str) > 15:
                return None

            # Llamar a la API
            response = requests.post(
                f"{API_URL}/calcular",
                json={"nit": nit_str},
                timeout=5
            )
            
            if response.status_code == 200:
                data = response.json()
                return str(data["digito_verificacion"])
            else:
                return None

        except Exception as e:
            print(f"  [ERROR] API: {e}")
            return None

    def es_nit_con_dv(self, valor):
        """
        Verifica si un valor tiene formato NIT con dígito de verificación.
        Formato esperado: números-dígito (ej: 890981212-5)
        
        Args:
            valor: Valor a verificar
            
        Returns:
            bool: True si tiene formato NIT-DV
        """
        if pd.isna(valor):
            return False
        
        valor_str = str(valor).strip()
        
        # Debe tener formato número-dígito
        if re.match(r'^\d+-\d$', valor_str):
            return True
        
        return False

    def extraer_nit_base(self, valor):
        """
        Extrae el NIT base (sin dígito de verificación) de un valor.
        Solo procesa valores con formato NIT-DV.
        
        Args:
            valor: Valor que debe ser NIT con DV (ej: 890981212-5)
            
        Returns:
            tuple: (nit_base, dv_actual) o (None, None) si no es válido
        """
        if not self.es_nit_con_dv(valor):
            return None, None
        
        valor_str = str(valor).strip()
        partes = valor_str.split('-')
        
        if len(partes) != 2:
            return None, None
        
        nit_base = partes[0]
        dv_actual = partes[1]
        
        # Validar que el NIT base sea numérico y razonable
        if not nit_base.isdigit() or len(nit_base) < 5 or len(nit_base) > 15:
            return None, None
        
        return nit_base, dv_actual

    def seleccionar_archivo(self):
        """Permite al usuario seleccionar el archivo Excel"""
        print("\n[1] SELECCIONAR ARCHIVO EXCEL")
        print("-" * 40)
        
        while True:
            archivo = input("\nIngrese la ruta del archivo Excel (o 'q' para salir): ").strip()
            
            if archivo.lower() == 'q':
                return False
            
            # Remover comillas si las tiene
            archivo = archivo.strip('"').strip("'")
            
            if not os.path.exists(archivo):
                print(f"  [ERROR] El archivo no existe: {archivo}")
                continue
            
            if not archivo.endswith(('.xlsx', '.xls', '.xlsm')):
                print("  [ERROR] El archivo debe ser Excel (.xlsx, .xls, .xlsm)")
                continue
            
            try:
                # Detectar el engine correcto
                if archivo.endswith('.xls'):
                    self.df = pd.read_excel(archivo, engine='xlrd')
                else:
                    self.df = pd.read_excel(archivo, engine='openpyxl')
                
                self.archivo_entrada = archivo
                print(f"\n  [OK] Archivo cargado: {os.path.basename(archivo)}")
                print(f"  [OK] Total de filas: {len(self.df)}")
                return True
                
            except Exception as e:
                print(f"  [ERROR] No se pudo leer el archivo: {e}")
                continue

    def seleccionar_columna(self):
        """Permite al usuario seleccionar la columna a procesar"""
        print("\n[2] SELECCIONAR COLUMNA")
        print("-" * 40)
        print("\nColumnas disponibles:")
        print()
        
        columnas = list(self.df.columns)
        for i, col in enumerate(columnas, 1):
            # Mostrar muestra de valores
            muestra = self.df[col].dropna().head(3).tolist()
            muestra_str = ", ".join([str(v)[:20] for v in muestra])
            print(f"  {i:3}. {col[:30]:<30} | Ej: {muestra_str[:40]}")
        
        print()
        
        while True:
            seleccion = input("Seleccione el numero de columna (o 'q' para salir): ").strip()
            
            if seleccion.lower() == 'q':
                return False
            
            try:
                indice = int(seleccion) - 1
                if 0 <= indice < len(columnas):
                    self.columna_seleccionada = columnas[indice]
                    print(f"\n  [OK] Columna seleccionada: {self.columna_seleccionada}")
                    return True
                else:
                    print("  [ERROR] Numero fuera de rango")
            except ValueError:
                print("  [ERROR] Ingrese un numero valido")

    def seleccionar_modo(self):
        """Permite al usuario seleccionar el modo de procesamiento"""
        print("\n[3] SELECCIONAR MODO DE PROCESAMIENTO")
        print("-" * 40)
        print()
        print("  1. Solo CORREGIR NITs con formato numero-digito (ej: 890981212-5)")
        print("     Solo procesa valores que ya tienen el guion y DV")
        print()
        print("  2. CALCULAR DV para TODOS los numeros")
        print("     Agrega el DV a numeros sin formato (ej: 890981212 -> 890981212-1)")
        print()
        
        while True:
            opcion = input("Seleccione modo (1 o 2): ").strip()
            
            if opcion == '1':
                self.modo_calcular_todos = False
                print("\n  [OK] Modo: Solo corregir NITs con DV existente")
                return True
            elif opcion == '2':
                self.modo_calcular_todos = True
                print("\n  [OK] Modo: Calcular DV para todos los numeros")
                return True
            else:
                print("  [ERROR] Ingrese 1 o 2")

    def es_numero_valido(self, valor):
        """Verifica si el valor es un número válido para calcular DV"""
        if pd.isna(valor):
            return False
        
        valor_str = str(valor).strip()
        
        # Quitar posibles decimales (.0)
        if valor_str.endswith('.0'):
            valor_str = valor_str[:-2]
        
        # Solo números, longitud razonable
        if valor_str.isdigit() and 5 <= len(valor_str) <= 15:
            return True
        
        return False

    def procesar_columna(self):
        """Procesa la columna seleccionada verificando y corrigiendo dígitos de verificación"""
        print("\n[4] PROCESANDO NITs")
        print("-" * 40)
        
        total = len(self.df)
        nits_encontrados = 0
        corregidos = 0
        correctos = 0
        ignorados = 0
        agregados = 0  # NITs a los que se les agregó DV
        
        print(f"\nProcesando {total} filas...")
        if self.modo_calcular_todos:
            print("Modo: Calcular DV para TODOS los numeros")
        else:
            print("Modo: Solo corregir NITs con formato numero-digito (ej: 890981212-5)")
        print()
        
        for idx in range(len(self.df)):
            valor_original = self.df.iloc[idx][self.columna_seleccionada]
            
            # MODO 1: Solo corregir NITs con DV existente
            if not self.modo_calcular_todos:
                if not self.es_nit_con_dv(valor_original):
                    ignorados += 1
                    continue
                
                nits_encontrados += 1
                nit_base, dv_actual = self.extraer_nit_base(valor_original)
                
                if nit_base is None:
                    ignorados += 1
                    continue
                
                dv_correcto = self.calcular_digito_verificacion(nit_base)
                
                if dv_correcto is None:
                    ignorados += 1
                    continue
                
                if dv_actual == dv_correcto:
                    correctos += 1
                else:
                    valor_nuevo = f"{nit_base}-{dv_correcto}"
                    self.df.at[idx, self.columna_seleccionada] = valor_nuevo
                    corregidos += 1
                    
                    if corregidos <= 20 or corregidos % 50 == 0:
                        print(f"  Fila {idx+2}: {valor_original} -> {valor_nuevo}")
            
            # MODO 2: Calcular DV para todos los números
            else:
                # Si ya tiene formato NIT-DV, corregir si es necesario
                if self.es_nit_con_dv(valor_original):
                    nits_encontrados += 1
                    nit_base, dv_actual = self.extraer_nit_base(valor_original)
                    
                    if nit_base is None:
                        ignorados += 1
                        continue
                    
                    dv_correcto = self.calcular_digito_verificacion(nit_base)
                    
                    if dv_correcto is None:
                        ignorados += 1
                        continue
                    
                    if dv_actual == dv_correcto:
                        correctos += 1
                    else:
                        valor_nuevo = f"{nit_base}-{dv_correcto}"
                        self.df.at[idx, self.columna_seleccionada] = valor_nuevo
                        corregidos += 1
                        
                        if corregidos <= 20 or corregidos % 50 == 0:
                            print(f"  Fila {idx+2}: {valor_original} -> {valor_nuevo}")
                
                # Si es un número sin DV, calcular y agregar
                elif self.es_numero_valido(valor_original):
                    nits_encontrados += 1
                    
                    # Limpiar el valor (quitar .0 si existe)
                    nit_str = str(valor_original).strip()
                    if nit_str.endswith('.0'):
                        nit_str = nit_str[:-2]
                    
                    dv_correcto = self.calcular_digito_verificacion(nit_str)
                    
                    if dv_correcto is None:
                        ignorados += 1
                        continue
                    
                    valor_nuevo = f"{nit_str}-{dv_correcto}"
                    self.df.at[idx, self.columna_seleccionada] = valor_nuevo
                    agregados += 1
                    
                    if agregados <= 20 or agregados % 50 == 0:
                        print(f"  Fila {idx+2}: {valor_original} -> {valor_nuevo}")
                
                else:
                    ignorados += 1
            
            # Mostrar progreso general
            if nits_encontrados % 100 == 0 and nits_encontrados > 0:
                print(f"  ... procesados {nits_encontrados} NITs")
        
        print()
        print("-" * 40)
        print(f"  Total filas:        {total}")
        print(f"  Valores ignorados:  {ignorados} (no procesables)")
        print(f"  NITs encontrados:   {nits_encontrados}")
        if self.modo_calcular_todos:
            print(f"  NITs con DV agregado: {agregados}")
        print(f"  NITs correctos:     {correctos}")
        print(f"  NITs corregidos:    {corregidos}")
        
        return corregidos + agregados

    def guardar_archivo(self):
        """Guarda el archivo modificado"""
        print("\n[4] GUARDAR ARCHIVO")
        print("-" * 40)
        
        # Generar nombre de archivo de salida
        base, ext = os.path.splitext(self.archivo_entrada)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        archivo_salida = f"{base}_nits_calculados_{timestamp}{ext}"
        
        print(f"\nArchivo de salida: {os.path.basename(archivo_salida)}")
        
        respuesta = input("\nGuardar archivo? (s/n): ").strip().lower()
        
        if respuesta == 's':
            try:
                self.df.to_excel(archivo_salida, index=False, engine='openpyxl')
                print(f"\n  [OK] Archivo guardado exitosamente!")
                print(f"  [OK] Ruta: {archivo_salida}")
                return True
            except Exception as e:
                print(f"\n  [ERROR] No se pudo guardar: {e}")
                return False
        else:
            print("\n  [INFO] Archivo no guardado")
            return False

    def ejecutar(self):
        """Ejecuta el programa interactivo"""
        self.limpiar_pantalla()
        self.mostrar_banner()
        
        # Iniciar la API
        if not self.iniciar_api():
            print("\n[ERROR] No se puede continuar sin la API")
            print("  Por favor inicie la API manualmente:")
            print("  cd backend; python -m uvicorn app:app --reload")
            return
        
        try:
            # Paso 1: Seleccionar archivo
            if not self.seleccionar_archivo():
                print("\n[INFO] Programa terminado por el usuario")
                return
            
            # Paso 2: Seleccionar columna
            if not self.seleccionar_columna():
                print("\n[INFO] Programa terminado por el usuario")
                return
            
            # Paso 3: Seleccionar modo
            if not self.seleccionar_modo():
                print("\n[INFO] Programa terminado por el usuario")
                return
            
            # Paso 4: Procesar
            modificados = self.procesar_columna()
            
            # Paso 5: Guardar
            if modificados > 0:
                self.guardar_archivo()
            else:
                print("\n[INFO] No hubo modificaciones, no se genera archivo")
            
            print("\n" + "=" * 60)
            print("  PROCESO COMPLETADO")
            print("=" * 60)
        
        finally:
            self.detener_api()


def main():
    """Función principal"""
    calculador = CalculadorNITsInteractivo()
    calculador.ejecutar()


if __name__ == "__main__":
    main()
