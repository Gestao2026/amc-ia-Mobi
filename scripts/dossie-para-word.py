#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Conversor do Dossiê do Edital para Word e PDF.

Pega o dossiê escrito em markdown e gera o arquivo formatado que vai para o
cliente: A4, títulos hierárquicos, tabelas reais, blocos de destaque e
numeração de página. Se o Microsoft Word estiver instalado, gera o PDF junto.

  dossie.md  ->  DOSSIE DO EDITAL - {edital}.docx
                 DOSSIE DO EDITAL - {edital}.pdf

Uso:
  python3 scripts/dossie-para-word.py <entrada.md> <saida.docx> [--sem-pdf]

Requer python-docx. O PDF depende do Word (Windows); sem ele, o .docx sai
normalmente e o PDF é ignorado com aviso.
"""

import re
import sys

from docx import Document
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor

AZUL = RGBColor(0x1F, 0x3B, 0x63)
CINZA = RGBColor(0x44, 0x44, 0x44)
CINZA_CLARO = "EDF1F7"
DESTAQUE = "F5F0E1"


def set_cell_bg(cell, hexcolor):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), hexcolor)
    tcPr.append(shd)


def add_bottom_border(paragraph, size=6, color="1F3B63"):
    pPr = paragraph._p.get_or_add_pPr()
    pbdr = OxmlElement("w:pBdr")
    bottom = OxmlElement("w:bottom")
    bottom.set(qn("w:val"), "single")
    bottom.set(qn("w:sz"), str(size))
    bottom.set(qn("w:space"), "4")
    bottom.set(qn("w:color"), color)
    pbdr.append(bottom)
    pPr.append(pbdr)


INLINE = re.compile(r"(\*\*.+?\*\*|`[^`]+`|\*[^*]+?\*|\[.+?\]\(.+?\))")


def add_runs(paragraph, text, base_size=None, base_color=None, base_bold=False):
    """Escreve texto com negrito, italico, codigo e links resolvidos."""
    text = text.replace("\\|", "|")
    for piece in INLINE.split(text):
        if not piece:
            continue
        bold = base_bold
        italic = False
        mono = False
        content = piece
        if piece.startswith("**") and piece.endswith("**") and len(piece) > 4:
            content, bold = piece[2:-2], True
        elif piece.startswith("`") and piece.endswith("`") and len(piece) > 2:
            content, mono = piece[1:-1], True
        elif piece.startswith("*") and piece.endswith("*") and len(piece) > 2:
            content, italic = piece[1:-1], True
        else:
            m = re.fullmatch(r"\[(.+?)\]\((.+?)\)", piece)
            if m:
                label, url = m.group(1), m.group(2)
                content = label if label == url else "%s (%s)" % (label, url)
        run = paragraph.add_run(content)
        run.bold = bold
        run.italic = italic
        if mono:
            run.font.name = "Consolas"
            run.font.size = Pt((base_size or 10.5) - 0.5)
        elif base_size:
            run.font.size = Pt(base_size)
        if base_color is not None:
            run.font.color.rgb = base_color


def split_row(line):
    line = line.strip().strip("|")
    parts = re.split(r"(?<!\\)\|", line)
    return [p.strip() for p in parts]


def is_separator(line):
    return bool(re.fullmatch(r"\|?[\s:\-|]+\|?", line.strip())) and "-" in line


def build(md_path, out_path):
    with open(md_path, encoding="utf-8") as fh:
        lines = fh.read().replace("\r\n", "\n").split("\n")

    doc = Document()

    sec = doc.sections[0]
    sec.page_width = Cm(21.0)
    sec.page_height = Cm(29.7)
    sec.top_margin = Cm(2.0)
    sec.bottom_margin = Cm(2.0)
    sec.left_margin = Cm(2.0)
    sec.right_margin = Cm(2.0)

    normal = doc.styles["Normal"]
    normal.font.name = "Calibri"
    normal.font.size = Pt(10.5)
    normal.paragraph_format.space_after = Pt(6)
    normal.paragraph_format.line_spacing = 1.15

    # rodape com numero de pagina
    footer = sec.footer.paragraphs[0]
    footer.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = footer.add_run()
    for instr in ("begin", "instrText", "end"):
        el = OxmlElement("w:" + ("fldChar" if instr != "instrText" else "instrText"))
        if instr == "instrText":
            el.set(qn("xml:space"), "preserve")
            el.text = " PAGE "
        else:
            el.set(qn("w:fldCharType"), instr)
        run._r.append(el)
    run.font.size = Pt(8)
    run.font.color.rgb = CINZA

    i = 0
    n = len(lines)
    while i < n:
        raw = lines[i]
        line = raw.strip()

        if not line:
            i += 1
            continue

        # regra horizontal
        if re.fullmatch(r"-{3,}|\*{3,}", line):
            p = doc.add_paragraph()
            p.paragraph_format.space_before = Pt(2)
            p.paragraph_format.space_after = Pt(8)
            add_bottom_border(p, size=4, color="C9D2E0")
            i += 1
            continue

        # tabela
        if line.startswith("|") and i + 1 < n and is_separator(lines[i + 1]):
            header = split_row(line)
            i += 2
            rows = []
            while i < n and lines[i].strip().startswith("|"):
                rows.append(split_row(lines[i]))
                i += 1
            cols = max([len(header)] + [len(r) for r in rows])
            table = doc.add_table(rows=1, cols=cols)
            table.style = "Table Grid"
            table.alignment = WD_TABLE_ALIGNMENT.CENTER
            table.autofit = True
            hdr = table.rows[0].cells
            blank_header = all(not c for c in header)
            for c in range(cols):
                cell = hdr[c]
                cell.text = ""
                p = cell.paragraphs[0]
                p.paragraph_format.space_after = Pt(2)
                txt = header[c] if c < len(header) else ""
                add_runs(p, txt, base_size=10, base_color=AZUL, base_bold=True)
                set_cell_bg(cell, CINZA_CLARO)
            if blank_header:
                # cabecalho vazio: mantem so a faixa, sem altura extra
                pass
            for r in rows:
                cells = table.add_row().cells
                for c in range(cols):
                    cell = cells[c]
                    cell.text = ""
                    p = cell.paragraphs[0]
                    p.paragraph_format.space_after = Pt(2)
                    add_runs(p, r[c] if c < len(r) else "", base_size=10)
            doc.add_paragraph().paragraph_format.space_after = Pt(2)
            continue

        # citacao / destaque
        if line.startswith(">"):
            bloco = []
            while i < n and lines[i].strip().startswith(">"):
                bloco.append(lines[i].strip().lstrip(">").strip())
                i += 1
            texto = " ".join(x for x in bloco if x)
            tbl = doc.add_table(rows=1, cols=1)
            tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
            cell = tbl.rows[0].cells[0]
            cell.text = ""
            p = cell.paragraphs[0]
            p.paragraph_format.space_before = Pt(4)
            p.paragraph_format.space_after = Pt(4)
            add_runs(p, texto, base_size=10)
            set_cell_bg(cell, DESTAQUE)
            doc.add_paragraph().paragraph_format.space_after = Pt(2)
            continue

        # titulos
        m = re.match(r"^(#{1,4})\s+(.*)$", line)
        if m:
            nivel = len(m.group(1))
            texto = m.group(2).strip()
            p = doc.add_paragraph()
            pf = p.paragraph_format
            if nivel == 1:
                pf.space_before = Pt(18)
                pf.space_after = Pt(8)
                add_runs(p, texto, base_size=18, base_color=AZUL, base_bold=True)
                add_bottom_border(p)
            elif nivel == 2:
                pf.space_before = Pt(14)
                pf.space_after = Pt(6)
                add_runs(p, texto, base_size=14, base_color=AZUL, base_bold=True)
            elif nivel == 3:
                pf.space_before = Pt(10)
                pf.space_after = Pt(4)
                add_runs(p, texto, base_size=12, base_color=AZUL, base_bold=True)
            else:
                pf.space_before = Pt(8)
                pf.space_after = Pt(3)
                add_runs(p, texto, base_size=11, base_color=CINZA, base_bold=True)
            p.style = doc.styles["Normal"]
            i += 1
            continue

        # lista com marcador
        if re.match(r"^[-*+]\s+", line):
            p = doc.add_paragraph(style="List Bullet")
            p.paragraph_format.space_after = Pt(3)
            add_runs(p, re.sub(r"^[-*+]\s+", "", line))
            i += 1
            continue

        # lista numerada
        if re.match(r"^\d+[.)]\s+", line):
            p = doc.add_paragraph(style="List Number")
            p.paragraph_format.space_after = Pt(3)
            add_runs(p, re.sub(r"^\d+[.)]\s+", "", line))
            i += 1
            continue

        # paragrafo comum
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        add_runs(p, line)
        i += 1

    doc.save(out_path)
    print("OK ->", out_path)


def gerar_pdf(docx_path):
    """Converte o .docx em PDF usando o Word instalado (somente Windows)."""
    import os

    docx_abs = os.path.abspath(docx_path)
    pdf_abs = os.path.splitext(docx_abs)[0] + ".pdf"
    try:
        import win32com.client  # type: ignore

        word = win32com.client.Dispatch("Word.Application")
    except Exception:
        # Sem pywin32, tenta pelo PowerShell, que existe em qualquer Windows.
        import subprocess

        ps = (
            "$w = New-Object -ComObject Word.Application; "
            "$w.Visible=$false; $w.DisplayAlerts=0; "
            "$d = $w.Documents.Open('%s',$false,$true); "
            "$d.SaveAs([ref]'%s',[ref]17); "
            "$d.Close([ref]0); $w.Quit()" % (docx_abs, pdf_abs)
        )
        try:
            subprocess.run(
                ["powershell", "-NoProfile", "-NonInteractive", "-Command", ps],
                check=True,
                capture_output=True,
                timeout=180,
            )
        except Exception as erro:
            print("PDF nao gerado (Word indisponivel):", erro)
            return None
        print("OK ->", pdf_abs)
        return pdf_abs

    word.Visible = False
    word.DisplayAlerts = 0
    doc = word.Documents.Open(docx_abs, False, True)
    doc.SaveAs(pdf_abs, FileFormat=17)
    doc.Close(0)
    word.Quit()
    print("OK ->", pdf_abs)
    return pdf_abs


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if len(args) < 2:
        print(__doc__)
        sys.exit(1)
    build(args[0], args[1])
    if "--sem-pdf" not in sys.argv:
        gerar_pdf(args[1])
