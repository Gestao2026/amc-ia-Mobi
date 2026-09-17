# -*- coding: utf-8 -*-
"""
Preenche os campos de um anexo-modelo que existe como pagina de um PDF de edital,
mantendo o texto fixo, a fonte, o corpo, a cor e a diagramacao originais.

Metodo: para cada paragrafo que contem placeholder, o paragrafo inteiro e apagado
(redacao em branco) e re-composto no mesmo retangulo, com a mesma fonte embutida,
o mesmo corpo e o mesmo entrelinhamento. Paragrafos sem placeholder nao sao tocados.
A fonte embutida vem do proprio PDF (subconjunto), com a tabela cmap reconstruida a
partir do ToUnicode. Assim a tipografia preenchida e identica a do edital.

Uso:
  python scripts/preencher-anexo-pdf.py --pdf EDITAL.pdf --pagina 27 \
      --sub "texto original do paragrafo" "texto novo" [--sub ...] --saida anexo-I.pdf
  python scripts/preencher-anexo-pdf.py --pdf EDITAL.pdf --pagina 27 --saida modelo.pdf   (so extrai a pagina)

Os textos de --sub sao comparados sem quebras de linha e com espacos normalizados.
Assinatura, data e local nunca sao preenchidos por este script: e regra da captadora.
"""
import argparse, os, re, sys, tempfile
import pymupdf


def _normaliza(t):
    # ligaduras tipograficas do PDF viram letras simples para a comparacao
    t = t.replace('ﬁ', 'fi').replace('ﬂ', 'fl').replace('ﬀ', 'ff')
    return ' '.join(t.split())


def reconstruir_fontes(doc, pagina_idx, pasta):
    """Extrai as fontes embutidas da pagina e reconstroi a cmap a partir do ToUnicode."""
    from fontTools.ttLib import TTFont, newTable
    from fontTools.ttLib.tables._c_m_a_p import cmap_format_4, cmap_format_12
    fontes = {}
    for f in doc[pagina_idx].get_fonts(full=True):
        xref, ext, ftype, basefont = f[0], f[1], f[2], f[3]
        tu = doc.xref_get_key(xref, 'ToUnicode')
        if tu[0] != 'xref':
            continue
        cmap_txt = doc.xref_stream(int(tu[1].split()[0])).decode('latin-1')
        m = {}
        for sec in re.findall(r'beginbfchar(.*?)endbfchar', cmap_txt, re.S):
            for a, b in re.findall(r'<([0-9A-Fa-f]+)>\s*<([0-9A-Fa-f]+)>', sec):
                m[int(a, 16)] = bytes.fromhex(b).decode('utf-16-be')
        for sec in re.findall(r'beginbfrange(.*?)endbfrange', cmap_txt, re.S):
            for a, b, c in re.findall(r'<([0-9A-Fa-f]+)>\s*<([0-9A-Fa-f]+)>\s*<([0-9A-Fa-f]+)>', sec):
                lo, hi, dst = int(a, 16), int(b, 16), int(c, 16)
                for i, gid in enumerate(range(lo, hi + 1)):
                    m[gid] = chr(dst + i)
        info = doc.extract_font(xref)
        if info[1] not in ('ttf', 'otf'):
            continue
        bruto = os.path.join(pasta, basefont.replace('+', '_') + '.raw.' + info[1])
        open(bruto, 'wb').write(info[3])
        tt = TTFont(bruto)
        go = tt.getGlyphOrder()
        cm = {ord(u): go[g] for g, u in m.items() if len(u) == 1 and g < len(go)}
        # ligaduras do PDF (fi, fl, ff) ficam acessiveis pelos codigos Unicode proprios
        for g, u in m.items():
            if u in ('fi', 'fl', 'ff') and g < len(go):
                cm[ord({'fi': 'ﬁ', 'fl': 'ﬂ', 'ff': 'ﬀ'}[u])] = go[g]
        cmap = newTable('cmap'); cmap.tableVersion = 0
        st4 = cmap_format_4(4); st4.platformID = 3; st4.platEncID = 1; st4.language = 0
        st4.cmap = {k: v for k, v in cm.items() if k < 0x10000}
        st12 = cmap_format_12(12); st12.platformID = 3; st12.platEncID = 10; st12.language = 0
        st12.cmap = dict(cm)
        cmap.tables = [st4, st12]
        tt['cmap'] = cmap
        nome = basefont.split('+')[-1]
        if 'name' not in tt:
            from fontTools.ttLib.tables._n_a_m_e import table__n_a_m_e
            nm = table__n_a_m_e(); nm.names = []
            for nid, val in [(1, nome.split('-')[0]), (2, nome.split('-')[-1]), (4, nome), (6, nome)]:
                nm.setName(val, nid, 3, 1, 0x409)
            tt['name'] = nm
        if 'post' not in tt:
            post = newTable('post'); post.formatType = 3.0
            post.italicAngle = 0; post.underlinePosition = -100; post.underlineThickness = 50
            post.isFixedPitch = 0; post.minMemType42 = 0; post.maxMemType42 = 0; post.minMemType1 = 0; post.maxMemType1 = 0
            tt['post'] = post
        if 'OS/2' not in tt:
            from fontTools.ttLib.tables.O_S_2f_2 import Panose
            os2 = newTable('OS/2'); os2.version = 4
            hhea = tt['hhea']
            for k, v in dict(xAvgCharWidth=500, usWeightClass=400, usWidthClass=5, fsType=0,
                             ySubscriptXSize=650, ySubscriptYSize=600, ySubscriptXOffset=0, ySubscriptYOffset=75,
                             ySuperscriptXSize=650, ySuperscriptYSize=600, ySuperscriptXOffset=0, ySuperscriptYOffset=350,
                             yStrikeoutSize=50, yStrikeoutPosition=250, sFamilyClass=0,
                             ulUnicodeRange1=1, ulUnicodeRange2=0, ulUnicodeRange3=0, ulUnicodeRange4=0,
                             achVendID='NONE', fsSelection=64, usFirstCharIndex=32, usLastCharIndex=0xFFFF,
                             sTypoAscender=hhea.ascent, sTypoDescender=hhea.descent, sTypoLineGap=hhea.lineGap,
                             usWinAscent=hhea.ascent, usWinDescent=abs(hhea.descent),
                             ulCodePageRange1=1, ulCodePageRange2=0, sxHeight=500, sCapHeight=700,
                             usDefaultChar=0, usBreakChar=32, usMaxContext=0).items():
                setattr(os2, k, v)
            os2.panose = Panose()
            tt['OS/2'] = os2
        saida = os.path.join(pasta, nome + '.ttf')
        tt.save(saida)
        fontes[nome] = (saida, set(cm.keys()))
    return fontes


