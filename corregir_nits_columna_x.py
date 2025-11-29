#!/usr/bin/env python3
"""
Script para corregir NITs en columna X del archivo Excel
"""

import pandas as pd
import re
from pathlib import Path
import logging
import requests

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class CorrectorNITsColumnaX:
    """Corrige NITs en columna X de un archivo Excel"""

    def __init__(self, archivo_entrada):
        self.archivo_entrada = archivo_entrada

    def calcular_digito_verificacion(self, nit_sin_dv):
        """
        Calcula el dígito de verificación de un NIT colombiano
        usando el algoritmo oficial de la DIAN
        """
        try:
            # Remover caracteres no numéricos
            nit_str = re.sub(r'\D', '', str(nit_sin_dv))

            if not nit_str or len(nit_str) > 15:
                return None

            # Pesos DIAN oficiales aplicados de izquierda a derecha
            pesos = [71, 67, 59, 53, 47, 43, 41, 37, 29, 23, 19, 17, 13, 7, 3]

            # Calcular suma multiplicando de izquierda a derecha
            suma = 0
            for i, digito in enumerate(nit_str):
                if i < len(pesos):
                    suma += int(digito) * pesos[i]

            # Calcular dígito de verificación
            residuo = suma % 11

            if residuo == 0 or residuo == 1:
                dv = residuo
            else:
                dv = 11 - residuo

            return str(dv)

        except Exception as e:
            logger.warning(f"Error calculando DV para {nit_sin_dv}: {e}")
            return None

    def es_nit(self, valor):
        """Determina si un valor es un NIT (tiene formato número-dígito)"""
        if pd.isna(valor):
            return False

        valor_str = str(valor).strip()

        # Patrón: números con guión y dígito al final
        if re.match(r'^\d+-\d$', valor_str):
            return True

        return False

    def corregir_nit(self, nit_str):
        """Corrige un NIT si es necesario"""
        if not self.es_nit(nit_str):
            return nit_str, False

        # Extraer partes
        partes = str(nit_str).split('-')
        if len(partes) != 2:
            return nit_str, False

        nit_base = partes[0]
        dv_actual = partes[1]

        # Calcular DV correcto
        dv_correcto = self.calcular_digito_verificacion(nit_base)

        if dv_correcto and dv_actual != dv_correcto:
            nit_corregido = f"{nit_base}-{dv_correcto}"
            return nit_corregido, True
        else:
            return nit_str, False

    def procesar_archivo(self):
        """Procesa el archivo Excel"""
        logger.info(f"Procesando archivo: {self.archivo_entrada}")

        # Leer Excel
        df = pd.read_excel(self.archivo_entrada)

        # Columna X en Excel es la columna 23 en pandas (DOCUMENTO DEL CLIENTE)
        columna_x = 'DOCUMENTO DEL CLIENTE'  # Columna 23

        if columna_x not in df.columns:
            logger.error(f"Columna {columna_x} no encontrada en el archivo")
            return

        logger.info(f"Procesando {len(df)} filas en columna {columna_x}")

        correcciones = 0

        for idx, row in df.iterrows():
            valor_original = row[columna_x]

            if self.es_nit(valor_original):
                valor_corregido, fue_corregido = self.corregir_nit(valor_original)

                if fue_corregido:
                    df.at[idx, columna_x] = valor_corregido
                    correcciones += 1
                    logger.info(f"Fila {idx+2}: {valor_original} → {valor_corregido}")

        # Generar archivo corregido
        archivo_salida = self.archivo_entrada.replace('.xlsx', '_corregido.xlsx')
        df.to_excel(archivo_salida, index=False)

        logger.info(f"✅ Archivo corregido guardado como: {archivo_salida}")
        logger.info(f"✅ Total de NITs corregidos: {correcciones}")

        return archivo_salida

def main():
    archivo_entrada = r"NEW_ARCHIVE_TO_BE_SENT\Copy of Copia de errores.xlsx"

    corrector = CorrectorNITsColumnaX(archivo_entrada)
    corrector.procesar_archivo()

if __name__ == "__main__":
    main()