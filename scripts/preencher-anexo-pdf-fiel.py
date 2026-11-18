# -*- coding: utf-8 -*-
"""
Preenche os campos de um anexo-modelo que existe como pagina de um PDF de edital,
mexendo apenas no fluxo de texto do proprio modelo.

Diferenca para o preencher-anexo-pdf.py: aqui nada e redesenhado. O script edita o
conteudo da pagina (content stream) e reaproveita o recurso de fonte que ja existe
no arquivo (o mesmo /FontN, com o mesmo subconjunto embutido). Nao entra fonte nova,
nao muda a metrica, nao muda a coordenada de nenhuma linha que nao seja do paragrafo
preenchido, e as ligaduras tipograficas e o kerning do texto original sao preservados
glifo a glifo.

Como funciona:
 1. Le o ToUnicode e o vetor /W do CIDFont, entao sabe ler e medir o que esta escrito.
 2. Decodifica o paragrafo alvo em uma lista de itens (glifo + ajuste de kerning),
    separando o kerning verdadeiro do espacejamento de justificacao.
 3. Compara o texto original com o texto novo (difflib) e troca so os trechos que
    mudaram. O que nao mudou sai com o mesmo glifo e o mesmo kerning de origem.
 4. Requebra o paragrafo na mesma largura de coluna do modelo, justifica com ajuste
    nos espacos e reescreve as linhas nas coordenadas originais.
 5. Se o paragrafo preenchido ocupar mais (ou menos) linhas que o modelo, os
    paragrafos seguintes descem (ou sobem) em bloco, sem serem recompostos.

Uso:
  python scripts/preencher-anexo-pdf-fiel.py --pdf EDITAL.pdf --pagina 29 \
      --sub "texto original do paragrafo" "texto novo" [--sub ...] --saida anexo-III.pdf

Assinatura, data e local nunca sao preenchidos por este script: e regra da captadora.
"""
import argparse
import difflib
import re
import statistics
import pymupdf

LIGADURAS = {'ﬁ': 'fi', 'ﬂ': 'fl', 'ﬀ': 'ff', 'ﬃ': 'ffi', 'ﬄ': 'ffl'}


def _normaliza(t):
    for lig, simples in LIGADURAS.items():
        t = t.replace(lig, simples)
    return ' '.join(t.split())


def _tounicode(doc, xref):
    """cid -> texto, lido do ToUnicode do Type0."""
    tu = doc.xref_get_key(xref, 'ToUnicode')
    if tu[0] != 'xref':
        return {}
    txt = doc.xref_stream(int(tu[1].split()[0])).decode('latin-1')
    m = {}
    for sec in re.findall(r'beginbfchar(.*?)endbfchar', txt, re.S):
        for a, b in re.findall(r'<([0-9A-Fa-f]+)>\s*<([0-9A-Fa-f]+)>', sec):
            m[int(a, 16)] = bytes.fromhex(b).decode('utf-16-be')
    for sec in re.findall(r'beginbfrange(.*?)endbfrange', txt, re.S):
        for a, b, c in re.findall(r'<([0-9A-Fa-f]+)>\s*<([0-9A-Fa-f]+)>\s*<([0-9A-Fa-f]+)>', sec):
            lo, hi, dst = int(a, 16), int(b, 16), int(c, 16)
            for i, cid in enumerate(range(lo, hi + 1)):
                m[cid] = chr(dst + i)
    return m


def _larguras(doc, xref_desc):
    """cid -> largura em milesimos, lido do /W e do /DW do CIDFont descendente."""
    t = doc.xref_object(xref_desc, compressed=True)
    dw = int(re.search(r'/DW\s+(-?\d+)', t).group(1)) if '/DW' in t else 1000
    if '/W' not in t:
        return dw, {}
    i0 = t.index('/W') + 2
    while t[i0] != '[':
        i0 += 1
    profundidade = 0
    fim = i0
    for j in range(i0, len(t)):
        if t[j] == '[':
            profundidade += 1
        elif t[j] == ']':
            profundidade -= 1
            if profundidade == 0:
                fim = j
                break
    toks = re.findall(r'\[[^\]]*\]|-?\d+', t[i0 + 1:fim])
    W = {}
    i = 0
    while i < len(toks):
        c = int(toks[i]); i += 1
        if toks[i].startswith('['):
            for k, v in enumerate(int(x) for x in toks[i][1:-1].split()):
                W[c + k] = v
            i += 1
        else:
            c2, w = int(toks[i]), int(toks[i + 1]); i += 2
            for cid in range(c, c2 + 1):
                W[cid] = w
    return dw, W


