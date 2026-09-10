#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Minerador de editais da AMC IA.

Lê a base local de editais (cache do CaptaHub), descarta os vencidos e ranqueia
os candidatos por aderência ao perfil da OSC, combinando tema (palavras-chave e
categoria oficial), território (UF) e prazo. O ranking é determinístico, então a
mesma entrada sempre devolve a mesma ordem.

Uso:
  python3 scripts/minerar-editais.py [--escopo Municipal|Estadual|Nacional|Internacional]
                                     [--area "palavra1,palavra2"]
                                     [--categorias "Assistência Social,Saúde"]
                                     [--uf AM]
                                     [--valor-min N] [--valor-max N]
                                     [--prazo-min-dias N] [--top N]
                                     [--incluir-continuos]

--uf prioriza os editais do território da OSC (a própria UF) e os de alcance
nacional ou internacional, e rebaixa os municipais/estaduais de outras UFs (a OSC
não é elegível por território). --categorias casa com a categoria oficial do
edital (campo novo do CaptaHub). Sem filtros, retorna os abertos por prazo.
"""

import argparse
import json
import sys
from datetime import date, datetime
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
BASE_COMPLETA = RAIZ / "base-editais" / "editais-abertos.json"
BASE_INDICE = RAIZ / "base-editais" / "editais-index.json"


def carregar_editais():
    """Carrega a base completa (com descrição) e cai para o índice se faltar."""
    caminho = BASE_COMPLETA if BASE_COMPLETA.exists() else BASE_INDICE
    if not caminho.exists():
        sys.exit("Base de editais não encontrada em base-editais/. Rode /configurar.")
    dados = json.loads(caminho.read_text(encoding="utf-8-sig"))
    if isinstance(dados, dict) and "editais" in dados:
        return dados["editais"]
    if isinstance(dados, list):
        return dados
    sys.exit("Formato inesperado da base de editais.")


def parse_data(valor):
    if not valor:
        return None
    valor = str(valor)[:10]
    for fmt in ("%Y-%m-%d", "%d/%m/%Y"):
        try:
            return datetime.strptime(valor, fmt).date()
        except ValueError:
            continue
    return None


def formatar_valor(e):
    """value vem null quando desconhecido. Usa value_brl e currency quando houver."""
    val = e.get("value")
    vbrl = e.get("value_brl")
    cur = str(e.get("currency") or "BRL").upper()
    if val is None and vbrl is None:
        return "não informado"
    if cur != "BRL" and val is not None:
        s = f"{cur} {val:,.0f}".replace(",", ".")
        if vbrl:
            s += " (R$ {:,.2f})".format(vbrl).replace(",", "X").replace(".", ",").replace("X", ".")
        return s
    v = vbrl if val is None else val
    return "R$ {:,.2f}".format(v).replace(",", "X").replace(".", ",").replace("X", ".")


def texto_busca(e):
    partes = [e.get("title", ""), e.get("description", ""), e.get("institution", ""),
              e.get("category", ""), e.get("uf", ""), e.get("municipio", "")]
    tags = e.get("tags") or []
    if isinstance(tags, list):
        partes.extend(tags)
    return " ".join(str(p) for p in partes).lower()


def pontuar(e, palavras, categorias, uf_osc):
    """Score determinístico: tema (palavra + categoria) e território (UF)."""
    texto = texto_busca(e)
    cat = str(e.get("category") or "")
    cat_low = cat.lower()
    score = 0
    hits = []

    # Tema por palavras-chave (cada palavra distinta soma, com teto)
    kw = sum(1 for p in palavras if p and p in texto)
    if kw:
        score += min(kw, 5)
        hits.append(f"tema:{kw}")

    # Tema por categoria oficial do edital
    tem_categoria = False
    if categorias and cat_low in [c.lower() for c in categorias]:
        score += 3
        tem_categoria = True
        hits.append(f"cat:{cat}")
    elif palavras and cat_low and any(p in cat_low for p in palavras):
        score += 2
        tem_categoria = True
        hits.append(f"cat~:{cat}")

    # Território por UF
    uf_e = str(e.get("uf") or "").upper()
    scope = str(e.get("scope") or "")
    eleg_territorio = True
    if uf_osc:
        uf_osc = uf_osc.upper()
        if uf_e == uf_osc:
            score += 4
            hits.append("UF-local")
        elif scope in ("Nacional", "Internacional"):
            score += 1
            hits.append("alcance")
        elif scope in ("Municipal", "Estadual") and uf_e and uf_e != uf_osc:
            score -= 6
            eleg_territorio = False
            hits.append("fora-territorio")

    relevante_tema = bool(kw) or tem_categoria
    return score, relevante_tema, eleg_territorio, hits


def main():
    p = argparse.ArgumentParser(description="Minerador de editais da AMC IA")
    p.add_argument("--escopo", default=None, help="Municipal, Estadual, Nacional ou Internacional")
    p.add_argument("--area", default=None, help="palavras-chave separadas por vírgula")
    p.add_argument("--categorias", default=None, help="categorias oficiais separadas por vírgula")
    p.add_argument("--uf", default=None, help="UF da OSC, para priorizar o território (ex: AM)")
    p.add_argument("--valor-min", type=float, default=None)
    p.add_argument("--valor-max", type=float, default=None)
    p.add_argument("--prazo-min-dias", type=int, default=0,
                   help="exigir ao menos N dias até o prazo de submissão")
    p.add_argument("--top", type=int, default=15)
    p.add_argument("--incluir-continuos", action="store_true",
                   help="incluir editais de fluxo contínuo (sem prazo fixo)")
    args = p.parse_args()

    hoje = date.today()
    editais = carregar_editais()
    palavras = [s.strip().lower() for s in args.area.split(",")] if args.area else []
    categorias = [s.strip() for s in args.categorias.split(",")] if args.categorias else []
    tem_tema = bool(palavras or categorias)

    candidatos = []
    descartados_vencidos = 0

    for e in editais:
        prazo = parse_data(e.get("deadline"))
        continuo = bool(e.get("is_continuous"))

        # Regra de ouro: prazo vencido descarta (exceto contínuos)
        if not continuo and prazo is not None:
            dias = (prazo - hoje).days
            if dias < 0:
                descartados_vencidos += 1
                continue
            if dias < args.prazo_min_dias:
                continue

        # Escopo
        if args.escopo and str(e.get("scope", "")).lower() != args.escopo.lower():
            continue

        # Faixa de valor (usa value_brl quando houver; null/0 conta como não informado)
        valor = e.get("value_brl") or e.get("value") or 0
        if args.valor_min is not None and valor and valor < args.valor_min:
            continue
        if args.valor_max is not None and valor and valor > args.valor_max:
            continue

        score, relevante_tema, eleg_territorio, hits = pontuar(e, palavras, categorias, args.uf)

        # Se há tema definido, exige aderência temática (palavra-chave ou categoria)
        if tem_tema and not relevante_tema:
            continue

        candidatos.append((score, eleg_territorio, hits, e))

    # Ordena por score desc, depois prazo mais próximo (None por último)
    def chave_ordem(c):
        prazo = parse_data(c[3].get("deadline"))
        return (-c[0], prazo is None, prazo or date.max)

    candidatos.sort(key=chave_ordem)
    selecionados = candidatos[: args.top]

    print(f"Editais na base: {len(editais)} | vencidos descartados: {descartados_vencidos} "
          f"| candidatos: {len(candidatos)} | exibindo: {len(selecionados)}\n")

    for i, (score, eleg, hits, e) in enumerate(selecionados, 1):
        prazo = e.get("deadline") or ("fluxo contínuo" if e.get("is_continuous") else "sem data")
        territorio = "" if eleg else "  ⚠ fora do território da OSC"
        print(f"{i}. {e.get('title', 'sem título')}")
        print(f"   Órgão: {e.get('institution', '-')} | Escopo: {e.get('scope', '-')} | "
              f"UF: {e.get('uf') or '-'} | Categoria: {e.get('category') or '-'}")
        print(f"   Valor: {formatar_valor(e)} | Prazo: {prazo} | Aderência (score): {score}{territorio}")
        print(f"   ID: {e.get('id')} | Link: {e.get('url') or '-'}")
        print()

    # Bloco machine-readable para o agente. Inclui o score e o sinal de território.
    saida = []
    for score, eleg, hits, e in selecionados:
        item = dict(e)
        item["_score"] = score
        item["_eleg_territorio"] = eleg
        item["_hits"] = hits
        saida.append(item)
    print("=== JSON_CANDIDATOS ===")
    print(json.dumps(saida, ensure_ascii=False))


if __name__ == "__main__":
    main()
