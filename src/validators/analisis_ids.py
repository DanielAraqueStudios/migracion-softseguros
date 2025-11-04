"""
Análisis de Identificaciones - Validación de Números de Documento
==================================================================
Este script analiza la calidad de los números de documento en ambos archivos
para identificar duplicados, formatos incorrectos y otros problemas.
"""

import pandas as pd
import re
from pathlib import Path
from datetime import datetime
import logging

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class AnalizadorIdentificaciones:
    """Analiza y valida números de identificación en archivos de clientes"""
    
    def __init__(self, ruta_softseguros, ruta_celer):
        self.ruta_softseguros = ruta_softseguros
        self.ruta_celer = ruta_celer
        self.df_softseguros = None
        self.df_celer = None
        self.resultados = {}
        
    def cargar_datos(self):
        """Carga los archivos Excel"""
        logger.info("Cargando archivos...")
        try:
            self.df_softseguros = pd.read_excel(self.ruta_softseguros)
            self.df_celer = pd.read_excel(self.ruta_celer)
            logger.info(f"SOFTSEGUROS: {len(self.df_softseguros)} registros cargados")
            logger.info(f"CELER: {len(self.df_celer)} registros cargados")
        except Exception as e:
            logger.error(f"Error al cargar archivos: {e}")
            raise
    
    def limpiar_identificacion(self, identificacion):
        """Limpia y normaliza un número de identificación"""
        if pd.isna(identificacion):
            return None
        # Convertir a string y eliminar espacios
        id_limpio = str(identificacion).strip()
        # Eliminar caracteres especiales comunes pero mantener guiones
        id_limpio = re.sub(r'[^\d\-]', '', id_limpio)
        return id_limpio if id_limpio else None
    
    def analizar_softseguros(self):
        """Analiza identificaciones en archivo SOFTSEGUROS"""
        logger.info("\n=== ANÁLISIS CLIENTES SOFTSEGUROS ===")
        
        df = self.df_softseguros.copy()
        col_id = 'NÚMERO DE DOCUMENTO'
        col_tipo = 'TIPO DE DOCUMENTO'
        col_nombre = 'NOMBRES'
        
        # Limpiar identificaciones
        df['ID_LIMPIO'] = df[col_id].apply(self.limpiar_identificacion)
        
        # 1. Identificaciones vacías o nulas
        ids_vacios = df[df['ID_LIMPIO'].isna()]
        logger.info(f"Registros sin identificación: {len(ids_vacios)}")
        
        # 2. Identificaciones duplicadas
        duplicados = df[df['ID_LIMPIO'].duplicated(keep=False) & df['ID_LIMPIO'].notna()]
        duplicados_agrupados = duplicados.groupby('ID_LIMPIO').agg({
            col_nombre: list,
            col_tipo: 'first'
        }).reset_index()
        
        logger.info(f"Identificaciones duplicadas: {len(duplicados_agrupados)}")
        if len(duplicados_agrupados) > 0:
            logger.warning("⚠️ DUPLICADOS ENCONTRADOS:")
            for _, row in duplicados_agrupados.iterrows():
                logger.warning(f"  ID: {row['ID_LIMPIO']} ({row[col_tipo]})")
                logger.warning(f"  Nombres: {', '.join(row[col_nombre])}")
        
        # 3. Validación por tipo de documento
        validaciones_tipo = {}
        for tipo_doc in df[col_tipo].unique():
            if pd.isna(tipo_doc):
                continue
            
            subset = df[df[col_tipo] == tipo_doc]
            ids_validos = subset['ID_LIMPIO'].notna()
            
            validaciones_tipo[tipo_doc] = {
                'total': len(subset),
                'con_id': ids_validos.sum(),
                'sin_id': (~ids_validos).sum()
            }
        
        logger.info("\nDistribución por tipo de documento:")
        for tipo, stats in validaciones_tipo.items():
            logger.info(f"  {tipo}: {stats['total']} registros "
                       f"({stats['con_id']} con ID, {stats['sin_id']} sin ID)")
        
        # 4. Validación de formatos específicos
        problemas_formato = []
        
        # NITs deben tener formato: números-dígito_verificación
        nits = df[df[col_tipo] == 'NIT']
        for idx, row in nits.iterrows():
            id_val = row['ID_LIMPIO']
            if id_val and not re.match(r'^\d+-\d$', id_val):
                problemas_formato.append({
                    'fila': idx + 2,  # +2 porque Excel empieza en 1 y tiene header
                    'nombre': row[col_nombre],
                    'id': id_val,
                    'tipo': 'NIT',
                    'problema': 'Formato incorrecto (debe ser XXXXXXXXX-X)'
                })
        
        # Cédulas deben ser solo números
        cedulas = df[df[col_tipo].isin(['C.C', 'CC', 'CEDULA', 'CÉDULA'])]
        for idx, row in cedulas.iterrows():
            id_val = row['ID_LIMPIO']
            if id_val and not re.match(r'^\d+$', id_val):
                problemas_formato.append({
                    'fila': idx + 2,
                    'nombre': row[col_nombre],
                    'id': id_val,
                    'tipo': row[col_tipo],
                    'problema': 'Formato incorrecto (debe contener solo números)'
                })
        
        logger.info(f"\nProblemas de formato: {len(problemas_formato)}")
        
        # Guardar resultados
        self.resultados['softseguros'] = {
            'total_registros': len(df),
            'ids_vacios': ids_vacios,
            'duplicados': duplicados,
            'duplicados_agrupados': duplicados_agrupados,
            'validaciones_tipo': validaciones_tipo,
            'problemas_formato': problemas_formato
        }
        
        return df
    
    def analizar_celer(self):
        """Analiza identificaciones en archivo CELER"""
        logger.info("\n=== ANÁLISIS CLIENTES VIGENTES CELER ===")
        
        df = self.df_celer.copy()
        col_id = 'Identificacion'
        col_tipo = 'Tipo_Doc'
        col_nombre = 'Tomador'
        
        # Limpiar identificaciones
        df['ID_LIMPIO'] = df[col_id].apply(self.limpiar_identificacion)
        
        # 1. Identificaciones vacías
        ids_vacios = df[df['ID_LIMPIO'].isna()]
        logger.info(f"Registros sin identificación: {len(ids_vacios)}")
        
        # 2. Identificaciones duplicadas
        duplicados = df[df['ID_LIMPIO'].duplicated(keep=False) & df['ID_LIMPIO'].notna()]
        duplicados_agrupados = duplicados.groupby('ID_LIMPIO').agg({
            col_nombre: list,
            col_tipo: 'first',
            'Póliza': list
        }).reset_index()
        
        logger.info(f"Identificaciones duplicadas: {len(duplicados_agrupados)}")
        if len(duplicados_agrupados) > 0:
            logger.info("ℹ️ DUPLICADOS (múltiples pólizas por cliente):")
            for _, row in duplicados_agrupados.head(5).iterrows():
                logger.info(f"  ID: {row['ID_LIMPIO']} ({row[col_tipo]})")
                logger.info(f"  Cliente: {row[col_nombre][0]}")
                logger.info(f"  Pólizas: {', '.join(map(str, row['Póliza']))}")
        
        # 3. Validación por tipo de documento
        validaciones_tipo = {}
        for tipo_doc in df[col_tipo].unique():
            if pd.isna(tipo_doc):
                continue
            
            subset = df[df[col_tipo] == tipo_doc]
            ids_validos = subset['ID_LIMPIO'].notna()
            
            validaciones_tipo[tipo_doc] = {
                'total': len(subset),
                'con_id': ids_validos.sum(),
                'sin_id': (~ids_validos).sum()
            }
        
        logger.info("\nDistribución por tipo de documento:")
        for tipo, stats in validaciones_tipo.items():
            logger.info(f"  {tipo}: {stats['total']} registros")
        
        # Guardar resultados
        self.resultados['celer'] = {
            'total_registros': len(df),
            'ids_vacios': ids_vacios,
            'duplicados': duplicados,
            'duplicados_agrupados': duplicados_agrupados,
            'validaciones_tipo': validaciones_tipo
        }
        
        return df
    
    def comparar_bases(self, df_soft, df_celer):
        """Compara las identificaciones entre ambas bases"""
        logger.info("\n=== COMPARACIÓN ENTRE BASES ===")
        
        ids_soft = set(df_soft['ID_LIMPIO'].dropna())
        ids_celer = set(df_celer['ID_LIMPIO'].dropna())
        
        # Clientes en común
        en_comun = ids_soft & ids_celer
        solo_softseguros = ids_soft - ids_celer
        solo_celer = ids_celer - ids_soft
        
        logger.info(f"IDs únicos en SOFTSEGUROS: {len(ids_soft)}")
        logger.info(f"IDs únicos en CELER: {len(ids_celer)}")
        logger.info(f"IDs en común: {len(en_comun)} ({len(en_comun)/len(ids_soft)*100:.1f}%)")
        logger.info(f"Solo en SOFTSEGUROS: {len(solo_softseguros)}")
        logger.info(f"Solo en CELER: {len(solo_celer)}")
        
        self.resultados['comparacion'] = {
            'ids_comun': en_comun,
            'solo_softseguros': solo_softseguros,
            'solo_celer': solo_celer
        }
    
    def generar_reporte(self, ruta_salida='data/output'):
        """Genera reportes en Excel de los problemas encontrados"""
        logger.info("\n=== GENERANDO REPORTES ===")
        
        Path(ruta_salida).mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        archivo_reporte = f"{ruta_salida}/analisis_ids_{timestamp}.xlsx"
        
        with pd.ExcelWriter(archivo_reporte, engine='openpyxl') as writer:
            # Hoja 1: Resumen
            resumen_data = []
            resumen_data.append(['ANÁLISIS DE IDENTIFICACIONES', ''])
            resumen_data.append(['Fecha', datetime.now().strftime('%Y-%m-%d %H:%M:%S')])
            resumen_data.append(['', ''])
            
            resumen_data.append(['CLIENTES SOFTSEGUROS', ''])
            resumen_data.append(['Total registros', self.resultados['softseguros']['total_registros']])
            resumen_data.append(['Sin identificación', len(self.resultados['softseguros']['ids_vacios'])])
            resumen_data.append(['IDs duplicados', len(self.resultados['softseguros']['duplicados_agrupados'])])
            resumen_data.append(['Problemas de formato', len(self.resultados['softseguros']['problemas_formato'])])
            resumen_data.append(['', ''])
            
            resumen_data.append(['CLIENTES VIGENTES CELER', ''])
            resumen_data.append(['Total registros', self.resultados['celer']['total_registros']])
            resumen_data.append(['Sin identificación', len(self.resultados['celer']['ids_vacios'])])
            resumen_data.append(['IDs duplicados (múltiples pólizas)', len(self.resultados['celer']['duplicados_agrupados'])])
            resumen_data.append(['', ''])
            
            resumen_data.append(['COMPARACIÓN', ''])
            resumen_data.append(['IDs en común', len(self.resultados['comparacion']['ids_comun'])])
            resumen_data.append(['Solo en SOFTSEGUROS', len(self.resultados['comparacion']['solo_softseguros'])])
            resumen_data.append(['Solo en CELER', len(self.resultados['comparacion']['solo_celer'])])
            
            df_resumen = pd.DataFrame(resumen_data, columns=['Métrica', 'Valor'])
            df_resumen.to_excel(writer, sheet_name='Resumen', index=False)
            
            # Hoja 2: Duplicados SOFTSEGUROS
            if len(self.resultados['softseguros']['duplicados']) > 0:
                self.resultados['softseguros']['duplicados'].to_excel(
                    writer, sheet_name='Duplicados_SoftSeguros', index=False
                )
            
            # Hoja 3: Duplicados CELER
            if len(self.resultados['celer']['duplicados']) > 0:
                self.resultados['celer']['duplicados'].to_excel(
                    writer, sheet_name='Duplicados_Celer', index=False
                )
            
            # Hoja 4: Problemas de formato
            if len(self.resultados['softseguros']['problemas_formato']) > 0:
                df_problemas = pd.DataFrame(self.resultados['softseguros']['problemas_formato'])
                df_problemas.to_excel(writer, sheet_name='Problemas_Formato', index=False)
            
            # Hoja 5: IDs sin datos
            if len(self.resultados['softseguros']['ids_vacios']) > 0:
                self.resultados['softseguros']['ids_vacios'].to_excel(
                    writer, sheet_name='Sin_ID_SoftSeguros', index=False
                )
            
            if len(self.resultados['celer']['ids_vacios']) > 0:
                self.resultados['celer']['ids_vacios'].to_excel(
                    writer, sheet_name='Sin_ID_Celer', index=False
                )
        
        logger.info(f"✅ Reporte generado: {archivo_reporte}")
        return archivo_reporte


def main():
    """Función principal"""
    # Rutas de los archivos
    ruta_softseguros = 'CLIENTES SOFTSEGUROS.xlsx'
    ruta_celer = 'CLIENTES VIGENTES CELER.xlsx'
    
    # Crear analizador
    analizador = AnalizadorIdentificaciones(ruta_softseguros, ruta_celer)
    
    # Cargar datos
    analizador.cargar_datos()
    
    # Analizar cada archivo
    df_soft = analizador.analizar_softseguros()
    df_celer = analizador.analizar_celer()
    
    # Comparar bases
    analizador.comparar_bases(df_soft, df_celer)
    
    # Generar reporte
    archivo_reporte = analizador.generar_reporte()
    
    logger.info("\n" + "="*60)
    logger.info("ANÁLISIS COMPLETADO")
    logger.info("="*60)
    logger.info(f"Revise el archivo: {archivo_reporte}")


if __name__ == "__main__":
    main()
