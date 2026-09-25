"""Checkpoint por junção, modo GRADE (testes de uma coluna, ex.: Life / Cengage).

Os exercícios são recortados da página original como vetor (show_pdf_page com clip, 1:1)
e reorganizados em páginas novas, com quebra automática:
  - exercício estreito (conteúdo cabe em meia página) entra em DUAS COLUNAS, na ordem
    de leitura (coluna esquerda de cima para baixo, depois a direita), alturas balanceadas;
  - exercício largo (texto de leitura, figuras em linha, instrução longa) ocupa a largura toda.
Overlays: cabeçalho EIC no lugar da faixa da editora, renumeração corrida, scores das
seções recalculados (os "__/N" originais são mascarados) e número de página.

Uso: python montar_fluxo.py config.json   (formato em references/config-fluxo.md)
"""
import json, re, sys, pymupdf as fitz

cfg = json.load(open(sys.argv[1], encoding='utf-8'))
F = {k: fitz.open(v) for k, v in cfg['fontes'].items()}
A = cfg['area']; C = cfg['cores']; CAB = cfg['cabecalho']; FT = cfg['fontes_ttf']
W, H = 595.32, 841.92
SX0, SX1 = A['x0'], A['x1']                 # faixa útil do ORIGINAL (clip horizontal)
COLW = A.get('largura_coluna', 255)         # largura do clip de um exercício estreito
TX = A.get('x_destino', 28)                 # onde o clip começa na página nova
TX2 = TX + A.get('passo_coluna', 272)       # onde começa a coluna direita
TOPO, BASE = A['topo'], A['base']
GAP, GAP_TIT = A.get('gap', 14), A.get('gap_titulo', 18)
XSCORE = A['x_score']
hexrgb = lambda h: tuple(int(h[i:i + 2], 16) / 255 for i in (1, 3, 5))
logo = open(cfg['logo'], 'rb').read() if cfg.get('logo') else None
out = fitz.open()


def nova_pagina():
    p = out.new_page(width=W, height=H)
    for nome, arq in FT.items():
        p.insert_font(fontname=nome, fontfile=arq)
    r = cfg['rodape']                       # linha + copyright da editora (não se remove)
    p.show_pdf_page(fitz.Rect(0, r['y0'], W, r['y1']), F[r['fonte']], r['pagina'] - 1,
                    clip=fitz.Rect(0, r['y0'], W, r['y1']))
    hb = CAB.get('altura', 56)
    p.draw_rect(fitz.Rect(0, 0, W, hb), color=None, fill=hexrgb(C['faixa']))
    if C.get('filete'):
        p.draw_rect(fitz.Rect(0, hb, W, hb + 3), color=None, fill=hexrgb(C['filete']))
    p.insert_text((40, hb / 2 + 7), CAB['curso'], fontname='interxb', fontsize=17, color=hexrgb(C.get('texto_faixa', C['tinta'])))
    larg = fitz.get_text_length(CAB['curso'], fontname='helv', fontsize=17) * 1.02
    p.insert_text((40 + larg + 12, hb / 2 + 6), CAB['subtitulo'], fontname='intermd', fontsize=11.5,
                  color=hexrgb(C.get('texto_faixa', C['tinta'])))
    if CAB.get('marca'):                             # símbolo neutro da versão (círculo, triângulo...)
        mx = 40 + larg + 12 + fitz.get_text_length(CAB['subtitulo'], fontname='helv', fontsize=11.5) * 1.04 + 17
        my = hb / 2 + 2; r = 5.5; tinta = hexrgb(C.get('texto_faixa', C['tinta']))
        if CAB['marca'] == 'circulo':
            p.draw_circle((mx + r, my), r, color=None, fill=tinta)
        elif CAB['marca'] == 'triangulo':
            p.draw_polyline([(mx, my + r), (mx + 2 * r, my + r), (mx + r, my - r), (mx, my + r)], color=None, fill=tinta, closePath=True)
        elif CAB['marca'] == 'quadrado':
            p.draw_rect(fitz.Rect(mx, my - r, mx + 2 * r, my + r), color=None, fill=tinta)
    if logo:
        lh = CAB.get('logo_altura', 30)
        p.insert_image(fitz.Rect(W - 40 - lh * 1.915, (hb - lh) / 2, W - 40, (hb + lh) / 2), stream=logo)
    if CAB.get('selo'):                              # selo do checkpoint, à esquerda do logo
        sh = CAB.get('selo_altura', 44); lw = CAB.get('logo_altura', 30) * 1.915
        x1 = W - 40 - lw - CAB.get('selo_gap', 16)
        p.insert_image(fitz.Rect(x1 - sh, (hb - sh) / 2, x1, (hb + sh) / 2), filename=CAB['selo'])
    return p


