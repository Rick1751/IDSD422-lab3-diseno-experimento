# generar_pdf.py — Convierte plantilla-protocolo.md en el PDF de informes/ (carátula + 9 secciones + bonus)
# Requisito:  pip install reportlab
# Uso (desde la raíz del repositorio):
#   python scripts/generar_pdf.py
# Antes de generar el PDF final, reemplaza los <<COMPLETAR>> de la cabecera de la plantilla
# (Equipo e Integrantes). El script se niega a generar el PDF final si quedan pendientes;
# con --permitir-pendientes genera una vista previa.

import argparse
import os
import re
import sys
import textwrap

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (KeepTogether, PageBreak, Paragraph, Preformatted, SimpleDocTemplate,
                                Spacer, Table, TableStyle)

PENDIENTE = "<<COMPLETAR>>"

# ---------------------------------------------------------------- fuentes (con tildes y símbolos)
FUENTES = [
    ("/usr/share/fonts/truetype/dejavu/", "DejaVuSans.ttf", "DejaVuSans-Bold.ttf", "DejaVuSans-Oblique.ttf", "DejaVuSansMono.ttf"),
    ("C:/Windows/Fonts/", "arial.ttf", "arialbd.ttf", "ariali.ttf", "consola.ttf"),
    ("/System/Library/Fonts/Supplemental/", "Arial.ttf", "Arial Bold.ttf", "Arial Italic.ttf", "Courier New.ttf"),
    ("/Library/Fonts/", "Arial.ttf", "Arial Bold.ttf", "Arial Italic.ttf", "Courier New.ttf"),
]
REEMPLAZOS = {"≈": "aprox.", "≥": ">=", "−": "-", "×": "x", "→": "->", "μ": "mu", "’": "'", "«": '"', "»": '"'}
BASE, MONO, SANEAR = "Helvetica", "Courier", True
for carpeta, r, b, i, m in FUENTES:
    if all(os.path.exists(carpeta + f) for f in (r, b, i, m)):
        pdfmetrics.registerFont(TTFont("Base", carpeta + r))
        pdfmetrics.registerFont(TTFont("Base-B", carpeta + b))
        pdfmetrics.registerFont(TTFont("Base-I", carpeta + i))
        pdfmetrics.registerFont(TTFont("Mono", carpeta + m))
        pdfmetrics.registerFontFamily("Base", normal="Base", bold="Base-B", italic="Base-I", boldItalic="Base-B")
        BASE, MONO, SANEAR = "Base", "Mono", False
        break

AZUL = colors.HexColor("#1F3A5F")
GRIS = colors.HexColor("#F2F4F7")
st = {
    "p": ParagraphStyle("p", fontName=BASE, fontSize=9.6, leading=13.4, spaceAfter=5),
    "h2": ParagraphStyle("h2", fontName=BASE if BASE == "Helvetica" else "Base-B", fontSize=13, leading=16,
                         textColor=AZUL, spaceBefore=12, spaceAfter=6),
    "b0": ParagraphStyle("b0", fontName=BASE, fontSize=9.6, leading=13.4, leftIndent=14, bulletIndent=3, spaceAfter=3),
    "b1": ParagraphStyle("b1", fontName=BASE, fontSize=9.6, leading=13.4, leftIndent=30, bulletIndent=19, spaceAfter=2),
    "cell": ParagraphStyle("cell", fontName=BASE, fontSize=8.6, leading=11.2),
    "cellh": ParagraphStyle("cellh", fontName=BASE if BASE == "Helvetica" else "Base-B", fontSize=8.6, leading=11.2,
                            textColor=colors.white),
    "code": ParagraphStyle("code", fontName=MONO, fontSize=7.4, leading=9.4, backColor=GRIS,
                           borderPadding=5, spaceBefore=4, spaceAfter=8, leftIndent=4),
    "tit": ParagraphStyle("tit", fontName=BASE if BASE == "Helvetica" else "Base-B", fontSize=24, leading=29,
                          textColor=AZUL, alignment=TA_CENTER, spaceAfter=10),
    "sub": ParagraphStyle("sub", fontName=BASE, fontSize=12, leading=17, alignment=TA_CENTER, spaceAfter=4),
    "ins": ParagraphStyle("ins", fontName=BASE, fontSize=10.5, leading=15, alignment=TA_CENTER, spaceAfter=2),
}


def sanear(t):
    if SANEAR:
        for k, v in REEMPLAZOS.items():
            t = t.replace(k, v)
    return t


def inline(t):
    """Markdown en línea -> marcado de reportlab."""
    t = sanear(t).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    codigos = []

    def guarda(m):
        codigos.append(m.group(1))
        return f"\x00{len(codigos) - 1}\x00"

    t = re.sub(r"`([^`]+)`", guarda, t)
    t = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", t)
    t = re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])", r"<i>\1</i>", t)
    t = re.sub(r"(https?://[^\s<)]+)", r'<a href="\1" color="#1155CC">\1</a>', t)
    return re.sub(r"\x00(\d+)\x00", lambda m: f'<font name="{MONO}" size="8.4">{codigos[int(m.group(1))]}</font>', t)


def bloque_codigo(lineas, ancho=100):
    out = []
    for ln in lineas:
        ln = sanear(ln).replace("\t", "    ")
        sangria = " " * (len(ln) - len(ln.lstrip()))
        out += textwrap.wrap(ln, ancho, subsequent_indent=sangria + "    ", drop_whitespace=False,
                             replace_whitespace=False) or [""]
    return Preformatted("\n".join(out), st["code"])


