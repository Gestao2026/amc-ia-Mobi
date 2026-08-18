#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Exportador de projeto da AMC IA.

Pega a proposta e o orçamento (em markdown) de um projeto e gera os arquivos
prontos para submeter, sem precisar instalar nada:

  proposta.doc              Word/Google Docs (editável, A4, formatado)
  proposta-impressao.html   versão para imprimir ou salvar como PDF
  orcamento.xls             Excel/Google Sheets (editável)
  orcamento.csv             planilha simples (compatibilidade máxima)
  orcamento-impressao.html  versão para imprimir
  projeto-completo.html     proposta + orçamento + parecer + nota, em um arquivo
  *.pdf                     gerados automaticamente se o Google Chrome existir

Uso:
  python3 scripts/exportar-projeto.py <osc-slug> <edital-slug> [--sem-pdf]

Sem osc-slug, usa a OSC ativa. Sem edital-slug, exporta se houver um único
projeto; com vários, lista as opções.
"""

import argparse
import html
import re
import subprocess
import sys
from datetime import date
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
OSCS = RAIZ / "minhas-oscs"

CHROME_MAC = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

CSS_BASE = """
  body{font-family:'Calibri','Segoe UI',Arial,sans-serif;font-size:11.5pt;color:#1a1a1a;line-height:1.5}
  h1{font-size:20pt;color:#0f3a4d;margin:0 0 4pt}
  h2{font-size:14pt;color:#0e7490;border-bottom:1px solid #cbd5e1;padding-bottom:3pt;margin:18pt 0 6pt}
  h3{font-size:12pt;color:#155e75;margin:12pt 0 4pt}
  p{text-align:justify;margin:0 0 8pt}
  ul,ol{margin:0 0 8pt 18pt}
  li{margin:0 0 3pt}
  table{border-collapse:collapse;width:100%;margin:8pt 0;font-size:10.5pt}
  th{background:#0e7490;color:#fff;text-align:left;padding:5pt 8pt;border:1px solid #0b5566}
  td{padding:5pt 8pt;border:1px solid #b6c2d1;vertical-align:top}
  tr:nth-child(even) td{background:#f1f5f9}
  blockquote{border-left:3px solid #0e7490;margin:8pt 0;padding:2pt 12pt;color:#475569;background:#f8fafc}
  hr{border:none;border-top:1px solid #cbd5e1;margin:14pt 0}
  .capa{text-align:center;padding:40pt 0 24pt;border-bottom:2px solid #0e7490;margin-bottom:18pt}
  .capa .org{font-size:13pt;color:#0e7490;font-weight:bold;letter-spacing:.5pt}
  .capa .tit{font-size:22pt;color:#0f3a4d;font-weight:bold;margin:14pt 0 6pt}
  .capa .sub{font-size:12pt;color:#475569}
  .rodape{margin-top:18pt;color:#94a3b8;font-size:9pt;text-align:center}
"""


# ── Conversor markdown -> HTML (leve, sem dependências) ──────────────────────
def md_para_html(md):
    """Converte um subconjunto de markdown em HTML. Retorna (html, tabelas)."""
    md = remover_secoes_internas(md)
    linhas = md.split("\n")
    out = []
    tabelas = []
    i = 0
    n = len(linhas)

    def inline(t):
        t = html.escape(t)
        t = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t)
        t = re.sub(r"(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)", r"<em>\1</em>", t)
        t = re.sub(r"`(.+?)`", r"<code>\1</code>", t)
        return t

    while i < n:
        linha = linhas[i]
        bruta = linha.rstrip()

        if not bruta.strip():
            i += 1
            continue

        # Tabela (linha com | e próxima de separador ---)
        if bruta.lstrip().startswith("|") and i + 1 < n and re.match(r"^\s*\|?[\s:|-]+\|?\s*$", linhas[i + 1]):
            bloco = []
            while i < n and linhas[i].strip().startswith("|"):
                bloco.append(linhas[i].strip())
                i += 1
            html_tab, linhas_tab = montar_tabela(bloco, inline)
            out.append(html_tab)
            tabelas.append(linhas_tab)
            continue

        # Cabeçalhos
        m = re.match(r"^(#{1,6})\s+(.*)$", bruta)
        if m:
            nivel = len(m.group(1))
            out.append(f"<h{nivel}>{inline(m.group(2).strip())}</h{nivel}>")
            i += 1
            continue

        # Regra horizontal
        if re.match(r"^\s*([-*_])\1\1+\s*$", bruta):
            out.append("<hr>")
            i += 1
            continue

        # Citação
        if bruta.lstrip().startswith(">"):
            cit = []
            while i < n and linhas[i].lstrip().startswith(">"):
                cit.append(inline(re.sub(r"^\s*>\s?", "", linhas[i])))
                i += 1
            out.append("<blockquote>" + "<br>".join(cit) + "</blockquote>")
            continue

        # Lista não ordenada
        if re.match(r"^\s*[-*]\s+", bruta):
            itens = []
            while i < n and re.match(r"^\s*[-*]\s+", linhas[i]):
                itens.append("<li>" + inline(re.sub(r"^\s*[-*]\s+", "", linhas[i]).rstrip()) + "</li>")
                i += 1
            out.append("<ul>" + "".join(itens) + "</ul>")
            continue

        # Lista ordenada
        if re.match(r"^\s*\d+\.\s+", bruta):
            itens = []
            while i < n and re.match(r"^\s*\d+\.\s+", linhas[i]):
                itens.append("<li>" + inline(re.sub(r"^\s*\d+\.\s+", "", linhas[i]).rstrip()) + "</li>")
                i += 1
            out.append("<ol>" + "".join(itens) + "</ol>")
            continue

        # Parágrafo (junta linhas até a próxima em branco)
        par = [bruta]
        i += 1
        while i < n and linhas[i].strip() and not re.match(r"^\s*(#{1,6}\s|[-*]\s|\d+\.\s|>|\|)", linhas[i]):
            par.append(linhas[i].rstrip())
            i += 1
        out.append("<p>" + inline(" ".join(par)) + "</p>")

    return "\n".join(out), tabelas


def montar_tabela(bloco, inline):
    def celulas(linha):
        return [c.strip() for c in linha.strip().strip("|").split("|")]

    cab = celulas(bloco[0])
    corpo = [celulas(l) for l in bloco[2:]]
    th = "".join(f"<th>{inline(c)}</th>" for c in cab)
    linhas_csv = [cab]
    trs = [f"<tr>{th}</tr>"]
    for row in corpo:
        tds = "".join(f"<td>{inline(c)}</td>" for c in row)
        trs.append(f"<tr>{tds}</tr>")
        linhas_csv.append(row)
    return "<table>" + "".join(trs) + "</table>", linhas_csv


def remover_secoes_internas(md):
    """Remove seções marcadas como uso interno (ex: 'Notas do CaptaBuilder (não submeter)')."""
    linhas = md.split("\n")
    out = []
    pulando = False
    for l in linhas:
        m = re.match(r"^(#{1,6})\s+(.*)$", l)
        if m:
            titulo = m.group(2).lower()
            if "não submeter" in titulo or "nao submeter" in titulo or titulo.startswith("notas do"):
                pulando = True
                continue
            else:
                pulando = False
        if not pulando:
            out.append(l)
    return "\n".join(out)


# ── Geração dos arquivos ─────────────────────────────────────────────────────
def doc_word(titulo, org, sub, corpo_html):
    """HTML compatível com Word (.doc), com página A4 e capa."""
    return f"""<html xmlns:o="urn:schemas-microsoft-com:office:office"
 xmlns:w="urn:schemas-microsoft-com:office:word" xmlns="http://www.w3.org/TR/REC-html40">
<head><meta charset="utf-8">
<!--[if gte mso 9]><xml><w:WordDocument><w:View>Print</w:View><w:Zoom>100</w:Zoom></w:WordDocument></xml><![endif]-->
<style>
@page Section1 {{ size:595.3pt 841.9pt; margin:2.5cm 2.5cm 2.5cm 3cm; }}
div.Section1 {{ page:Section1; }}
{CSS_BASE}
</style></head>
<body><div class="Section1">
<div class="capa"><div class="org">{html.escape(org)}</div>
<div class="tit">{html.escape(titulo)}</div>
<div class="sub">{html.escape(sub)}</div></div>
{corpo_html}
</div></body></html>"""


def html_impressao(titulo, corpo_html, org="", sub=""):
    capa = ""
    if org or sub:
        capa = (f'<div class="capa"><div class="org">{html.escape(org)}</div>'
                f'<div class="tit">{html.escape(titulo)}</div>'
                f'<div class="sub">{html.escape(sub)}</div></div>')
    return f"""<!doctype html><html lang="pt-br"><head><meta charset="utf-8">
<title>{html.escape(titulo)}</title>
<style>@page {{ size:A4; margin:2cm 2cm 2cm 2.5cm; }}
{CSS_BASE}
@media screen {{ body{{max-width:780px;margin:24px auto;padding:0 16px}} }}
</style></head><body>{capa}{corpo_html}
<div class="rodape">Gerado pela AMC IA</div></body></html>"""


def planilha_xls(titulo, tabelas):
    linhas_html = ""
    for tab in tabelas:
        for r, row in enumerate(tab):
            tag = "th" if r == 0 else "td"
            cels = "".join(f"<{tag}>{html.escape(c)}</{tag}>" for c in row)
            linhas_html += f"<tr>{cels}</tr>"
        linhas_html += "<tr></tr>"
    return f"""<html xmlns:x="urn:schemas-microsoft-com:office:excel"><head><meta charset="utf-8">
<!--[if gte mso 9]><xml><x:ExcelWorkbook><x:ExcelWorksheets><x:ExcelWorksheet>
<x:Name>Orcamento</x:Name><x:WorksheetOptions><x:DisplayGridlines/></x:WorksheetOptions>
</x:ExcelWorksheet></x:ExcelWorksheets></x:ExcelWorkbook></xml><![endif]-->
<style>table{{border-collapse:collapse}}th{{background:#0e7490;color:#fff}}th,td{{border:1px solid #999;padding:4px 8px;font-family:Calibri,Arial}}</style>
</head><body><h3>{html.escape(titulo)}</h3><table>{linhas_html}</table></body></html>"""


def csv_de_tabelas(tabelas):
    out = []
    for tab in tabelas:
        for row in tab:
            cels = []
            for c in row:
                c = c.replace('"', '""')
                if any(ch in c for ch in [",", '"', "\n", ";"]):
                    c = f'"{c}"'
                cels.append(c)
            out.append(";".join(cels))
        out.append("")
    return "\n".join(out)


def gerar_pdf(html_path, pdf_path):
    if not Path(CHROME_MAC).exists():
        return False
    try:
        subprocess.run(
            [CHROME_MAC, "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
             f"--print-to-pdf={pdf_path}", f"file://{html_path}"],
            check=True, capture_output=True, timeout=60,
        )
        return Path(pdf_path).exists()
    except Exception:
        # tenta o headless clássico
        try:
            subprocess.run(
                [CHROME_MAC, "--headless", "--disable-gpu",
                 f"--print-to-pdf={pdf_path}", f"file://{html_path}"],
                check=True, capture_output=True, timeout=60,
            )
            return Path(pdf_path).exists()
        except Exception:
            return False


# ── Orquestração ─────────────────────────────────────────────────────────────
def osc_ativa():
    f = OSCS / ".ativa"
    if f.exists() and f.read_text(encoding="utf-8").strip():
        return f.read_text(encoding="utf-8").strip()
    return None


def titulo_projeto(pasta, edital_slug):
    estado = pasta / "estado.md"
    if estado.exists():
        m = re.search(r"(?m)^#\s+(.+)$", estado.read_text(encoding="utf-8", errors="ignore"))
        if m:
            return m.group(1).strip()
    return edital_slug.replace("-", " ").title()


def nome_osc(slug):
    perfil = OSCS / slug / "perfil-osc.md"
    if perfil.exists():
        m = re.search(r"(?im)nome da organiza[çc][ãa]o:\s*\*?\*?\s*(.+)$", perfil.read_text(encoding="utf-8", errors="ignore"))
        if m:
            return re.sub(r"\*", "", m.group(1)).strip()
    return slug.replace("-", " ").title()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("osc", nargs="?", default=None)
    ap.add_argument("edital", nargs="?", default=None)
    ap.add_argument("--sem-pdf", action="store_true")
    args = ap.parse_args()

    slug = args.osc or osc_ativa()
    if not slug:
        sys.exit("Nenhuma OSC ativa. Cadastre com /osc-nova ou informe o slug.")
    base = OSCS / slug / "projetos"
    if not base.exists():
        sys.exit(f"A OSC '{slug}' não tem projetos.")

    edital = args.edital
    if not edital:
        projetos = [p.name for p in base.iterdir() if p.is_dir()]
        if len(projetos) == 1:
            edital = projetos[0]
        else:
            print("Informe qual projeto exportar. Projetos disponíveis:")
            for p in projetos:
                print("  -", p)
            sys.exit(0)

    pasta = base / edital
    if not pasta.exists():
        sys.exit(f"Projeto não encontrado: {pasta}")

    saida = pasta / "entrega-final"
    saida.mkdir(exist_ok=True)

    org = nome_osc(slug)
    titulo = titulo_projeto(pasta, edital)
    hoje = date.today().strftime("%d/%m/%Y")
    gerados = []

    # Proposta
    prop_md = pasta / "proposta.md"
    corpo_completo = ""
    if prop_md.exists() and prop_md.read_text(encoding="utf-8").strip():
        corpo, _ = md_para_html(prop_md.read_text(encoding="utf-8"))
        corpo_completo += corpo
        sub = f"Proposta para {titulo}. {hoje}"
        (saida / "proposta.doc").write_text(doc_word(titulo, org, sub, corpo), encoding="utf-8")
        p_html = saida / "proposta-impressao.html"
        p_html.write_text(html_impressao(titulo, corpo, org, sub), encoding="utf-8")
        gerados += ["proposta.doc", "proposta-impressao.html"]
        if not args.sem_pdf and gerar_pdf(p_html.resolve(), (saida / "proposta.pdf").resolve()):
            gerados.append("proposta.pdf")
    else:
        print("Aviso: proposta.md ausente ou vazia. Rode /projeto-escrever antes para incluir a proposta.")

    # Orçamento
    orc_md = pasta / "orcamento.md"
    if orc_md.exists() and orc_md.read_text(encoding="utf-8").strip():
        corpo, tabelas = md_para_html(orc_md.read_text(encoding="utf-8"))
        corpo_completo += "<h1>Orçamento</h1>" + corpo
        (saida / "orcamento.xls").write_text(planilha_xls("Orçamento. " + titulo, tabelas), encoding="utf-8")
        (saida / "orcamento.csv").write_text(csv_de_tabelas(tabelas), encoding="utf-8-sig")
        o_html = saida / "orcamento-impressao.html"
        o_html.write_text(html_impressao("Orçamento. " + titulo, corpo), encoding="utf-8")
        gerados += ["orcamento.xls", "orcamento.csv", "orcamento-impressao.html"]
        if not args.sem_pdf and gerar_pdf(o_html.resolve(), (saida / "orcamento.pdf").resolve()):
            gerados.append("orcamento.pdf")
    else:
        print("Aviso: orcamento.md ausente ou vazio. Rode /projeto-orcamento antes para incluir o orçamento.")

    # Projeto completo (proposta + orçamento + parecer + nota)
    extras = ""
    for arq, tit in [("elegibilidade.md", "Parecer de Elegibilidade"), ("score.md", "Avaliação CaptaScore")]:
        f = pasta / arq
        if f.exists() and f.read_text(encoding="utf-8").strip():
            c, _ = md_para_html(f.read_text(encoding="utf-8"))
            extras += f"<hr><h1>{tit}</h1>" + c
    if corpo_completo:
        completo = html_impressao(titulo, corpo_completo + extras, org, f"Documento completo. {hoje}")
        c_html = saida / "projeto-completo.html"
        c_html.write_text(completo, encoding="utf-8")
        gerados.append("projeto-completo.html")
        if not args.sem_pdf and gerar_pdf(c_html.resolve(), (saida / "projeto-completo.pdf").resolve()):
            gerados.append("projeto-completo.pdf")

    if not gerados:
        sys.exit("Nada para exportar. O projeto precisa de proposta.md e/ou orcamento.md.")

    print(f"\nEntrega final gerada em: {saida}\n")
    for g in gerados:
        print("  -", g)
    if not any(g.endswith(".pdf") for g in gerados):
        print("\nPDF não gerado automaticamente. Abra o arquivo -impressao.html no navegador e use "
              "Imprimir, depois Salvar como PDF.")


if __name__ == "__main__":
    main()