def largura_conteudo(bl):
    p = F[bl['fonte']][bl['pagina'] - 1]
    clip = fitz.Rect(SX0, bl['y0'], SX1, bl['y1'])
    mx = 0
    for b in p.get_text('dict', clip=clip)['blocks']:
        if b['type'] == 1:
            mx = max(mx, b['bbox'][2]); continue
        for l in b['lines']:
            for s in l['spans']:
                if s['text'].strip() and not re.fullmatch(r'\s*__/\d+\s*', s['text']):
                    mx = max(mx, s['bbox'][2])
    for d in p.get_drawings():
        r = d['rect']
        if r.intersects(clip) and r.width < 400:
            mx = max(mx, r.x1)
    return mx


def colar(p, bl, tx, ty, largo, numero_novo=None):
    src, pno = F[bl['fonte']], bl['pagina'] - 1
    x1 = SX1 if largo else SX0 + COLW
    clip = fitz.Rect(SX0, bl['y0'], x1, bl['y1'])
    dx, dy = tx - SX0, ty - bl['y0']
    p.show_pdf_page(fitz.Rect(tx, ty, tx + clip.width, ty + clip.height), src, pno, clip=clip)
    orig = None
    for b in src[pno].get_text('rawdict', clip=clip)['blocks']:
        for l in b.get('lines', []):
            for s in l['spans']:
                txt = ''.join(c['c'] for c in s['chars'])
                r = fitz.Rect(s['bbox'])
                if re.fullmatch(r'\s*__/\d+\s*', txt):          # score original: sai
                    p.draw_rect(fitz.Rect(r.x0 + dx - 1, r.y0 + dy - 1, r.x1 + dx + 1, r.y1 + dy + 1),
                                color=None, fill=(1, 1, 1))
                if numero_novo is not None and orig is None and abs(r.x0 - bl.get('x_numero', 72)) < 3 \
                        and r.y0 < bl['y0'] + 30 and 'Bold' in s['font']:
                    m = re.match(r'\s*(\d+)', txt)
                    if m:
                        ch = [c for c in s['chars'] if c['c'].isdigit()][:len(m.group(1))]
                        cr = fitz.Rect(ch[0]['bbox']) | fitz.Rect(ch[-1]['bbox'])
                        p.draw_rect(fitz.Rect(cr.x0 + dx - .5, cr.y0 + dy - .5, cr.x1 + dx + .8, cr.y1 + dy + .5),
                                    color=None, fill=(1, 1, 1))
                        # espaço livre até o próximo elemento da linha (texto, ícone de áudio, desenho)
                        prox = [fitz.Rect(s2['bbox']).x0 for s2 in l['spans']
                                if fitz.Rect(s2['bbox']).x0 > cr.x1 + .5 and ''.join(c2['c'] for c2 in s2['chars']).strip()]
                        faixa = fitz.Rect(cr.x1 + .5, cr.y0, cr.x1 + 40, cr.y1)
                        for d_ in src[pno].get_drawings():
                            if d_['rect'].intersects(faixa): prox.append(d_['rect'].x0)
                        for im in src[pno].get_image_info():
                            if fitz.Rect(im['bbox']).intersects(faixa): prox.append(im['bbox'][0])
                        livre = (min(prox) - cr.x0 - 2) if prox else 99
                        fs = s['size']
                        larg = fitz.Font(fontfile=FT['carb']).text_length(str(numero_novo), fontsize=fs)
                        xn = cr.x0
                        if larg > livre: xn = cr.x1 - larg   # sem espaço à direita: alinha pela direita (como " 9" / "10")
                        p.insert_text((xn + dx, ch[0]['origin'][1] + dy), str(numero_novo),
                                      fontname='carb', fontsize=fs, color=(0, 0, 0))
                        orig = m.group(1)
    for fix in bl.get('corrigir', []):                           # erro do livro: reescreve a linha
        for b in src[pno].get_text('rawdict', clip=clip)['blocks']:
            for l in b.get('lines', []):
                txt = ''.join(c['c'] for s_ in l['spans'] for c in s_['chars'])
                if fix['de'] in txt:
                    lb = fitz.Rect(l['bbox']); sp0 = l['spans'][0]
                    by = sp0['chars'][0]['origin'][1] + dy; x = fix.get('x_inicio', lb.x0) + dx
                    fnt = fitz.Font(fontfile=FT['car']); x_fim = x + sum(fnt.text_length(sg[0], fontsize=sp0['size']) for sg in fix['segmentos']) + 18 * any(len(sg) > 2 for sg in fix['segmentos'])
                    p.draw_rect(fitz.Rect(x - .5, lb.y0 + dy - .5, max(lb.x1 + dx + 1.5, x_fim + 1), lb.y1 + dy + .5),
                                color=None, fill=(1, 1, 1))
                    x0l = x
                    for seg in fix['segmentos']:
                        texto, fonte = seg[0], seg[1]
                        if len(seg) > 2: x = x0l + seg[2]          # posição fixa (ex.: texto do item alinhado)
                        p.insert_text((x, by), texto, fontname=fonte, fontsize=sp0['size'], color=(0, 0, 0))
                        x += fitz.Font(fontfile=FT[fonte]).text_length(texto, fontsize=sp0['size'])
    return orig



