#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Hook PostToolUse da AMC IA. Vigia a acentuação dos entregáveis.

O CLAUDE.md trata a acentuação em pt_BR como regra de prioridade absoluta. Este
hook é o mecanismo que faz a regra valer: depois de cada escrita em um entregável
(projeto de OSC ou material do captador), roda o verificador e, se encontrar
palavra que em português NUNCA se escreve sem acento, devolve a lista para
correção imediata.

Só reage ao bloco CORRIGIR do verificador. O bloco CONFERIR (palavras como
"esta", em que a forma sem acento também existe) é decisão de quem escreve e
nunca interrompe o trabalho.

Nunca trava por conta própria: qualquer falha do hook sai com código 0.
"""

import json
import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent.parent
VERIFICADOR = RAIZ / "scripts" / "verificar-acentuacao.py"
EXTENSOES = (".md", ".html", ".txt")


def main():
    try:
        payload = json.load(sys.stdin)
    except Exception:
        sys.exit(0)

    if payload.get("tool_name", "") not in ("Write", "Edit", "MultiEdit"):
        sys.exit(0)

    caminho = (payload.get("tool_input", {}) or {}).get("file_path", "") or ""
    if not caminho.endswith(EXTENSOES):
        sys.exit(0)

    # Só vigia entregáveis: projetos das OSCs (Fase 1) e materiais do captador (Fase 2)
    norm = caminho.replace("\\", "/")
    if "minhas-oscs" not in norm and "captador/entregas" not in norm:
        sys.exit(0)

    arquivo = Path(caminho)
    if not arquivo.exists() or not VERIFICADOR.exists():
        sys.exit(0)

    try:
        r = subprocess.run(
            [sys.executable, str(VERIFICADOR), str(arquivo)],
            capture_output=True, text=True, encoding="utf-8", errors="replace",
            timeout=20,
        )
    except Exception:
        sys.exit(0)

    saida = r.stdout or ""
    if "CORRIGIR" not in saida:
        sys.exit(0)

    # Devolve só o bloco CORRIGIR, que é o que exige ação
    bloco = saida.split("CONFERIR")[0].strip()
    sys.stderr.write(
        "Acentuação (regra da AMC IA): palavras sem acento em "
        + arquivo.name + ". Corrija agora no arquivo.\n\n" + bloco
    )
    sys.exit(2)


if __name__ == "__main__":
    main()