def _fontes_da_pagina(doc, pg):
    """nome do recurso (/Font8) -> (cid2uni, uni2cid, dw, W)."""
    saida = {}
    for f in pg.get_fonts(full=True):
        xref, refname = f[0], f[4]
        desc = doc.xref_get_key(xref, 'DescendantFonts')
        if desc[0] != 'array':
            continue
        xdesc = int(re.search(r'(\d+)\s+0\s+R', desc[1]).group(1))
        cid2uni = _tounicode(doc, xref)
        dw, W = _larguras(doc, xdesc)
        uni2cid = {}
        for cid, u in cid2uni.items():
            uni2cid.setdefault(u, cid)
        saida[refname] = (cid2uni, uni2cid, dw, W)
    return saida


def _le_itens(trecho, cid2uni):
    """Le o miolo de um array TJ e devolve [('g', cid, texto), ('a', valor)]."""
    itens = []
    i, n = 0, len(trecho)
    while i < n:
        ch = trecho[i:i + 1]
        if ch == b'(':
            i += 1
            buf = bytearray()
            profundidade = 1
            while i < n:
                c = trecho[i:i + 1]
                if c == b'\\':
                    nx = trecho[i + 1:i + 2]
                    if nx.isdigit():
                        octal = trecho[i + 1:i + 4]
                        k = 0
                        while k < 3 and octal[k:k + 1].isdigit():
                            k += 1
                        buf.append(int(octal[:k], 8) & 0xFF)
                        i += 1 + k
                        continue
                    mapa = {b'n': 10, b'r': 13, b't': 9, b'b': 8, b'f': 12}
                    if nx in mapa:
                        buf.append(mapa[nx])
                    elif nx != b'\n':
                        buf += nx
                    i += 2
                    continue
                if c == b'(':
                    profundidade += 1
                elif c == b')':
                    profundidade -= 1
                    if profundidade == 0:
                        i += 1
                        break
                buf += c
                i += 1
            for k in range(0, len(buf) - 1, 2):
                cid = buf[k] * 256 + buf[k + 1]
                itens.append(('g', cid, cid2uni.get(cid, '�')))
            continue
        if ch == b'<':
            j = trecho.index(b'>', i)
            by = bytes.fromhex(trecho[i + 1:j].decode('latin-1'))
            for k in range(0, len(by) - 1, 2):
                cid = by[k] * 256 + by[k + 1]
                itens.append(('g', cid, cid2uni.get(cid, '�')))
            i = j + 1
            continue
        m = re.match(rb'-?[\d.]+', trecho[i:])
        if m:
            itens.append(('a', float(m.group(0))))
            i += m.end()
            continue
        i += 1
    return itens


class Bloco:
    """Um BT ... ET do content stream."""

    def __init__(self, ini, fim, bruto, fonte, corpo, x, y, itens, ctm):
        self.ini, self.fim, self.bruto = ini, fim, bruto
        self.fonte, self.corpo, self.x, self.y = fonte, corpo, x, y
        self.itens = itens
        self.ctm = ctm
        self.texto = ''.join(t for tipo, *r in itens if tipo == 'g' for t in [r[1]])


def _ctms(data):
    """Matriz vigente em cada BT. Duas linhas so sao comparaveis sob a mesma matriz."""
    def mul(m, n):
        a, b, c, d, e, f = m
        A, B, C, D, E, F = n
        return (a * A + b * C, a * B + b * D, c * A + d * C, c * B + d * D,
                e * A + f * C + E, e * B + f * D + F)

    ctm = (1.0, 0, 0, 1.0, 0, 0)
    pilha, operandos, saida = [], [], {}
    for m in re.finditer(rb"(-?\d*\.?\d+)|([A-Za-z'\"*]+)", data):
        if m.group(1):
            operandos.append(float(m.group(1)))
            continue
        op = m.group(2)
        if op == b'q':
            pilha.append(ctm)
        elif op == b'Q' and pilha:
            ctm = pilha.pop()
        elif op == b'cm' and len(operandos) >= 6:
            ctm = mul(tuple(operandos[-6:]), ctm)
        elif op == b'BT':
            saida[m.start()] = ctm
        operandos = []
    return saida


