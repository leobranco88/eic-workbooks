"""Gera blocos de múltipla escolha com as opções numa linha só (regra fundamental)."""
import pymupdf as fitz, re
CAR=fitz.Font(fontfile='/usr/share/fonts/truetype/crosextra/Carlito-Regular.ttf')
def linhas(pdf,pag,y0,y1):
    p=fitz.open(pdf)[pag-1]; out=[]
    for b in p.get_text('rawdict',clip=fitz.Rect(60,y0,545,y1))['blocks']:
        for l in b.get('lines',[]):
            t=''.join(c['c'] for s in l['spans'] for c in s['chars']).strip()
            if t: out.append((l['bbox'],t))
    return sorted(out,key=lambda x:x[0][1])
def mcq(fonte,pdf,partes,max_larg=440,gap=26,troca=None,**extra):
    troca=troca or {}
    """partes: [(pagina,y0,y1)] em ordem; a primeira começa no enunciado."""
    blocos=[]; primeiro=True
    for pag,y0,y1 in partes:
        ls=linhas(pdf,pag,y0,y1)
        itens=[]; cur=None
        for bb,t in ls:
            if abs(bb[0]-90)<3 and re.match(r'([1-9]|[A-E])\b',t):
                cur={'q':bb,'ops':[]}; itens.append(cur)
            elif abs(bb[0]-108)<3 and re.match(r'[a-e]\.',t) and cur:
                cur['ops'].append((bb,t))
        for k,it in enumerate(itens):
            ops=[re.sub(r'^[a-e]\.\s*','',t).strip() for _,t in it['ops']]
            ops=[troca.get(o,o) for o in ops]
            fs=10.98; ws=[CAR.text_length(o,fontsize=fs) for o in ops]
            pos=[];x=0
            for w in ws: pos.append(x); x+=18+w+gap
            seg=[]
            for j,(o,px) in enumerate(zip(ops,pos)):
                seg+= [[f'{"abcde"[j]}.','car',px],[o,'car',px+18]]
            seg[0]=[seg[0][0],'car']
            a_bb=it['ops'][0][0]; last_bb=it['ops'][-1][0]
            cabe = x-gap <= max_larg
            yb = a_bb[3]+3 if cabe else last_bb[3]+3
            fix=[{"de":it['ops'][0][1][:18],"x_inicio":108,"segmentos":seg}] if cabe else []
            if primeiro:
                b=dict(tipo='exercicio',fonte=fonte,pagina=pag,y0=y0,y1=yb,**extra); primeiro=False
            else:
                b=dict(tipo='continuacao',fonte=fonte,pagina=pag,y0=it['q'][1]-4,y1=yb)
            if fix: b['corrigir']=fix
            blocos.append(b)
    return blocos
