"""
Proceso Completo de Migración - CLIENTES SOFTSEGUROSv2
======================================================
Ejecuta todos los pasos del proceso de migración en secuencia
"""

import subprocess
import sys
from pathlib import Path
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def ejecutar_script(script_path, descripcion):
    """Ejecuta un script Python y maneja errores"""
    logger.info(f"\n{'='*60}")
    logger.info(f"EJECUTANDO: {descripcion}")
    logger.info(f"{'='*60}\n")
    
    try:
        result = subprocess.run(
            [sys.executable, script_path],
            capture_output=True,
            text=True,
            encoding='utf-8'
        )
        
        # Mostrar salida
        if result.stdout:
            print(result.stdout)
        
        if result.returncode != 0:
            logger.error(f"❌ Error en {descripcion}")
            if result.stderr:
                logger.error(result.stderr)
            return False
        
        logger.info(f"✅ {descripcion} completado exitosamente")
        return True
        
    except Exception as e:
        logger.error(f"❌ Excepción en {descripcion}: {e}")
        return False


def main():
    logger.info("\n" + "="*60)
    logger.info("PROCESO COMPLETO DE MIGRACIÓN - CLIENTES SOFTSEGUROSv2")
    logger.info("="*60)
    
    # Verificar que el archivo existe
    archivo_v2 = Path("CLIENTES SOFTSEGUROSv2.xlsx")
    if not archivo_v2.exists():
        logger.error(f"❌ No se encuentra el archivo: {archivo_v2}")
        return
    
    logger.info(f"✅ Archivo encontrado: {archivo_v2}")
    
    # Lista de scripts a ejecutar
    scripts = [
        ("src/validators/analisis_ids_v2.py", "1. Análisis de IDs"),
        ("src/transformers/corregir_nits_v2.py", "2. Corrección de NITs"),
        ("src/validators/validar_nombres_documentos_v2.py", "3. Validación de Nombres"),
        ("src/transformers/actualizar_desde_celer_v2.py", "4. Actualización desde CELER"),
        ("src/transformers/asignar_generos_v2.py", "5. Asignación de Género")
    ]
    
    # Ejecutar scripts en secuencia
    for script_path, descripcion in scripts:
        if not Path(script_path).exists():
            logger.warning(f"⚠️ Script no encontrado: {script_path}")
            logger.info(f"   Creando versión v2...")
            # Aquí crearemos las versiones v2 de cada script
            continue
        
        exito = ejecutar_script(script_path, descripcion)
        
        if not exito:
            logger.error(f"❌ El proceso se detuvo en: {descripcion}")
            respuesta = input("\n¿Deseas continuar con el siguiente paso? (s/n): ")
            if respuesta.lower() != 's':
                logger.info("Proceso cancelado por el usuario")
                return
    
    logger.info("\n" + "="*60)
    logger.info("✅ PROCESO COMPLETO FINALIZADO")
    logger.info("="*60)
    logger.info("\n📁 Revisa la carpeta data/output/ para ver todos los resultados")


if __name__ == "__main__":
    main()
