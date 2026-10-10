#!/usr/bin/env python3
"""Leitura semanal das métricas de negócio da Mobilizando.

Só LÊ: o Checkpoint e o Controle de Submissão (Drive G) e os projetos do CaptaHub.
Grava apenas na pasta 09 (04_NEGOCIOS_METRICAS): o histórico das leituras e o painel em HTML.
Não escreve em planilha, no CaptaHub nem em nenhum sistema externo.
Os nomes de clientes não saem daqui, só contagens e valores.

Uso: python3 scripts/metricas-semanal.py
"""
import collections
import datetime
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unicodedata

import openpyxl

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DRIVE = r"G:\Meu Drive\_82 - Rosepaula Aparecida Andrade Rodrigues"
CHECKPOINT = os.path.join(DRIVE, "08 - Checkpoint", "01 - Checkpoint.xlsx")
CONTROLE = os.path.join(
    DRIVE, "04 - Controle de Submissão_", "01 - Mineração de Editais",
    "01 - Planejamento de Submissões", "1 - Controle de Submissão_.xlsx",
)
SAIDA = os.path.join(RAIZ, "mobilizando mkt - pasta 09", "04_NEGOCIOS_METRICAS")
MODELO = os.path.join(RAIZ, "scripts", "metricas-painel-modelo.html")
REF_APROVACAO = 0.30  # plano da mentoria
MESES = ["janeiro", "fevereiro", "março", "abril", "maio", "junho", "julho",
         "agosto", "setembro", "outubro", "novembro", "dezembro"]


def num(v):
    if v is None or v == "":
        return None
    if isinstance(v, (int, float)):
        return float(v)
    s = re.sub(r"[^\d,.\-]", "", str(v))
    if not s:
        return None
    if "," in s:
        s = s.replace(".", "").replace(",", ".")
    try:
        return float(s)
    except ValueError:
        return None


def norm(s):
    s = unicodedata.normalize("NFKD", str(s or "")).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]", "", s.lower())[:30]


def carregar(caminho, aba=None):
    """Copia o arquivo para uma pasta temporária (o Excel pode estar com ele aberto) e lê."""
    pasta = tempfile.mkdtemp()
    try:
        copia = os.path.join(pasta, "leitura.xlsx")
        shutil.copyfile(caminho, copia)
        wb = openpyxl.load_workbook(copia, data_only=True, read_only=True)
        ws = wb[aba] if aba else wb.worksheets[0]
        linhas = [list(r) + [None] * 30 for r in ws.iter_rows(values_only=True)]
        wb.close()
        return linhas
    finally:
        shutil.rmtree(pasta, ignore_errors=True)


def ler_captahub():
    try:
        r = subprocess.run(
            [sys.executable, os.path.join(RAIZ, "scripts", "captahub-api.py"), "projetos", "--all"],
            capture_output=True, text=True, encoding="utf-8", errors="replace", cwd=RAIZ, timeout=120,
            env={**os.environ, "PYTHONIOENCODING": "utf-8"},
        )
        m = re.search(r"=== PROJETOS ===\n", r.stdout)
        return json.loads(r.stdout[m.end():]) if m else None
    except Exception:
        return None


