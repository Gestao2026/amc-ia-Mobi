#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Hook PostToolUse da AMC IA. Alimenta a Sala dos Agentes.

A cada ação do sistema, descobre qual agente da captação está trabalhando e
grava no formato que a sala (sala-dos-agentes.html) consome:

    window.AGENTS_STATUS = { _meta: {...}, categories: { <id>: {...} } };

Os ids de sala (prod, copy, pag, ad, vid, sales, data) são os mesmos do
escritório, remapeados para os papéis da captação. Nunca bloqueia. Sai sempre 0.
"""

import json
import re
import sys
import time
from datetime import datetime
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent.parent
SAIDA = RAIZ / ".claude" / "agents-memory" / "agents-status.js"

# Cada agente da captação mora numa "sala" do escritório (id do boneco):
#   data = MINERADOR | pag = CAPTADOC | copy = CAPTABUILDER
#   sales = CAPTABUDGET | vid = CAPTASCORE | ad = POSICIONADOR | prod = ORQUESTRADOR
# Mapas: (regex) -> (id_sala, comando, atividade)
REGRAS_ARQUIVO = [
    (r"elegibilidade\.md",          ("pag",   "projeto-elegibilidade", "Checando elegibilidade da OSC")),
    (r"proposta\.md",               ("copy",  "projeto-escrever",      "Escrevendo a proposta")),
    (r"orcamento\.md",              ("sales", "projeto-orcamento",     "Montando o orçamento técnico")),
    (r"score\.md",                  ("vid",   "projeto-avaliar",       "Avaliando a chance de aprovação")),
    (r"prestacao-contas",           ("copy",  "projeto-prestacao-contas", "Apoiando a prestação de contas")),
    (r"projetos/.+/edital\.md",     ("data",  "edital-analisar",       "Analisando o edital")),
    (r"perfil-osc\.md",             ("prod",  "osc-nova",              "Cadastrando a OSC")),
    (r"estado\.md",                 ("prod",  "projeto",               "Atualizando o projeto")),
    (r"captador/perfil",            ("ad",    "captador-perfil",       "Posicionando o captador")),
    (r"captador/oferta",            ("ad",    "assessoria-estruturar", "Estruturando a oferta")),
    (r"captador/entregas/conteudo", ("ad",    "captador-conteudo",     "Criando conteúdo de autoridade")),
    (r"captador/entregas/pagina",   ("ad",    "captador-pagina",       "Montando a página da assessoria")),
    (r"captador/entregas/anuncios", ("ad",    "captador-anuncio",      "Gerando anúncios para atrair OSCs")),
    (r"captador/entregas/comercial",("ad",    "assessoria-pitch",      "Escrevendo a proposta comercial")),
]
REGRAS_COMANDO = [
    (r"captahub-editais\.py",       ("data",  "edital-minerar",   "Puxando editais do CaptaHub")),
    (r"minerar-editais\.py",        ("data",  "edital-minerar",   "Minerando editais alinhados à OSC")),
    (r"verificar-acentuacao\.py",   ("copy",  "projeto-revisar",  "Revisando o português")),
    (r"exportar-projeto\.py",       ("prod",  "projeto-exportar", "Gerando a entrega final em Word e PDF")),
]
REGRAS_AGENTE = {
    "captador-doc":          ("pag",   "projeto-elegibilidade", "Checando elegibilidade da OSC"),
    "captador-builder":      ("copy",  "projeto-escrever",      "Escrevendo a proposta"),
    "captador-budget":       ("sales", "projeto-orcamento",     "Montando o orçamento técnico"),
    "captador-score":        ("vid",   "projeto-avaliar",       "Avaliando a chance de aprovação"),
    "minerador-editais":     ("data",  "edital-minerar",        "Minerando editais"),
    "revisor-proposta":      ("copy",  "projeto-revisar",       "Revisando o projeto"),
    "orquestrador-captacao": ("prod",  "pipeline",              "Conduzindo o fluxo"),
    "posicionador-captador": ("ad",    "captador-conteudo",     "Posicionando o captador"),
}


def osc_ativa():
    try:
        s = (RAIZ / "minhas-oscs" / ".ativa").read_text(encoding="utf-8").strip()
        return s or None
    except Exception:
        return None


def detectar(payload):
    tool = payload.get("tool_name", "") or ""
    entrada = payload.get("tool_input", {}) or {}

    if tool in ("Task", "Agent"):
        alvo = (str(entrada.get("subagent_type", "")) + " " +
                str(entrada.get("description", "")) + " " +
                str(entrada.get("prompt", ""))).lower()
        for chave, info in REGRAS_AGENTE.items():
            if chave in alvo:
                return info

    caminho = str(entrada.get("file_path", "")).replace("\\", "/")
    if caminho:
        for padrao, info in REGRAS_ARQUIVO:
            if re.search(padrao, caminho):
                return info

    comando = str(entrada.get("command", ""))
    if comando:
        for padrao, info in REGRAS_COMANDO:
            if re.search(padrao, comando):
                return info
    return None


def ler_estado_atual():
    """Lê o agents-status.js anterior para preservar categorias recentes."""
    try:
        txt = SAIDA.read_text(encoding="utf-8")
        m = re.search(r"window\.AGENTS_STATUS\s*=\s*(\{.*\})\s*;", txt, re.DOTALL)
        if m:
            return json.loads(m.group(1))
    except Exception:
        pass
    return {"_meta": {}, "categories": {}}


def main():
    try:
        payload = json.load(sys.stdin)
    except Exception:
        sys.exit(0)

    info = detectar(payload)
    if not info:
        sys.exit(0)

    id_sala, comando, atividade = info
    agora_ms = int(time.time() * 1000)
    hora = datetime.now().strftime("%H:%M")

    estado = ler_estado_atual()
    estado.setdefault("categories", {})
    estado["categories"][id_sala] = {
        "lastTool": payload.get("tool_name", ""),
        "lastSkill": comando,
        "lastTask": atividade,
        "timestamp": agora_ms,
    }
    estado["_meta"] = {
        "timestamp": agora_ms,
        "updated": hora,
        "lastSkill": comando,
        "activeProductName": osc_ativa() or "",
    }

    try:
        SAIDA.parent.mkdir(parents=True, exist_ok=True)
        SAIDA.write_text(
            "window.AGENTS_STATUS = " + json.dumps(estado, ensure_ascii=False) + ";\n",
            encoding="utf-8",
        )
    except Exception:
        pass

    sys.exit(0)


if __name__ == "__main__":
    main()