def _pula_string(b, i):
    """Devolve o indice logo depois do ) que fecha a string literal iniciada em b[i] == '('."""
    n = len(b)
    j = i + 1
    profundidade = 1
    while j < n:
        c = b[j:j + 1]
        if c == b'\\':
            j += 2
            continue
        if c == b'(':
            profundidade += 1
        elif c == b')':
            profundidade -= 1
            if profundidade == 0:
                return j + 1
        j += 1
    return n


def _operandos_de_texto(b):
    """Miolos de texto de um BT, na ordem do fluxo.

    Le tanto o array de [ ... ] TJ quanto a string solta de ( ... ) Tj e de < ... > Tj.
    O edital usa as duas formas na mesma pagina: quando uma linha justificada termina
    com uma palavra curta, o gerador emite essa palavra em um Tj proprio. Ignorar o Tj
    fazia o paragrafo ser lido pela metade e a busca pelo texto do modelo falhar.
    """
    saida = []
    i, n = 0, len(b)
    while i < n:
        c = b[i:i + 1]
        if c == b'(':
            fim = _pula_string(b, i)
            if re.match(rb'\s*(Tj|TJ|\'|")', b[fim:]):
                saida.append(b[i:fim])
            i = fim
            continue
        if c == b'<' and b[i + 1:i + 2] != b'<':
            fim = b.find(b'>', i)
            fim = n if fim < 0 else fim + 1
            if re.match(rb'\s*(Tj|TJ|\'|")', b[fim:]):
                saida.append(b[i:fim])
            i = fim
            continue
        if c == b'[':
            j, profundidade = i, 0
            while j < n:
                cj = b[j:j + 1]
                if cj == b'(':
                    j = _pula_string(b, j)
                    continue
                if cj == b'[':
                    profundidade += 1
                elif cj == b']':
                    profundidade -= 1
                    if profundidade == 0:
                        j += 1
                        break
                j += 1
            if re.match(rb'\s*TJ', b[j:]):
                saida.append(b[i + 1:j - 1])
            i = j
            continue
        i += 1
    return saida


def _blocos(data, fontes):
    ctms = _ctms(data)
    saida = []
    for m in re.finditer(rb'BT\n(.*?)\nET', data, re.S):
        b = m.group(1)
        fm = re.search(rb'/(Font\d+)\n([\d.]+)\nTf', b)
        tm = re.search(rb'Tf\n[\d.\-]+\n[\d.\-]+\n[\d.\-]+\n[\d.\-]+\n([\d.\-]+)\n([\d.\-]+)\nTm', b)
        if not fm or not tm:
            continue
        nome = fm.group(1).decode()
        cid2uni = fontes.get(nome, ({}, {}, 1000, {}))[0]
        itens = []
        for arr in _operandos_de_texto(b):
            itens += _le_itens(arr, cid2uni)
        saida.append(Bloco(m.start(), m.end(), b, nome, float(fm.group(2)),
                           float(tm.group(1)), float(tm.group(2)), itens,
                           tuple(round(v, 4) for v in ctms.get(m.start(), (0,) * 6))))
    return saida


def _pares(itens, cid_espaco):
    """[(cid, texto, kern_antes)] com o espacejamento de justificacao removido.

    Regra: o ajuste que vem logo depois de um espaco e justificacao (word spacing)
    e sai fora; qualquer outro ajuste e kerning de par e fica com o glifo seguinte.
    """
    saida = []
    pendente = 0.0
    ultimo_foi_espaco = False
    for it in itens:
        if it[0] == 'a':
            if not ultimo_foi_espaco:
                pendente += it[1]
            continue
        cid, txt = it[1], it[2]
        saida.append([cid, txt, pendente])
        pendente = 0.0
        ultimo_foi_espaco = (cid == cid_espaco)
    return saida


