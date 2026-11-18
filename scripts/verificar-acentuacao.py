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
    "submissao": "submissão", "convenio": "convênio",
    "orcamento": "orçamento", "contemplacao": "contemplação",
    "introducao": "introdução", "conclusao": "conclusão", "acao": "ação",
    "funcao": "função", "solucao": "solução", "opcao": "opção", "decisao": "decisão",
    "sessao": "sessão", "inicio": "início", "indice": "índice", "video": "vídeo",
    "memoria": "memória", "sabado": "sábado", "automatico": "automático",
}
# Nota: "recurso" e "rubrica" NÃO entram aqui. As duas se escrevem sem acento em
# português, então sinalizá-las era ruído puro (a ferramenta sugeria a mesma
# palavra como correção dela mesma).

# Palavras ambíguas: a forma sem acento também existe e costuma estar certa.
# Aqui a ferramenta avisa para conferir, nunca afirma que há erro.
#   esta (pronome: "esta proposta")      x  está (verbo)
#   publico (verbo: "eu publico")        x  público
#   pratica (verbo: "ela pratica")       x  prática
#   analise (verbo: "que ele analise")   x  análise
#   duvida (verbo: "ele duvida")         x  dúvida
#   inicio (verbo: "eu inicio")          x  início
AMBIGUAS = {"esta", "publico", "pratica", "analise", "duvida", "inicio"}


EXTENSOES_ARQUIVO = "md|py|json|html|htm|txt|csv|xls|xlsx|doc|docx|pdf|js|css|yml|yaml|png|jpg"


def limpar(texto):
    """Remove blocos de código, inline code, URLs, nomes de arquivo, caminhos e
    chaves JSON. São as fontes de ruído: o CLAUDE.md isenta explicitamente nome de
    arquivo, slug e identificador interno da regra de acentuação."""
    texto = re.sub(r"```.*?```", " ", texto, flags=re.DOTALL)
    texto = re.sub(r"`[^`]*`", " ", texto)
    texto = re.sub(r"https?://\S+", " ", texto)
    # nomes de arquivo (orcamento.md, exportar-projeto.py, score.md...)
    texto = re.sub(r"[\w.-]+\.(?:%s)\b" % EXTENSOES_ARQUIVO, " ", texto, flags=re.I)
    # caminhos de pasta (minhas-oscs/.../projetos/, .claude/agents/...)
    texto = re.sub(r"[\w./{}-]*/[\w./{}-]+", " ", texto)
    # comandos de barra (/projeto-orcamento, /projeto-avaliar)
    texto = re.sub(r"/[a-z][a-z-]+", " ", texto)
    texto = re.sub(r'"[a-zA-Z_][a-zA-Z0-9_]*"\s*:', " ", texto)  # chaves JSON
    return texto


def main():
    if len(sys.argv) < 2:
        sys.exit("Uso: python3 scripts/verificar-acentuacao.py <arquivo>")
    caminho = Path(sys.argv[1])
    if not caminho.exists():
        sys.exit(f"Arquivo não encontrado: {caminho}")

    linhas = caminho.read_text(encoding="utf-8", errors="ignore").splitlines()
    erros = []      # forma sem acento não existe em português: corrigir
    conferir = []   # a forma sem acento também existe: só o autor decide
    for n, linha in enumerate(linhas, 1):
        limpa = limpar(linha)
        for token in re.findall(r"[A-Za-zÀ-ÿ]+", limpa):
            base = token.lower()
            if base in SUSPEITAS:
                (conferir if base in AMBIGUAS else erros).append(
                    (n, token, SUSPEITAS[base])
                )

    if not erros and not conferir:
        print(f"OK. Nenhuma palavra suspeita de falta de acento em {caminho.name}.")
        return

    if erros:
        print(f"CORRIGIR em {caminho.name}: {len(erros)} palavra(s) sem acento.\n")
        for n, encontrado, esperado in erros:
            print(f"  linha {n}: '{encontrado}' -> '{esperado}'")
        print()

    if conferir:
        print(f"CONFERIR (a forma sem acento também existe; só corrija se for o caso): "
              f"{len(conferir)}\n")
        for n, encontrado, esperado in conferir:
            print(f"  linha {n}: '{encontrado}' pode ser '{esperado}'")
        print("\n  Exemplo: \"esta proposta\" está certo (pronome). "
              "\"esta pronto\" está errado (verbo, vira \"está\").")


if __name__ == "__main__":
    main()
