#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Conferência de português da AMC IA, para rodar sob pedido.

Junta duas checagens num relatório só:
  1. Acentuação: usa a lista e a limpeza de scripts/verificar-acentuacao.py,
     para que exista uma única lista de palavras no projeto.
  2. Travessão (—) e meia-risca usada como travessão ( – ).

Lê .md, .html, .htm, .txt e .docx. Não altera o arquivo: só aponta.
A pontuação (vírgula e ponto final) não é conferida aqui, porque regra
automática erra demais; ela fica para a releitura da skill.

Uso:
  python .claude/skills/revisar-portugues/scripts/revisar.py <arquivo> [<arquivo> ...]
"""

import importlib.util
import re
import sys
import zipfile
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[4]
VERIFICADOR = RAIZ / "scripts" / "verificar-acentuacao.py"

spec = importlib.util.spec_from_file_location("verificar_acentuacao", VERIFICADOR)
va = importlib.util.module_from_spec(spec)
spec.loader.exec_module(va)

TRAVESSAO = "—"
MEIA_RISCA_SOLTA = re.compile(r"\s–\s")


def ler_linhas(caminho):
    if caminho.suffix.lower() == ".docx":
        with zipfile.ZipFile(caminho) as z:
            xml = z.read("word/document.xml").decode("utf-8", errors="ignore")
        paragrafos = re.findall(r"<w:p[ >].*?</w:p>", xml, flags=re.DOTALL)
        linhas = []
        for p in paragrafos:
            texto = "".join(re.findall(r"<w:t[^>]*>(.*?)</w:t>", p, flags=re.DOTALL))
            linhas.append(texto)
        return linhas, "parágrafo"
    texto = caminho.read_text(encoding="utf-8", errors="ignore")
    if caminho.suffix.lower() in (".html", ".htm"):
        texto = re.sub(r"<(script|style)\b.*?</\1>", " ", texto, flags=re.DOTALL | re.I)
        texto = re.sub(r"<[^>]+>", " ", texto)
    return texto.splitlines(), "linha"


def revisar(caminho):
    linhas, unidade = ler_linhas(caminho)
    erros, conferir, travessoes = [], [], []
    for n, linha in enumerate(linhas, 1):
        for token in re.findall(r"[A-Za-zÀ-ÿ]+", va.limpar(linha)):
            base = token.lower()
            if base in va.SUSPEITAS:
                (conferir if base in va.AMBIGUAS else erros).append(
                    (n, token, va.SUSPEITAS[base]))
        if TRAVESSAO in linha or MEIA_RISCA_SOLTA.search(linha):
            trecho = linha.strip()
            travessoes.append((n, trecho[:90] + ("..." if len(trecho) > 90 else "")))

    print(f"=== {caminho.name} ({len(linhas)} {unidade}s)")
    if not (erros or conferir or travessoes):
        print("OK. Nada a apontar em acento nem travessão.\n")
        return 0
    if erros:
        print(f"\nCORRIGIR, sem acento: {len(erros)}")
        for n, achado, certo in erros:
            print(f"  {unidade} {n}: '{achado}' -> '{certo}'")
    if conferir:
        print(f"\nCONFERIR, a forma sem acento também existe: {len(conferir)}")
        for n, achado, certo in conferir:
            print(f"  {unidade} {n}: '{achado}' pode ser '{certo}'")
    if travessoes:
        print(f"\nTRAVESSÃO: {len(travessoes)}")
        for n, trecho in travessoes:
            print(f"  {unidade} {n}: {trecho}")
    print()
    return len(erros) + len(travessoes)


def main():
    if len(sys.argv) < 2:
        sys.exit("Uso: python .claude/skills/revisar-portugues/scripts/revisar.py <arquivo> [...]")
    for arg in sys.argv[1:]:
        caminho = Path(arg)
        if not caminho.exists():
            print(f"Arquivo não encontrado: {caminho}\n")
            continue
        revisar(caminho)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