def _largura(pares, corpo, W, dw):
    total = 0.0
    for cid, _txt, kern in pares:
        total += W.get(cid, dw) / 1000 * corpo - kern / 1000 * corpo
    return total


def _fim_visivel(itens, corpo, W, dw, cid_espaco):
    """Onde termina o ultimo glifo visivel da linha, ja contando kerning e justificacao."""
    x = 0.0
    fim = 0.0
    for it in itens:
        if it[0] == 'a':
            x -= it[1] / 1000 * corpo
            continue
        x += W.get(it[1], dw) / 1000 * corpo
        if it[1] != cid_espaco:
            fim = x
    return fim


def _codifica(texto, uni2cid):
    """texto -> [[cid, texto, kern]] usando ligadura quando o modelo tem o glifo."""
    saida = []
    i = 0
    while i < len(texto):
        casou = False
        for lig, simples in LIGADURAS.items():
            n = len(simples)
            if texto[i:i + n] == simples and (lig in uni2cid or simples in uni2cid):
                cid = uni2cid.get(lig, uni2cid.get(simples))
                saida.append([cid, simples, 0.0])
                i += n
                casou = True
                break
        if casou:
            continue
        ch = texto[i]
        if ch not in uni2cid:
            raise SystemExit(f'A fonte embutida do modelo nao tem o caractere {ch!r}. '
                             'Ajuste a grafia do preenchimento.')
        saida.append([uni2cid[ch], ch, 0.0])
        i += 1
    return saida


def _splice(pares_orig, texto_novo, uni2cid):
    """Troca so os trechos que mudaram, preservando glifo e kerning do que ficou."""
    chars, dono = [], []
    for idx, (_cid, txt, _k) in enumerate(pares_orig):
        for c in txt:
            chars.append(c)
            dono.append(idx)
    antigo = ''.join(chars)
    sm = difflib.SequenceMatcher(None, antigo, texto_novo, autojunk=False)
    saida = []
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == 'equal':
            vistos = []
            for k in range(i1, i2):
                if not vistos or vistos[-1] != dono[k]:
                    vistos.append(dono[k])
            for idx in vistos:
                saida.append(list(pares_orig[idx]))
        elif tag in ('replace', 'insert'):
            saida += _codifica(texto_novo[j1:j2], uni2cid)
    if saida:
        saida[0][2] = pares_orig[0][2] if pares_orig else 0.0
    return saida


def _quebra(pares, corpo, W, dw, largura_alvo, cid_espaco):
    """Requebra em linhas de no maximo largura_alvo. Devolve lista de listas.

    A linha que nao e a ultima termina com o glifo de espaco, como no modelo.
    """
    def adv(par):
        return (W.get(par[0], dw) - par[2]) / 1000 * corpo

    # separa em palavras, guardando o proprio glifo de espaco que veio do modelo
    palavras, atual, espacos = [], [], []
    for par in pares:
        if par[0] == cid_espaco:
            palavras.append(atual)
            espacos.append(par)
            atual = []
        else:
            atual.append(par)
    palavras.append(atual)
    espacos.append(None)

    linhas, linha, largura = [], [], 0.0
    for k, palavra in enumerate(palavras):
        larg_pal = sum(adv(p) for p in palavra)
        if not linha:
            linha, largura = list(palavra), larg_pal
        elif largura + adv(espaco_ant) + larg_pal <= largura_alvo:
            linha.append(espaco_ant)
            linha += palavra
            largura += adv(espaco_ant) + larg_pal
        else:
            linha.append(espaco_ant)
            linhas.append(linha)
            linha, largura = list(palavra), larg_pal
        espaco_ant = espacos[k] if espacos[k] is not None else [cid_espaco, ' ', 0.0]
    linhas.append(linha)
    return linhas


