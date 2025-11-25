"""
Actualización de Datos SOFTSEGUROS desde CELER
===============================================
Este script actualiza los datos de SOFTSEGUROS tomando como fuente de verdad
el archivo CELER. Compara y actualiza: nombres, fecha de nacimiento, teléfono,
email y dirección.
"""

import pandas as pd
import re
from pathlib import Path
from datetime import datetime
import logging
from openpyxl.styles import Font, PatternFill, Alignment

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class ActualizadorDatos:
    """Actualiza datos de SOFTSEGUROS con información de CELER"""
    
    def __init__(self, archivo_softseguros, archivo_celer):
        self.archivo_softseguros = archivo_softseguros
        self.archivo_celer = archivo_celer
        self.df_soft = None
        self.df_celer = None
        self.cambios = []
        self.estadisticas = {
            'nombres': 0,
            'fecha_nacimiento': 0,
            'telefono': 0,
            'email': 0,
            'direccion': 0,
            'total_registros_procesados': 0,
            'registros_con_cambios': 0
        }
        
    def cargar_datos(self):
        """Carga ambos archivos Excel"""
        logger.info("Cargando archivos...")
        try:
            self.df_soft = pd.read_excel(self.archivo_softseguros)
            self.df_celer = pd.read_excel(self.archivo_celer)
            logger.info(f"✅ SOFTSEGUROS: {len(self.df_soft)} registros")
            logger.info(f"✅ CELER: {len(self.df_celer)} registros")
        except Exception as e:
            logger.error(f"❌ Error al cargar archivos: {e}")
            raise
    
    def limpiar_identificacion(self, identificacion):
        """Limpia identificación para comparación"""
        if pd.isna(identificacion):
            return None
        return re.sub(r'[^\d]', '', str(identificacion))
    
    def normalizar_texto(self, texto):
        """Normaliza texto para comparación"""
        if pd.isna(texto) or texto == '':
            return None
        texto = str(texto).strip().upper()
        texto = re.sub(r'\s+', ' ', texto)
        return texto if texto else None
    
    def normalizar_fecha(self, fecha):
        """Normaliza fecha para comparación"""
        if pd.isna(fecha) or fecha == '':
            return None
        return str(fecha).strip()
    
    def separar_nombre_completo(self, nombre_completo):
        """
        Intenta separar un nombre completo en nombres y apellidos
        Asume: primeras 2 palabras = nombres, resto = apellidos
        """
        if not nombre_completo:
            return None, None
        
        partes = nombre_completo.strip().split()
        
        if len(partes) == 0:
            return None, None
        elif len(partes) == 1:
            return partes[0], ''
        elif len(partes) == 2:
            return partes[0], partes[1]
        else:
            # Asumimos: primeras 2 palabras = nombres, resto = apellidos
            nombres = ' '.join(partes[:2])
            apellidos = ' '.join(partes[2:])
            return nombres, apellidos
    
    def limpiar_telefono(self, telefono):
        """Limpia número de teléfono eliminando .0 y convirtiendo a entero"""
        if pd.isna(telefono) or telefono == '':
            return ''
        
        try:
            # Convertir a float primero, luego a int para eliminar decimales
            telefono_limpio = int(float(telefono))
            return str(telefono_limpio)
        except (ValueError, TypeError):
            # Si no se puede convertir, devolver como string sin espacios
            return str(telefono).strip()
    
    def valores_diferentes(self, valor_soft, valor_celer):
        """Compara si dos valores son diferentes (considerando normalización)"""
        # Si CELER está vacío, no actualizar
        if valor_celer is None or valor_celer == '':
            return False
        
        # Si SOFTSEGUROS está vacío y CELER tiene dato, actualizar
        if (valor_soft is None or valor_soft == '') and valor_celer:
            return True
        
        # Comparar valores normalizados
        return str(valor_soft).strip().upper() != str(valor_celer).strip().upper()
    
    def preparar_datos(self):
        """Prepara DataFrames con identificaciones limpias"""
        logger.info("\n=== PREPARANDO DATOS ===")
        
        # SOFTSEGUROS - crear índice por ID limpio
        self.df_soft['ID_LIMPIO'] = self.df_soft['NÚMERO DE DOCUMENTO'].apply(
            self.limpiar_identificacion
        )
        
        # CELER - crear índice por ID limpio
        self.df_celer['ID_LIMPIO'] = self.df_celer['Identificacion'].apply(
            self.limpiar_identificacion
        )
        
        # Crear diccionario para búsqueda rápida en CELER
        self.celer_dict = {}
        for idx, row in self.df_celer.iterrows():
            id_limpio = row['ID_LIMPIO']
            if id_limpio:
                self.celer_dict[id_limpio] = {
                    'Tomador': row.get('Tomador'),
                    'F_Nac_Tomador': row.get('F_Nac_Tomador'),
                    'Celular_Pers': row.get('Celular_Pers'),
                    'Mail_Pers': row.get('Mail_Pers'),
                    'Direccion_Pers': row.get('Direccion_Pers'),
                    'Ciudad_Pers': row.get('Ciudad_Pers')
                }
        
        logger.info(f"✅ Índice CELER creado con {len(self.celer_dict)} registros")
    
    def actualizar_datos(self):
        """Actualiza datos de SOFTSEGUROS con información de CELER"""
        logger.info("\n=== ACTUALIZANDO DATOS ===")
        
        registros_encontrados = 0
        registros_no_encontrados = 0
        
        for idx, row_soft in self.df_soft.iterrows():
            self.estadisticas['total_registros_procesados'] += 1
            id_limpio = row_soft['ID_LIMPIO']
            
            if not id_limpio or id_limpio not in self.celer_dict:
                registros_no_encontrados += 1
                continue
            
            registros_encontrados += 1
            row_celer = self.celer_dict[id_limpio]
            cambios_en_registro = []
            
            # 1. ACTUALIZAR NOMBRES Y APELLIDOS
            nombre_celer_completo = self.normalizar_texto(row_celer['Tomador'])
            if nombre_celer_completo:
                nombres_soft = self.normalizar_texto(row_soft['NOMBRES'])
                apellidos_soft = self.normalizar_texto(row_soft['APELLIDOS'])
                nombre_soft_completo = f"{nombres_soft or ''} {apellidos_soft or ''}".strip()
                
                if nombre_soft_completo != nombre_celer_completo:
                    # Separar nombre completo de CELER
                    nombres_nuevo, apellidos_nuevo = self.separar_nombre_completo(nombre_celer_completo)
                    
                    if nombres_nuevo:
                        self.df_soft.at[idx, 'NOMBRES'] = nombres_nuevo
                        cambios_en_registro.append({
                            'campo': 'NOMBRES',
                            'valor_anterior': row_soft['NOMBRES'],
                            'valor_nuevo': nombres_nuevo
                        })
                        self.estadisticas['nombres'] += 1
                    
                    if apellidos_nuevo:
                        self.df_soft.at[idx, 'APELLIDOS'] = apellidos_nuevo
                        cambios_en_registro.append({
                            'campo': 'APELLIDOS',
                            'valor_anterior': row_soft['APELLIDOS'],
                            'valor_nuevo': apellidos_nuevo
                        })
            
            # 2. ACTUALIZAR FECHA DE NACIMIENTO
            fecha_celer = self.normalizar_fecha(row_celer['F_Nac_Tomador'])
            fecha_soft = self.normalizar_fecha(row_soft['FECHA DE NACIMIENTO'])
            
            if fecha_celer and self.valores_diferentes(fecha_soft, fecha_celer):
                self.df_soft.at[idx, 'FECHA DE NACIMIENTO'] = fecha_celer
                cambios_en_registro.append({
                    'campo': 'FECHA DE NACIMIENTO',
                    'valor_anterior': fecha_soft,
                    'valor_nuevo': fecha_celer
                })
                self.estadisticas['fecha_nacimiento'] += 1
            
            # 3. ACTUALIZAR TELÉFONO MÓVIL
            telefono_celer = self.limpiar_telefono(row_celer['Celular_Pers'])
            telefono_soft = self.limpiar_telefono(row_soft['TELÉFONO MÓVIL'])
            
            if telefono_celer and self.valores_diferentes(telefono_soft, telefono_celer):
                self.df_soft.at[idx, 'TELÉFONO MÓVIL'] = telefono_celer
                cambios_en_registro.append({
                    'campo': 'TELÉFONO MÓVIL',
                    'valor_anterior': telefono_soft,
                    'valor_nuevo': telefono_celer
                })
                self.estadisticas['telefono'] += 1
            
            # 4. ACTUALIZAR EMAIL
            email_celer = self.normalizar_texto(row_celer['Mail_Pers'])
            email_soft = self.normalizar_texto(row_soft['EMAIL'])
            
            if email_celer and self.valores_diferentes(email_soft, email_celer):
                self.df_soft.at[idx, 'EMAIL'] = email_celer
                cambios_en_registro.append({
                    'campo': 'EMAIL',
                    'valor_anterior': email_soft,
                    'valor_nuevo': email_celer
                })
                self.estadisticas['email'] += 1
            
            # 5. ACTUALIZAR DIRECCIÓN
            direccion_celer = self.normalizar_texto(row_celer['Direccion_Pers'])
            direccion_soft = self.normalizar_texto(row_soft['DIRECCIÓN PRINCIPAL'])
            
            if direccion_celer and self.valores_diferentes(direccion_soft, direccion_celer):
                self.df_soft.at[idx, 'DIRECCIÓN PRINCIPAL'] = direccion_celer
                cambios_en_registro.append({
                    'campo': 'DIRECCIÓN PRINCIPAL',
                    'valor_anterior': direccion_soft,
                    'valor_nuevo': direccion_celer
                })
                self.estadisticas['direccion'] += 1
            
            # 6. ACTUALIZAR CIUDAD (bonus)
            ciudad_celer = self.normalizar_texto(row_celer['Ciudad_Pers'])
            ciudad_soft = self.normalizar_texto(row_soft['CIUDAD'])
            
            if ciudad_celer and self.valores_diferentes(ciudad_soft, ciudad_celer):
                self.df_soft.at[idx, 'CIUDAD'] = ciudad_celer
            
            # Registrar cambios si hubo alguno
            if cambios_en_registro:
                self.estadisticas['registros_con_cambios'] += 1
                for cambio in cambios_en_registro:
                    self.cambios.append({
                        'id_documento': row_soft['NÚMERO DE DOCUMENTO'],
                        'nombre_cliente': f"{row_soft['NOMBRES']} {row_soft['APELLIDOS']}",
                        'campo': cambio['campo'],
                        'valor_anterior': cambio['valor_anterior'],
                        'valor_nuevo': cambio['valor_nuevo']
                    })
        
        logger.info(f"\n📊 RESUMEN DE ACTUALIZACIÓN:")
        logger.info(f"  Total registros procesados: {self.estadisticas['total_registros_procesados']}")
        logger.info(f"  Registros encontrados en CELER: {registros_encontrados}")
        logger.info(f"  Registros NO encontrados en CELER: {registros_no_encontrados}")
        logger.info(f"  Registros con cambios: {self.estadisticas['registros_con_cambios']}")
        logger.info(f"\n📝 CAMBIOS POR CAMPO:")
        logger.info(f"  Nombres/Apellidos: {self.estadisticas['nombres']}")
        logger.info(f"  Fechas de nacimiento: {self.estadisticas['fecha_nacimiento']}")
        logger.info(f"  Teléfonos: {self.estadisticas['telefono']}")
        logger.info(f"  Emails: {self.estadisticas['email']}")
        logger.info(f"  Direcciones: {self.estadisticas['direccion']}")
        logger.info(f"\n  TOTAL DE CAMBIOS: {len(self.cambios)}")
        
        if len(self.cambios) > 0:
            logger.info(f"\n🔍 PRIMEROS 5 CAMBIOS:")
            for cambio in self.cambios[:5]:
                logger.info(f"\n  ID: {cambio['id_documento']} - {cambio['nombre_cliente'][:40]}")
                logger.info(f"  Campo: {cambio['campo']}")
                logger.info(f"  Anterior: {str(cambio['valor_anterior'])[:50]}")
                logger.info(f"  Nuevo: {str(cambio['valor_nuevo'])[:50]}")
    
    def generar_archivo_actualizado(self, ruta_salida='./data/output'):
        """Genera el archivo Excel actualizado"""
        logger.info("\n=== GENERANDO ARCHIVO ACTUALIZADO ===")
        
        Path(ruta_salida).mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        archivo_salida = f"{ruta_salida}/CLIENTES_SOFTSEGUROS_ACTUALIZADO_{timestamp}.xlsx"
        
        # Eliminar columnas auxiliares
        df_final = self.df_soft.drop(columns=['ID_LIMPIO'], errors='ignore')
        
        # Limpiar todos los teléfonos antes de exportar (eliminar .0)
        if 'TELÉFONO MÓVIL' in df_final.columns:
            df_final['TELÉFONO MÓVIL'] = df_final['TELÉFONO MÓVIL'].apply(self.limpiar_telefono)
        
        # Guardar Excel con formato
        with pd.ExcelWriter(archivo_salida, engine='openpyxl') as writer:
            df_final.to_excel(writer, sheet_name='CLIENTES', index=False)
            
            worksheet = writer.sheets['CLIENTES']
            self._aplicar_formato_header(worksheet)
            self._ajustar_ancho_columnas(worksheet)
        
        logger.info(f"✅ Archivo actualizado: {archivo_salida}")
        return archivo_salida
    
    def generar_reporte_cambios(self, ruta_salida='./data/output'):
        """Genera reporte detallado de cambios realizados"""
        logger.info("\n=== GENERANDO REPORTE DE CAMBIOS ===")
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        archivo_reporte = f"{ruta_salida}/REPORTE_ACTUALIZACIONES_{timestamp}.xlsx"
        
        with pd.ExcelWriter(archivo_reporte, engine='openpyxl') as writer:
            # Hoja 1: Resumen
            resumen = [
                ['REPORTE DE ACTUALIZACIÓN DE DATOS', ''],
                ['Fecha', datetime.now().strftime('%Y-%m-%d %H:%M:%S')],
                ['Archivo origen SOFTSEGUROS', self.archivo_softseguros],
                ['Archivo base CELER', self.archivo_celer],
                ['', ''],
                ['ESTADÍSTICAS GENERALES', ''],
                ['Total registros procesados', self.estadisticas['total_registros_procesados']],
                ['Registros con cambios', self.estadisticas['registros_con_cambios']],
                ['Total de cambios realizados', len(self.cambios)],
                ['', ''],
                ['CAMBIOS POR CAMPO', ''],
                ['Nombres/Apellidos actualizados', self.estadisticas['nombres']],
                ['Fechas de nacimiento actualizadas', self.estadisticas['fecha_nacimiento']],
                ['Teléfonos actualizados', self.estadisticas['telefono']],
                ['Emails actualizados', self.estadisticas['email']],
                ['Direcciones actualizadas', self.estadisticas['direccion']],
            ]
            
            df_resumen = pd.DataFrame(resumen, columns=['Descripción', 'Valor'])
            df_resumen.to_excel(writer, sheet_name='Resumen', index=False)
            
            # Hoja 2: Detalle de cambios
            if self.cambios:
                df_cambios = pd.DataFrame(self.cambios)
                df_cambios.to_excel(writer, sheet_name='Detalle_Cambios', index=False)
            
            # Aplicar formato a todas las hojas
            for sheet_name in writer.sheets:
                worksheet = writer.sheets[sheet_name]
                self._aplicar_formato_header(worksheet)
                self._ajustar_ancho_columnas(worksheet)
        
        logger.info(f"✅ Reporte de cambios: {archivo_reporte}")
        return archivo_reporte
    
    def _aplicar_formato_header(self, worksheet):
        """Aplica formato profesional a los encabezados"""
        header_fill = PatternFill(start_color="366092", end_color="366092", fill_type="solid")
        header_font = Font(bold=True, color="FFFFFF", size=11)
        
        for cell in worksheet[1]:
            cell.fill = header_fill
            cell.font = header_font
            cell.alignment = Alignment(horizontal="center", vertical="center")
    
    def _ajustar_ancho_columnas(self, worksheet):
        """Ajusta automáticamente el ancho de las columnas"""
        for column in worksheet.columns:
            max_length = 0
            column_letter = column[0].column_letter
            
            for cell in column:
                if cell.value:
                    max_length = max(max_length, len(str(cell.value)))
            
            adjusted_width = min(max_length + 2, 60)
            worksheet.column_dimensions[column_letter].width = adjusted_width


def main():
    """Función principal"""
    # Archivos de entrada
    archivo_softseguros = './data/output/CLIENTES_SOFTSEGUROS_CORREGIDO_20251107_155219.xlsx'
    archivo_celer = 'CLIENTES VIGENTES CELER.xlsx'
    
    logger.info("="*60)
    logger.info("ACTUALIZACIÓN DE DATOS SOFTSEGUROS DESDE CELER")
    logger.info("="*60)
    
    # Crear actualizador
    actualizador = ActualizadorDatos(archivo_softseguros, archivo_celer)
    
    # Cargar datos
    actualizador.cargar_datos()
    
    
    # Preparar datos
    actualizador.preparar_datos()
    
    # Actualizar datos
    actualizador.actualizar_datos()
    
    # Generar archivos de salida
    archivo_actualizado = actualizador.generar_archivo_actualizado()
    archivo_reporte = actualizador.generar_reporte_cambios()
    
    logger.info("\n" + "="*60)
    logger.info("✅ PROCESO COMPLETADO")
    logger.info("="*60)
    logger.info(f"📁 Archivo actualizado: {archivo_actualizado}")
    logger.info(f"📊 Reporte de cambios: {archivo_reporte}")


if __name__ == "__main__":
    main()
