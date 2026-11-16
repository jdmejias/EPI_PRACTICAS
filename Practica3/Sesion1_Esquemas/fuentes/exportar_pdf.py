# -*- coding: utf-8 -*-
"""
Exporta las láminas SVG a un PDF A3 apaisado (una lámina por página) usando
Microsoft Edge en modo headless, añade la portada y genera vistas previas PNG.
Uso: python exportar_pdf.py <carpeta_salida>
"""
import os
import subprocess
import sys
import tempfile
from pathlib import Path

import fitz  # PyMuPDF

OUT = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
HERE = Path(__file__).resolve().parent
EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
SHEETS = ["ICT_01_Conjunto_3D", "ICT_02_Plano_General_2D", "ICT_03_Vivienda_Planta_Baja",
          "ICT_04_Vivienda_Planta_Primera", "ICT_05_Local_y_Zonas_Comunes"]
PAGE_CSS = "@page{size:420mm 297mm;margin:0}html,body{margin:0;padding:0;background:#fff}"


def print_pdf(html_path, pdf_path):
    subprocess.run([EDGE, "--headless", "--disable-gpu", "--no-pdf-header-footer",
                    "--print-to-pdf=" + str(pdf_path), html_path.as_uri()],
                   check=True, capture_output=True, timeout=120)


def main():
    tmp = Path(tempfile.mkdtemp(prefix="ict_pdf_"))
    parts = []
    cover = HERE / "portada.html"
    pdf = tmp / "00_portada.pdf"
    print_pdf(cover, pdf)
    parts.append(pdf)
    for s in SHEETS:
        html = tmp / (s + ".html")
        html.write_text('<!doctype html><html><head><meta charset="utf-8"><style>%s'
                        'img{display:block;width:420mm;height:297mm}</style></head><body>'
                        '<img src="%s"></body></html>' % (PAGE_CSS, (OUT / (s + ".svg")).as_uri()),
                        encoding="utf-8")
        pdf = tmp / (s + ".pdf")
        print_pdf(html, pdf)
        parts.append(pdf)
    book = fitz.open()
    for p in parts:
        with fitz.open(p) as d:
            book.insert_pdf(d, from_page=0, to_page=0)   # 1 página por lámina
    target = OUT / "ICT_Sesion1_Esquemas_3D_2D.pdf"
    book.save(target)
    prev = OUT / "previsualizacion_png"
    prev.mkdir(exist_ok=True)
    names = ["ICT_00_Portada"] + SHEETS
    for i, page in enumerate(book):
        page.get_pixmap(dpi=150).save(prev / (names[i] + ".png"))
    print("PDF:", target, "| páginas:", book.page_count,
          "| tamaño pág. 1 (mm):", [round(v / 72 * 25.4) for v in book[0].rect[2:]])


if __name__ == "__main__":
    main()
