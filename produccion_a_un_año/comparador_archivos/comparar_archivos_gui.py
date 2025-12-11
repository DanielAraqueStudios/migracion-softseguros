"""
Comparador de Archivos - Interfaz Gráfica con Pestañas
======================================================
GUI para comparar archivos Excel:
- Pestaña 1: Maviso Manual vs Maviso Generado
- Pestaña 2: Maviso vs CELER (validar datos originales)
- Pestaña 3: Validar Mensuales sin Prima
"""

import sys
from pathlib import Path
from datetime import datetime
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QTextEdit, QFileDialog, QGroupBox,
    QProgressBar, QFrame, QMessageBox, QTabWidget
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QFont, QColor, QPalette
import subprocess
import os
import pandas as pd

from comparar_archivos import ComparadorMaviso
from comparar_maviso_celer import ComparadorMavisoCeler


# Estilos CSS para tema oscuro
DARK_STYLE = """
QMainWindow {
    background-color: #1e1e1e;
}
QWidget {
    background-color: #1e1e1e;
    color: #d4d4d4;
    font-family: 'Segoe UI', Arial, sans-serif;
}
QTabWidget::pane {
    border: 1px solid #3c3c3c;
    border-radius: 4px;
    background-color: #1e1e1e;
}
QTabBar::tab {
    background-color: #2d2d2d;
    color: #d4d4d4;
    padding: 10px 20px;
    margin-right: 2px;
    border-top-left-radius: 4px;
    border-top-right-radius: 4px;
}
QTabBar::tab:selected {
    background-color: #0e639c;
    color: white;
}
QTabBar::tab:hover:!selected {
    background-color: #3c3c3c;
}
QGroupBox {
    border: 1px solid #3c3c3c;
    border-radius: 8px;
    margin-top: 12px;
    padding-top: 10px;
    font-weight: bold;
    color: #569cd6;
}
QGroupBox::title {
    subcontrol-origin: margin;
    left: 10px;
    padding: 0 5px;
}
QPushButton {
    background-color: #0e639c;
    color: white;
    border: none;
    border-radius: 4px;
    padding: 8px 16px;
    font-weight: bold;
    min-width: 120px;
}
QPushButton:hover {
    background-color: #1177bb;
}
QPushButton:pressed {
    background-color: #0d5a8c;
}
QPushButton:disabled {
    background-color: #3c3c3c;
    color: #6c6c6c;
}
QPushButton#btnComparar {
    background-color: #16825d;
    font-size: 14px;
    padding: 12px 24px;
}
QPushButton#btnComparar:hover {
    background-color: #1a9e6f;
}
QPushButton#btnExportar {
    background-color: #c27c0e;
}
QPushButton#btnExportar:hover {
    background-color: #d98f1a;
}
QPushButton#btnAbrir {
    background-color: #6a9955;
}
QPushButton#btnAbrir:hover {
    background-color: #7cb668;
}
QTextEdit {
    background-color: #252526;
    border: 1px solid #3c3c3c;
    border-radius: 4px;
    padding: 8px;
    font-family: 'Consolas', 'Courier New', monospace;
    font-size: 11px;
    color: #d4d4d4;
}
QLabel {
    color: #d4d4d4;
}
QLabel#titulo {
    font-size: 18px;
    font-weight: bold;
    color: #569cd6;
    padding: 5px;
}
QLabel#subtitulo {
    font-size: 11px;
    color: #808080;
    padding-bottom: 5px;
}
QLabel#archivo {
    background-color: #252526;
    border: 1px solid #3c3c3c;
    border-radius: 4px;
    padding: 8px;
    color: #9cdcfe;
}
QLabel#estadistica {
    font-size: 24px;
    font-weight: bold;
    color: #4ec9b0;
}
QLabel#estadistica_label {
    font-size: 11px;
    color: #808080;
}
QProgressBar {
    border: 1px solid #3c3c3c;
    border-radius: 4px;
    text-align: center;
    background-color: #252526;
}
QProgressBar::chunk {
    background-color: #16825d;
    border-radius: 3px;
}
QFrame#separator {
    background-color: #3c3c3c;
    max-height: 1px;
}
"""


