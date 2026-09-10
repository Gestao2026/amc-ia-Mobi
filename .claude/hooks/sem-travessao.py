#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Hook PreToolUse da AMC IA. Bloqueia travessão (—) em textos gerados.

Regra do projeto: nada de travessão em proposta, parecer, orçamento, score ou
qualquer entregável. Use vírgula, ponto, dois pontos ou parênteses.

Lê o payload do Claude Code em stdin. Se o conteúdo a ser escrito num arquivo
de texto da pasta minhas-oscs/ contiver travessão, sai com código 2 (bloqueia)
e devolve a orientação no stderr.
"""

import json
import sys

TRAVESSAO = "—"  # —
EXTENSOES = (".md", ".html", ".txt")


def main():
    try:
        payload = json.load(sys.stdin)
    except Exception:
        sys.exit(0)  # sem payload válido, não interfere

    tool = payload.get("tool_name", "")
    entrada = payload.get("tool_input", {}) or {}
    caminho = entrada.get("file_path", "") or ""

    # Só vigia entregáveis: projetos das OSCs (Fase 1) e materiais do captador (Fase 2)
    caminho_norm = caminho.replace("\\", "/")
    if "minhas-oscs" not in caminho_norm and "captador/entregas" not in caminho_norm:
        sys.exit(0)
    if not caminho.endswith(EXTENSOES):
        sys.exit(0)

    if tool == "Write":
        conteudo = entrada.get("content", "") or ""
    elif tool in ("Edit", "MultiEdit"):
        conteudo = entrada.get("new_string", "") or ""
    else:
        sys.exit(0)

    if TRAVESSAO in conteudo:
        sys.stderr.write(
            "Travessao (—) encontrado no texto. Regra da AMC IA: substitua "
            "por virgula, ponto, dois pontos ou parenteses antes de salvar."
        )
        sys.exit(2)  # bloqueia a escrita

    sys.exit(0)


if __name__ == "__main__":
    main()