# ======================================================================================
# Modo GRADE: cada exercício é uma faixa na largura toda. O enunciado vai em cima; os
# itens (1, 2, 3... ou A, B, C...) entram numa grade de 1 a 3 colunas, lida por linha,
# conforme a largura do maior item. Exercícios nunca dividem colunas entre si, e o
# espaço vazio entre itens do original é aparado.
# ======================================================================================
GUT = A.get('entre_colunas', 18)          # espaço entre colunas da grade
IND = A.get('recuo_itens', 18)            # recuo dos itens em relação ao enunciado
XI = A.get('x_item_origem', 84)           # onde o clip de um item começa no original
GAP_ITEM = A.get('gap_item', 10)
UTIL = W - 2 * TX                          # largura útil


def conteudo(src_pg, clip):
    """Retângulo real ocupado (texto, imagem e desenhos) dentro do clip."""
    r = fitz.Rect()
    for b in src_pg.get_text('dict', clip=clip)['blocks']:
        if b['type'] == 1:
            r |= fitz.Rect(b['bbox']) & clip; continue
        for l in b['lines']:
            for s in l['spans']:
                if s['text'].strip() and not re.fullmatch(r'\s*__/\d+\s*', s['text']):
                    r |= fitz.Rect(s['bbox'])
    for d in src_pg.get_drawings():
        if d['rect'].intersects(clip) and d['rect'].width < 450:
            r |= (d['rect'] & clip)
    return r


def pedacos_exercicio(blocos):
    """Enunciado + itens de um exercício (blocos: exercicio + continuacoes)."""
    enun, itens_ = None, []
    for k, bl in enumerate(blocos):
        ys = cortes(bl)
        if k == 0 and bl.get('fim_enunciado'): ys = [bl['fim_enunciado']]   # itens sem rótulo à esquerda (foto + rótulo)
        pg = F[bl['fonte']][bl['pagina'] - 1]
        ini = [bl['y0']] + ys if k == 0 else ([bl['y0']] + ys if not ys or ys[0] > bl['y0'] + 6 else ys)
        fins = ini[1:] + [bl['y1']]
        for j, (a, b) in enumerate(zip(ini, fins)):
            if b - a < 6: continue
            c = conteudo(pg, fitz.Rect(SX0, a, SX1, b))
            if c.is_empty: continue
            p_ = dict(bl, y0=a, y1=min(b, c.y1 + 4))
            p_['w'] = c.x1 - XI
            p_['h'] = p_['y1'] - p_['y0']
            if k == 0 and j == 0 and ys:
                enun = p_
            else:
                itens_.append(p_)
    return enun, itens_