def preencher(pdf, pagina, subs, saida):
    doc = pymupdf.open(pdf)
    idx = pagina - 1
    pasta = tempfile.mkdtemp(prefix='fonte-anexo-')
    fontes = reconstruir_fontes(doc, idx, pasta)
    out = pymupdf.open()
    out.insert_pdf(doc, from_page=idx, to_page=idx)
    pg = out[0]
    d = pg.get_text('dict')
    blocos = [b for b in d['blocks'] if b['type'] == 0]
    textos = [_normaliza(''.join(s['text'] for l in b['lines'] for s in l['spans'])) for b in blocos]
    pendentes = {_normaliza(k): v for k, v in subs.items()}
    # limite direito = margem do texto na pagina (maior x1 entre os blocos de corpo)
    xr = max(b['bbox'][2] for b in blocos if b['bbox'][0] < 100 and b['bbox'][1] > 150)
    # entrelinha padrao do corpo: menor distancia entre linhas de um mesmo paragrafo
    dist = [l2['bbox'][1] - l1['bbox'][1] for b in blocos for l1, l2 in zip(b['lines'], b['lines'][1:])]
    corpo_lh = min(dist) if dist else 14 * 1.38
    feitas = []
    # um paragrafo pode estar dividido em varios blocos consecutivos (uma linha por bloco)
    planos = []
    for chave, novo in list(pendentes.items()):
        achado = None
        for i in range(len(blocos)):
            acc = ''
            for j in range(i, len(blocos)):
                acc = (acc + ' ' + textos[j]).strip()
                if acc == chave:
                    achado = (i, j)
                    break
                if not chave.startswith(acc):
                    break
            if achado:
                break
        if not achado:
            raise SystemExit('Paragrafo nao encontrado na pagina: ' + chave[:80])
        planos.append((achado, chave, novo))
        pendentes.pop(chave)
    # Recomposicao do corpo. Cada paragrafo e re-escrito no lugar, com a mesma fonte e a mesma
    # entrelinha. Quando o texto preenchido ocupa mais linhas que o modelo, os paragrafos abaixo
    # descem o mesmo tanto, para que nada se sobreponha. Paragrafos acima do primeiro preenchido
    # nao sao tocados. Titulos (corpo diferente do texto) e o rodape ficam como estao.
    if not planos:
        out.save(saida, garbage=3, deflate=True)
        return []
    substituidos = {}
    for (i, j), chave, novo in planos:
        substituidos[i] = (j, novo, chave)
    corpo_size = blocos[planos[0][0][0]]['lines'][0]['spans'][0]['size']
    primeiro = min(p[0][0] for p in planos)
    ordem = sorted(range(len(blocos)), key=lambda k: blocos[k]['bbox'][1])
    delta = 0.0
    k = 0
    # medir a altura que um texto ocupa numa largura, com a fonte dada
    medidor = pymupdf.open(); mp = medidor.new_page(width=pg.rect.width, height=3000)

    def altura(texto, size, fpath, fnome, lh, largura, just):
        r = pymupdf.Rect(0, 0, largura, 2900)
        rc = mp.insert_textbox(r, texto, fontsize=size, fontname='F_' + fnome.replace('-', ''), fontfile=fpath,
                               lineheight=lh / size, align=just)
        usado = r.height - rc
        return max(1, round(usado / lh)) * lh

    # Passo 1: montar a lista de paragrafos do corpo, do primeiro preenchido para baixo.
    itens = []
    while k < len(ordem):
        bi = ordem[k]
        b = blocos[bi]
        span = b['lines'][0]['spans'][0]
        if b['bbox'][1] < blocos[primeiro]['bbox'][1] - 1 or span['size'] != corpo_size:
            k += 1
            continue
        if bi in substituidos:
            j, novo, chave = substituidos[bi]
            run = [blocos[x] for x in range(bi, j + 1)]
            k += (j - bi) + 1
            itens.append((run, novo, chave, span))
        else:
            k += 1
            itens.append(([b], ''.join(s['text'] for l in b['lines'] for s in l['spans']), None, span))
    # Passo 2: apagar todos esses paragrafos de uma vez (a redacao e feita antes de qualquer
    # insercao, para que um paragrafo deslocado nunca seja apagado pela redacao do seguinte).
    for run, texto, chave, span in itens:
        x0 = min(bb['bbox'][0] for bb in run); y0 = min(bb['bbox'][1] for bb in run); y1 = max(bb['bbox'][3] for bb in run)
        pg.add_redact_annot(pymupdf.Rect(x0 - 1, y0 - 2, xr + 2, y1 + 2), fill=(1, 1, 1))
    pg.apply_redactions(images=pymupdf.PDF_REDACT_IMAGE_NONE)
    # Passo 3: re-escrever cada paragrafo, deslocando para baixo o que vier depois de um
    # paragrafo que cresceu.
    for run, texto, chave, span in itens:
        size = span['size']
        color = span['color']
        rgb = (((color >> 16) & 255) / 255, ((color >> 8) & 255) / 255, (color & 255) / 255)
        fnome = span['font'].split('+')[-1]
        if fnome not in fontes:
            raise SystemExit(f'Fonte {fnome} nao pode ser reconstruida a partir do PDF.')
        fpath, chars = fontes[fnome]
        faltam = sorted({c for c in texto if ord(c) not in chars and not c.isspace()})
        if faltam:
            raise SystemExit(f'A fonte embutida nao tem os caracteres {faltam}. Ajuste o texto ou use outra grafia.')
        linhas = [l['bbox'][1] for bb in run for l in bb['lines']]
        lh = (linhas[1] - linhas[0]) if len(linhas) > 1 else corpo_lh
        x0 = min(bb['bbox'][0] for bb in run); y0 = min(bb['bbox'][1] for bb in run)
        just = pymupdf.TEXT_ALIGN_JUSTIFY if len(linhas) > 1 else 0
        h_antiga = len(linhas) * lh
        h_nova = altura(texto, size, fpath, fnome, lh, xr - x0, just)
        rc = pg.insert_textbox(pymupdf.Rect(x0, y0 - 2 + delta, xr, pg.rect.height - 40), texto, fontsize=size,
                               fontname='F_' + fnome.replace('-', ''), fontfile=fpath, color=rgb,
                               lineheight=lh / size, align=just)
        if rc < 0:
            raise SystemExit('O texto nao coube na pagina depois do preenchimento.')
        if chave is not None:
            delta += h_nova - h_antiga
            feitas.append((chave[:60], texto[:60]))
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
    print(f'{len(feitas)} paragrafo(s) preenchido(s) -> {a.saida}')


if __name__ == '__main__':
    main()