def _emite(linha, corpo, W, dw, largura_alvo, cid_espaco, justificar):
    """Monta o miolo do array TJ de uma linha."""
    conteudo = list(linha)
    while conteudo and conteudo[-1][0] == cid_espaco:
        conteudo.pop()
    largura = _largura(conteudo, corpo, W, dw)
    espacos = [i for i, p in enumerate(conteudo) if p[0] == cid_espaco]
    ajuste_espaco = 0.0
    if justificar and espacos:
        sobra = largura_alvo - largura
        ajuste_espaco = -sobra / len(espacos) / corpo * 1000
    partes = []
    buffer_hex = []

    def descarrega():
        if buffer_hex:
            partes.append('<' + ''.join(buffer_hex) + '>')
            buffer_hex.clear()

    for i, (cid, _txt, kern) in enumerate(conteudo):
        if kern:
            descarrega()
            partes.append(f'{kern:g}')
        buffer_hex.append(f'{cid:04X}')
        if i in espacos and ajuste_espaco:
            descarrega()
            partes.append(f'{ajuste_espaco:.3f}')
    # o espaco de fim de linha do modelo e mantido, como no original
    if linha and linha[-1][0] == cid_espaco:
        buffer_hex.append(f'{cid_espaco:04X}')
    descarrega()
    return '\n'.join(partes)


def _bloco_texto(fonte, corpo, x, y, miolo):
    return ('BT\n0\nTr\n/%s\n%s\nTf\n1.0\n0\n0\n-1.0\n%s\n%s\nTm\n0\n0\nTd\n[\n%s\n]\nTJ\nET'
            % (fonte, _num(corpo), _num(x), _num(y), miolo))


def _num(v):
    s = f'{v:.6f}'.rstrip('0')
    return s + '0' if s.endswith('.') else s


