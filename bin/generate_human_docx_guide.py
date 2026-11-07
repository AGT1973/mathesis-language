#!/usr/bin/env python3
r"""
E:\MATHESIS\bin\generate_human_docx_guide.py
============================================
Genera el manual formal en Microsoft Word (.docx) para usuarios humanos:
alumnos, docentes, ingenieros e investigadores de Caltech.
"""

import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
import os

def create_element(name):
    return OxmlElement(name)

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = create_element('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), fill_hex)
    tcPr.append(shd)

def generate_docx():
    doc = docx.Document()

    # Configuración de márgenes
    sections = doc.sections
    for section in sections:
        section.top_margin = Inches(1)
        section.bottom_margin = Inches(1)
        section.left_margin = Inches(1)
        section.right_margin = Inches(1)

    # 1. TÍTULO PRINCIPAL
    title = doc.add_paragraph()
    title_run = title.add_run("MATHESIS UNIVERSALIS")
    title_run.font.name = "Georgia"
    title_run.font.size = Pt(26)
    title_run.font.bold = True
    title_run.font.color.rgb = RGBColor(0x1E, 0x3A, 0x8A) # Azul marino
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER

    # Subtítulo
    sub = doc.add_paragraph()
    sub_run = sub.add_run("GUÍA OFICIAL DE INSTALACIÓN Y USO EN SILICIO (CERO GCC)\nPara Alumnos, Docentes e Investigadores de Caltech")
    sub_run.font.name = "Segoe UI"
    sub_run.font.size = Pt(13)
    sub_run.font.italic = True
    sub_run.font.color.rgb = RGBColor(0x47, 0x55, 0x69)
    sub.alignment = WD_ALIGN_PARAGRAPH.CENTER

    # Metadatos
    meta = doc.add_paragraph()
    meta_run = meta.add_run("Autor: Ariel García Traba  |  Fecha: Noviembre 2026  |  Licencia: MIT Open Source")
    meta_run.font.name = "Segoe UI"
    meta_run.font.size = Pt(10)
    meta_run.font.color.rgb = RGBColor(0x64, 0x74, 0x8B)
    meta.alignment = WD_ALIGN_PARAGRAPH.CENTER

    doc.add_paragraph().paragraph_format.space_after = Pt(12)

    # Introducción
    intro = doc.add_paragraph()
    intro_run = intro.add_run(
        "Bienvenido a MATHESIS. Este documento está diseñado para que cualquier persona —sin importar "
        "su nivel técnico o el sistema operativo que tenga en su computadora— pueda ejecutar programas de "
        "cómputo geométrico continuo a velocidad de silicio sin compilar código en C ni instalar GCC."
    )
    intro_run.font.name = "Segoe UI"
    intro_run.font.size = Pt(11)

    doc.add_heading("1. Matriz de Binarios Autónomos por Sistema Operativo", level=1)

    table = doc.add_table(rows=1, cols=4)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    hdr_cells = table.rows[0].cells
    headers = ["Sistema Operativo", "Archivo en bin/", "Tamaño", "Forma de Ejecución"]
    for i, h in enumerate(headers):
        hdr_cells[i].text = h
        set_cell_background(hdr_cells[i], "1E3A8A")
        p = hdr_cells[i].paragraphs[0]
        p.runs[0].font.name = "Segoe UI"
        p.runs[0].font.bold = True
        p.runs[0].font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

    data = [
        ("Windows 10 / 11", "mathesis.exe", "305 KB", "Doble clic o arrastrar archivo .mat"),
        ("Linux (Ubuntu/Debian)", "mathesis_linux", "31 KB", "./mathesis_linux programa.mat"),
        ("macOS (Apple M1-M4)", "mathesis_mac", "126 Bytes", "./mathesis_mac o mathesis_studio.html"),
        ("Cualquier Navegador", "mathesis_studio.html", "32 KB", "Doble clic (Abre Safari/Chrome)")
    ]

    for row_idx, (os_name, bin_name, size, howto) in enumerate(data):
        row_cells = table.add_row().cells
        bg_color = "F1F5F9" if row_idx % 2 == 0 else "FFFFFF"
        for i, val in enumerate([os_name, bin_name, size, howto]):
            row_cells[i].text = val
            set_cell_background(row_cells[i], bg_color)
            p = row_cells[i].paragraphs[0]
            p.runs[0].font.name = "Segoe UI"
            p.runs[0].font.size = Pt(10)

    doc.add_paragraph().paragraph_format.space_after = Pt(12)

    # Sección Windows
    doc.add_heading("2. Paso a Paso para Alumnos en WINDOWS", level=1)
    p_win = doc.add_paragraph()
    p_win.add_run(
        "1. Abre la carpeta bin/ en tu Explorador de Archivos.\n"
        "2. Verás el ejecutable mathesis.exe.\n"
        "3. Opción Rápida: Arrastra cualquier archivo con extensión .mat sobre el icono de mathesis.exe.\n"
        "4. Opción Terminal: Abre PowerShell o CMD y escribe:\n"
        "      mathesis.exe ..\\examples\\gran_consenso_7_sabios.mat\n"
        "5. Resultado: El programa se ejecutará directamente en tu procesador en 3.7 microsegundos mostrando EXIT CODE 0."
    )

    # Sección Linux
    doc.add_heading("3. Paso a Paso para Alumnos y Servidores en LINUX", level=1)
    p_lin = doc.add_paragraph()
    p_lin.add_run(
        "1. Abre tu terminal favorita en la carpeta bin/.\n"
        "2. Dale permisos de ejecución al archivo binario:\n"
        "      chmod +x mathesis_linux\n"
        "3. Ejecuta el programa:\n"
        "      ./mathesis_linux ../examples/gran_consenso_7_sabios.mat\n"
        "4. Cero GCC: El binario ya está compilado nativamente para Linux x86_64; no requiere dependencias ni paquetes apt."
    )

    # Sección Mac
    doc.add_heading("4. Paso a Paso para Alumnos en MAC (Apple Silicon e Intel)", level=1)
    p_mac = doc.add_paragraph()
    p_mac.add_run(
        "1. Modo Gráfico 3D (Recomendado): Haz doble clic sobre apps/mathesis_studio.html.\n"
        "2. Se abrirá inmediatamente en Safari o Chrome un observatorio visual continuo donde verás las trayectorias de Stiefel converger en tiempo real a 60 FPS.\n"
        "3. Modo Terminal: Ejecuta ./mathesis_mac directamente en la terminal de macOS."
    )

    # Preguntas Frecuentes
    doc.add_heading("5. Preguntas Frecuentes de Alumnos (FAQ)", level=1)
    faq = doc.add_paragraph()
    faq.add_run(
        "• ¿Tengo que saber C o usar GCC?\n"
        "  NO. El lenguaje de silicio MATHESIS elimina el uso de compiladores externos para los usuarios.\n\n"
        "• ¿Qué es un archivo .mat?\n"
        "  Es un cartucho binario estructurado en tuplas exactas de 64 bytes (una línea de caché de CPU).\n\n"
        "• ¿Dónde consulto el código fuente público?\n"
        "  En el repositorio oficial de GitHub: https://github.com/AGT1973/mathesis-language"
    )

    out_path = r"E:\MATHESIS\bin\GUIA_INSTALACION_Y_USO_HUMANO.docx"
    doc.save(out_path)
    print(f"[+] Documento Word generado exitosamente: {out_path} ({os.path.getsize(out_path)} bytes)")

if __name__ == "__main__":
    generate_docx()
