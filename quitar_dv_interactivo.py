#!/usr/bin/env python3
"""
Programa interactivo para quitar el dígito de verificación de NITs.

Convierte NITs con formato número-dígito (ej: 890981212-5) a solo el número base (890981212).
"""

import pandas as pd
import re
import os
from pathlib import Path
from datetime import datetime


class QuitarDVInteractivo:
    """Quita el dígito de verificación de NITs en archivos Excel"""

    def __init__(self):
        self.df = None
        self.archivo_entrada = None
        self.columna_seleccionada = None

    def limpiar_pantalla(self):
        """Limpia la pantalla de la consola"""
        os.system('cls' if os.name == 'nt' else 'clear')

    def mostrar_banner(self):
        """Muestra el banner del programa"""
        print("=" * 60)
        print("  QUITAR DIGITO DE VERIFICACION DE NITs")
        print("  Convierte: 890981212-5 -> 890981212")
        print("=" * 60)
        print()

    def es_nit_con_dv(self, valor):
        """
        Verifica si el valor tiene formato NIT con dígito de verificación.
        Formato esperado: números-dígito (ej: 890981212-5)
        """
        if pd.isna(valor):
            return False
        
        valor_str = str(valor).strip()
        # Patrón: uno o más dígitos, guión, un dígito
        patron = r'^\d+-\d$'
        return bool(re.match(patron, valor_str))

    def extraer_nit_base(self, valor):
        """
        Extrae solo el número base del NIT (sin el guión y DV).
        Ejemplo: 890981212-5 -> 890981212
        """
        valor_str = str(valor).strip()
        # Quitar el guión y todo lo que sigue
        if '-' in valor_str:
            return valor_str.split('-')[0]
        return valor_str

    def seleccionar_archivo(self):
        """Permite al usuario seleccionar un archivo Excel"""
        print("\n[1] SELECCIONAR ARCHIVO EXCEL")
        print("-" * 40)
        
        while True:
            ruta = input("\nIngrese la ruta del archivo Excel (o 'q' para salir): ").strip()
            
            if ruta.lower() == 'q':
                return False
            
            # Quitar comillas si las tiene
            ruta = ruta.strip('"').strip("'")
            
            if not os.path.exists(ruta):
                print(f"  [ERROR] Archivo no encontrado: {ruta}")
                continue
            
            if not ruta.lower().endswith(('.xlsx', '.xls', '.xlsm')):
                print("  [ERROR] El archivo debe ser Excel (.xlsx, .xls, .xlsm)")
                continue
            
            try:
                self.df = pd.read_excel(ruta, dtype=str)
                self.archivo_entrada = ruta
                print(f"  [OK] Archivo cargado: {os.path.basename(ruta)}")
                print(f"  [OK] Total de filas: {len(self.df)}")
                return True
            except Exception as e:
                print(f"  [ERROR] No se pudo leer el archivo: {e}")
                continue

    def seleccionar_columna(self):
        """Permite al usuario seleccionar la columna a procesar"""
        print("\n[2] SELECCIONAR COLUMNA")
        print("-" * 40)
        
        columnas = list(self.df.columns)
        
        print("\nColumnas disponibles:\n")
        for i, col in enumerate(columnas, 1):
            # Mostrar muestra de valores
            muestra = self.df[col].dropna().head(3).tolist()
            muestra_str = ", ".join(str(v)[:20] for v in muestra)
            print(f"  {i:3}. {col[:30]:<30} | Ej: {muestra_str}")
        
        while True:
            seleccion = input("\nSeleccione el numero de columna (o 'q' para salir): ").strip()
            
            if seleccion.lower() == 'q':
                return False
            
            try:
                idx = int(seleccion) - 1
                if 0 <= idx < len(columnas):
                    self.columna_seleccionada = columnas[idx]
                    print(f"\n  [OK] Columna seleccionada: {self.columna_seleccionada}")
                    return True
                else:
                    print("  [ERROR] Numero fuera de rango")
            except ValueError:
                print("  [ERROR] Ingrese un numero valido")

    def procesar_columna(self):
        """Procesa la columna quitando el DV de los NITs"""
        print("\n[3] PROCESANDO NITs")
        print("-" * 40)
        
        total = len(self.df)
        print(f"\nProcesando {total} filas...")
        print("Solo se procesan NITs con formato numero-digito (ej: 890981212-5)\n")
        
        modificados = 0
        encontrados = 0
        ignorados = 0
        procesados = 0
        
        for idx in range(len(self.df)):
            valor_original = self.df.iloc[idx][self.columna_seleccionada]
            
            # Solo procesar si tiene formato NIT-DV
            if not self.es_nit_con_dv(valor_original):
                ignorados += 1
                continue
            
            encontrados += 1
            
            # Extraer solo el NIT base (sin DV)
            nit_base = self.extraer_nit_base(valor_original)
            
            # Actualizar el valor
            valor_nuevo = nit_base
            self.df.at[idx, self.columna_seleccionada] = valor_nuevo
            modificados += 1
            
            print(f"  Fila {idx + 1}: {valor_original} -> {valor_nuevo}")
            
            procesados += 1
            if procesados % 100 == 0:
                print(f"  ... procesados {procesados} NITs")
        
        print("\n" + "-" * 40)
        print(f"  Total filas:        {total}")
        print(f"  Valores ignorados:  {ignorados} (sin formato NIT-DV)")
        print(f"  NITs procesados:    {encontrados}")
        print(f"  NITs modificados:   {modificados}")
        
        return modificados

    def guardar_archivo(self):
        """Guarda el archivo procesado"""
        print("\n[4] GUARDAR ARCHIVO")
        print("-" * 40)
        
        # Generar nombre de salida
        base, ext = os.path.splitext(self.archivo_entrada)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        archivo_salida = f"{base}_sin_dv_{timestamp}.xlsx"
        
        print(f"\nArchivo de salida: {os.path.basename(archivo_salida)}")
        
        confirmar = input("\nGuardar archivo? (s/n): ").strip().lower()
        
        if confirmar == 's':
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
        
        # Paso 1: Seleccionar archivo
        if not self.seleccionar_archivo():
            print("\n[INFO] Programa terminado por el usuario")
            return
        
        # Paso 2: Seleccionar columna
        if not self.seleccionar_columna():
            print("\n[INFO] Programa terminado por el usuario")
            return
        
        # Paso 3: Procesar
        modificados = self.procesar_columna()
        
        # Paso 4: Guardar
        if modificados > 0:
            self.guardar_archivo()
        else:
            print("\n[INFO] No hubo modificaciones, no se genera archivo")
        
        print("\n" + "=" * 60)
        print("  PROCESO COMPLETADO")
        print("=" * 60)


def main():
    """Función principal"""
    quitador = QuitarDVInteractivo()
    quitador.ejecutar()


if __name__ == "__main__":
    main()
