#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ponte com o CaptaHub. Puxa os editais ao vivo e atualiza o cache local.

O CaptaHub é a fonte da verdade dos editais. Este script baixa os editais e
atualiza o cache em base-editais/, que o /edital-minerar usa para filtrar pelo
perfil da OSC. Sem conexão, o sistema continua com o último cache baixado.

Dois caminhos de conexão (preferência para a API por token):
  1. API REST por token (recomendado): CAPTAHUB_API_URL + CAPTAHUB_API_TOKEN.
     Usa o conector captahub-api.py (mesma autenticação do resto do sistema).
  2. Banco direto (legado): SUPABASE_URL + SUPABASE_KEY (PostgREST).

Sem dependências externas, só a biblioteca padrão.

Uso:
  python3 scripts/captahub-editais.py            # baixa e atualiza o cache
  python3 scripts/captahub-editais.py --testar   # só testa a conexão
"""

import importlib.util
import json
import sys
import urllib.request
import urllib.error
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
BASE = RAIZ / "base-editais"
CAMPOS_INDICE = ["id", "title", "institution", "scope", "category",
                 "deadline", "is_continuous", "value", "url"]


def carregar_env():
    env = {}
    f = RAIZ / ".env"
    if f.exists():
        for linha in f.read_text(encoding="utf-8").splitlines():
            linha = linha.strip()
            if not linha or linha.startswith("#") or "=" not in linha:
                continue
            k, v = linha.split("=", 1)
            env[k.strip()] = v.strip().strip('"').strip("'")
    return env


def mascarar(valor):
    if not valor or len(valor) < 10:
        return "***"
    return valor[:8] + "..." + valor[-4:]


def carregar_cliente_api(env):
    """Carrega o conector captahub-api.py se o token da API estiver no .env."""
    url = env.get("CAPTAHUB_API_URL", "")
    token = env.get("CAPTAHUB_API_TOKEN", "")
    if not url or not token:
        return None
    caminho = Path(__file__).resolve().parent / "captahub-api.py"
    if not caminho.exists():
        return None
    spec = importlib.util.spec_from_file_location("captahub_api", caminho)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.CaptaHubClient(url, token)


def buscar_editais_legado(url, key, tabela):
    """Caminho antigo: leitura direta do banco via PostgREST."""
    endpoint = f"{url.rstrip('/')}/rest/v1/{tabela}?select=*&order=deadline.asc"
    req = urllib.request.Request(endpoint, headers={
        "apikey": key,
        "Authorization": f"Bearer {key}",
        "Accept": "application/json",
    })
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))


def ids_do_cache_atual():
    """Ids dos editais que já estão no cache, para detectar os novos.

    A identidade de um edital é o `id` (uuid do CaptaHub), nunca a URL nem o
    título: a mesma URL pode hospedar editais diferentes, e títulos se repetem.
    Por isso nada é deduplicado; só comparamos por id para sinalizar novidades.
    """
    f = BASE / "editais-index.json"
    if not f.exists():
        return None
    try:
        dados = json.loads(f.read_text(encoding="utf-8-sig"))
        itens = dados.get("editais", []) if isinstance(dados, dict) else dados
        return {e.get("id") for e in itens if e.get("id")}
    except Exception:
        return None


def escrever_cache(editais):
    BASE.mkdir(parents=True, exist_ok=True)
    (BASE / "editais-abertos.json").write_text(
        json.dumps(editais, ensure_ascii=False, indent=2), encoding="utf-8")
    indice = [{c: e.get(c) for c in CAMPOS_INDICE} for e in editais]
    (BASE / "editais-index.json").write_text(
        json.dumps({"total": len(indice), "campos": CAMPOS_INDICE, "editais": indice},
                   ensure_ascii=False, indent=2), encoding="utf-8")


def main():
    testar = "--testar" in sys.argv
    env = carregar_env()

    cli = carregar_cliente_api(env)
    editais = None
    fonte = None

    # Caminho 1: API por token (recomendado)
    if cli is not None:
        print(f"Conectando ao CaptaHub (API). {cli.base_url}  "
              f"token: {mascarar(env.get('CAPTAHUB_API_TOKEN', ''))}")
        try:
            # Puxa os editais abertos (descarta vencidos no servidor, mantém contínuos).
            editais = cli.iter_editais(only_open=True, page_size=200)
            fonte = "API"
        except Exception as e:
            print(f"Falha na API do CaptaHub: {e}")
            if not (env.get("SUPABASE_URL") and env.get("SUPABASE_KEY")):
                print("O sistema segue com o cache local de editais.")
                sys.exit(1)
            print("Tentando o caminho legado (banco direto).")

    # Caminho 2: banco direto (legado), se a API não estiver disponível
    if editais is None:
        url = env.get("SUPABASE_URL", "")
        key = env.get("SUPABASE_KEY", "")
        tabela = env.get("CAPTAHUB_EDITAIS_TABLE", "editais")
        if not url or not key:
            print("CaptaHub não conectado. Faltam CAPTAHUB_API_TOKEN (API) "
                  "ou SUPABASE_URL/SUPABASE_KEY (legado) no .env.")
            print("Rode /captahub-conectar para configurar. Por enquanto, o sistema "
                  "usa o cache local de editais.")
            sys.exit(2)
        print(f"Conectando ao CaptaHub (banco direto). {url}  chave: {mascarar(key)}  tabela: {tabela}")
        try:
            editais = buscar_editais_legado(url, key, tabela)
            fonte = "banco direto"
        except urllib.error.HTTPError as e:
            corpo = ""
            try:
                corpo = e.read().decode("utf-8")[:200]
            except Exception:
                pass
            print(f"Falha na conexão (HTTP {e.code}). {corpo}")
            print("Confira a tabela e as credenciais. O cache local continua válido.")
            sys.exit(1)
        except Exception as e:
            print(f"Não foi possível conectar ao CaptaHub: {e}")
            print("O sistema segue com o cache local de editais.")
            sys.exit(1)

    if not isinstance(editais, list):
        print("Resposta inesperada do CaptaHub. O cache local continua válido.")
        sys.exit(1)

    print(f"CaptaHub respondeu ({fonte}): {len(editais)} editais.")
    if testar:
        print("Conexão OK (modo teste, cache não alterado).")
        return

    # Detecta os novos por id (sem remover nada: a lista mantém todos).
    antigos = ids_do_cache_atual()
    novos = [e for e in editais if e.get("id") not in antigos] if antigos else []

    escrever_cache(editais)
    print(f"Cache atualizado em base-editais/ ({len(editais)} editais, nenhum removido).")
    if antigos is None:
        print("Primeira atualização do cache: não há base anterior para comparar.")
    elif novos:
        print(f"Editais novos desde a última atualização: {len(novos)}")
        for e in novos[:15]:
            print(f"  + {e.get('title', 'sem título')}  ({e.get('deadline') or 'sem data'})")
    else:
        print("Nenhum edital novo desde a última atualização.")
    print("Agora rode /edital-minerar para filtrar pelo perfil da OSC.")


if __name__ == "__main__":
    main()
