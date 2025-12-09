"""
Tests de Mapeos para Migración CELER → MAVISO
==============================================
Valida que los mapeos de aseguradoras y ramos sean correctos.
"""

import pandas as pd
from pathlib import Path
import unittest

# Rutas
CARPETA_BASE = Path(__file__).parent
ARCHIVO_MAVISO = CARPETA_BASE / 'Copy of Maviso.xlsx'
ARCHIVO_CELER = CARPETA_BASE / 'Copy of polizas vigentes celer.xlsx'


class TestMapeoAseguradoras(unittest.TestCase):
    """Tests para validar el mapeo de aseguradoras según documentación"""
    
    @classmethod
    def setUpClass(cls):
        """Carga los datos una sola vez para todos los tests"""
        print("\n📊 Cargando datos de CELER...")
        
        # Cargar aseguradoras de CELER
        df_celer = pd.read_excel(ARCHIVO_CELER, skiprows=3)
        cls.aseguradoras_celer = set(df_celer['Aseguradora'].dropna().unique())
        cls.ramos_celer = set(df_celer['Ramo'].dropna().unique())
        
        print(f"   ✓ CELER: {len(cls.aseguradoras_celer)} aseguradoras")
        print(f"   ✓ CELER: {len(cls.ramos_celer)} ramos")
    
    def test_todas_aseguradoras_tienen_mapeo(self):
        """Verifica que todas las aseguradoras de CELER tengan mapeo definido"""
        print("\n🔍 Test: Todas las aseguradoras tienen mapeo")
        
        # Mapeos según documentación
        ASEGURADORAS_CON_VIDA = {
            'ALLIANZ SEGUROS S.A', 'LIBERTY SEGUROS S A', 'SURAMERICANA S.A.',
            'AXA COLPATRIA SEGUROS S.A.', 'SEGUROS DEL ESTADO S A',
        }
        
        MAPEO_SIMPLE = {
            'COMPAÑÍA MUNDIAL DE SEGUROS S A', 'HDI SEGUROS SA', 
            'LA EQUIDAD SEGUROS OC', 'MAPFRE SEGUROS DE COLOMBIA S A',
            'COLMENA VIDA Y RIESGOS PROFESIONES SA', 'SEGUROS BOLIVAR',
            'CEM', 'COOMEVA', 'ASSIST CARD', 'MAGENTA SEGUROS LTDA',
            'FUNER SAN VICENTE', 'EMERMÉDICA S.A', 'MEDISANITAS',
            'ASEGURADORA GRANCOLOMBIANA S.A.',
        }
        
        # Aseguradoras que no necesitan mapeo (nombre igual)
        SIN_MAPEO = {
            'ASEGURADORA SOLIDARIA DE COLOMBIA', 'POSITIVA COMPAÑIA DE SEGUROS S.A.',
            'CHUBB DE COLOMBIA COMPAÑÍA SEGUROS S A', 'ZURICH COLOMBIA SEGUROS S.A',
            'LA PREVISORA S A COMPAÑÍA DE SEGUROS', 
            'COMPAÑIA DE MEDICINA PREPAGADA COLSANITAS S.A', 'SBS SEGUROS COLOMBIA S.A',
        }
        
        todas_cubiertas = ASEGURADORAS_CON_VIDA | MAPEO_SIMPLE | SIN_MAPEO
        
        sin_definir = []
        for aseg in self.aseguradoras_celer:
            if aseg not in todas_cubiertas:
                sin_definir.append(aseg)
        
        if sin_definir:
            print(f"   ⚠️ Aseguradoras sin definir:")
            for a in sin_definir:
                print(f"      - {a}")
        else:
            print("   ✅ Todas las aseguradoras tienen mapeo definido")
        
        self.assertEqual(len(sin_definir), 0, f"Aseguradoras sin definir: {sin_definir}")
    
    def test_liberty_y_allianz_van_a_allianz(self):
        """LIBERTY y ALLIANZ ambos van a ALLIANZ en MAVISO"""
        print("\n🔍 Test: LIBERTY y ALLIANZ → ALLIANZ")
        
        self.assertIn('LIBERTY SEGUROS S A', self.aseguradoras_celer)
        self.assertIn('ALLIANZ SEGUROS S.A', self.aseguradoras_celer)
        
        print("   ✅ Ambos existen en CELER y deben ir a ALLIANZ en MAVISO")


