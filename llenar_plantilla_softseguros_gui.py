#!/usr/bin/env python3
"""
GUI para llenar plantilla de SoftSeguros con datos de Celer.
Dark mode profesional con logs y progreso en tiempo real.
"""

import sys
import os
import pandas as pd
import re
from datetime import datetime
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QTextEdit, QGroupBox, QFileDialog, QMessageBox,
    QComboBox
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QFont


class LlenadorThread(QThread):
    """Thread para ejecutar el llenado sin bloquear la GUI"""
    log_signal = pyqtSignal(str, str)  # mensaje, tipo
    finished_signal = pyqtSignal(bool, str, dict)  # éxito, mensaje, estadísticas
    
    def __init__(self, archivo_nits, columna_nits, archivo_celer, archivo_salida):
        super().__init__()
        self.archivo_nits = archivo_nits
        self.columna_nits = columna_nits
        self.archivo_celer = archivo_celer
        self.archivo_salida = archivo_salida
    
    def separar_nombre_apellidos(self, nombre_completo):
        """Separa el nombre completo en nombres y apellidos"""
        if pd.isna(nombre_completo) or not str(nombre_completo).strip():
            return "", ""
        
        nombre_str = str(nombre_completo).strip().upper()
        
        # Si tiene coma, separar por coma (APELLIDOS, NOMBRES)
        if ',' in nombre_str:
            partes = nombre_str.split(',', 1)
            apellidos = partes[0].strip()
            nombres = partes[1].strip() if len(partes) > 1 else ""
            return nombres, apellidos
        
        # Sin coma: primeras 2 palabras son apellidos, resto son nombres
        palabras = nombre_str.split()
        if len(palabras) <= 2:
            return "", nombre_str
        elif len(palabras) == 3:
            apellidos = " ".join(palabras[:2])
            nombres = palabras[2]
            return nombres, apellidos
        else:
            apellidos = " ".join(palabras[:2])
            nombres = " ".join(palabras[2:])
            return nombres, apellidos
    
    def mapear_tipo_documento(self, tipo_celer):
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
    
    def mapear_genero(self, genero_celer):
        """Mapea el género de Celer a SoftSeguros"""
        if pd.isna(genero_celer):
            return ""
        
        genero = str(genero_celer).upper().strip()
        
        if genero in ['M', 'MASCULINO', 'HOMBRE']:
            return 'Masculino'
        elif genero in ['F', 'FEMENINO', 'MUJER']:
            return 'Femenino'
        
        return genero
    
    def mapear_estado_civil(self, estado_celer):
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
    
    def limpiar_identificacion(self, valor):
        """Limpia la identificación para comparación (solo números)"""
        if pd.isna(valor):
            return ""
        return re.sub(r'\D', '', str(valor))
    
    def run(self):
        try:
            # 1. Leer NITs
            self.log_signal.emit("📂 Leyendo archivo de NITs...", "info")
            df_nits = pd.read_excel(self.archivo_nits, dtype=str)
            
            # Usar la columna seleccionada
            if self.columna_nits not in df_nits.columns:
                raise ValueError(f"Columna '{self.columna_nits}' no encontrada en el archivo")
            
            nits_buscar = df_nits[self.columna_nits].dropna().apply(self.limpiar_identificacion).unique().tolist()
            nits_buscar = [n for n in nits_buscar if n]
            
            self.log_signal.emit(f"✅ Columna seleccionada: {self.columna_nits}", "success")
            self.log_signal.emit(f"✅ NITs a buscar: {len(nits_buscar)}", "success")
            
            # 2. Leer CELER
            self.log_signal.emit("📂 Leyendo datos de CELER...", "info")
            df_celer = pd.read_excel(self.archivo_celer, dtype=str)
            df_celer['_id_limpia'] = df_celer['Identificacion'].apply(self.limpiar_identificacion)
            
            self.log_signal.emit(f"✅ Registros CELER: {len(df_celer)}", "success")
            
            # 3. Definir columnas de SoftSeguros (formato estándar)
            self.log_signal.emit("📋 Preparando estructura SoftSeguros...", "info")
            columnas_plantilla = [
                'NOMBRES', 'APELLIDOS', 'SOBRENOMBRE (ALIAS)', 'NÚMERO DE DOCUMENTO',
                'TIPO DE DOCUMENTO', 'GÉNERO', 'ESTADO CIVIL', 'FECHA DE NACIMIENTO',
                'TELÉFONO MÓVIL', 'TIPO TELÉFONO MÓVIL', 'TELÉFONO PRINCIPAL',
                'TIPO DE TELÉFONO PRINCIPAL', 'TELÉFONO SECUNDARIO', 'TIPO DE TELÉFONO SECUNDARIO',
                'EMAIL', 'TIPO EMAIL', 'EMAIL SECUNDARIO', 'TIPO EMAIL SECUNDARIO',
                'DIRECCIÓN PRINCIPAL', 'TIPO DIRECCIÓN', 'DIRECCIÓN SECUNDARIA',
                'TIPO DIRECCIÓN SECUNDARIA', 'PAÍS', 'ESTADO', 'CIUDAD', 'OCUPACIÓN',
                'INGRESO MENSUAL', 'PATRIMONIO', 'CASA PROPIA', 'NÚMERO DE CASAS',
                'HIJOS', 'NÚMERO DE HIJOS', 'VEHÍCULOS', 'NÚMERO DE VEHÍCULOS',
                'PAGINA WEB', 'REDES SOCIALES', 'NOMBRE DE CONTACTO', 'CATEGORÍAS',
                'OBSERVACIONES', 'CARGADO POR'
            ]
            
            self.log_signal.emit(f"✅ Estructura definida: {len(columnas_plantilla)} campos", "success")
            
            # 4. Buscar y mapear
            self.log_signal.emit("", "info")
            self.log_signal.emit("🔍 Buscando y mapeando datos...", "info")
            self.log_signal.emit("="*60, "info")
            
            registros_encontrados = []
            no_encontrados = []
            
            for i, nit in enumerate(nits_buscar, 1):
                match = df_celer[df_celer['_id_limpia'] == nit]
                
                if len(match) == 0:
                    no_encontrados.append(nit)
                    self.log_signal.emit(f"⚠️ [{i}/{len(nits_buscar)}] NIT {nit}: No encontrado", "warning")
                    continue
                
                row = match.iloc[0]
                nombres, apellidos = self.separar_nombre_apellidos(row.get('Nombre', ''))
                
                registro = {
                    'NOMBRES': nombres,
                    'APELLIDOS': apellidos,
                    'SOBRENOMBRE (ALIAS)': '',
                    'NÚMERO DE DOCUMENTO': row.get('Identificacion', ''),
                    'TIPO DE DOCUMENTO': self.mapear_tipo_documento(row.get('Tipo_Doc', '')),
                    'GÉNERO': self.mapear_genero(row.get('Genero', '')),
                    'ESTADO CIVIL': self.mapear_estado_civil(row.get('Estado_civil', '')),
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
                
                if i <= 10 or i % 50 == 0:
                    self.log_signal.emit(f"✅ [{i}/{len(nits_buscar)}] {nit}: {nombres} {apellidos}", "success")
            
            # 5. Guardar
            if registros_encontrados:
                self.log_signal.emit("", "info")
                self.log_signal.emit("💾 Guardando plantilla...", "info")
                
                df_resultado = pd.DataFrame(registros_encontrados)
                
                for col in columnas_plantilla:
                    if col not in df_resultado.columns:
                        df_resultado[col] = ''
                
                df_resultado = df_resultado[columnas_plantilla]
                df_resultado.to_excel(self.archivo_salida, index=False, engine='openpyxl')
                
                self.log_signal.emit(f"✅ Plantilla guardada: {os.path.basename(self.archivo_salida)}", "success")
            
            # Mostrar TODOS los no encontrados en los logs
            if no_encontrados:
                self.log_signal.emit("", "warning")
                self.log_signal.emit("="*60, "warning")
                self.log_signal.emit(f"⚠️ NITs NO ENCONTRADOS EN CELER ({len(no_encontrados)}):", "warning")
                self.log_signal.emit("="*60, "warning")
                for nit in no_encontrados:
                    self.log_signal.emit(f"  • {nit}", "warning")
                self.log_signal.emit("="*60, "warning")
            
            # Estadísticas
            estadisticas = {
                'total': len(nits_buscar),
                'encontrados': len(registros_encontrados),
                'no_encontrados': len(no_encontrados)
            }
            
            self.finished_signal.emit(True, "Proceso completado", estadisticas)
            
        except Exception as e:
            self.log_signal.emit(f"❌ Error: {str(e)}", "error")
            self.finished_signal.emit(False, str(e), {})


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Llenar Plantilla SoftSeguros - Migración Clientes CELER")
        self.setMinimumSize(1000, 700)
        
        # Variables
        self.archivo_nits = None
        self.columna_nits = None
        self.archivo_celer = None
        self.archivo_salida = None
        
        # Setup UI
        self.init_ui()
        self.aplicar_estilos()
    
    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Título
        titulo = QLabel("📋 Llenar Plantilla SoftSeguros desde CELER")
        titulo.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(titulo)
        
        subtitulo = QLabel("Migración de datos de clientes desde InformedePersonas CELER")
        subtitulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitulo.setObjectName("subtitulo")
        layout.addWidget(subtitulo)
        
        # Grupo: Archivos
        grupo_archivos = QGroupBox("📁 Archivos")
        layout_archivos = QVBoxLayout(grupo_archivos)
        
        # Archivo NITs
        layout_nits = QHBoxLayout()
        lbl_nits = QLabel("NITs a buscar:")
        lbl_nits.setMinimumWidth(150)
        self.lbl_ruta_nits = QLabel("No seleccionado")
        self.lbl_ruta_nits.setObjectName("archivo")
        btn_nits = QPushButton("📂 Seleccionar")
        btn_nits.clicked.connect(self.seleccionar_nits)
        layout_nits.addWidget(lbl_nits)
        layout_nits.addWidget(self.lbl_ruta_nits, 1)
        layout_nits.addWidget(btn_nits)
        layout_archivos.addLayout(layout_nits)
        
        # Selector de columna para NITs
        layout_columna = QHBoxLayout()
        lbl_columna = QLabel("Columna de NITs:")
        lbl_columna.setMinimumWidth(150)
        self.combo_columna = QComboBox()
        self.combo_columna.setEnabled(False)
        self.combo_columna.currentTextChanged.connect(self.columna_seleccionada)
        layout_columna.addWidget(lbl_columna)
        layout_columna.addWidget(self.combo_columna, 1)
        layout_archivos.addLayout(layout_columna)
        
        # Archivo CELER
        layout_celer = QHBoxLayout()
        lbl_celer = QLabel("Datos CELER:")
        lbl_celer.setMinimumWidth(150)
        self.lbl_ruta_celer = QLabel("No seleccionado")
        self.lbl_ruta_celer.setObjectName("archivo")
        btn_celer = QPushButton("📂 Seleccionar")
        btn_celer.clicked.connect(self.seleccionar_celer)
        layout_celer.addWidget(lbl_celer)
        layout_celer.addWidget(self.lbl_ruta_celer, 1)
        layout_celer.addWidget(btn_celer)
        layout_archivos.addLayout(layout_celer)
        
        layout.addWidget(grupo_archivos)
        
        # Botón Ejecutar
        layout_btn = QHBoxLayout()
        layout_btn.addStretch()
        self.btn_ejecutar = QPushButton("🚀 EJECUTAR MIGRACIÓN")
        self.btn_ejecutar.setObjectName("btnEjecutar")
        self.btn_ejecutar.clicked.connect(self.ejecutar_llenado)
        self.btn_ejecutar.setEnabled(False)
        self.btn_ejecutar.setMinimumHeight(50)
        layout_btn.addWidget(self.btn_ejecutar)
        layout_btn.addStretch()
        layout.addLayout(layout_btn)
        
        # Grupo: Estadísticas
        grupo_stats = QGroupBox("📊 Estadísticas")
        layout_stats = QHBoxLayout(grupo_stats)
        
        self.stats_widgets = {}
        stats_config = [
            ('total', 'Total NITs', '#4ec9b0'),
            ('encontrados', 'Encontrados', '#6a9955'),
            ('no_encontrados', 'No Encontrados', '#f44747')
        ]
        
        for key, label, color in stats_config:
            container = QWidget()
            container_layout = QVBoxLayout(container)
            container_layout.setContentsMargins(10, 5, 10, 5)
            
            lbl = QLabel(label)
            lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            lbl.setStyleSheet(f"color: {color}; font-weight: bold;")
            
            valor = QLabel("0")
            valor.setAlignment(Qt.AlignmentFlag.AlignCenter)
            valor.setStyleSheet(f"color: {color}; font-size: 24px; font-weight: bold;")
            self.stats_widgets[key] = valor
            
            container_layout.addWidget(lbl)
            container_layout.addWidget(valor)
            layout_stats.addWidget(container)
        
        layout.addWidget(grupo_stats)
        
        # Grupo: Logs
        grupo_logs = QGroupBox("📝 Logs")
        layout_logs = QVBoxLayout(grupo_logs)
        
        self.txt_logs = QTextEdit()
        self.txt_logs.setReadOnly(True)
        self.txt_logs.setMinimumHeight(200)
        layout_logs.addWidget(self.txt_logs)
        
        layout_btns_log = QHBoxLayout()
        btn_limpiar = QPushButton("🗑️ Limpiar")
        btn_limpiar.clicked.connect(self.limpiar_logs)
        
        self.btn_abrir = QPushButton("📂 Abrir Archivo")
        self.btn_abrir.setObjectName("btnAbrir")
        self.btn_abrir.clicked.connect(self.abrir_archivo_salida)
        self.btn_abrir.setEnabled(False)
        
        layout_btns_log.addWidget(btn_limpiar)
        layout_btns_log.addStretch()
        layout_btns_log.addWidget(self.btn_abrir)
        layout_logs.addLayout(layout_btns_log)
        
        layout.addWidget(grupo_logs)
    
    def aplicar_estilos(self):
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1e1e1e;
            }
            QWidget {
                background-color: #1e1e1e;
                color: #d4d4d4;
                font-family: 'Segoe UI', Arial;
                font-size: 11pt;
            }
            QLabel {
                color: #d4d4d4;
            }
            QLabel#subtitulo {
                color: #858585;
                font-size: 10pt;
            }
            QLabel#archivo {
                color: #4ec9b0;
                font-style: italic;
            }
            QGroupBox {
                border: 2px solid #3f3f3f;
                border-radius: 8px;
                margin-top: 12px;
                padding-top: 10px;
                font-weight: bold;
                color: #4ec9b0;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 15px;
                padding: 0 5px;
            }
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                          stop:0 #404040, stop:1 #2d2d2d);
                color: #d4d4d4;
                border: 1px solid #555;
                border-radius: 6px;
                padding: 8px 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                          stop:0 #4a4a4a, stop:1 #383838);
                border: 1px solid #666;
            }
            QPushButton:pressed {
                background: #2d2d2d;
            }
            QPushButton:disabled {
                background: #2a2a2a;
                color: #666;
            }
            QPushButton#btnEjecutar {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                          stop:0 #0e639c, stop:1 #0d4a75);
                font-size: 13pt;
            }
            QPushButton#btnEjecutar:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                          stop:0 #1177bb, stop:1 #0e5a8a);
            }
            QPushButton#btnAbrir {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                          stop:0 #0a7d3e, stop:1 #085d2e);
            }
            QPushButton#btnAbrir:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                          stop:0 #0c9449, stop:1 #0a7238);
            }
            QComboBox {
                background-color: #3c3c3c;
                color: #d4d4d4;
                border: 1px solid #555;
                border-radius: 4px;
                padding: 5px;
                min-height: 25px;
            }
            QComboBox:disabled {
                background-color: #2a2a2a;
                color: #666;
            }
            QComboBox:hover {
                border: 1px solid #666;
            }
            QComboBox::drop-down {
                border: none;
                width: 20px;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid #d4d4d4;
                margin-right: 5px;
            }
            QComboBox QAbstractItemView {
                background-color: #3c3c3c;
                color: #d4d4d4;
                selection-background-color: #0e639c;
                border: 1px solid #555;
            }
            QTextEdit {
                background-color: #252526;
                color: #d4d4d4;
                border: 1px solid #3f3f3f;
                border-radius: 6px;
                padding: 8px;
                font-family: 'Consolas', 'Courier New', monospace;
                font-size: 10pt;
            }
        """)
    
    def seleccionar_nits(self):
        archivo, _ = QFileDialog.getOpenFileName(
            self,
            "Seleccionar archivo de NITs",
            "",
            "Excel Files (*.xlsx *.xls)"
        )
        if archivo:
            try:
                self.archivo_nits = archivo
                self.lbl_ruta_nits.setText(archivo)
                
                # Leer columnas del archivo
                df = pd.read_excel(archivo, nrows=0)
                columnas = list(df.columns)
                
                # Llenar combobox con columnas
                self.combo_columna.clear()
                self.combo_columna.addItems(columnas)
                self.combo_columna.setEnabled(True)
                
                # Seleccionar primera columna por defecto
                if columnas:
                    self.columna_nits = columnas[0]
                    self.log(f"📋 Columnas disponibles: {len(columnas)}", "info")
                    self.log(f"✅ Columna seleccionada: {columnas[0]}", "success")
                
                self.verificar_archivos()
                
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error al leer archivo:\n{str(e)}")
                self.archivo_nits = None
                self.combo_columna.clear()
                self.combo_columna.setEnabled(False)
    
    def seleccionar_celer(self):
        archivo, _ = QFileDialog.getOpenFileName(
            self,
            "Seleccionar InformedePersonas CELER",
            "",
            "Excel Files (*.xlsx *.xls)"
        )
        if archivo:
            self.archivo_celer = archivo
            self.lbl_ruta_celer.setText(archivo)
            self.verificar_archivos()
    
    def columna_seleccionada(self, columna):
        """Actualiza la columna seleccionada"""
        if columna:
            self.columna_nits = columna
            self.log(f"📋 Columna seleccionada: {columna}", "info")
    
    def verificar_archivos(self):
        if self.archivo_nits and self.columna_nits and self.archivo_celer:
            self.btn_ejecutar.setEnabled(True)
        else:
            self.btn_ejecutar.setEnabled(False)
    
    def ejecutar_llenado(self):
        # Generar nombre de archivo de salida
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        carpeta_salida = os.path.join(os.path.dirname(__file__), "conciliador_clientes", "plantilla", "output")
        os.makedirs(carpeta_salida, exist_ok=True)
        self.archivo_salida = os.path.join(carpeta_salida, f"PLANTILLA_LLENA_{timestamp}.xlsx")
        
        self.btn_ejecutar.setEnabled(False)
        self.limpiar_logs()
        
        self.log("", "info")
        self.log("="*60, "info")
        self.log("🚀 INICIANDO MIGRACIÓN DE CLIENTES", "info")
        self.log("="*60, "info")
        
        # Iniciar thread
        self.worker = LlenadorThread(
            self.archivo_nits,
            self.columna_nits,
            self.archivo_celer,
            self.archivo_salida
        )
        self.worker.log_signal.connect(self.log)
        self.worker.finished_signal.connect(self.llenado_completado)
        self.worker.start()
    
    def llenado_completado(self, exito, mensaje, estadisticas):
        if exito:
            self.log("", "info")
            self.log("="*60, "success")
            self.log("✅ MIGRACIÓN COMPLETADA", "success")
            self.log("="*60, "success")
            self.log(f"📊 Total NITs: {estadisticas.get('total', 0)}", "info")
            self.log(f"✅ Encontrados: {estadisticas.get('encontrados', 0)}", "success")
            self.log(f"⚠️ No encontrados: {estadisticas.get('no_encontrados', 0)}", "warning")
            self.log(f"💾 Archivo: {os.path.basename(self.archivo_salida)}", "success")
            
            # Actualizar estadísticas
            for key, valor in estadisticas.items():
                if key in self.stats_widgets:
                    self.stats_widgets[key].setText(str(valor))
            
            self.btn_abrir.setEnabled(True)
        else:
            self.log(f"❌ Error: {mensaje}", "error")
        
        self.btn_ejecutar.setEnabled(True)
    
    def abrir_archivo_salida(self):
        if self.archivo_salida and os.path.exists(self.archivo_salida):
            if os.name == 'nt':
                os.startfile(self.archivo_salida)
            self.log(f"📂 Abriendo: {os.path.basename(self.archivo_salida)}", "info")
    
    def limpiar_logs(self):
        self.txt_logs.clear()
    
    def log(self, mensaje: str, tipo: str = "info"):
        colores = {
            "info": "#d4d4d4",
            "success": "#6a9955",
            "warning": "#dcdcaa",
            "error": "#f44747"
        }
        color = colores.get(tipo, "#d4d4d4")
        self.txt_logs.append(f'<span style="color: {color};">{mensaje}</span>')


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
