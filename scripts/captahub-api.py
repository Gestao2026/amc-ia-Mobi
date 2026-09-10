#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Cliente da API pública REST do CaptaHub.

O CaptaHub é a fonte da verdade: editais (globais, leitura), pipeline de projetos
e clientes (OSCs), ambos por usuário. Este módulo conversa com a API versionada
em /v1, autenticando com o token pessoal (Bearer). É o conector único da AMC
IA: injeta a base URL e o token, faz GET/POST/PATCH, trata paginação e normaliza
os erros no padrão da API.

Diferença para o captahub-editais.py: aquele lê o banco direto (PostgREST), é o
caminho legado de cache de editais. Este usa a API pública oficial e cobre também
pipeline e clientes.

Sem dependências externas, só a biblioteca padrão.

Credenciais ficam no .env (nunca em outro arquivo):
  CAPTAHUB_API_URL=https://<host>/functions/v1/api
  CAPTAHUB_API_TOKEN=cpth_...

Uso como ferramenta de linha de comando (o que os comandos e agentes chamam):
  python3 scripts/captahub-api.py testar
  python3 scripts/captahub-api.py editais --scope Nacional --only-open --limit 20
  python3 scripts/captahub-api.py edital --id <uuid>
  python3 scripts/captahub-api.py estagios
  python3 scripts/captahub-api.py projetos --status submetido
  python3 scripts/captahub-api.py projeto-criar --nome "..." --cliente-id <uuid> --edital-id <uuid>
  python3 scripts/captahub-api.py projeto-atualizar --id <uuid> --status elaborar_projeto --nota-tecnica 8.5
  python3 scripts/captahub-api.py clientes --uf PE
  python3 scripts/captahub-api.py cliente-criar --nome "OSC Teste" --uf PE
  python3 scripts/captahub-api.py cliente-atualizar --id <uuid> --site https://...

Uso como biblioteca (importável por outro script):
  from importlib import import_module
  # ou rode via subprocess; o cliente também pode ser instanciado:
  cli = CaptaHubClient.from_env()
  print(cli.me())
