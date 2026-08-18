#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Verificador de acentuação pt_BR da AMC IA.

Varre um arquivo de texto (.md, .html, .txt, .json) e sinaliza palavras que
quase sempre devem aparecer acentuadas em português, mas foram encontradas sem
acento. É um alerta heurístico: pode haver falso positivo (ex: o verbo "publica"
contra o adjetivo "pública"). Use como apoio, não como verdade absoluta.

Uso:
  python3 scripts/verificar-acentuacao.py <arquivo>
"""

import re
import sys
from pathlib import Path

# Palavra sem acento -> forma acentuada esperada (contexto mais comum)
SUSPEITAS = {
    "nao": "não", "sao": "são", "voce": "você", "esta": "está", "ja": "já",
    "tambem": "também", "tres": "três", "publico": "público", "logico": "lógico",
    "estrategia": "estratégia", "duvida": "dúvida", "metodo": "método",
    "pratica": "prática", "analise": "análise", "especifico": "específico",
    "basico": "básico", "unico": "único", "numero": "número", "codigo": "código",
    "pagina": "página", "area": "área", "historia": "história", "tecnica": "técnica",
    "proximo": "próximo", "ultimo": "último", "critico": "crítico", "facil": "fácil",
    "dificil": "difícil", "possivel": "possível", "impossivel": "impossível",
    "orgao": "órgão", "criterio": "critério", "elegivel": "elegível",
    "execucao": "execução", "prestacao": "prestação", "avaliacao": "avaliação",
    "submissao": "submissão", "orcamento": "orçamento", "rubrica": "rubrica",
    "convenio": "convênio", "contemplacao": "contemplação", "recurso": "recurso",
    "introducao": "introdução", "conclusao": "conclusão", "acao": "ação",
    "funcao": "função", "solucao": "solução", "opcao": "opção", "decisao": "decisão",
    "sessao": "sessão", "inicio": "início", "indice": "índice", "video": "vídeo",
    "memoria": "memória", "sabado": "sábado", "automatico": "automático",
}

# Palavras ambíguas (verbo x substantivo/adjetivo): só avisar, não afirmar
AMBIGUAS = {"publico", "pratica", "criterio", "recurso", "rubrica"}


def limpar(texto):
    """Remove blocos de código, inline code, URLs e chaves JSON para reduzir ruído."""
    texto = re.sub(r"```.*?```", " ", texto, flags=re.DOTALL)
    texto = re.sub(r"`[^`]*`", " ", texto)
    texto = re.sub(r"https?://\S+", " ", texto)
    texto = re.sub(r'"[a-zA-Z_][a-zA-Z0-9_]*"\s*:', " ", texto)  # chaves JSON
    return texto


def main():
    if len(sys.argv) < 2:
        sys.exit("Uso: python3 scripts/verificar-acentuacao.py <arquivo>")
    caminho = Path(sys.argv[1])
    if not caminho.exists():
        sys.exit(f"Arquivo não encontrado: {caminho}")

    linhas = caminho.read_text(encoding="utf-8", errors="ignore").splitlines()
    achados = []
    for n, linha in enumerate(linhas, 1):
        limpa = limpar(linha)
        for token in re.findall(r"[A-Za-zÀ-ÿ]+", limpa):
            base = token.lower()
            if base in SUSPEITAS:
                marca = " (ambígua, confira o contexto)" if base in AMBIGUAS else ""
                achados.append((n, token, SUSPEITAS[base], marca))

    if not achados:
        print(f"OK. Nenhuma palavra suspeita de falta de acento em {caminho.name}.")
        return

    print(f"Palavras suspeitas em {caminho.name}: {len(achados)}\n")
    for n, encontrado, esperado, marca in achados:
        print(f"  linha {n}: '{encontrado}' -> talvez '{esperado}'{marca}")


if __name__ == "__main__":
    main()