class ComparadorThread(QThread):
    """Thread para ejecutar la comparación sin bloquear la GUI"""
    
    log_signal = pyqtSignal(str, str)  # mensaje, tipo
    finished_signal = pyqtSignal(bool, str, dict)  # éxito, mensaje, estadísticas
    
    def __init__(self, comparador, tipo="maviso"):
        super().__init__()
        self.comparador = comparador
        self.tipo = tipo
    
    def run(self):
        try:
            self.log_signal.emit("=" * 50, "info")
            self.log_signal.emit("INICIANDO COMPARACIÓN", "info")
            self.log_signal.emit("=" * 50, "info")
            
            # Ejecutar comparación
            exito, mensaje, resultados = self.comparador.comparar()
            
            if exito:
                # Emitir logs de discrepancias
                for disc in self.comparador.obtener_discrepancias():
                    self.log_signal.emit(f"❌ DISCREPANCIA - Póliza: {disc['poliza']}", "error")
                    
                    if self.tipo == "maviso":
                        self.log_signal.emit(f"   Fila manual: {disc['fila_manual']} | Fila generado: {disc['fila_generado']}", "warning")
                        for err in disc['errores']:
                            self.log_signal.emit(f"   → {err['campo']}: Manual='{err['manual']}' vs Generado='{err['generado']}'", "warning")
                    else:  # celer
                        self.log_signal.emit(f"   Fila Maviso: {disc['fila_maviso']} | Fila CELER: {disc['fila_celer']}", "warning")
                        for err in disc['errores']:
                            self.log_signal.emit(f"   → {err['campo']}: Maviso='{err['maviso']}' vs CELER='{err['celer']}'", "warning")
                
                # Logs de solo en uno
                if self.tipo == "maviso":
                    solo_1 = resultados.get('solo_manual', [])
                    solo_2 = resultados.get('solo_generado', [])
                    label_1, label_2 = "ARCHIVO MANUAL", "ARCHIVO GENERADO"
                else:
                    solo_1 = resultados.get('solo_maviso', [])
                    solo_2 = resultados.get('solo_celer', [])
                    label_1, label_2 = "MAVISO", "CELER"
                
                if solo_1:
                    self.log_signal.emit("", "info")
                    self.log_signal.emit(f"⚠️ PÓLIZAS SOLO EN {label_1}:", "warning")
                    for item in solo_1[:20]:
                        self.log_signal.emit(f"   • {item['poliza']} (Fila {item['fila']})", "warning")
                    if len(solo_1) > 20:
                        self.log_signal.emit(f"   ... y {len(solo_1) - 20} más", "warning")
                
                if solo_2:
                    self.log_signal.emit("", "info")
                    self.log_signal.emit(f"⚠️ PÓLIZAS SOLO EN {label_2}:", "warning")
                    for item in solo_2[:20]:
                        self.log_signal.emit(f"   • {item['poliza']} (Fila {item['fila']})", "warning")
                    if len(solo_2) > 20:
                        self.log_signal.emit(f"   ... y {len(solo_2) - 20} más", "warning")
                
                self.finished_signal.emit(True, mensaje, self.comparador.obtener_estadisticas())
            else:
                self.finished_signal.emit(False, mensaje, {})
                
        except Exception as e:
            self.log_signal.emit(f"❌ Error: {str(e)}", "error")
            self.finished_signal.emit(False, str(e), {})