def cortes(bl):
    p = F[bl['fonte']][bl['pagina'] - 1]
    clip = fitz.Rect(SX0, bl['y0'], SX1, bl['y1'])
    ys = []
    for b in p.get_text('dict', clip=clip)['blocks']:
        if b['type'] != 0: continue
        for l in b['lines']:
            sp = [s for s in l['spans'] if s['text'].strip()]
            if not sp: continue
            x0 = sp[0]['bbox'][0]; t = sp[0]['text'].strip()
            if abs(x0 - bl.get('x_item', 90)) < 3 and re.fullmatch(r'([1-9]|[A-E])(\s.*)?', t):
                ys.append(round(l['bbox'][1] - 4, 1))
    return sorted(set(y for y in ys if y > bl['y0'] + 2))


def colar_item(p, it, tx, ty):
    src, pno = F[it['fonte']], it['pagina'] - 1
    clip = fitz.Rect(XI, it['y0'], XI + it['wcol'], it['y1'])
    p.show_pdf_page(fitz.Rect(tx, ty, tx + clip.width, ty + clip.height), src, pno, clip=clip)
    dx, dy = tx - XI, ty - it['y0']
    for b in src[pno].get_text('rawdict', clip=clip)['blocks']:
        for l in b.get('lines', []):
            for s in l['spans']:
                txt = ''.join(c['c'] for c in s['chars']); r = fitz.Rect(s['bbox'])
                if re.fullmatch(r'\s*__/\d+\s*', txt):
                    p.draw_rect(fitz.Rect(r.x0 + dx - 1, r.y0 + dy - 1, r.x1 + dx + 1, r.y1 + dy + 1), color=None, fill=(1, 1, 1))
    corrigir_linhas(p, it, clip, dx, dy)


def corrigir_linhas(p, bl, clip, dx, dy):
    src, pno = F[bl['fonte']], bl['pagina'] - 1
    for fix in bl.get('corrigir', []):
        for b in src[pno].get_text('rawdict', clip=clip)['blocks']:
            for l in b.get('lines', []):
                txt = ''.join(c['c'] for s_ in l['spans'] for c in s_['chars'])
                if fix['de'] in txt:
                    lb = fitz.Rect(l['bbox']); sp0 = l['spans'][0]
                    by = sp0['chars'][0]['origin'][1] + dy; x = fix.get('x_inicio', lb.x0) + dx
                    fnt = fitz.Font(fontfile=FT['car']); x_fim = x + sum(fnt.text_length(sg[0], fontsize=sp0['size']) for sg in fix['segmentos']) + 18 * any(len(sg) > 2 for sg in fix['segmentos'])
                    p.draw_rect(fitz.Rect(x - .5, lb.y0 + dy - .5, max(lb.x1 + dx + 1.5, x_fim + 1), lb.y1 + dy + .5), color=None, fill=(1, 1, 1))
                    x0l = x
                    for seg in fix['segmentos']:
                        texto, fonte = seg[0], seg[1]
                        if len(seg) > 2: x = x0l + seg[2]          # posição fixa (ex.: texto do item alinhado)
                        p.insert_text((x, by), texto, fontname=fonte, fontsize=sp0['size'], color=(0, 0, 0))
                        x += fitz.Font(fontfile=FT[fonte]).text_length(texto, fontsize=sp0['size'])