def ler_checkpoint(hoje):
    L = carregar(CHECKPOINT)
    rot = {}
    for i, r in enumerate(L):
        if isinstance(r[0], str) and r[0].strip() and r[0].strip() not in rot:
            rot[r[0].strip()] = i

    def serie(nome):
        if nome not in rot:
            return [0.0] * 12
        r = L[rot[nome]]
        return [num(r[i]) or 0.0 for i in range(1, 13)]

    ate = hoje.month            # meses até o corrente
    comp = max(hoje.month - 1, 0)  # meses completos
    sub, meta, apr, cap, rem = (serie("Editais Submetidos"), serie("Meta de Submissão"),
                                serie("Aprovações"), serie("Valor Captado"), serie("Remuneração"))
    reun, meta_reun = serie("Reuniões realizadas"), serie("Meta de reuniões")

    # contratos e clientes, na seção "Contrato"
    contratos_ano, clientes_total = 0, 0
    if "Mês" in rot:
        i0 = rot["Mês"]
        datas = L[i0][1:15]
        i = i0 + 2
        while i < len(L) and any(c not in (None, "") for c in L[i][1:15]):
            for j, c in enumerate(L[i][1:15]):
                if isinstance(c, str) and c.strip():
                    clientes_total += 1
                    d = datas[j]
                    if isinstance(d, datetime.datetime) and d.year == hoje.year and d.month <= hoje.month:
                        contratos_ano += 1
            i += 1
    sem_sucesso = 0
    if "Reuniões Sem Sucesso" in rot:
        i = rot["Reuniões Sem Sucesso"] + 1
        while i < len(L) and any(c not in (None, "") for c in L[i][:3]):
            if isinstance(L[i][1], str) and L[i][1].strip():
                sem_sucesso += 1
            i += 1
    fixo = []
    if "Valor Fixo" in rot:
        fixo = [num(c) for c in L[rot["Valor Fixo"]][1:14] if num(c)]
    return {
        "sub_fev_ate": sum(sub[1:ate]), "sub_comp": sum(sub[1:comp]), "sub_mes": sub[hoje.month - 1],
        "meta_comp": sum(meta[0:comp]), "meta_mes": meta[hoje.month - 1], "meta_ano": sum(meta),
        "meses_fev_comp": max(comp - 1, 1),
        "apr_qtd": sum(apr[1:ate]), "captado": sum(cap[1:ate]), "remuneracao": sum(rem[1:ate]),
        "jan": {"aprovacoes": apr[0], "captado": cap[0], "remuneracao": rem[0]},
        "reunioes": sum(reun[0:comp]), "meta_reunioes": sum(meta_reun[0:comp]),
        "contratos_ano": contratos_ano, "clientes_total": clientes_total, "sem_sucesso": sem_sucesso,
        "fixo": fixo,
    }


def ler_controle(captahub):
    valor_ch = {norm(p["nome"]): p.get("valor_solicitado") for p in (captahub or []) if p.get("nome")}

    def linhas(aba):
        out = []
        for r in carregar(CONTROLE, aba)[2:]:
            if not r[1]:
                continue
            nome = str(r[1]).replace("\n", " ").strip()
            valor = num(r[4])
            if not valor:
                valor = valor_ch.get(norm(nome)) or None
            res = r[12] if isinstance(r[12], datetime.datetime) else None
            out.append({"nome": nome, "valor": valor, "status": str(r[11] or "").strip(), "resultado": res})
        return out

    return linhas("GERAL"), linhas("REPROVADOS")