class TabMavisoVsMaviso(QWidget):
    """Pestaña: Comparar Maviso Manual vs Maviso Generado"""
    
    def __init__(self):
        super().__init__()
        self.comparador = ComparadorMaviso()
        self.ruta_manual = None
        self.ruta_generado = None
        self.ruta_ultimo_reporte = None
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        layout.setContentsMargins(15, 15, 15, 15)
        
        # Título
        titulo = QLabel("📊 Maviso Manual vs Maviso Generado")
        titulo.setObjectName("titulo")
        layout.addWidget(titulo)
        
        subtitulo = QLabel("Compara el archivo corregido manualmente contra el generado por el script")
        subtitulo.setObjectName("subtitulo")
        layout.addWidget(subtitulo)
        
        # Grupo: Archivos
        grupo_archivos = QGroupBox("📁 Archivos a Comparar")
        layout_archivos = QVBoxLayout(grupo_archivos)
        
        # Archivo Manual
        layout_manual = QHBoxLayout()
        lbl_manual = QLabel("Archivo Manual:")
        lbl_manual.setMinimumWidth(150)
        self.lbl_ruta_manual = QLabel("No seleccionado")
        self.lbl_ruta_manual.setObjectName("archivo")
        btn_manual = QPushButton("📂 Seleccionar")
        btn_manual.clicked.connect(self.seleccionar_archivo_manual)
        layout_manual.addWidget(lbl_manual)
        layout_manual.addWidget(self.lbl_ruta_manual, 1)
        layout_manual.addWidget(btn_manual)
        layout_archivos.addLayout(layout_manual)
        
        # Archivo Generado
        layout_generado = QHBoxLayout()
        lbl_generado = QLabel("Archivo Generado:")
        lbl_generado.setMinimumWidth(150)
        self.lbl_ruta_generado = QLabel("No seleccionado")
        self.lbl_ruta_generado.setObjectName("archivo")
        btn_generado = QPushButton("📂 Seleccionar")
        btn_generado.clicked.connect(self.seleccionar_archivo_generado)
        layout_generado.addWidget(lbl_generado)
        layout_generado.addWidget(self.lbl_ruta_generado, 1)
        layout_generado.addWidget(btn_generado)
        layout_archivos.addLayout(layout_generado)
        
        layout.addWidget(grupo_archivos)
        
        # Botón Comparar
        layout_btn = QHBoxLayout()
        layout_btn.addStretch()
        self.btn_comparar = QPushButton("🔍 COMPARAR")
        self.btn_comparar.setObjectName("btnComparar")
        self.btn_comparar.clicked.connect(self.ejecutar_comparacion)
        self.btn_comparar.setEnabled(False)
        layout_btn.addWidget(self.btn_comparar)
        layout_btn.addStretch()
        layout.addLayout(layout_btn)
        
        # Grupo: Estadísticas
        grupo_stats = QGroupBox("📊 Resultados")
        layout_stats = QHBoxLayout(grupo_stats)
        
        # Crear widgets de estadísticas
        self.stats_widgets = {}
        stats_config = [
            ('total_manual', 'Total Manual', '#4ec9b0'),
            ('total_generado', 'Total Generado', '#4ec9b0'),
            ('coincidencias', 'Coincidencias', '#6a9955'),
            ('discrepancias', 'Discrepancias', '#f44747'),
            ('solo_manual', 'Solo Manual', '#dcdcaa'),
            ('solo_generado', 'Solo Generado', '#dcdcaa'),
        ]
        
        for key, label, color in stats_config:
            frame = QFrame()
            frame_layout = QVBoxLayout(frame)
            frame_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
            
            lbl_valor = QLabel("--")
            lbl_valor.setObjectName("estadistica")
            lbl_valor.setStyleSheet(f"color: {color};")
            lbl_valor.setAlignment(Qt.AlignmentFlag.AlignCenter)
            
            lbl_nombre = QLabel(label)
            lbl_nombre.setObjectName("estadistica_label")
            lbl_nombre.setAlignment(Qt.AlignmentFlag.AlignCenter)
            
            frame_layout.addWidget(lbl_valor)
            frame_layout.addWidget(lbl_nombre)
            layout_stats.addWidget(frame)
            
            self.stats_widgets[key] = lbl_valor
        
        layout.addWidget(grupo_stats)
        
        # Grupo: Logs
        grupo_logs = QGroupBox("📋 Log de Comparación")
        layout_logs = QVBoxLayout(grupo_logs)
        
        self.txt_logs = QTextEdit()
        self.txt_logs.setReadOnly(True)
        self.txt_logs.setMinimumHeight(150)
        layout_logs.addWidget(self.txt_logs)
        
        layout_btns_log = QHBoxLayout()
        btn_limpiar = QPushButton("🗑️ Limpiar")
        btn_limpiar.clicked.connect(self.limpiar_logs)
        self.btn_exportar = QPushButton("📊 Exportar Reporte")
        self.btn_exportar.setObjectName("btnExportar")
        self.btn_exportar.clicked.connect(self.exportar_reporte)
        self.btn_exportar.setEnabled(False)
        layout_btns_log.addWidget(btn_limpiar)
        layout_btns_log.addStretch()
        layout_btns_log.addWidget(self.btn_exportar)
        layout_logs.addLayout(layout_btns_log)
        
        layout.addWidget(grupo_logs, 1)
    
    def seleccionar_archivo_manual(self):
        """Abre diálogo para seleccionar archivo manual"""
        # Buscar carpeta padre (produccion_a_un_año)
        carpeta_base = Path(__file__).parent.parent
        archivo, _ = QFileDialog.getOpenFileName(
            self,
            "Seleccionar archivo manual (corregido)",
            str(carpeta_base),
            "Excel Files (*.xlsx *.xls)"
        )
        if archivo:
            self.ruta_manual = archivo
            self.lbl_ruta_manual.setText(Path(archivo).name)
            self.log(f"✅ Archivo manual: {Path(archivo).name}", "success")
            self.verificar_archivos()
    
    def seleccionar_archivo_generado(self):
        """Abre diálogo para seleccionar archivo generado"""
        # Buscar en carpeta output del padre
        carpeta_base = Path(__file__).parent.parent / 'output'
        if not carpeta_base.exists():
            carpeta_base = Path(__file__).parent.parent
        archivo, _ = QFileDialog.getOpenFileName(
            self,
            "Seleccionar archivo generado (script)",
            str(carpeta_base),
            "Excel Files (*.xlsx *.xls)"
        )
        if archivo:
            self.ruta_generado = archivo
            self.lbl_ruta_generado.setText(Path(archivo).name)
            self.log(f"✅ Archivo generado: {Path(archivo).name}", "success")
            self.verificar_archivos()
    
    def verificar_archivos(self):
        """Verifica si ambos archivos están seleccionados"""
        self.btn_comparar.setEnabled(
            self.ruta_manual is not None and self.ruta_generado is not None
        )
    
    def ejecutar_comparacion(self):
        """Inicia la comparación de archivos"""
        self.btn_comparar.setEnabled(False)
        self.btn_exportar.setEnabled(False)
        
        # Resetear estadísticas
        for widget in self.stats_widgets.values():
            widget.setText("--")
        
        # Cargar archivos
        self.log("", "info")
        self.log("📂 Cargando archivos...", "info")
        
        exito, mensaje = self.comparador.cargar_archivo_manual(self.ruta_manual)
        if not exito:
            self.log(f"❌ {mensaje}", "error")
            self.btn_comparar.setEnabled(True)
            return
        self.log(f"✅ {mensaje}", "success")
        
        exito, mensaje = self.comparador.cargar_archivo_generado(self.ruta_generado)
        if not exito:
            self.log(f"❌ {mensaje}", "error")
            self.btn_comparar.setEnabled(True)
            return
        self.log(f"✅ {mensaje}", "success")
        
        # Ejecutar comparación en thread
        self.worker_thread = ComparadorThread(self.comparador, "maviso")
        self.worker_thread.log_signal.connect(self.log)
        self.worker_thread.finished_signal.connect(self.comparacion_terminada)
        self.worker_thread.start()
    
    def comparacion_terminada(self, exito: bool, mensaje: str, estadisticas: dict):
        """Callback cuando termina la comparación"""
        self.btn_comparar.setEnabled(True)
        
        if exito:
            # Actualizar estadísticas
            for key, widget in self.stats_widgets.items():
                valor = estadisticas.get(key, 0)
                widget.setText(str(valor))
            
            self.log("", "info")
            self.log("=" * 50, "success")
            self.log("✅ COMPARACIÓN COMPLETADA", "success")
            self.log("=" * 50, "success")
            
            self.btn_exportar.setEnabled(True)
        else:
            self.log(f"❌ Error: {mensaje}", "error")
    
    def exportar_reporte(self):
        """Exporta el reporte de comparación y lo abre automáticamente"""
        try:
            ruta = self.comparador.exportar_reporte()
            self.ruta_ultimo_reporte = ruta
            self.log(f"📊 Reporte exportado: {ruta}", "success")
            
            # Abrir automáticamente el archivo
            os.startfile(ruta)
            self.log(f"📂 Abriendo reporte automáticamente...", "info")
        except Exception as e:
            self.log(f"❌ Error exportando: {str(e)}", "error")
    
    def log(self, mensaje: str, tipo: str = "info"):
        """Agrega un mensaje al log con formato de color"""
        colores = {
            "info": "#d4d4d4",
            "success": "#6a9955",
            "warning": "#dcdcaa",
            "error": "#f44747"
        }
        color = colores.get(tipo, "#d4d4d4")
        self.txt_logs.append(f'<span style="color: {color};">{mensaje}</span>')
        
        # Auto-scroll al final
        scrollbar = self.txt_logs.verticalScrollBar()
        if scrollbar:
            scrollbar.setValue(scrollbar.maximum())
    
    def limpiar_logs(self):
        """Limpia el área de logs"""
        self.txt_logs.clear()