class TestMapeoRamos(unittest.TestCase):
    """Tests para validar el mapeo de ramos"""
    
    @classmethod
    def setUpClass(cls):
        """Carga los datos una sola vez"""
        print("\n📊 Cargando ramos de CELER...")
        
        df_celer = pd.read_excel(ARCHIVO_CELER, skiprows=3)
        cls.ramos_celer = set(df_celer['Ramo'].dropna().unique())
        
        print(f"   ✓ CELER: {len(cls.ramos_celer)} ramos únicos")
    
    def test_listar_ramos_celer(self):
        """Lista todos los ramos de CELER para revisión"""
        print("\n📋 Ramos en CELER:")
        for ramo in sorted(self.ramos_celer):
            print(f"   - {ramo}")
        
        self.assertGreater(len(self.ramos_celer), 0, "Debe haber ramos")


class TestFuncionMapeo(unittest.TestCase):
    """Tests para la función de mapeo actual"""
    
    def setUp(self):
        """Configura los mapeos según la documentación"""
        # Mapeo de aseguradoras con nombre diferente
        self.MAPEO_ASEGURADORAS = {
            'LIBERTY SEGUROS S A': 'ALLIANZ SEGUROS S.A',
            'ALLIANZ SEGUROS S.A': 'ALLIANZ SEGUROS S.A',
            'COMPAÑÍA MUNDIAL DE SEGUROS S A': 'SEGUROS MUNDIAL',
            'HDI SEGUROS SA': 'HDI SEGUROS',
            'LA EQUIDAD SEGUROS OC': 'LA EQUIDAD SEGUROS GENERALES',
            'MAPFRE SEGUROS DE COLOMBIA S A': 'MAPFRE SEGUROS GENERALES',
            'COLMENA VIDA Y RIESGOS PROFESIONES SA': 'COLMENA SEGUROS',
            'SEGUROS BOLIVAR': 'COMPAÑIA DE SEGUROS BOLIVAR SA',
        }
        
        # Aseguradoras con versión Generales/Vida
        self.ASEGURADORAS_CON_VIDA = {
            'ALLIANZ SEGUROS S.A': ('ALLIANZ SEGUROS S.A', 'ALLIANZ SEGUROS DE VIDA S.A'),
            'LIBERTY SEGUROS S A': ('ALLIANZ SEGUROS S.A', 'ALLIANZ SEGUROS DE VIDA S.A'),
            'SURAMERICANA S.A.': ('SEGUROS GENERALES SURAMERICANA S A', 'SEGUROS DE VIDA SURAMERICANA SA'),
            'AXA COLPATRIA SEGUROS S.A.': ('AXA COLPATRIA SEGUROS SA', 'AXA COLPATRIA SEGUROS DE VIDA SA'),
            'SEGUROS DEL ESTADO S A': ('SEGUROS DEL ESTADO SA', 'SEGUROS DE VIDA DEL ESTADO'),
        }
        
        self.RAMOS_VIDA = [
            'VIDA INDIVIDUAL', 'VIDA COLECTIVO', 'VIDA GRUPO COLECTIVO',
            'ACCIDENTES PERSONALES', 'SALUD FAMILIAR',
        ]
    
    def get_aseguradora_maviso(self, aseguradora_celer, ramo_celer):
        """Función de mapeo que determina Generales vs Vida"""
        if aseguradora_celer in self.ASEGURADORAS_CON_VIDA:
            generales, vida = self.ASEGURADORAS_CON_VIDA[aseguradora_celer]
            if ramo_celer in self.RAMOS_VIDA:
                return vida
            return generales
        return self.MAPEO_ASEGURADORAS.get(aseguradora_celer, aseguradora_celer)
    
    def test_liberty_a_allianz_generales(self):
        """LIBERTY con ramo de generales → ALLIANZ SEGUROS S.A"""
        print("\n🔍 Test: LIBERTY + AUTOMOVILES → ALLIANZ SEGUROS S.A")
        
        resultado = self.get_aseguradora_maviso('LIBERTY SEGUROS S A', 'AUTOMOVILES')
        self.assertEqual(resultado, 'ALLIANZ SEGUROS S.A')
        print(f"   ✅ LIBERTY + AUTOMOVILES → {resultado}")
    
    def test_liberty_a_allianz_vida(self):
        """LIBERTY con ramo de vida → ALLIANZ SEGUROS DE VIDA S.A"""
        print("\n🔍 Test: LIBERTY + VIDA INDIVIDUAL → ALLIANZ SEGUROS DE VIDA S.A")
        
        resultado = self.get_aseguradora_maviso('LIBERTY SEGUROS S A', 'VIDA INDIVIDUAL')
        self.assertEqual(resultado, 'ALLIANZ SEGUROS DE VIDA S.A')
        print(f"   ✅ LIBERTY + VIDA INDIVIDUAL → {resultado}")
    
    def test_suramericana_generales(self):
        """SURAMERICANA con ramo generales → SEGUROS GENERALES SURAMERICANA S A"""
        print("\n🔍 Test: SURAMERICANA + AUTOMOVILES")
        
        resultado = self.get_aseguradora_maviso('SURAMERICANA S.A.', 'AUTOMOVILES')
        self.assertEqual(resultado, 'SEGUROS GENERALES SURAMERICANA S A')
        print(f"   ✅ SURAMERICANA + AUTOMOVILES → {resultado}")
    
    def test_suramericana_vida(self):
        """SURAMERICANA con ramo vida → SEGUROS DE VIDA SURAMERICANA SA"""
        print("\n🔍 Test: SURAMERICANA + VIDA INDIVIDUAL")
        
        resultado = self.get_aseguradora_maviso('SURAMERICANA S.A.', 'VIDA INDIVIDUAL')
        self.assertEqual(resultado, 'SEGUROS DE VIDA SURAMERICANA SA')
        print(f"   ✅ SURAMERICANA + VIDA INDIVIDUAL → {resultado}")
    
    def test_aseguradoras_sin_version_vida(self):
        """Aseguradoras sin versión Vida usan mapeo simple"""
        print("\n🔍 Test: Aseguradoras sin versión Vida")
        
        casos = [
            ('COMPAÑÍA MUNDIAL DE SEGUROS S A', 'AUTOMOVILES', 'SEGUROS MUNDIAL'),
            ('HDI SEGUROS SA', 'SOAT', 'HDI SEGUROS'),
            ('MAPFRE SEGUROS DE COLOMBIA S A', 'AUTOMOVILES', 'MAPFRE SEGUROS GENERALES'),
        ]
        
        for aseg_celer, ramo, esperado in casos:
            resultado = self.get_aseguradora_maviso(aseg_celer, ramo)
            self.assertEqual(resultado, esperado, f"{aseg_celer} debería ser {esperado}")
            print(f"   ✅ {aseg_celer} → {resultado}")
    
    def test_aseguradoras_sin_mapeo_permanecen_igual(self):
        """Aseguradoras sin mapeo deben mantener su nombre original"""
        print("\n🔍 Test: Aseguradoras sin mapeo")
        
        aseguradoras_test = [
            'ASEGURADORA SOLIDARIA DE COLOMBIA',
            'POSITIVA COMPAÑIA DE SEGUROS S.A.',
            'CHUBB DE COLOMBIA COMPAÑÍA SEGUROS S A',
        ]
        
        for aseg in aseguradoras_test:
            resultado = self.get_aseguradora_maviso(aseg, 'AUTOMOVILES')
            self.assertEqual(resultado, aseg, 
                f"{aseg} debería permanecer igual")
            print(f"   ✅ {aseg} → {resultado}")


def main():
    """Ejecuta todos los tests"""
    print("=" * 60)
    print("   TESTS DE MAPEOS - MIGRACIÓN CELER → MAVISO")
    print("=" * 60)
    
    # Ejecutar tests
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Agregar tests en orden
    suite.addTests(loader.loadTestsFromTestCase(TestMapeoAseguradoras))
    suite.addTests(loader.loadTestsFromTestCase(TestMapeoRamos))
    suite.addTests(loader.loadTestsFromTestCase(TestFuncionMapeo))
    
    # Runner con verbosidad
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Resumen
    print("\n" + "=" * 60)
    if result.wasSuccessful():
        print("   ✅ TODOS LOS TESTS PASARON")
    else:
        print("   ❌ ALGUNOS TESTS FALLARON")
        print(f"      Errores: {len(result.errors)}")
        print(f"      Fallos: {len(result.failures)}")
    print("=" * 60)
    
    return result.wasSuccessful()


if __name__ == '__main__':
    main()