"""

import argparse
import json
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent

# Os 11 estágios canônicos do pipeline, na ordem (espelho do servidor).
ESTAGIOS_PIPELINE = [
    "selecionado", "encontrar_cliente", "checklist", "contrato",
    "separar_documentos", "elaborar_projeto", "submetido", "aprovado",
    "reprovado", "pagamento_pendente", "pagamento_recebido",
]

LIMITE_MAX = 200
LIMITE_PADRAO = 50


def carregar_env():
    """Lê o .env linha a linha (mesmo padrão dos outros scripts do projeto)."""
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
    """Mascara um segredo para exibição (nunca mostra o token inteiro)."""
    if not valor:
        return "***"
    if len(valor) < 12:
        return "***"
    return valor[:8] + "..." + valor[-4:]


class CaptaHubAPIError(Exception):
    """Erro normalizado da API. Carrega status HTTP, code e mensagem da API."""

    # Mapa de status para explicação amigável em português.
    EXPLICACAO = {
        400: "requisição malformada",
        401: "token inválido ou ausente",
        403: "token sem o escopo necessário para esta ação",
        404: "não encontrado (ou não pertence ao dono do token)",
        422: "dados inválidos (falha de validação)",
        429: "limite de chamadas excedido (tente de novo em instantes)",
        500: "erro interno do CaptaHub",
    }

    def __init__(self, status, code, message, payload=None):
        self.status = status
        self.code = code or "erro"
        self.message = message or "sem mensagem"
        self.payload = payload
        explicacao = self.EXPLICACAO.get(status, "erro de comunicação")
        super().__init__(f"HTTP {status} ({explicacao}). {self.code}: {self.message}")


class CaptaHubClient:
    """Conector único do CaptaHub. Injeta base URL + Bearer, normaliza erro e paginação."""

    def __init__(self, base_url, token, timeout=30):
        if not base_url:
            raise ValueError("CAPTAHUB_API_URL ausente.")
        if not token:
            raise ValueError("CAPTAHUB_API_TOKEN ausente.")
        self.base_url = base_url.rstrip("/")
        self.token = token
        self.timeout = timeout

    @classmethod
    def from_env(cls, timeout=30):
        env = carregar_env()
        url = env.get("CAPTAHUB_API_URL", "")
        token = env.get("CAPTAHUB_API_TOKEN", "")
        if not url or not token:
            raise ValueError(
                "CaptaHub (API) não conectado. Faltam CAPTAHUB_API_URL e/ou "
                "CAPTAHUB_API_TOKEN no .env. Rode /captahub-conectar."
            )
        return cls(url, token, timeout=timeout)

    # ----- camada de transporte -----

    def _request(self, method, path, params=None, body=None):
        url = self.base_url + path
        if params:
            limpos = {}
            for k, v in params.items():
                if v is None:
                    continue
                if isinstance(v, bool):
                    v = "true" if v else "false"
                limpos[k] = v
            if limpos:
                url += "?" + urllib.parse.urlencode(limpos)

        dados = None
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Accept": "application/json",
        }
        if body is not None:
            dados = json.dumps(body, ensure_ascii=False).encode("utf-8")
            headers["Content-Type"] = "application/json"

        req = urllib.request.Request(url, data=dados, method=method, headers=headers)
        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                bruto = resp.read().decode("utf-8")
                return json.loads(bruto) if bruto else {}
        except urllib.error.HTTPError as e:
            corpo = ""
            try:
                corpo = e.read().decode("utf-8")
            except Exception:
                pass
            code, message, payload = None, None, None
            if corpo:
                try:
                    payload = json.loads(corpo)
                    erro = payload.get("error", {}) if isinstance(payload, dict) else {}
                    code = erro.get("code")
                    message = erro.get("message")
                except Exception:
                    message = corpo[:300]
            raise CaptaHubAPIError(e.code, code, message, payload) from None
        except urllib.error.URLError as e:
            raise CaptaHubAPIError(0, "conexao", f"Não foi possível alcançar o CaptaHub: {e.reason}") from None

    def get(self, path, params=None):
        return self._request("GET", path, params=params)

    def post(self, path, body):
        return self._request("POST", path, body=body)

    def patch(self, path, body):
        return self._request("PATCH", path, body=body)

    def paginar(self, path, params=None, page_size=LIMITE_PADRAO, maximo=None):
        """Percorre todas as páginas de uma lista. Retorna a lista completa de itens.

        A API responde { data:[...], total, limit, offset, has_next }.
        """
        params = dict(params or {})
        page_size = min(page_size, LIMITE_MAX)
        offset = int(params.get("offset", 0) or 0)
        itens = []
        while True:
            params["limit"] = page_size
            params["offset"] = offset
            resp = self.get(path, params=params)
            lote = resp.get("data", []) if isinstance(resp, dict) else (resp or [])
            itens.extend(lote)
            if maximo is not None and len(itens) >= maximo:
                return itens[:maximo]
            tem_proxima = bool(resp.get("has_next")) if isinstance(resp, dict) else False
            if not tem_proxima or not lote:
                return itens
            offset += page_size

    # ----- meta -----

    def me(self):
        return self.get("/v1/me")

    # ----- editais (globais, leitura) -----

    def listar_editais(self, **filtros):
        """Filtros aceitos: scope, category, q, value_min, value_max,
        deadline_after, deadline_before, is_continuous, only_open, limit, offset."""
        return self.get("/v1/editais", params=filtros)

    def iter_editais(self, page_size=LIMITE_PADRAO, maximo=None, **filtros):
        return self.paginar("/v1/editais", params=filtros, page_size=page_size, maximo=maximo)

    def obter_edital(self, edital_id):
        return self.get(f"/v1/editais/{edital_id}")

    # ----- pipeline (por usuário) -----

    def estagios(self):
        return self.get("/v1/pipeline/estagios")

    def listar_projetos(self, **filtros):
        """Filtros: status, cliente_id, edital_id, limit, offset."""
        return self.get("/v1/projetos", params=filtros)

    def iter_projetos(self, page_size=LIMITE_PADRAO, maximo=None, **filtros):
        return self.paginar("/v1/projetos", params=filtros, page_size=page_size, maximo=maximo)

    def obter_projeto(self, projeto_id):
        return self.get(f"/v1/projetos/{projeto_id}")

    def criar_projeto(self, nome, cliente_id, edital_id, descricao=None, status=None):
        body = {"nome": nome, "cliente_id": cliente_id, "edital_id": edital_id}
        if descricao is not None:
            body["descricao"] = descricao
        if status is not None:
            body["status"] = status
        return self.post("/v1/projetos", body)

    def atualizar_projeto(self, projeto_id, **campos):
        """Campos parciais: status, nota_tecnica, chance_aprovacao,
        valor_solicitado, valor_aprovado, data_submissao."""
        body = {k: v for k, v in campos.items() if v is not None}
        if "status" in body and body["status"] not in ESTAGIOS_PIPELINE:
            raise ValueError(
                f"Estágio inválido: {body['status']}. Válidos: {', '.join(ESTAGIOS_PIPELINE)}."
            )
        return self.patch(f"/v1/projetos/{projeto_id}", body)

    # ----- clientes / OSCs (por usuário) -----

    def listar_clientes(self, **filtros):
        """Filtros: q, uf, area, limit, offset."""
        return self.get("/v1/clientes", params=filtros)

    def iter_clientes(self, page_size=LIMITE_PADRAO, maximo=None, **filtros):
        return self.paginar("/v1/clientes", params=filtros, page_size=page_size, maximo=maximo)

    def obter_cliente(self, cliente_id):
        return self.get(f"/v1/clientes/{cliente_id}")

    def criar_cliente(self, nome, **campos):
        body = {"nome": nome}
        body.update({k: v for k, v in campos.items() if v is not None})
        return self.post("/v1/clientes", body)

    def atualizar_cliente(self, cliente_id, **campos):
        """Edição parcial. ATENÇÃO: status_documental SUBSTITUI o objeto inteiro
        no servidor (não faz merge). Para atualizar um documento, envie o objeto
        completo de status_documental."""
        body = {k: v for k, v in campos.items() if v is not None}
        return self.patch(f"/v1/clientes/{cliente_id}", body)


# =========================================================================
# Camada de linha de comando (o que os comandos e agentes invocam via Bash)
# =========================================================================

def _formatar_reais(valor):
    """value vem null quando desconhecido (nunca 0). Trata isso."""
    if valor is None:
        return "não informado"
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def _emitir_json(rotulo, obj):
    print(f"\n=== {rotulo} ===")
    print(json.dumps(obj, ensure_ascii=False))


def _csv_para_lista(valor):
    if valor is None:
        return None
    return [s.strip() for s in valor.split(",") if s.strip()]


def _json_param(valor, nome):
    if valor is None:
        return None
    try:
        return json.loads(valor)
    except Exception:
        sys.exit(f"Valor inválido para {nome}: esperado JSON. Recebi: {valor}")


def cmd_testar(cli, args):
    dados = cli.me()
    usuario = dados.get("user", {})
    escopos = dados.get("scopes", [])
    print("Conexão com o CaptaHub OK.")
    print(f"  Dono do token: {usuario.get('name', '-')} <{usuario.get('email', '-')}>")
    print(f"  ID do usuário: {usuario.get('id', '-')}")
    print(f"  Escopos: {', '.join(escopos) if escopos else 'nenhum'}")
    _emitir_json("ME", dados)


def cmd_editais(cli, args):
    filtros = {
        "scope": args.scope, "category": args.category, "q": args.q,
        "value_min": args.value_min, "value_max": args.value_max,
        "deadline_after": args.deadline_after, "deadline_before": args.deadline_before,
        "is_continuous": args.is_continuous, "only_open": args.only_open,
        "limit": args.limit, "offset": args.offset,
    }
    if args.all:
        itens = cli.iter_editais(page_size=args.limit or LIMITE_PADRAO,
                                 **{k: v for k, v in filtros.items() if k not in ("limit", "offset")})
        total = len(itens)
    else:
        resp = cli.listar_editais(**filtros)
        itens = resp.get("data", [])
        total = resp.get("total", len(itens))

    print(f"Editais retornados: {len(itens)} (total no filtro: {total})\n")
    for i, e in enumerate(itens, 1):
        print(f"{i}. {e.get('title', 'sem título')}")
        print(f"   Órgão: {e.get('institution', '-')} | Escopo: {e.get('scope', '-')} | Categoria: {e.get('category', '-')}")
        print(f"   Valor: {_formatar_reais(e.get('value'))} | Prazo: {e.get('deadline') or 'sem data'} | Contínuo: {'sim' if e.get('is_continuous') else 'não'}")
        print(f"   ID: {e.get('id')} | Link: {e.get('url') or '-'}")
        print()
    _emitir_json("EDITAIS", itens)


def cmd_edital(cli, args):
    e = cli.obter_edital(args.id)
    print(f"{e.get('title')}")
    print(f"  Órgão: {e.get('institution')} | Escopo: {e.get('scope')} | Categoria: {e.get('category')}")
    print(f"  Valor: {_formatar_reais(e.get('value'))} | Prazo: {e.get('deadline') or 'sem data'}")
    print(f"  Link: {e.get('url') or '-'}")
    _emitir_json("EDITAL", e)


def cmd_estagios(cli, args):
    dados = cli.estagios()
    if isinstance(dados, dict):
        estagios = dados.get("estagios") or dados.get("data") or []
    else:
        estagios = dados
    print("Estágios do pipeline (ordem oficial):")
    for i, est in enumerate(estagios, 1):
        if isinstance(est, dict):
            print(f"  {i:>2}. {est.get('value'):<22} {est.get('label', '')}")
        else:
            print(f"  {i:>2}. {est}")
    _emitir_json("ESTAGIOS", dados)


def cmd_projetos(cli, args):
    filtros = {"status": args.status, "cliente_id": args.cliente_id,
               "edital_id": args.edital_id, "limit": args.limit, "offset": args.offset}
    if args.all:
        itens = cli.iter_projetos(page_size=args.limit or LIMITE_PADRAO,
                                  **{k: v for k, v in filtros.items() if k not in ("limit", "offset")})
        total = len(itens)
    else:
        resp = cli.listar_projetos(**filtros)
        itens = resp.get("data", [])
        total = resp.get("total", len(itens))
    print(f"Projetos retornados: {len(itens)} (total no filtro: {total})\n")
    for i, p in enumerate(itens, 1):
        print(f"{i}. {p.get('nome')}  [{p.get('status')}]")
        print(f"   ID: {p.get('id')} | Cliente: {p.get('cliente_id')} | Edital: {p.get('edital_id')}")
        nota = p.get("nota_tecnica")
        print(f"   Nota técnica: {nota if nota is not None else '-'} | Chance: {p.get('chance_aprovacao') or '-'} | Submissão: {p.get('data_submissao') or '-'}")
        print()
    _emitir_json("PROJETOS", itens)


def cmd_projeto(cli, args):
    p = cli.obter_projeto(args.id)
    _emitir_json("PROJETO", p)
    print(f"{p.get('nome')}  [{p.get('status')}]  (id {p.get('id')})")


def cmd_projeto_criar(cli, args):
    p = cli.criar_projeto(nome=args.nome, cliente_id=args.cliente_id,
                          edital_id=args.edital_id, descricao=args.descricao,
                          status=args.status)
    print(f"Projeto criado: {p.get('nome')}  [{p.get('status')}]  (id {p.get('id')})")
    _emitir_json("PROJETO_CRIADO", p)


def cmd_projeto_atualizar(cli, args):
    p = cli.atualizar_projeto(
        args.id, status=args.status, nota_tecnica=args.nota_tecnica,
        chance_aprovacao=args.chance_aprovacao, valor_solicitado=args.valor_solicitado,
        valor_aprovado=args.valor_aprovado, data_submissao=args.data_submissao)
    print(f"Projeto atualizado: {p.get('nome')}  [{p.get('status')}]  (id {p.get('id')})")
    _emitir_json("PROJETO_ATUALIZADO", p)


def cmd_clientes(cli, args):
    filtros = {"q": args.q, "uf": args.uf, "area": args.area,
               "limit": args.limit, "offset": args.offset}
    if args.all:
        itens = cli.iter_clientes(page_size=args.limit or LIMITE_PADRAO,
                                  **{k: v for k, v in filtros.items() if k not in ("limit", "offset")})
        total = len(itens)
    else:
        resp = cli.listar_clientes(**filtros)
        itens = resp.get("data", [])
        total = resp.get("total", len(itens))
    print(f"Clientes (OSCs) retornados: {len(itens)} (total no filtro: {total})\n")
    for i, c in enumerate(itens, 1):
        print(f"{i}. {c.get('nome')} {('(' + c.get('sigla') + ')') if c.get('sigla') else ''}")
        print(f"   ID: {c.get('id')} | UF: {c.get('uf') or '-'} | Município: {c.get('municipio') or '-'} | CNPJ: {c.get('cnpj') or '-'}")
        areas = c.get("areas_tematicas") or []
        print(f"   Áreas: {', '.join(areas) if areas else '-'}")
        print()
    _emitir_json("CLIENTES", itens)


def cmd_cliente(cli, args):
    c = cli.obter_cliente(args.id)
    _emitir_json("CLIENTE", c)
    print(f"{c.get('nome')}  (id {c.get('id')})")


def cmd_cliente_criar(cli, args):
    c = cli.criar_cliente(
        nome=args.nome, sigla=args.sigla, cnpj=args.cnpj,
        natureza_juridica=args.natureza_juridica, fundacao=args.fundacao,
        municipio=args.municipio, uf=args.uf,
        territorios=_csv_para_lista(args.territorios),
        areas_tematicas=_csv_para_lista(args.areas_tematicas),
        missao=args.missao, site=args.site, email=args.email, telefone=args.telefone,
        status_documental=_json_param(args.status_documental, "--status-documental"),
        historico_aprovacoes=_json_param(args.historico_aprovacoes, "--historico-aprovacoes"))
    print(f"Cliente (OSC) criado: {c.get('nome')}  (id {c.get('id')})")
    _emitir_json("CLIENTE_CRIADO", c)


def cmd_cliente_atualizar(cli, args):
    c = cli.atualizar_cliente(
        args.id, sigla=args.sigla, cnpj=args.cnpj,
        natureza_juridica=args.natureza_juridica, fundacao=args.fundacao,
        municipio=args.municipio, uf=args.uf,
        territorios=_csv_para_lista(args.territorios),
        areas_tematicas=_csv_para_lista(args.areas_tematicas),
        missao=args.missao, site=args.site, email=args.email, telefone=args.telefone,
        status_documental=_json_param(args.status_documental, "--status-documental"),
        historico_aprovacoes=_json_param(args.historico_aprovacoes, "--historico-aprovacoes"),
        nome=args.nome)
    print(f"Cliente (OSC) atualizado: {c.get('nome')}  (id {c.get('id')})")
    _emitir_json("CLIENTE_ATUALIZADO", c)


def construir_parser():
    p = argparse.ArgumentParser(description="Cliente da API pública do CaptaHub.")
    sub = p.add_subparsers(dest="comando", required=True)

    sub.add_parser("testar", help="Testa a conexão (GET /v1/me).")
    sub.add_parser("me", help="Dono do token e escopos (GET /v1/me).")

    pe = sub.add_parser("editais", help="Lista editais (globais).")
    pe.add_argument("--scope", choices=["Municipal", "Estadual", "Nacional", "Internacional"])
    pe.add_argument("--category")
    pe.add_argument("--q")
    pe.add_argument("--value-min", dest="value_min", type=float)
    pe.add_argument("--value-max", dest="value_max", type=float)
    pe.add_argument("--deadline-after", dest="deadline_after")
    pe.add_argument("--deadline-before", dest="deadline_before")
    pe.add_argument("--is-continuous", dest="is_continuous", action="store_true", default=None)
    pe.add_argument("--only-open", dest="only_open", action="store_true", default=None)
    pe.add_argument("--limit", type=int)
    pe.add_argument("--offset", type=int)
    pe.add_argument("--all", action="store_true", help="Percorre todas as páginas.")

    ped = sub.add_parser("edital", help="Um edital (GET /v1/editais/{id}).")
    ped.add_argument("--id", required=True)

    sub.add_parser("estagios", help="Estágios do pipeline (GET /v1/pipeline/estagios).")

    pp = sub.add_parser("projetos", help="Lista projetos do usuário.")
    pp.add_argument("--status")
    pp.add_argument("--cliente-id", dest="cliente_id")
    pp.add_argument("--edital-id", dest="edital_id")
    pp.add_argument("--limit", type=int)
    pp.add_argument("--offset", type=int)
    pp.add_argument("--all", action="store_true")

    ppg = sub.add_parser("projeto", help="Um projeto (GET /v1/projetos/{id}).")
    ppg.add_argument("--id", required=True)

    ppc = sub.add_parser("projeto-criar", help="Cria um projeto (POST /v1/projetos).")
    ppc.add_argument("--nome", required=True)
    ppc.add_argument("--cliente-id", dest="cliente_id", required=True)
    ppc.add_argument("--edital-id", dest="edital_id", required=True)
    ppc.add_argument("--descricao")
    ppc.add_argument("--status")

    ppa = sub.add_parser("projeto-atualizar", help="Atualiza um projeto (PATCH /v1/projetos/{id}).")
    ppa.add_argument("--id", required=True)
    ppa.add_argument("--status")
    ppa.add_argument("--nota-tecnica", dest="nota_tecnica", type=float)
    ppa.add_argument("--chance-aprovacao", dest="chance_aprovacao")
    ppa.add_argument("--valor-solicitado", dest="valor_solicitado", type=float)
    ppa.add_argument("--valor-aprovado", dest="valor_aprovado", type=float)
    ppa.add_argument("--data-submissao", dest="data_submissao")

    pc = sub.add_parser("clientes", help="Lista clientes (OSCs) do usuário.")
    pc.add_argument("--q")
    pc.add_argument("--uf")
    pc.add_argument("--area")
    pc.add_argument("--limit", type=int)
    pc.add_argument("--offset", type=int)
    pc.add_argument("--all", action="store_true")

    pcg = sub.add_parser("cliente", help="Um cliente (GET /v1/clientes/{id}).")
    pcg.add_argument("--id", required=True)

    def add_campos_cliente(parser, com_nome_obrigatorio):
        if com_nome_obrigatorio:
            parser.add_argument("--nome", required=True)
        else:
            parser.add_argument("--nome")
        parser.add_argument("--sigla")
        parser.add_argument("--cnpj")
        parser.add_argument("--natureza-juridica", dest="natureza_juridica")
        parser.add_argument("--fundacao", help="AAAA-MM-DD")
        parser.add_argument("--municipio")
        parser.add_argument("--uf")
        parser.add_argument("--territorios", help="lista separada por vírgula")
        parser.add_argument("--areas-tematicas", dest="areas_tematicas", help="lista separada por vírgula")
        parser.add_argument("--missao")
        parser.add_argument("--site")
        parser.add_argument("--email")
        parser.add_argument("--telefone")
        parser.add_argument("--status-documental", dest="status_documental",
                            help='objeto JSON de booleanos. SUBSTITUI o objeto inteiro no PATCH.')
        parser.add_argument("--historico-aprovacoes", dest="historico_aprovacoes",
                            help='array JSON de {financiador, valor, ano}')

    pcc = sub.add_parser("cliente-criar", help="Cria um cliente/OSC (POST /v1/clientes).")
    add_campos_cliente(pcc, com_nome_obrigatorio=True)

    pca = sub.add_parser("cliente-atualizar", help="Atualiza um cliente/OSC (PATCH /v1/clientes/{id}).")
    pca.add_argument("--id", required=True)
    add_campos_cliente(pca, com_nome_obrigatorio=False)

    return p


DISPATCH = {
    "testar": cmd_testar, "me": cmd_testar,
    "editais": cmd_editais, "edital": cmd_edital,
    "estagios": cmd_estagios,
    "projetos": cmd_projetos, "projeto": cmd_projeto,
    "projeto-criar": cmd_projeto_criar, "projeto-atualizar": cmd_projeto_atualizar,
    "clientes": cmd_clientes, "cliente": cmd_cliente,
    "cliente-criar": cmd_cliente_criar, "cliente-atualizar": cmd_cliente_atualizar,
}


def main():
    args = construir_parser().parse_args()
    try:
        cli = CaptaHubClient.from_env()
    except ValueError as e:
        sys.exit(str(e))

    try:
        DISPATCH[args.comando](cli, args)
    except CaptaHubAPIError as e:
        print(f"Falha na chamada ao CaptaHub. {e}")
        if e.status == 401:
            print("Confira o CAPTAHUB_API_TOKEN no .env. Rode /captahub-conectar.")
        sys.exit(1)
    except ValueError as e:
        sys.exit(str(e))


if __name__ == "__main__":
    main()