class TabMavisoVsCeler(QWidget):
    """Pestaña: Comparar Maviso vs CELER (datos originales)"""
    
    def __init__(self):
        super().__init__()
        self.comparador = ComparadorMavisoCeler()
        self.ruta_maviso = None
        self.ruta_celer = None
        self.ruta_ultimo_reporte = None
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        layout.setContentsMargins(15, 15, 15, 15)
        
        # Título
        titulo = QLabel("🔄 Maviso vs CELER (Validar Datos Originales)")
        titulo.setObjectName("titulo")
        layout.addWidget(titulo)
        
        subtitulo = QLabel("Valida que Maviso tenga los mismos valores de Prima, Fechas y Modalidad que CELER")
        subtitulo.setObjectName("subtitulo")
        layout.addWidget(subtitulo)
        
        # Grupo: Archivos
        grupo_archivos = QGroupBox("📁 Archivos a Comparar")
        layout_archivos = QVBoxLayout(grupo_archivos)
        
        # Archivo Maviso
        layout_maviso = QHBoxLayout()
        lbl_maviso = QLabel("Archivo Maviso:")
        lbl_maviso.setMinimumWidth(150)
        self.lbl_ruta_maviso = QLabel("No seleccionado")
        self.lbl_ruta_maviso.setObjectName("archivo")
        btn_maviso = QPushButton("📂 Seleccionar")
        btn_maviso.clicked.connect(self.seleccionar_archivo_maviso)
        layout_maviso.addWidget(lbl_maviso)
        layout_maviso.addWidget(self.lbl_ruta_maviso, 1)
        layout_maviso.addWidget(btn_maviso)
        layout_archivos.addLayout(layout_maviso)
        
        # Archivo CELER
        layout_celer = QHBoxLayout()
        lbl_celer = QLabel("Archivo CELER:")
        lbl_celer.setMinimumWidth(150)
        self.lbl_ruta_celer = QLabel("No seleccionado")
        self.lbl_ruta_celer.setObjectName("archivo")
        btn_celer = QPushButton("📂 Seleccionar")
        btn_celer.clicked.connect(self.seleccionar_archivo_celer)
        layout_celer.addWidget(lbl_celer)
        layout_celer.addWidget(self.lbl_ruta_celer, 1)
        layout_celer.addWidget(btn_celer)
        layout_archivos.addLayout(layout_celer)
        
        layout.addWidget(grupo_archivos)
        
        # Botón Comparar
        layout_btn = QHBoxLayout()
        layout_btn.addStretch()
        self.btn_comparar = QPushButton("🔍 COMPARAR")
        self.btn_comparar.setObjectName("btnComparar")
        self.btn_comparar.clicked.connect(self.ejecutar_comparacion)
        self.btn_comparar.setEnabled(False)
        layout_btn.addWidget(self.btn_comparar)
        layout_btn.addStretch()
        layout.addLayout(layout_btn)
        
        # Grupo: Estadísticas
        grupo_stats = QGroupBox("📊 Resultados")
        layout_stats = QHBoxLayout(grupo_stats)
        
        self.stats_widgets = {}
        stats_config = [
            ('total_maviso', 'Total Maviso', '#4ec9b0'),
            ('total_celer', 'Total CELER', '#4ec9b0'),
            ('coincidencias', 'Coincidencias', '#6a9955'),
            ('discrepancias', 'Discrepancias', '#f44747'),
            ('solo_maviso', 'Solo Maviso', '#dcdcaa'),
            ('solo_celer', 'Solo CELER', '#dcdcaa'),
        ]
        
        for key, label, color in stats_config:
            frame = QFrame()
            frame_layout = QVBoxLayout(frame)
            frame_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
            
            lbl_valor = QLabel("--")
            lbl_valor.setObjectName("estadistica")
            lbl_valor.setStyleSheet(f"color: {color};")
            lbl_valor.setAlignment(Qt.AlignmentFlag.AlignCenter)
            
            lbl_nombre = QLabel(label)
            lbl_nombre.setObjectName("estadistica_label")
            lbl_nombre.setAlignment(Qt.AlignmentFlag.AlignCenter)
            
            frame_layout.addWidget(lbl_valor)
            frame_layout.addWidget(lbl_nombre)
            layout_stats.addWidget(frame)
            
            self.stats_widgets[key] = lbl_valor
        
        layout.addWidget(grupo_stats)
        
        # Grupo: Logs
        grupo_logs = QGroupBox("📋 Log de Comparación")
        layout_logs = QVBoxLayout(grupo_logs)
        
        self.txt_logs = QTextEdit()
        self.txt_logs.setReadOnly(True)
        self.txt_logs.setMinimumHeight(150)
        layout_logs.addWidget(self.txt_logs)
        
        layout_btns_log = QHBoxLayout()
        btn_limpiar = QPushButton("🗑️ Limpiar")
        btn_limpiar.clicked.connect(self.limpiar_logs)
        
        self.btn_corregir = QPushButton("🔧 Corregir Modalidades")
        self.btn_corregir.setObjectName("btnCorregir")
        self.btn_corregir.clicked.connect(self.corregir_modalidades)
        self.btn_corregir.setEnabled(False)
        self.btn_corregir.setToolTip("Actualiza las modalidades en MAVISO para que coincidan con CELER")
        
        self.btn_exportar = QPushButton("📊 Exportar Reporte")
        self.btn_exportar.setObjectName("btnExportar")
        self.btn_exportar.clicked.connect(self.exportar_reporte)
        self.btn_exportar.setEnabled(False)
        layout_btns_log.addWidget(btn_limpiar)
        layout_btns_log.addWidget(self.btn_corregir)
        layout_btns_log.addStretch()
        layout_btns_log.addWidget(self.btn_exportar)
        layout_logs.addLayout(layout_btns_log)
        
        layout.addWidget(grupo_logs, 1)
    
    def seleccionar_archivo_maviso(self):
        carpeta_base = Path(__file__).parent.parent
        archivo, _ = QFileDialog.getOpenFileName(
            self, "Seleccionar archivo Maviso", str(carpeta_base), "Excel Files (*.xlsx *.xls)"
        )
        if archivo:
            self.ruta_maviso = archivo
            self.lbl_ruta_maviso.setText(Path(archivo).name)
            self.log(f"✅ Archivo Maviso: {Path(archivo).name}", "success")
            self.verificar_archivos()
    
    def seleccionar_archivo_celer(self):
        carpeta_base = Path(__file__).parent.parent
        archivo, _ = QFileDialog.getOpenFileName(
            self, "Seleccionar archivo CELER", str(carpeta_base), "Excel Files (*.xlsx *.xls)"
        )
        if archivo:
            self.ruta_celer = archivo
            self.lbl_ruta_celer.setText(Path(archivo).name)
            self.log(f"✅ Archivo CELER: {Path(archivo).name}", "success")
            self.verificar_archivos()
    
    def verificar_archivos(self):
        self.btn_comparar.setEnabled(self.ruta_maviso is not None and self.ruta_celer is not None)
    
    def ejecutar_comparacion(self):
        self.btn_comparar.setEnabled(False)
        self.btn_exportar.setEnabled(False)
        
        for widget in self.stats_widgets.values():
            widget.setText("--")
        
        self.log("", "info")
        self.log("📂 Cargando archivos...", "info")
        
        exito, mensaje = self.comparador.cargar_maviso(self.ruta_maviso)
        if not exito:
            self.log(f"❌ {mensaje}", "error")
            self.btn_comparar.setEnabled(True)
            return
        self.log(f"✅ {mensaje}", "success")
        
        exito, mensaje = self.comparador.cargar_celer(self.ruta_celer)
        if not exito:
            self.log(f"❌ {mensaje}", "error")
            self.btn_comparar.setEnabled(True)
            return
        self.log(f"✅ {mensaje}", "success")
        
        self.worker_thread = ComparadorThread(self.comparador, "celer")
        self.worker_thread.log_signal.connect(self.log)
        self.worker_thread.finished_signal.connect(self.comparacion_terminada)
        self.worker_thread.start()
    
    def comparacion_terminada(self, exito: bool, mensaje: str, estadisticas: dict):
        self.btn_comparar.setEnabled(True)
        
        if exito:
            for key, widget in self.stats_widgets.items():
                valor = estadisticas.get(key, 0)
                widget.setText(str(valor))
            
            self.log("", "info")
            self.log("=" * 50, "success")
            self.log("✅ COMPARACIÓN COMPLETADA", "success")
            self.log("=" * 50, "success")
            
            self.btn_exportar.setEnabled(True)
            self.btn_corregir.setEnabled(True)
        else:
            self.log(f"❌ Error: {mensaje}", "error")
    
    def exportar_reporte(self):
        try:
            ruta = self.comparador.exportar_reporte()
            self.ruta_ultimo_reporte = ruta
            self.log(f"📊 Reporte exportado: {ruta}", "success")
            os.startfile(ruta)
        except Exception as e:
            self.log(f"❌ Error exportando: {str(e)}", "error")
    
    def log(self, mensaje: str, tipo: str = "info"):
        colores = {
            "info": "#d4d4d4",
            "success": "#6a9955",
            "warning": "#dcdcaa",
            "error": "#f44747"
        }
        color = colores.get(tipo, "#d4d4d4")
        self.txt_logs.append(f'<span style="color: {color};">{mensaje}</span>')
        scrollbar = self.txt_logs.verticalScrollBar()
        if scrollbar:
            scrollbar.setValue(scrollbar.maximum())
    
    def limpiar_logs(self):
        self.txt_logs.clear()
    
    def corregir_modalidades(self):
        """Corrige las modalidades en MAVISO para que coincidan con CELER"""
        if not self.ruta_maviso or not self.comparador.resultados:
            QMessageBox.warning(self, "Advertencia", "Debe ejecutar la comparación primero")
            return
        
        respuesta = QMessageBox.question(
            self,
            "Confirmar Corrección",
            "¿Desea actualizar las modalidades en MAVISO para que coincidan con CELER?\n\n"
            "CELER se usará como fuente correcta.\n"
            "Se creará un archivo nuevo con los cambios.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if respuesta != QMessageBox.StandardButton.Yes:
            return
        
        try:
            self.log("", "info")
            self.log("🔧 Iniciando corrección de modalidades...", "info")
            
            # Cargar MAVISO
            df_maviso = pd.read_excel(self.ruta_maviso)
            self.log(f"📂 Archivo MAVISO cargado: {len(df_maviso)} registros", "info")
            
            # Cargar CELER
            df_celer = pd.read_excel(self.ruta_celer, skiprows=3)
            self.log(f"📂 Archivo CELER cargado: {len(df_celer)} registros", "info")
            
            # Columnas
            MAVISO_COL_POLIZA = 0
            MAVISO_COL_MODALIDAD = 21
            CELER_COL_POLIZA = 20
            CELER_COL_MODALIDAD = 27
            
            # Crear diccionario de CELER
            celer_dict = {}
            for idx, row in df_celer.iterrows():
                poliza = str(row.iloc[CELER_COL_POLIZA]).strip()
                modalidad = str(row.iloc[CELER_COL_MODALIDAD]).strip().upper()
                celer_dict[poliza] = modalidad
            
            # Corregir MAVISO
            cambios = []
            for idx, row in df_maviso.iterrows():
                poliza = str(row.iloc[MAVISO_COL_POLIZA]).strip()
                modalidad_maviso = str(row.iloc[MAVISO_COL_MODALIDAD]).strip().upper()
                
                if poliza in celer_dict:
                    modalidad_celer = celer_dict[poliza]
                    if modalidad_maviso != modalidad_celer and modalidad_celer in ['MENSUAL', 'ANUAL']:
                        # Actualizar
                        df_maviso.at[idx, df_maviso.columns[MAVISO_COL_MODALIDAD]] = modalidad_celer
                        cambios.append({
                            'poliza': poliza,
                            'fila': idx + 2,
                            'anterior': modalidad_maviso,
                            'nuevo': modalidad_celer
                        })
            
            if len(cambios) == 0:
                self.log("✅ No se encontraron discrepancias de modalidad para corregir", "success")
                QMessageBox.information(self, "Información", "No hay cambios necesarios.")
                return
            
            # Guardar archivo corregido
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            ruta_base = Path(self.ruta_maviso)
            ruta_salida = ruta_base.parent / f"{ruta_base.stem}_modalidades_corregidas_{timestamp}.xlsx"
            
            df_maviso.to_excel(ruta_salida, index=False)
            
            self.log(f"\n✅ Corrección completada:", "success")
            self.log(f"   Cambios realizados: {len(cambios)}", "success")
            self.log(f"   Archivo guardado: {ruta_salida.name}", "success")
            
            # Mostrar resumen
            self.log("\n📋 Resumen de cambios:", "info")
            for i, cambio in enumerate(cambios[:10], 1):
                self.log(
                    f"   {i}. Póliza {cambio['poliza']} (Fila {cambio['fila']}): "
                    f"{cambio['anterior']} → {cambio['nuevo']}",
                    "warning"
                )
            
            if len(cambios) > 10:
                self.log(f"   ... y {len(cambios) - 10} cambios más", "info")
            
            QMessageBox.information(
                self,
                "Corrección Exitosa",
                f"Se corrigieron {len(cambios)} modalidades.\n\n"
                f"Archivo guardado en:\n{ruta_salida}"
            )
            
            # Abrir archivo
            if os.name == 'nt':
                os.startfile(ruta_salida)
            
        except Exception as e:
            self.log(f"❌ Error al corregir: {str(e)}", "error")
            QMessageBox.critical(self, "Error", f"Error al corregir modalidades:\n{str(e)}")


class ComparadorGUI(QMainWindow):
    """Ventana principal con pestañas"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle("🔍 Comparador de Archivos - SoftSeguros")
        self.setMinimumSize(950, 750)
        self.setStyleSheet(DARK_STYLE)
        
        # Widget central
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setContentsMargins(10, 10, 10, 10)
        
        # Crear pestañas
        self.tabs = QTabWidget()
        
        # Pestaña 1: Maviso vs Maviso
        self.tab_maviso = TabMavisoVsMaviso()
        self.tabs.addTab(self.tab_maviso, "📊 Maviso Manual vs Generado")
        
        # Pestaña 2: Maviso vs CELER
        self.tab_celer = TabMavisoVsCeler()
        self.tabs.addTab(self.tab_celer, "🔄 Maviso vs CELER")
        
        # Pestaña 3: Validar Mensuales sin Prima
        self.tab_validar = TabValidarMensuales()
        self.tabs.addTab(self.tab_validar, "⚠️ Validar Mensuales sin Prima")
        
        layout.addWidget(self.tabs)


# ==================================================================================
# Thread para Validación de Mensuales
# ==================================================================================

class ValidadorThread(QThread):
    """Thread para ejecutar validación sin bloquear la GUI"""
    log = pyqtSignal(str)
    terminado = pyqtSignal(bool, str, dict)
    
    def __init__(self, ruta_archivo):
        super().__init__()
        self.ruta_archivo = ruta_archivo
    
    def run(self):
        try:
            # Configuración de columnas
            COL_POLIZA = 0
            COL_PRIMA = 14
            COL_MODALIDAD = 21
            
            self.log.emit("📂 Cargando archivo...")
            df = pd.read_excel(self.ruta_archivo)
            self.log.emit(f"   Total registros: {len(df)}")
            
            # Filtrar MENSUALES
            self.log.emit("\n🔍 Filtrando pólizas MENSUALES (Col 21)...")
            mask_mensual = df.iloc[:, COL_MODALIDAD].astype(str).str.strip().str.upper() == 'MENSUAL'
            df_mensuales = df[mask_mensual]
            self.log.emit(f"   Pólizas MENSUALES: {len(df_mensuales)}")
            
            # Filtrar prima = 0
            self.log.emit("\n🔍 Filtrando pólizas con Prima = 0 (Col 14)...")
            mask_prima_cero = df_mensuales.iloc[:, COL_PRIMA].fillna(0) == 0
            df_problema = df_mensuales[mask_prima_cero]
            self.log.emit(f"   MENSUALES con Prima = 0: {len(df_problema)}")
            
            # Preparar estadísticas
            stats = {
                'total': len(df),
                'mensuales': len(df_mensuales),
                'problematicas': len(df_problema),
                'porcentaje': len(df_problema)/len(df_mensuales)*100 if len(df_mensuales) > 0 else 0,
                'df_problema': df_problema
            }
            
            self.log.emit("\n✅ Validación completada")
            self.terminado.emit(True, "Validación exitosa", stats)
            
        except Exception as e:
            self.log.emit(f"\n❌ Error: {str(e)}")
            self.terminado.emit(False, f"Error: {str(e)}", {})


# ==================================================================================
# Pestaña: Validar Mensuales sin Prima
# ==================================================================================

class TabValidarMensuales(QWidget):
    """Pestaña para validar pólizas mensuales sin prima"""
    
    def __init__(self):
        super().__init__()
        self.ruta_archivo = None
        self.validador_thread = None
        self.df_resultados = None
        self.inicializar_ui()
    
    def inicializar_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        
        # Título
        titulo = QLabel("⚠️ Validación de Pólizas MENSUALES sin Prima")
        titulo.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(titulo)
        
        # Grupo: Selección de archivo
        grupo_archivo = QGroupBox("📁 Archivo a Validar")
        grupo_archivo.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        layout_archivo = QVBoxLayout()
        
        layout_btn_archivo = QHBoxLayout()
        self.btn_seleccionar = QPushButton("📂 Seleccionar Archivo MAVISO")
        self.btn_seleccionar.clicked.connect(self.seleccionar_archivo)
        self.btn_seleccionar.setMinimumHeight(40)
        layout_btn_archivo.addWidget(self.btn_seleccionar)
        
        self.lbl_archivo = QLabel("Ningún archivo seleccionado")
        self.lbl_archivo.setWordWrap(True)
        self.lbl_archivo.setStyleSheet("padding: 8px; background-color: #2d2d2d; border-radius: 4px;")
        
        layout_archivo.addLayout(layout_btn_archivo)
        layout_archivo.addWidget(self.lbl_archivo)
        grupo_archivo.setLayout(layout_archivo)
        layout.addWidget(grupo_archivo)
        
        # Grupo: Estadísticas
        grupo_stats = QGroupBox("📊 Estadísticas")
        grupo_stats.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        layout_stats = QVBoxLayout()
        
        self.lbl_total = QLabel("Total pólizas: -")
        self.lbl_mensuales = QLabel("Pólizas MENSUALES: -")
        self.lbl_problematicas = QLabel("MENSUALES sin prima: -")
        self.lbl_porcentaje = QLabel("Porcentaje: -")
        
        for lbl in [self.lbl_total, self.lbl_mensuales, self.lbl_problematicas, self.lbl_porcentaje]:
            lbl.setFont(QFont("Segoe UI", 10))
            layout_stats.addWidget(lbl)
        
        grupo_stats.setLayout(layout_stats)
        layout.addWidget(grupo_stats)
        
        # Botones de acción
        layout_botones = QHBoxLayout()
        
        self.btn_validar = QPushButton("🔍 Validar")
        self.btn_validar.setEnabled(False)
        self.btn_validar.clicked.connect(self.validar)
        self.btn_validar.setMinimumHeight(45)
        self.btn_validar.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        
        self.btn_exportar = QPushButton("💾 Exportar Resultados")
        self.btn_exportar.setEnabled(False)
        self.btn_exportar.clicked.connect(self.exportar_resultados)
        self.btn_exportar.setMinimumHeight(45)
        
        layout_botones.addWidget(self.btn_validar, 2)
        layout_botones.addWidget(self.btn_exportar, 1)
        layout.addLayout(layout_botones)
        
        # Log
        grupo_log = QGroupBox("📋 Registro de Actividad")
        grupo_log.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        layout_log = QVBoxLayout()
        
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setFont(QFont("Consolas", 9))
        self.log_text.setMinimumHeight(200)
        
        layout_log.addWidget(self.log_text)
        grupo_log.setLayout(layout_log)
        layout.addWidget(grupo_log)
        
        # Barra de progreso
        self.progress = QProgressBar()
        self.progress.setVisible(False)
        self.progress.setTextVisible(False)
        layout.addWidget(self.progress)
    
    def seleccionar_archivo(self):
        """Selecciona el archivo a validar"""
        ruta, _ = QFileDialog.getOpenFileName(
            self,
            "Seleccionar archivo MAVISO",
            "../output",
            "Archivos Excel (*.xlsx *.xls)"
        )
        
        if ruta:
            self.ruta_archivo = ruta
            nombre = Path(ruta).name
            self.lbl_archivo.setText(f"📄 {nombre}")
            self.btn_validar.setEnabled(True)
            self.agregar_log(f"Archivo seleccionado: {nombre}")
    
    def validar(self):
        """Ejecuta la validación"""
        if not self.ruta_archivo:
            QMessageBox.warning(self, "Advertencia", "Debe seleccionar un archivo primero")
            return
        
        self.btn_validar.setEnabled(False)
        self.btn_exportar.setEnabled(False)
        self.progress.setVisible(True)
        self.progress.setRange(0, 0)  # Modo indeterminado
        self.log_text.clear()
        
        # Limpiar estadísticas
        self.lbl_total.setText("Total pólizas: Validando...")
        self.lbl_mensuales.setText("Pólizas MENSUALES: Validando...")
        self.lbl_problematicas.setText("MENSUALES sin prima: Validando...")
        self.lbl_porcentaje.setText("Porcentaje: Validando...")
        
        # Iniciar thread
        self.validador_thread = ValidadorThread(self.ruta_archivo)
        self.validador_thread.log.connect(self.agregar_log)
        self.validador_thread.terminado.connect(self.validacion_terminada)
        self.validador_thread.start()
    
    def validacion_terminada(self, exito, mensaje, stats):
        """Callback cuando termina la validación"""
        self.progress.setVisible(False)
        self.btn_validar.setEnabled(True)
        
        if exito:
            # Actualizar estadísticas
            self.lbl_total.setText(f"Total pólizas: {stats['total']:,}")
            self.lbl_mensuales.setText(f"Pólizas MENSUALES: {stats['mensuales']:,}")
            self.lbl_problematicas.setText(f"MENSUALES sin prima: {stats['problematicas']:,}")
            self.lbl_porcentaje.setText(f"Porcentaje: {stats['porcentaje']:.1f}%")
            
            # Guardar resultados
            self.df_resultados = stats.get('df_problema')
            self.btn_exportar.setEnabled(len(self.df_resultados) > 0 if self.df_resultados is not None else False)
            
            if stats['problematicas'] > 0:
                self.agregar_log(f"\n⚠️ Se encontraron {stats['problematicas']} pólizas problemáticas")
            else:
                self.agregar_log("\n✅ No se encontraron problemas")
        else:
            QMessageBox.critical(self, "Error", mensaje)
    
    def exportar_resultados(self):
        """Exporta los resultados a Excel"""
        if self.df_resultados is None or len(self.df_resultados) == 0:
            QMessageBox.warning(self, "Advertencia", "No hay resultados para exportar")
            return
        
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            archivo_salida = Path('../output') / f'mensuales_sin_prima_{timestamp}.xlsx'
            
            # Preparar datos
            resultado = pd.DataFrame({
                'Póliza': self.df_resultados.iloc[:, 0],
                'Prima Neta': self.df_resultados.iloc[:, 14],
                'Modalidad': self.df_resultados.iloc[:, 21],
                'Fila Excel': self.df_resultados.index + 2,
                'Placa': self.df_resultados.iloc[:, 1],
                'Asegurado': self.df_resultados.iloc[:, 2],
                'Fecha Inicio': self.df_resultados.iloc[:, 10],
                'Fecha Fin': self.df_resultados.iloc[:, 11],
            })
            
            resultado.to_excel(archivo_salida, index=False)
            self.agregar_log(f"\n💾 Reporte exportado: {archivo_salida.name}")
            
            QMessageBox.information(
                self,
                "Éxito",
                f"Reporte exportado correctamente:\n{archivo_salida}"
            )
            
            # Abrir archivo
            if os.name == 'nt':
                os.startfile(archivo_salida)
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al exportar:\n{str(e)}")
    
    def agregar_log(self, mensaje):
        """Agrega mensaje al log"""
        self.log_text.append(mensaje)
        self.log_text.verticalScrollBar().setValue(
            self.log_text.verticalScrollBar().maximum()
        )


# ==================================================================================
# Ventana Principal
# ==================================================================================

class ComparadorGUI(QMainWindow):
    """Ventana principal con pestañas"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Comparador de Archivos - SoftSeguros")
        self.setMinimumSize(1000, 800)
        
        # Aplicar estilos
        self.setStyleSheet(DARK_STYLE)
        
        # Widget central
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setContentsMargins(10, 10, 10, 10)
        
        # Crear pestañas
        self.tabs = QTabWidget()
        
        # Pestaña 1: Maviso vs Maviso
        self.tab_maviso = TabMavisoVsMaviso()
        self.tabs.addTab(self.tab_maviso, "📊 Maviso Manual vs Generado")
        
        # Pestaña 2: Maviso vs CELER
        self.tab_celer = TabMavisoVsCeler()
        self.tabs.addTab(self.tab_celer, "🔄 Maviso vs CELER")
        
        # Pestaña 3: Validar Mensuales sin Prima
        self.tab_validar = TabValidarMensuales()
        self.tabs.addTab(self.tab_validar, "⚠️ Validar Mensuales sin Prima")
        
        layout.addWidget(self.tabs)


def main():
    app = QApplication(sys.argv)
    
    # Configurar fuente por defecto
    font = QFont("Segoe UI", 10)
    app.setFont(font)
    
    ventana = ComparadorGUI()
    ventana.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