def tabla(filas, ancho):
    filas = [f for f in filas if not re.match(r"^\|[\s:|-]+\|$", f)]
    celdas = [[c.strip() for c in f.strip().strip("|").split("|")] for f in filas]
    n = len(celdas[0])
    datos = [[Paragraph(inline(c), st["cellh" if i == 0 else "cell"]) for c in fila] for i, fila in enumerate(celdas)]
    pesos = {2: [0.30, 0.70], 3: [0.16, 0.42, 0.42]}.get(n, [1 / n] * n)
    t = Table(datos, colWidths=[ancho * p for p in pesos], repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), AZUL), ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#9AA5B1")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"), ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, GRIS]),
        ("LEFTPADDING", (0, 0), (-1, -1), 4), ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 3), ("BOTTOMPADDING", (0, 0), (-1, -1), 3)]))
    return [t, Spacer(1, 7)]


def cuerpo(md, ancho):
    lineas = md.split("\n")
    i = next(k for k, ln in enumerate(lineas) if ln.startswith("## "))
    flow, par = [], []

    def cierra():
        if par:
            flow.append(Paragraph(inline(" ".join(s.strip() for s in par)), st["p"]))
            par.clear()

    while i < len(lineas):
        ln = lineas[i]
        if ln.startswith("```"):
            cierra()
            j = i + 1
            while not lineas[j].startswith("```"):
                j += 1
            bloque = bloque_codigo(lineas[i + 1:j])
            flow.append(KeepTogether([bloque]) if j - i < 26 else bloque)
            i = j
        elif ln.startswith("## "):
            cierra()
            flow.append(Paragraph(inline(ln[3:]), st["h2"]))
        elif ln.startswith("|"):
            cierra()
            j = i
            while j < len(lineas) and lineas[j].startswith("|"):
                j += 1
            flow += tabla(lineas[i:j], ancho)
            i = j - 1
        elif re.match(r"^\s*- ", ln):
            cierra()
            nivel = 1 if len(ln) - len(ln.lstrip()) >= 2 else 0
            flow.append(Paragraph(inline(ln.strip()[2:]), st[f"b{nivel}"], bulletText="•" if nivel == 0 else "–"))
        elif not ln.strip():
            cierra()
        else:
            par.append(ln)
        i += 1
    cierra()
    return flow


def campo(md, nombre):
    m = re.search(rf"\*\*{nombre}:\*\*\s*(.+?)(?:\s·\s\*\*|\n|$)", md)
    return m.group(1).strip() if m else ""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--md", default="plantilla-protocolo.md")
    ap.add_argument("--out", default="informes/protocolo_lab3_RetailAndina.pdf")
    ap.add_argument("--permitir-pendientes", action="store_true")
    a = ap.parse_args()
    md = open(a.md, encoding="utf-8").read()
    if PENDIENTE in md and not a.permitir_pendientes:
        sys.exit(f"Quedan {PENDIENTE} en {a.md}: completa Equipo e Integrantes y vuelve a ejecutar.")
    equipo, integ, fecha, repo = (campo(md, c) for c in ("Equipo", "Integrantes", "Fecha", "Repositorio \\(fork\\)"))

    os.makedirs(os.path.dirname(a.out), exist_ok=True)
    doc = SimpleDocTemplate(a.out, pagesize=A4, leftMargin=2 * cm, rightMargin=2 * cm, topMargin=2 * cm,
                            bottomMargin=2 * cm, title="Práctica 3 · Diseño de un experimento de ubicación de producto",
                            author=integ)
    ancho = A4[0] - 4 * cm
    cab = [Spacer(1, 2.2 * cm),
           Paragraph("ESCUELA POLITÉCNICA NACIONAL", st["sub"]),
           Paragraph("Facultad de Ingeniería de Sistemas · Ciencia de Datos e Inteligencia Artificial", st["sub"]),
           Spacer(1, 1.6 * cm),
           Paragraph("Práctica 3 (Tópico 3)<br/>Diseño de un experimento de ubicación de producto", st["tit"]),
           Paragraph("Caso RetailAndina S.A.", st["sub"]),
           Paragraph("IDSD422 · Estadística y Programación para Ciencia de Datos I · 2026-B", st["sub"]),
           Spacer(1, 1.6 * cm),
           Paragraph(f"<b>Equipo:</b> {inline(equipo)}", st["ins"]),
           Paragraph(f"<b>Integrantes:</b> {inline(integ)}", st["ins"]),
           Paragraph(f"<b>Fecha de entrega:</b> {inline(fecha)}", st["ins"]),
           Spacer(1, 0.8 * cm),
           Paragraph("<b>Enlace del fork (entrega):</b>", st["ins"]),
           Paragraph(inline(repo), st["ins"]),
           PageBreak()]

    def pie(canvas, d):
        canvas.saveState()
        canvas.setFont(BASE, 7.5)
        canvas.setFillColor(colors.HexColor("#6B7785"))
        canvas.drawString(2 * cm, 1.2 * cm, sanear("IDSD422 · Práctica 3 · RetailAndina · " + repo))
        canvas.drawRightString(A4[0] - 2 * cm, 1.2 * cm, f"pág. {d.page}")
        canvas.restoreState()

    doc.build(cab + cuerpo(md, ancho), onFirstPage=lambda c, d: None, onLaterPages=pie)
    print("PDF generado:", a.out)


if __name__ == "__main__":
    main()
