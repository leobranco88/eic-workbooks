"""Enche o pé da página do writing com mais linhas de resposta, no mesmo passo das originais,
e desce o score ("__/10") para a última linha. Uso:
    python estender_linhas.py prova.pdf [base=770]
Acha sozinho a página: a última com linhas de underscore (30+). Regrava o PDF no lugar."""
import sys, re, pymupdf as fitz
CARLITO = '/usr/share/fonts/truetype/crosextra/Carlito-Regular.ttf'
CARLITO_B = '/usr/share/fonts/truetype/crosextra/Carlito-Bold.ttf'
arq = sys.argv[1]; BASE = float(sys.argv[2]) if len(sys.argv) > 2 else 770
d = fitz.open(arq)
alvo = None
for p in d:
    ls = [s for b in p.get_text('dict')['blocks'] for l in b.get('lines', []) for s in l['spans']
          if re.fullmatch(r'_{30,}\s*', s['text'])]
    if ls: alvo = (p, ls)
p, ls = alvo
ls.sort(key=lambda s: s['origin'][1])
passo = ls[-1]['origin'][1] - ls[-2]['origin'][1] if len(ls) > 1 else 28.2
ult = ls[-1]; x, y = ult['origin']; txt = ult['text'].rstrip(); tam = ult['size']
sc = [s for b in p.get_text('dict')['blocks'] for l in b.get('lines', []) for s in l['spans']
      if re.fullmatch(r'\s*__/\d+\s*', s['text'])]
novas = 0
while y + passo + 4 <= BASE:
    y += passo
    p.insert_text((x, y), txt, fontname='carl', fontfile=CARLITO, fontsize=tam, color=(0, 0, 0)); novas += 1
if sc and novas:
    s = sc[-1]; r = fitz.Rect(s['bbox'])
    p.draw_rect(r + (-1, -1, 1, 1), color=None, fill=(1, 1, 1))
    p.insert_text((s['origin'][0], y), s['text'].strip(), fontname='carlb', fontfile=CARLITO_B,
                  fontsize=s['size'], color=(0, 0, 0))
d.saveIncr() if False else d.save(arq + '.tmp', garbage=3, deflate=True)
import os; os.replace(arq + '.tmp', arq)
print(f'{novas} linhas novas na página {p.number + 1} (passo {passo:.1f} pt)')