def main():
    hoje = datetime.date.today()
    ck = ler_checkpoint(hoje)
    captahub = ler_captahub()
    geral, reprov = ler_controle(captahub)

    reprovados = [r for r in reprov if r["status"] == "Reprovado"]
    abertos = [r for r in geral if r["status"] == "Submetido"]
    v_reprov = sum(r["valor"] or 0 for r in reprovados)
    resolvidos = ck["apr_qtd"] + len(reprovados)
    v_com_resultado = ck["captado"] + v_reprov
    taxa_qtd = ck["apr_qtd"] / resolvidos if resolvidos else None
    taxa_val = ck["captado"] / v_com_resultado if v_com_resultado else None

    ritmo = ck["sub_comp"] / ck["meses_fev_comp"] if ck["meses_fev_comp"] else 0
    meses_restantes = max(13 - hoje.month, 1)
    necessario = max(ck["meta_ano"] - ck["sub_fev_ate"], 0) / meses_restantes

    pagamentos = 0
    status_ch = collections.Counter(p["status"] for p in (captahub or []))
    pagamentos += status_ch.get("pagamento_recebido", 0) + status_ch.get("pagamento_pendente", 0)
    for r in geral + reprov:
        if r["status"] in ("Pagamento Recebido", "Pagamento Pendente"):
            pagamentos += 1

    datas_res = sorted(r["resultado"] for r in abertos if r["resultado"])
    prox = collections.Counter(d.strftime("%d/%m") for d in datas_res if d.date() >= hoje)
    sem_valor_abertos = sum(1 for r in abertos if not r["valor"])

    dados = {
        "data": hoje.isoformat(),
        "periodo": f"fevereiro até {hoje.strftime('%d/%m/%Y')}",
        "mes_corrente": MESES[hoje.month - 1],
        "aprovacao": {
            "aprovados": ck["apr_qtd"], "reprovados": len(reprovados), "resolvidos": resolvidos,
            "taxa_qtd": taxa_qtd, "taxa_valor": taxa_val, "valor_aprovado": ck["captado"],
            "valor_reprovado": v_reprov, "referencia": REF_APROVACAO,
            "sem_valor": sum(1 for r in reprovados if not r["valor"]),
        },
        "submissoes": {
            "realizado": ck["sub_fev_ate"], "meta_ano": ck["meta_ano"], "meta_ate_mes_anterior": ck["meta_comp"],
            "realizado_ate_mes_anterior": ck["sub_comp"],
            "pct_meta_acumulada": ck["sub_comp"] / ck["meta_comp"] if ck["meta_comp"] else None,
            "pct_meta_ano": ck["sub_fev_ate"] / ck["meta_ano"] if ck["meta_ano"] else None,
            "mes_realizado": ck["sub_mes"], "mes_meta": ck["meta_mes"],
            "ritmo_mes": ritmo, "necessario_mes": necessario, "meses_restantes": meses_restantes,
            "valor_submetido": ck["captado"] + v_reprov + sum(r["valor"] or 0 for r in abertos),
        },
        "recebimento": {
            "remuneracao": ck["remuneracao"], "captado": ck["captado"],
            "taxa": ck["remuneracao"] / ck["captado"] if ck["captado"] else None,
            "media_remuneracao": ck["remuneracao"] / ck["apr_qtd"] if ck["apr_qtd"] else None,
            "media_captado": ck["captado"] / ck["apr_qtd"] if ck["apr_qtd"] else None,
            "janeiro": ck["jan"], "pagamentos_registrados": pagamentos,
        },
        "recorrente": {"valor_fixo_max": sum(ck["fixo"]), "contratos_com_fixo": len(ck["fixo"])},
        "funil": {
            "reunioes": ck["reunioes"], "meta_reunioes": ck["meta_reunioes"],
            "contratos_ano": ck["contratos_ano"], "clientes_total": ck["clientes_total"],
            "sem_sucesso": ck["sem_sucesso"],
        },
        "pipeline": {
            "abertos": len(abertos), "valor": sum(r["valor"] or 0 for r in abertos),
            "sem_valor": sem_valor_abertos, "proximos_resultados": dict(prox),
        },
    }

    # divergências entre as fontes
    alertas = []
    if captahub:
        reprov_chave = {(norm(r["nome"]), round(r["valor"] or 0)) for r in reprovados}
        for p in captahub:
            if p["status"] == "aprovado" and (norm(p["nome"]), round(p.get("valor_solicitado") or 0)) in reprov_chave:
                alertas.append({"nivel": "alto", "texto":
                    f"O CaptaHub traz como Aprovado um projeto que a planilha de submissão traz como Reprovado: {p['nome'][:60]}. Confirmar e corrigir o lado errado."})
        ch_sub = status_ch.get("submetido", 0)
        if ch_sub != len(abertos):
            alertas.append({"nivel": "medio", "texto":
                f"Projetos em Submetido: {len(abertos)} na planilha e {ch_sub} no CaptaHub."})
    else:
        alertas.append({"nivel": "medio", "texto": "O CaptaHub não respondeu nesta leitura. Os números usam só o Checkpoint e a planilha."})
    localizadas = ck["apr_qtd"] + len(reprovados) + len(abertos)
    if localizadas != ck["sub_fev_ate"]:
        alertas.append({"nivel": "medio", "texto":
            f"O Checkpoint conta {int(ck['sub_fev_ate'])} submissões e a planilha traz {int(localizadas)} com status. Conferir a diferença."})
    if ritmo and necessario > 1.5 * ritmo:
        alertas.insert(0, {"nivel": "alto", "texto":
            f"Ritmo de {ritmo:.1f} submissões por mês contra {necessario:.1f} necessárias para fechar a meta do ano. Recalibrar a meta ou aumentar a capacidade."})
    if taxa_qtd is not None and taxa_qtd < REF_APROVACAO:
        alertas.append({"nivel": "medio", "texto":
            f"Taxa de aprovação de {taxa_qtd * 100:.0f}%, abaixo da referência de {REF_APROVACAO * 100:.0f}%. Passar o CaptaEstrategista antes de entrar em cada edital."})
    if pagamentos == 0:
        alertas.append({"nivel": "alto", "texto":
            "O recebimento de fato não está registrado em lugar nenhum (nenhum projeto em Pagamento pendente ou recebido). A taxa de recebimento do painel é a remuneração prevista."})
    if sem_valor_abertos:
        alertas.append({"nivel": "info", "texto":
            f"{sem_valor_abertos} projeto(s) aguardando resultado estão sem valor na planilha e ficaram fora da soma do pipeline."})
    if prox:
        alertas.append({"nivel": "info", "texto":
            "Resultados previstos: " + ", ".join(f"{d} ({n})" for d, n in prox.items()) + "."})
    dados["alertas"] = alertas

    # histórico e variação
    os.makedirs(SAIDA, exist_ok=True)
    hist_caminho = os.path.join(SAIDA, "historico.json")
    try:
        hist = json.load(open(hist_caminho, encoding="utf-8"))
    except Exception:
        hist = []
    hist = [h for h in hist if h["data"] != dados["data"]]
    anterior = hist[-1] if hist else None
    atual = {
        "data": dados["data"], "taxa_qtd": taxa_qtd, "aprovados": ck["apr_qtd"], "resolvidos": resolvidos,
        "realizado": ck["sub_fev_ate"], "remuneracao": ck["remuneracao"], "captado": ck["captado"],
        "abertos": len(abertos), "valor_pipeline": dados["pipeline"]["valor"],
    }
    dados["anterior"] = anterior
    hist.append(atual)
    hist = hist[-60:]
    json.dump(hist, open(hist_caminho, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    dados["historico"] = hist

    modelo = open(MODELO, encoding="utf-8").read()
    corpo = json.dumps(dados, ensure_ascii=False).replace("</", "<\\/")
    html = modelo.replace("/*DADOS*/null", corpo)
    saida_html = os.path.join(SAIDA, "painel.html")
    open(saida_html, "w", encoding="utf-8").write(html)

    pct = lambda v: "sem dado" if v is None else f"{v * 100:.1f}%"
    print(f"Leitura de {hoje.strftime('%d/%m/%Y')} ({dados['periodo']})")
    print(f"Aprovação: {ck['apr_qtd']:.0f} de {resolvidos:.0f} ({pct(taxa_qtd)}); em valor {pct(taxa_val)}")
    print(f"Submissões: {ck['sub_fev_ate']:.0f} de {ck['meta_ano']:.0f} no ano; ritmo {ritmo:.1f}/mês, necessário {necessario:.1f}/mês")
    print(f"Remuneração: R$ {ck['remuneracao']:,.0f} sobre R$ {ck['captado']:,.0f} captados")
    print(f"Pipeline: {len(abertos)} projetos, R$ {dados['pipeline']['valor']:,.0f}")
    print(f"Alertas: {len(alertas)}")
    print(f"Painel: {saida_html}")


if __name__ == "__main__":
    main()
