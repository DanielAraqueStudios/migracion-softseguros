"""
Comparador de Archivos - Interfaz Gráfica con Pestañas
======================================================
GUI para comparar archivos Excel:
- Pestaña 1: Maviso Manual vs Maviso Generado
- Pestaña 2: Maviso vs CELER (validar datos originales)
"""

import sys
from pathlib import Path
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QTextEdit, QFileDialog, QGroupBox,
    QProgressBar, QFrame, QMessageBox, QTabWidget
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QFont, QColor, QPalette
import subprocess
import os

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
        lbl_generado = QLabel("Archivo Generado (script):")
        lbl_generado.setMinimumWidth(180)
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
        self.btn_comparar = QPushButton("🔍 COMPARAR ARCHIVOS")
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
        self.txt_logs.setMinimumHeight(200)
        layout_logs.addWidget(self.txt_logs)
        
        # Botones de logs
        layout_btns_log = QHBoxLayout()
        btn_limpiar = QPushButton("🗑️ Limpiar")
        btn_limpiar.clicked.connect(self.limpiar_logs)
        self.btn_exportar = QPushButton("📊 Exportar Reporte")
        self.btn_exportar.setObjectName("btnExportar")
        self.btn_exportar.clicked.connect(self.exportar_reporte)
        self.btn_exportar.setEnabled(False)
        self.btn_abrir = QPushButton("📂 Abrir Reporte")
        self.btn_abrir.setObjectName("btnAbrir")
        self.btn_abrir.clicked.connect(self.abrir_reporte)
        self.btn_abrir.setEnabled(False)
        layout_btns_log.addWidget(btn_limpiar)
        layout_btns_log.addStretch()
        layout_btns_log.addWidget(self.btn_exportar)
        layout_btns_log.addWidget(self.btn_abrir)
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
        self.btn_abrir.setEnabled(False)
        
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
        self.thread = ComparadorThread(self.comparador)
        self.thread.log_signal.connect(self.log)
        self.thread.finished_signal.connect(self.comparacion_terminada)
        self.thread.start()
    
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
            self.btn_abrir.setEnabled(True)
            
            # Abrir automáticamente el archivo
            os.startfile(ruta)
            self.log(f"📂 Abriendo reporte automáticamente...", "info")
        except Exception as e:
            self.log(f"❌ Error exportando: {str(e)}", "error")
    
    def abrir_reporte(self):
        """Abre el último reporte exportado en Excel"""
        if self.ruta_ultimo_reporte and Path(self.ruta_ultimo_reporte).exists():
            try:
                os.startfile(self.ruta_ultimo_reporte)
                self.log(f"📂 Abriendo reporte: {self.ruta_ultimo_reporte}", "info")
            except Exception as e:
                self.log(f"❌ Error abriendo archivo: {str(e)}", "error")
        else:
            self.log("⚠️ No hay reporte para abrir. Exporte primero.", "warning")
    
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
        scrollbar.setValue(scrollbar.maximum())
    
    def limpiar_logs(self):
        """Limpia el área de logs"""
        self.txt_logs.clear()


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