# ---------- monta a lista de faixas ----------
faixas = []          # cada faixa: {'tipo': 'solto'|'ex'|'score', ...}
atual = None
for bl in cfg['blocos']:
    if bl['tipo'] == 'continuacao' and atual is not None:
        atual['blocos'].append(bl); continue
    if bl['tipo'] == 'exercicio':
        atual = {'tipo': 'ex', 'blocos': [bl], 'prende': bl.get('prende', False)}
        faixas.append(atual); continue
    atual = None
    if bl['tipo'] == 'score':
        faixas.append({'tipo': 'score', 'texto': bl['texto']})
    else:
        pg = F[bl['fonte']][bl['pagina'] - 1]
        c = conteudo(pg, fitz.Rect(SX0, bl['y0'], SX1, bl['y1']))
        y1 = min(bl['y1'], c.y1 + 4) if not c.is_empty else bl['y1']
        faixas.append({'tipo': 'solto', 'bl': dict(bl, y1=y1), 'h': y1 - bl['y0'],
                       'prende': bl['tipo'] == 'titulo' or bl.get('prende', False)})

CAP_ = BASE - TOPO - 2
for f in faixas:
    if f['tipo'] != 'ex': continue
    enun, its = pedacos_exercicio(f['blocos'])
    f['enun'] = enun
    wmax = max(it['w'] for it in its)
    livre = UTIL - IND
    ncol = max(1, min(A.get('max_colunas', 3), int((livre + GUT) // (wmax + GUT + 4))))
    ncol = min(ncol, f['blocos'][0].get('colunas', ncol), len(its))
    if any(re.search(r'(^|\s)[a-h]\)\s', F[it['fonte']][it['pagina'] - 1].get_text(clip=fitz.Rect(SX0, it['y0'], SX1, it['y1'])))
           for it in its):
        ncol = 1                                   # exercício de associar (a), b)...): uma coluna, pares na mesma linha
    if f['blocos'][0].get('colunas_forcar'):        # largura medida no original ficou maior que o texto corrigido
        ncol = f['blocos'][0]['colunas_forcar']
    wcol = (livre - GUT * (ncol - 1)) / ncol
    for it in its: it['wcol'] = min(wcol, SX1 - XI)
    linhas = [its[k:k + ncol] for k in range(0, len(its), ncol)]
    f['ncol'], f['wcol'], f['linhas'] = ncol, wcol, linhas
    f['h_linhas'] = [max(it['h'] for it in ln) for ln in linhas]
    f['h_enun'] = enun['h'] if enun else 0
    f['gap'] = GAP_ITEM
    f['h'] = f['h_enun'] + 4 + sum(f['h_linhas']) + GAP_ITEM * (len(linhas) - 1)
    # um pouco maior que a página: aperta o espaço entre linhas para caber inteiro
    if f['h'] > CAP_ and len(linhas) > 1:
        sem_gap = f['h'] - GAP_ITEM * (len(linhas) - 1)
        if sem_gap + 2 * (len(linhas) - 1) <= CAP_:
            f['gap'] = min(GAP_ITEM, (CAP_ - sem_gap) / (len(linhas) - 1))
            f['h'] = sem_gap + f['gap'] * (len(linhas) - 1)

for k, f in enumerate(faixas):
    if f['tipo'] == 'score' and k > 0: faixas[k - 1]['cola_score'] = True

CAP = BASE - TOPO
SPLIT = cfg.get('quebrar_exercicios', False)
import itertools


class Paginador:
    """Faz a paginação. Com desenhar=False só simula (para escolher a ordem dos exercícios)."""

    def __init__(self, faixas, desenhar):
        self.fx, self.d = faixas, desenhar
        self.pags = 0; self.pag = None; self.y = TOPO; self.n = 0; self.rel = []
        self.ult = None                      # (y do topo da última linha, altura, x direito ocupado)
        self.quebra()

    def quebra(self):
        self.pags += 1; self.y = TOPO
        self.pag = nova_pagina() if self.d else None

    def altura_com_cola(self, k):
        f = self.fx[k]
        h = f.get('h', 16)
        if f.get('prende') and k + 1 < len(self.fx):
            nx = self.fx[k + 1]
            if nx['tipo'] == 'ex':
                parcial = nx['h_enun'] + 4 + sum(nx['h_linhas'][:2]) + GAP_ITEM
                hx = nx['h'] if nx['h'] <= CAP and not SPLIT else min(nx['h'], parcial)
                g = nx['blocos'][0].get('grupo')
                if cfg.get('grupo_na_mesma_pagina') and g:          # título vai junto com o grupo do mesmo áudio
                    tot, j = 0, k + 1
                    while j < len(self.fx) and self.fx[j].get('tipo') == 'ex' and self.fx[j]['blocos'][0].get('grupo') == g:
                        tot += self.fx[j]['h'] + (GAP if j > k + 1 else 0); j += 1
                    if tot <= CAP: hx = max(hx, tot)
                h += 6 + hx   # texto de leitura/título vão com o exercício INTEIRO
            else:
                h += 6 + self.altura_com_cola(k + 1)
        return h

    def exercicio(self, f):
        self.n += 1; orig = None
        if f['enun']:
            if self.d: orig = colar(self.pag, f['enun'], TX, self.y, True, self.n)
            self.y += f['enun']['h'] + 4
        for li, ln in enumerate(f['linhas']):
            hl = f['h_linhas'][li]; rest = len(f['linhas']) - li
            if self.y + hl > BASE: self.quebra()
            if rest == 2 and self.y + hl + f['gap'] + f['h_linhas'][li + 1] > BASE and li >= 2 and self.y > TOPO:
                self.quebra()
            xdir = 0
            for ci, it in enumerate(ln):
                tx = TX + IND + ci * (f['wcol'] + GUT)
                xdir = max(xdir, tx + it['w'])
                if not self.d: continue
                if orig is None and not f['enun'] and li == 0 and ci == 0:
                    orig = colar(self.pag, it, tx - (XI - SX0), self.y, True, self.n)
                else:
                    colar_item(self.pag, it, tx, self.y)
            self.ult = (self.y, hl, xdir)
            self.y += hl + f['gap']
        self.y += GAP - f['gap']
        if self.d:
            self.rel.append(f'ex {self.n:>2} = {f["blocos"][0]["fonte"]} ex {orig}  (p{len(out)}, {f["ncol"]} col.)')

    def score(self, f):
        t = f['texto']; pw = fitz.get_text_length(t, fontname='hebo', fontsize=11)
        # na linha do último item, à direita (como no original), se houver espaço livre
        if self.ult and self.ult[2] < XSCORE - pw - 12:
            yb = self.ult[0] + self.ult[1] - 3
            if self.d: self.pag.insert_text((XSCORE - pw, yb), t, fontname='carb', fontsize=11, color=(0, 0, 0))
            self.y += GAP_TIT - GAP
        else:
            if self.y + 16 > BASE: self.quebra()
            if self.d: self.pag.insert_text((XSCORE - pw, self.y + 11), t, fontname='carb', fontsize=11, color=(0, 0, 0))
            self.y += 16 + GAP_TIT
        self.ult = None

    def rodar(self, ate=None):
        for k, f in enumerate(self.fx[:ate]):
            if f['tipo'] == 'score':
                self.score(f); continue
            need = self.altura_com_cola(k)
            if f['tipo'] == 'ex':
                if f['h'] <= CAP and (not SPLIT or f['blocos'][0].get('inteiro')): need = max(need, f['h'])
                else: need = min(f['h'], f['h_enun'] + 4 + sum(f['h_linhas'][:2]) + GAP_ITEM)
                g = f['blocos'][0].get('grupo')
                if cfg.get('grupo_na_mesma_pagina') and g and not (k and self.fx[k - 1].get('tipo') == 'ex'
                                                                   and self.fx[k - 1]['blocos'][0].get('grupo') == g):
                    tot, j = 0, k                  # mesmo áudio: o grupo inteiro começa na mesma página
                    while j < len(self.fx) and self.fx[j].get('tipo') == 'ex' and self.fx[j]['blocos'][0].get('grupo') == g:
                        tot += self.fx[j]['h'] + (GAP if j > k else 0); j += 1
                    if tot <= CAP: need = max(need, tot)
            if self.y + need > BASE and self.y > TOPO: self.quebra()
            elif f['tipo'] == 'solto' and f['bl'].get('nova_pagina') and self.y > TOPO: self.quebra()   # seção abre página
            self.ult = None
            if f['tipo'] == 'solto':
                if self.d:
                    colar(self.pag, f['bl'], TX, self.y, True)
                    if f['bl'].get('icone'):            # figurinha da seção, logo depois do título
                        bl = f['bl']; pgs = F[bl['fonte']][bl['pagina'] - 1]
                        c = conteudo(pgs, fitz.Rect(SX0, bl['y0'], SX1, bl['y1']))
                        xs = [ch['bbox'][2] for b_ in pgs.get_text('rawdict', clip=fitz.Rect(SX0, bl['y0'], SX1, bl['y1']))['blocks']
                              for l_ in b_.get('lines', []) for s_ in l_['spans'] for ch in s_['chars'] if ch['c'].strip()]
                        if xs: c.x1 = max(xs)                   # fim da última letra, sem os espaços
                        dx, dy = TX - SX0, self.y - bl['y0']
                        ih = A.get('icone_altura', 24)
                        cy = (c.y0 + c.y1) / 2 + dy
                        x0 = c.x1 + dx + A.get('icone_gap', 7)
                        self.pag.insert_image(fitz.Rect(x0, cy - ih / 2 - 1, x0 + ih * 1.5, cy + ih / 2 - 1),
                                              filename=bl['icone'], keep_proportion=True)
                self.y += f['h'] + (6 if f['prende'] else GAP)
            else:
                self.exercicio(f)
        return self.pags, self.y


# ---------- escolhe a ordem dos exercícios dentro de cada seção ----------
# A ordem entre seções é fixa; dentro de cada seção, testa as permutações dos exercícios
# (os blocos soltos, como título e texto de leitura, ficam no lugar) e fica com a que
# termina a seção na página mais cedo e mais acima. Desligue com "ordem_livre": false.
if cfg.get('ordem_livre', True):
    secoes, ini = [], 0
    for k, f in enumerate(faixas):
        if f['tipo'] == 'score':
            secoes.append((ini, k)); ini = k + 1
    for a, b in secoes:
        idx = [k for k in range(a, b) if faixas[k]['tipo'] == 'ex']
        if len(idx) < 2 or len(idx) > 6: continue
        exs = [faixas[k] for k in idx]
        melhor = None
        for perm in itertools.permutations(exs):
            tent = list(faixas)
            for k, e in zip(idx, perm): tent[k] = e
            primeiro = tent[idx[0]]
            if primeiro['h'] > CAP - 40: continue            # não abre seção com exercício de página cheia
            # exercícios do mesmo "grupo" (ex.: mesmo áudio) ficam juntos e na ordem original
            ok = True
            for gname in {e['blocos'][0].get('grupo') for e in perm} - {None}:
                pos = [n for n, e in enumerate(perm) if e['blocos'][0].get('grupo') == gname]
                orig_ = [e for e in exs if e['blocos'][0].get('grupo') == gname]
                if pos != list(range(pos[0], pos[0] + len(pos))) or [perm[n] for n in pos] != orig_:
                    ok = False
            if not ok: continue
            r = Paginador(tent, False).rodar(b + 1)
            chave = (r[0], r[1])
            if melhor is None or chave < melhor[0]: melhor = (chave, perm)
        if melhor:
            for k, e in zip(idx, melhor[1]): faixas[k] = e

pg = Paginador(faixas, True)
pg.rodar()
tot = len(out)
for k, p in enumerate(out, 1):
    p.insert_text((W - 40 - 24, 818), f'{k} / {tot}', fontname='intermd', fontsize=8, color=hexrgb(C.get('numero_pagina', C['tinta'])))
out.set_metadata({'title': cfg.get('titulo_pdf', ''), 'author': 'EIC'})
out.save(cfg['saida'], garbage=4, deflate=True)
print('\n'.join(pg.rel)); print(f'{tot} páginas · salvo em {cfg["saida"]}')