def preencher(pdf, pagina, subs, saida):
    doc = pymupdf.open(pdf)
    out = pymupdf.open()
    out.insert_pdf(doc, from_page=pagina - 1, to_page=pagina - 1)
    pg = out[0]
    fontes = _fontes_da_pagina(out, pg)
    conteudos = pg.get_contents()
    if len(conteudo_lista := list(conteudos)) != 1:
        raise SystemExit('A pagina tem %d fluxos de conteudo; este script so trata um.' % len(conteudo_lista))
    xref_conteudo = conteudo_lista[0]
    data = pg.read_contents()
    blocos = _blocos(data, fontes)

    # corpo do texto: o tamanho de fonte mais frequente entre os blocos com texto
    corpos = [b.corpo for b in blocos if b.texto.strip()]
    corpo_padrao = statistics.mode(corpos)
    corpo_blocos = [b for b in blocos if b.corpo == corpo_padrao and b.texto.strip()]
    # a moldura do corpo: dentro dela, e so dentro dela, as coordenadas se comparam
    moldura = statistics.mode([b.ctm for b in corpo_blocos])
    corpo_blocos = [b for b in corpo_blocos if b.ctm == moldura]

    # linhas do corpo, agrupadas por coordenada y (uma linha pode estar em dois blocos)
    linhas_y = sorted({round(b.y, 2) for b in corpo_blocos})
    entrelinha = min((b - a for a, b in zip(linhas_y, linhas_y[1:])), default=33.6)

    # largura de coluna: a da linha cheia mais larga do proprio modelo, medida ate o
    # ultimo glifo visivel. Nao se inventa margem: usa-se a que o edital ja praticou.
    nome_fonte = statistics.mode([b.fonte for b in corpo_blocos])
    cid2uni, uni2cid, dw, W = fontes[nome_fonte]
    cid_espaco = uni2cid.get(' ')
    larguras = []
    for y in linhas_y:
        da_linha = sorted([b for b in corpo_blocos if round(b.y, 2) == y], key=lambda b: b.x)
        if not da_linha:
            continue
        base = da_linha[0].x
        fim = 0.0
        for b in da_linha:
            f = _fim_visivel(b.itens, corpo_padrao, W, dw, cid_espaco)
            if f:
                fim = b.x - base + f
        if sum(1 for b in da_linha for it in b.itens if it[0] == 'g') > 40:
            larguras.append(fim)  # linha cheia, portanto justificada ate a margem
    largura_alvo = max(larguras)

    feitas = []
    for original, novo in subs.items():
        chave = _normaliza(original)
        # acha os blocos consecutivos cujo texto junto forma o paragrafo
        alvo = None
        for i in range(len(corpo_blocos)):
            acc = ''
            for j in range(i, len(corpo_blocos)):
                acc += corpo_blocos[j].texto
                if _normaliza(acc) == chave:
                    alvo = (i, j)
                    break
                if not chave.startswith(_normaliza(acc)):
                    break
            if alvo:
                break
        if not alvo:
            raise SystemExit('Paragrafo nao encontrado na pagina: ' + chave[:80])
        i, j = alvo
        run = corpo_blocos[i:j + 1]
        ys = sorted({round(b.y, 2) for b in run})
        x0 = min(b.x for b in run)
        pares = []
        for b in run:
            pares += _pares(b.itens, cid_espaco)
        pares_novos = _splice(pares, _normaliza(novo), uni2cid)
        linhas = _quebra(pares_novos, corpo_padrao, W, dw, largura_alvo - (x0 - 6.0), cid_espaco)
        # coordenadas: as do modelo, e a entrelinha do modelo para linha que sobre
        coords = list(ys) + [ys[-1] + entrelinha * (k + 1) for k in range(max(0, len(linhas) - len(ys)))]
        novos = []
        for k, linha in enumerate(linhas):
            miolo = _emite(linha, corpo_padrao, W, dw, largura_alvo - (x0 - 6.0), cid_espaco,
                           justificar=(k < len(linhas) - 1))
            novos.append(_bloco_texto(nome_fonte, corpo_padrao, x0, coords[k], miolo))
        # a cor vigente e a do operador rg imediatamente anterior ao paragrafo
        achados = list(re.finditer(rb'([\d.]+\n[\d.]+\n[\d.]+\nrg)\n', data[:run[0].ini]))
        cor = b'\n' + achados[-1].group(1) + b'\n' if achados else b'\n'
        junta = cor.join(x.encode('latin-1') for x in novos)
        ini, fim = run[0].ini, max(b.fim for b in run)
        data = data[:ini] + junta + data[fim:]
        fim_novo = ini + len(junta)
        deslocamento = (len(linhas) - len(ys)) * entrelinha
        feitas.append((chave[:60], _normaliza(novo)[:60], len(ys), len(linhas)))
        # reposiciona (sem recompor) o que vem abaixo, se o paragrafo mudou de altura.
        # O que acabou de ser escrito fica fora: ja nasceu na coordenada certa.
        if deslocamento:
            blocos = _blocos(data, fontes)
            limite = ys[-1] + entrelinha / 2
            pedacos, ult = [], 0
            for b in blocos:
                if b.ctm == moldura and b.y > limite and b.ini >= fim_novo:
                    novo_bt = re.sub(rb'(Tf\n[\d.\-]+\n[\d.\-]+\n[\d.\-]+\n[\d.\-]+\n[\d.\-]+\n)[\d.\-]+(\nTm)',
                                     lambda mm: mm.group(1) + _num(b.y + deslocamento).encode('latin-1') + mm.group(2),
                                     b.bruto, count=1)
                    pedacos.append(data[ult:b.ini] + b'BT\n' + novo_bt + b'\nET')
                    ult = b.fim
            data = b''.join(pedacos) + data[ult:]
        blocos = _blocos(data, fontes)
        corpo_blocos = [b for b in blocos
                        if b.corpo == corpo_padrao and b.texto.strip() and b.ctm == moldura]

    out.update_stream(xref_conteudo, data)
    out.save(saida, garbage=3, deflate=True)
    return feitas


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--pdf', required=True)
    ap.add_argument('--pagina', type=int, required=True)
    ap.add_argument('--sub', nargs=2, action='append', default=[], metavar=('ORIGINAL', 'NOVO'))
    ap.add_argument('--saida', required=True)
    a = ap.parse_args()
    feitas = preencher(a.pdf, a.pagina, dict(a.sub), a.saida)
    for chave, novo, antes, depois in feitas:
        print(f'  paragrafo de {antes} para {depois} linha(s)')
    print(f'{len(feitas)} paragrafo(s) preenchido(s) -> {a.saida}')


if __name__ == '__main__':
    main()
