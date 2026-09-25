import base64, glob, html as H, re, sys, json, os, importlib
b64=lambda p: base64.b64encode(open(p,'rb').read()).decode()
D=importlib.import_module(sys.argv[1]); VER=sys.argv[2] if len(sys.argv)>2 else 'complete'
CP=D.CP; UA,UB=D.UNITS; UN=f'Units {UA}-{UB}'
TURMA=getattr(D,'TURMA','Teens 1'); TAG=TURMA.replace(' ','')          # Teens 2 em diante: definir no módulo de dados
FUNDO=getattr(D,'COR_FUNDO','#ECEBE6'); LINHA=getattr(D,'COR_LINHA','#D6D4CC')   # fundo do painel e filetes
COR=getattr(D,'COR','#FFD60A'); COR_PRETO=getattr(D,'COR_SOBRE_PRETO',None) or getattr(D,'COR','#FFD60A'); COR_TXT=getattr(D,'COR_TEXTO','#0A0A0F')  # cor da turma e texto sobre ela
ICONES=getattr(D,'ICONES','icons')   # figurinhas da turma
SCRIPTS=getattr(D,'SCRIPTS','/home/claude/t1/scripts_teens1.json')
BASE=f'Checkpoint{CP}_{TAG}_U{UA}-U{UB}'
V={'complete':{'pdf':BASE+'.pdf','html':BASE+'.html','map':D.DIR+'/map_complete.txt','nome':'Complete','marca':'●','minutos':80,
               'pts':D.PTS['complete']},
   'speed':{'pdf':BASE+'_Speed.pdf','html':BASE+'_Speed.html','map':D.DIR+'/map_speed.txt','nome':'Speed','marca':'▲','minutos':50,
               'pts':D.PTS['speed']}}[VER]
OUTRA={'complete':(BASE+'_Speed.html','▲ Speed'),'speed':(BASE+'.html','● Complete')}[VER]
DICT_PDF=f'Checkpoint{CP}_{TAG}_Dictation.pdf'
MAPA=[]
for l in open(V['map']):
    m=re.match(r'ex\s+(\d+) = (U\d+x?) ex (\d+)\s+\(p(\d+)',l)
    if m: MAPA.append((int(m.group(1)),f'{m.group(2)}-{m.group(3)}',int(m.group(4))))
NUM={o:n for n,o,p in MAPA}; PAG={o:p for n,o,p in MAPA}
def nums(origs): return sorted(NUM[o] for o in origs if o in NUM)
def fmt(ns): return ', '.join(map(str,ns[:-1]))+(' e ' if len(ns)>1 else '')+str(ns[-1]) if ns else ''
W=D.W
NSPEED=sum(D.PTS['speed'].values())
TR=[(lab,f,ids) for lab,f,ids in D.TRACKS]
_SCR=json.load(open(SCRIPTS))
def _sid(f): return os.path.basename(f).replace('life3e_ame_L1_asmt_','').replace('life3e_ame_L2_asmt_','').replace('.mp3','')
_scr=[]
for lab,f,ids in D.TRACKS:
    d=dict(_SCR.get(_sid(f),{'cast':[],'linhas':[]}))
    if d.get('aviso'):
        o=d.get('aviso_ex'); d['aviso']=d['aviso'].format(n=NUM[o]) if o in NUM else None
    _scr.append(d)
SCR_JSON=json.dumps(_scr, ensure_ascii=False)
TR_ON=[any(i in NUM for i in ids) for lab,f,ids in TR]
t1='data:audio/mpeg;base64,'+b64(TR[0][1]) if TR_ON[0] else ''
t2='data:audio/mpeg;base64,'+b64(TR[1][1]) if TR_ON[1] else ''
def _dur(f):                                   # duração da primeira faixa, antes do áudio carregar
    import subprocess
    try: d=float(subprocess.run(['ffprobe','-v','quiet','-show_entries','format=duration','-of','csv=p=0',f],capture_output=True,text=True).stdout)
    except Exception: return '0:00'
    return f'{int(d//60)}:{int(round(d%60)):02d}'
DUR0=_dur(TR[0][1] if TR_ON[0] else TR[1][1])
LBL=[lab for lab,f,ids in TR]
EXS=[fmt(nums(ids)) for lab,f,ids in TR]
PG_TR=[min((PAG[i] for i in ids if i in PAG),default=1) for lab,f,ids in TR]
pages=sorted(glob.glob(f'{D.DIR}/html/{VER}/pg-*.png'), key=lambda f:int(f.split('-')[-1][:-4]))
imgs='\n'.join(f'<img id="p{i}" alt="Page {i}" src="data:image/png;base64,{b64(p)}">' for i,p in enumerate(pages,1))

# ---------- answer key (numeração do checkpoint) ----------
ANS=D.ANS; LONGO=D.LONGO; SECAO=D.SECAO
def ak_html():
    out=''
    ordem=sorted(SECAO.items(), key=lambda kv: min([NUM[o] for o in kv[1] if o in NUM] or [999]))   # seções na ordem da prova
    for sec,origs in ordem:
        exs=sorted((NUM[o],o) for o in origs if o in NUM)
        if not exs: continue
        rows=''
        for n,o in exs:
            ans=ANS[o]; lis=''.join(f'<li>{a}</li>' for a in ans)
            tag='ul' if ans[0][:2]=='A ' else 'ol'
            if tag=='ul': lis=''.join(f'<li><b>{a[0]}</b> {a[2:]}</li>' for a in ans)
            rows+=f'<div class="kex"><b>{n}</b><{tag} class="{"one" if o in LONGO else ""}">{lis}</{tag}></div>'
        out+=f'<div class="ksec"><h3>{sec}<span>/{V["pts"][sec]}</span></h3>{rows}</div>'
    if W in NUM:
        out+=f'<div class="ksec"><h3>Writing<span>/10</span></h3><div class="kex"><b>{NUM[W]}</b><p>Resposta pessoal. Corrigir pela rubrica abaixo (5 critérios de 0 a 2).</p></div></div>'
    return out
def mapa_html():
    return ' · '.join(f'{n} = {o.replace("-"," ex. ")}' for n,o,p in MAPA)

# ---------- rubric (bilíngue, inglês por cima) ----------
def P(en,pt): return f'{en}<span class="pt">{pt}</span>'
RUB=D.RUB
def rub_html():
    rules=[P('<b>One point per item, no half points.</b>','<b>Um ponto por item, sem meio ponto.</b>'),
           P(f'<b>When the item is the form of the word, spelling counts</b> (ex. {fmt(nums(D.GRAFIA))}).','<b>Quando o item é a forma da palavra, a grafia conta.</b>'),
           P('<b>Contracted and full forms are equal.</b> Capital letters and punctuation never lose points, except in the writing (criterion 4).','<b>Contração e forma cheia valem igual.</b> Maiúscula e pontuação não descontam, exceto no writing (critério 4).'),
           P('<b>Two options marked, or an unclear letter, score zero.</b>','<b>Duas opções marcadas, ou letra ilegível, não pontuam.</b>')]
    if W not in NUM:
        rules[2]=P('<b>Contracted and full forms are equal.</b> Capital letters and punctuation never lose points.','<b>Contração e forma cheia valem igual.</b> Maiúscula e pontuação não descontam.')
    out='<div class="rules">'+''.join(f'<p>{r}</p>' for r in rules)+'</div>'
    if VER=='speed':
        conv=''.join(f'<td><b>{k}</b>{round(k*100/NSPEED)}</td>' for k in range(0,NSPEED+1))
        linhas=''.join('<tr>'+''.join(f'<td><b>{k}</b>{round(k*100/NSPEED)}</td>' for k in range(i,min(i+12,NSPEED+1)))+'</tr>' for i in range(0,NSPEED+1,12))
        out+=f'<div class="rsec"><h3>Speed version: grade<span class="pt inl">Versão Speed: nota</span><em>{NSPEED} items → 100</em></h3><p class="intro">{P(f"Count the correct items (1 point each, {NSPEED} in total) and convert: grade = correct × 100 ÷ {NSPEED}, rounded.",f"Conte os acertos ({NSPEED} itens) e converta pela tabela: acertos em cima, nota embaixo.")}</p><div class="wrapt"><table class="convt">{linhas}</table></div></div>'
    for en,pt,rows in RUB:
        rows=[(fmt(nums(o)),a,b) for o,a,b in sorted(rows, key=lambda r: min(nums(r[0]) or [999])) if nums(o)]
        if not rows: continue
        pts=V['pts'][en]
        tr=''.join(f'<tr><td class="rn">{n}</td><td>{a}</td><td class="acc">{b}</td></tr>' for n,a,b in rows)
        out+=f'<div class="rsec"><h3>{en}<span class="pt inl">{pt}</span><em>{pts} points</em></h3><table class="rt"><colgroup><col style="width:62px"><col style="width:46%"><col></colgroup><tr><th>Ex.</th><th>{P("What counts","O que conta")}</th><th>{P("Also accept","Aceitar também")}</th></tr>{tr}</table></div>'
    if W not in NUM: return out
    WN=NUM[W]
    crit=D.WCRIT
    tr=''.join(f'<tr><td class="rn">{i}</td><td class="cn">{P(a,b)}</td><td>{P(c,d)}</td><td>{P(e,f)}</td><td>{P("Doesn’t do it.","Não faz.")}</td></tr>' for i,(a,b,c,d,e,f) in enumerate(crit,1))
    out+=f'''<div class="rsec"><h3>Writing<span class="pt inl">Produção escrita</span><em>10 points</em></h3>
    <p class="intro">{P(D.WINTRO[0].format(WN=WN),D.WINTRO[1].format(WN=WN))}</p>
    <table class="rt crit"><colgroup><col style="width:30px"><col style="width:170px"><col><col><col style="width:90px"></colgroup><tr><th></th><th>{P("Criterion","Critério")}</th><th>{P("2 points","2 pontos")}</th><th>{P("1 point","1 ponto")}</th><th>0</th></tr>{tr}</table></div>'''
    return out

WORDS=D.WORDS; QUEST=D.QUEST; SENT=D.SENT
DOPC=' <b>Na versão Speed, a parte D é opcional: use só se sobrar tempo.</b>' if (VER=='speed' and getattr(D,'SPEED_D_OPCIONAL',False)) else ''
def dict_html():
    w=''.join(f'<li><span class="rv">{a}</span><em>{u}</em></li>' for a,u in WORDS)
    s=''.join(f'<li><span class="rv">{x}</span></li>' for x in SENT)
    sp=''.join(f'<li><span class="qq">{q}</span><span class="rv">{a}</span><em>{h}</em></li>' for q,a,h in QUEST)
    return f'''<div class="dnote">Diagnóstico: o ditado <b>não vale nota</b> e não entra nos 100 pontos. Isso não aparece na folha do aluno.
    Os áudios das palavras e das frases ficam no player do topo, no botão <b>Dictation</b>: toque cada palavra duas vezes e cada frase três vezes. A parte C são 4 perguntas para responder; a parte D é livre, conduzida pelo professor. Esta aba é a referência para a correção. Anote os erros por padrão
    ({D.DICT_ERROS}) para o plano de reforço.</div>
    <div class="dcols"><div><h4>A · Words</h4><ol class="dw">{w}</ol></div><div><h4>B · Sentences</h4><ol class="ds">{s}</ol></div></div>
    <div class="dsp"><h4>C · Questions</h4><p class="dhow">O aluno ouve cada pergunta (player do topo, botão Dictation, C1 a C4) e escreve a resposta ao lado. <b>Vale qualquer resposta verdadeira que responda à pergunta com a estrutura da unidade.</b> As respostas abaixo são só modelo.</p><ol class="dsl">{sp}</ol></div>
    <div class="dsp"><h4>D · Parte do professor</h4><p class="dhow">Três linhas livres, feitas com a turma: use para o que ela precisar naquele dia (soletrar nomes, palavras extras, uma pergunta de revisão). A folha avisa o aluno: <i>Your teacher is going to do this part with you.</i> Anote o que foi feito, para o reforço.{DOPC}</p></div>'''

import json
def soletrar(x):
    out=[]
    for ch in x:
        if ch=='.': out.append('dot')
        elif ch=='@': out.append('at')
        elif ch=='-': continue
        elif ch.lower()=='a': out.append('ay')       # 'A' sozinho a voz lê como artigo
        elif ch.lower()=='q': out.append('cue')      # 'Q' sozinho a voz lê errado
        else: out.append(ch.upper() if ch.isalpha() else ch)
    return out
DJ={f'w{i}':w for i,(w,u) in enumerate(WORDS)}
DJ.update({f's{i}':x.replace('’',"'") for i,x in enumerate(SENT)})
DJ.update({f'c{i}':q.replace('’',"'") for i,(q,a,h) in enumerate(QUEST)})
DICT_JSON=json.dumps(DJ,ensure_ascii=False)
# áudios do ElevenLabs (pacote do gerador). Na parte C só entram perguntas.
import os
AUDJ={}
PACOTE=D.PACK
if os.path.exists(PACOTE):
    pk=json.load(open(PACOTE))['audios']
    mapa={**{f'A{i+1:02d}':f'w{i}' for i in range(10)},**{f'B{i+1}':f's{i}' for i in range(4)},**{f'C{i+1}':f'c{i}' for i in range(4)}}
    ESPERADO={**{f'A{i+1:02d}':(w[0].upper()+w[1:])+'.' for i,(w,u) in enumerate(WORDS)},
              **{f'B{i+1}':x.replace('’',"'") for i,x in enumerate(SENT)},
              **{f'C{i+1}':q.replace('’',"'") for i,(q,a_,h) in enumerate(QUEST)}}
    for k,v in pk.items():
        if k.startswith('C') and not v['texto'].strip().endswith('?'): continue   # só perguntas
        if k in ESPERADO and v['texto'].strip()!=ESPERADO[k]: continue   # áudio de um texto antigo: não usa
        AUDJ[mapa[k]]=v['mp3']
AUD_JSON=json.dumps(AUDJ)
CONTEUDO=D.CONTEUDO
def onde(origs,suf):
    if isinstance(origs,str): return origs
    ns=nums(origs)
    if ns: return 'ex. '+fmt(ns)+suf.replace(' + ',' e ')
    return suf.split('+ ')[-1] if '+ ' in suf else None   # só o ditado cobre nesta versão
def conteudo_html():
    cols=''
    for un,areas in CONTEUDO:
        rows=''
        for ar,its in areas:
            li=''.join((lambda w: f'<li class="{"" if w else "fora"}"><span>{t}</span><em>{w or "fora deste checkpoint"}</em></li>')(onde(o,sf)) for t,o,sf in its)
            rows+=f'<div class="crow"><b>{ar}</b><ul>{li}</ul></div>'
        cols+=f'<div class="ccol"><h3>{un}</h3>{rows}</div>'
    return cols
HTML=f'''<!DOCTYPE html>
<html lang="pt-BR"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{TURMA} · Checkpoint {CP} · {UN} · {V["nome"]} · Professor</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>
:root{{--ink:#0A0A0F;--desk:{FUNDO};--bar:#FFFFFF;--line:{LINHA};--soft:#6B6A66;--yellow:{COR};--onblack:{COR_PRETO};--yt:{COR_TXT};--neon:#E4FF1A;
  box-sizing:border-box;padding-bottom:env(safe-area-inset-bottom,0px)}}
@media (prefers-color-scheme: dark){{:root:not([data-theme="light"]){{--ink:#F2F1EC;--desk:#16161A;--bar:#0F0F12;--line:#34333A;--soft:#A09FA8}}}}
:root[data-theme="dark"]{{--ink:#F2F1EC;--desk:#16161A;--bar:#0F0F12;--line:#34333A;--soft:#A09FA8}}
*,*::before,*::after{{box-sizing:inherit}}
html{{scroll-padding-top:calc(env(safe-area-inset-top,0px) + 96px)}}
body{{margin:0;background:var(--desk);color:var(--ink);font-family:Inter,"Helvetica Neue",Arial,sans-serif;font-size:15px}}
::selection{{background:var(--neon);color:#0A0A0F}}
button{{font:inherit;color:inherit;cursor:pointer}}
:focus-visible{{outline:2px solid var(--ink);outline-offset:3px}}
.player{{position:sticky;top:0;z-index:5;background:var(--bar);border-bottom:1px solid var(--line);padding:calc(env(safe-area-inset-top,0px) + 10px) 0 8px}}
.in{{max-width:920px;margin:0 auto;padding:0 18px}}
.prow{{display:flex;align-items:center;gap:12px}}
.tracks{{display:flex;gap:6px;flex:none}}
.trk{{border:1px solid var(--line);background:transparent;border-radius:6px;font-size:12.5px;padding:6px 9px;color:var(--soft);line-height:1.2;text-align:left}}
.trk b{{display:block;color:var(--ink);font-weight:700;font-size:13px}}
.trk[aria-pressed="true"]{{background:var(--yellow);border-color:var(--yellow);color:var(--yt)}}
.trk[aria-pressed="true"] b{{color:#0A0A0F}}
.play{{width:44px;height:44px;border-radius:50%;border:0;background:#0A0A0F;color:var(--onblack);display:grid;place-items:center;flex:none}}
.play svg{{width:17px;height:17px}}
.small{{border:1px solid var(--line);background:transparent;border-radius:6px;font-size:13px;padding:6px 9px;color:var(--soft);flex:none;text-decoration:none;display:inline-block}}
.dl{{color:var(--ink);border-color:var(--ink)}}
.track{{flex:1;min-width:0}}
.bar{{position:relative;height:20px;cursor:pointer;touch-action:none}}
.bar::before{{content:"";position:absolute;left:0;right:0;top:9px;height:2px;background:var(--line)}}
.fill{{position:absolute;left:0;top:9px;height:2px;background:var(--ink);width:0}}
.knob{{position:absolute;top:4px;width:12px;height:12px;border-radius:50%;background:var(--ink);transform:translateX(-6px);left:0}}
.times{{display:flex;justify-content:space-between;font-size:12px;color:var(--soft);font-variant-numeric:tabular-nums}}
.cast{{margin:8px 0 0;font-size:13px;color:var(--soft)}}
.cast b{{color:var(--ink);font-weight:700;margin-right:6px}}
.cast .ler{{color:var(--ink);background:#EFEEE9;padding:1px 6px;border-radius:3px}}
.shead{{margin:0 0 10px;padding-bottom:8px;border-bottom:1px dashed var(--line);font-size:13px;color:var(--soft)}}
.shead b{{color:var(--ink);margin-right:6px}}
.shead .aviso{{display:block;margin-top:5px}}
.cast .ler{{color:var(--ink)}}
.shead .aviso{{color:var(--yt);background:var(--yellow);display:inline-block;padding:2px 8px;border-radius:3px;font-weight:600}}
.sbtn[aria-expanded="true"]{{background:#0A0A0F;color:var(--onblack);border-color:#0A0A0F}}
.spanel{{margin-top:8px;max-height:40vh;overflow:auto;border-top:1px solid var(--line);padding:8px 0 4px;font-size:14px;line-height:1.55}}
.spanel p{{margin:0 0 6px;display:grid;grid-template-columns:110px 1fr;gap:10px}}
.spanel p b{{font-weight:700}}
.spanel p.nar{{color:var(--soft);font-style:italic}}
.player.dmode .cast,.player.dmode .spanel,.player.dmode .sbtn{{display:none}}
.dstrip{{margin-top:10px;border-top:1px solid var(--line);padding-top:8px}}
.drow{{display:flex;flex-wrap:wrap;align-items:center;gap:6px;margin-bottom:6px}}
.dl2{{font-size:12.5px;font-weight:700;width:96px;flex:none}}
.dl2.sp{{margin-left:14px;width:auto;margin-right:4px}}
.di{{min-width:32px;height:30px;border:1px solid var(--line);background:transparent;border-radius:6px;font-weight:700;font-size:13px;font-variant-numeric:tabular-nums}}
.di.done{{background:#EFEEE9;color:#0A0A0F}}
.di.on{{background:var(--yellow);border-color:var(--yellow);color:var(--yt)}}
.dstop{{margin-left:auto;border:1px solid var(--ink);background:transparent;border-radius:6px;font-size:12.5px;padding:5px 10px}}
.dmsg{{margin:2px 0 0;font-size:12px;color:var(--soft)}}
.player.dmode .track,.player.dmode .play,.player.dmode .back{{display:none}}
.player.dmode .dl{{margin-left:auto}}
.nav{{display:flex;gap:16px;margin-top:8px;font-size:13px;flex-wrap:wrap}}
.nav a{{color:var(--soft);text-decoration:none}}
.nav a:hover{{color:var(--ink)}}
.vers{{margin-left:auto;display:flex;gap:6px;align-self:center;font-size:13.5px;font-weight:700}}
.vers span,.vers a{{padding:7px 12px;border-radius:6px;border:1px solid var(--line);text-decoration:none;color:var(--soft)}}
.vers span.on{{background:#0A0A0F;color:var(--onblack);border-color:#0A0A0F}}
.vers a:hover{{color:var(--ink);border-color:var(--ink)}}
.convt{{border-collapse:collapse;font-size:12.5px;font-variant-numeric:tabular-nums;margin-top:6px}}
.convt td{{border:1px solid #D6D4CC;padding:3px 6px;text-align:center;min-width:34px;color:#2E2D33}}
.convt td b{{display:block;font-size:11px;color:#6B6A66;font-weight:600}}
.tbtn[aria-expanded="true"]{{background:#0A0A0F;color:var(--onblack);border-color:#0A0A0F}}
.timer{{position:fixed;right:18px;bottom:calc(18px + env(safe-area-inset-bottom,0px));z-index:20;background:var(--bar);border:1px solid var(--line);
  padding:16px 16px 14px;width:236px;box-shadow:0 10px 30px rgba(0,0,0,.12)}}
.tring{{position:relative;width:200px;height:200px;margin:0 auto}}
.tring svg{{width:100%;height:100%;transform:rotate(-90deg)}}
.tbg{{fill:none;stroke:#EFEEE9;stroke-width:14}}
.tfg{{fill:none;stroke:var(--yellow);stroke-width:14;stroke-linecap:round}}
.timer.fim .tfg{{stroke:#0A0A0F}}
.timer.alerta .tfg{{stroke:#0A0A0F}}
.tread{{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center}}
.tread b{{font-size:44px;font-weight:800;letter-spacing:-.03em;font-variant-numeric:tabular-nums;color:var(--ink)}}
.tread span{{font-size:12px;color:var(--soft);margin-top:2px;text-align:center;max-width:140px}}
.tctl,.tpre{{display:flex;gap:6px;margin-top:10px}}
.tctl button,.tpre button{{flex:1;border:1px solid var(--line);background:transparent;border-radius:6px;font-size:12.5px;padding:6px 4px;color:var(--ink)}}
.tctl .tgo{{background:#0A0A0F;color:var(--onblack);border-color:#0A0A0F;font-weight:700}}
.timer.big{{inset:0;width:auto;display:flex;flex-direction:column;align-items:center;justify-content:center;border:0;box-shadow:none;background:var(--desk)}}
.timer.big .tring{{width:min(72vh,80vw);height:min(72vh,80vw)}}
.timer.big .tread b{{font-size:min(16vh,18vw)}}
.timer.big .tread span{{font-size:18px;max-width:none}}
.timer.big .tctl,.timer.big .tpre{{width:min(560px,90vw)}}
.fab{{position:fixed;left:18px;bottom:calc(18px + env(safe-area-inset-bottom,0px));z-index:19;border:0;border-radius:999px;background:#0A0A0F;color:var(--onblack);
  font-weight:700;font-size:14px;padding:12px 18px;box-shadow:0 8px 24px rgba(0,0,0,.18)}}
.fab[aria-expanded="true"]{{background:var(--yellow);color:var(--yt)}}
.guia{{position:fixed;left:18px;bottom:calc(76px + env(safe-area-inset-bottom,0px));z-index:21;width:min(560px,calc(100vw - 36px));max-height:calc(100vh - 200px);
  overflow:auto;background:#fff;color:#0A0A0F;border:1px solid var(--line);padding:22px 24px 18px;box-shadow:0 14px 40px rgba(0,0,0,.18)}}
.ghead{{display:flex;justify-content:space-between;align-items:center}}
.guia h2{{margin:0;font-size:22px;font-weight:800;letter-spacing:-.02em}}
.gx{{border:1px solid #D6D4CC;background:#fff;border-radius:6px;font-size:13px;padding:5px 10px}}
.guia h3{{font-size:14px;font-weight:700;margin:18px 0 8px;padding-bottom:4px;border-bottom:1.5px solid #0A0A0F}}
.gt{{width:100%;border-collapse:collapse;font-size:13.5px;line-height:1.4}}
.gt th{{text-align:left;font-size:13px;padding:6px 8px 6px 0;border-bottom:1px solid #D6D4CC}}
.gt td{{padding:7px 8px 7px 0;border-bottom:1px solid #EFEEE9;vertical-align:top}}
.gt td:first-child{{font-weight:700;width:78px}}
.gr,.gs{{margin:10px 0 0;padding-left:20px;font-size:13.5px;line-height:1.55}}
.gr li,.gs li{{margin-bottom:5px}}
.hero{{padding:26px 0 4px}}
.hin{{display:flex;align-items:center;gap:18px}}
.hero .selo{{width:92px;height:92px;flex:none}}
.hero .k{{margin:0;font-size:13px;color:var(--soft);font-weight:600}}
.hero h1{{margin:2px 0 2px;font-size:30px;font-weight:800;letter-spacing:-.03em}}
.hero .u{{margin:0;font-size:14px;color:var(--soft)}}
.stk{{height:30px;vertical-align:-5px;margin-left:10px}}
.prog{{padding:14px 0 0}}
.pbox{{background:var(--bar);border:1px solid var(--line);padding:22px 26px 18px}}
.phead h2{{margin:0;font-size:20px;font-weight:800;letter-spacing:-.02em}}
.phead p{{margin:4px 0 0;font-size:13.5px;color:var(--soft)}}
.pgrid{{display:grid;grid-template-columns:1fr 1fr;gap:10px 34px;margin-top:14px}}
.ccol h3{{margin:0 0 6px;font-size:15px;font-weight:800;padding:4px 8px;background:var(--yellow);color:var(--yt);display:inline-block}}
.crow{{display:grid;grid-template-columns:86px 1fr;gap:10px;padding:7px 0;border-bottom:1px solid var(--line)}}
.crow:last-child{{border-bottom:0}}
.crow b{{font-size:12.5px;font-weight:700;padding-top:1px}}
.crow ul{{margin:0;padding:0;list-style:none}}
.crow li{{display:flex;justify-content:space-between;gap:10px;font-size:13.5px;line-height:1.5}}
.crow li em{{font-style:normal;font-size:12.5px;font-weight:600;white-space:nowrap;font-variant-numeric:tabular-nums}}
.crow li.fora{{color:var(--soft)}}
.crow li.fora em{{font-weight:400;font-style:italic}}
.pages{{max-width:920px;margin:0 auto;padding:22px 18px 10px;display:flex;flex-direction:column;gap:20px}}
.pages img{{width:100%;height:auto;display:block;background:#fff;border:1px solid var(--line)}}
.teacher{{max-width:920px;margin:0 auto;padding:10px 18px 70px;display:flex;flex-direction:column;gap:20px}}
.box{{background:#fff;color:#0A0A0F;border:1px solid var(--line);padding:26px 32px 28px}}
.bhead{{display:flex;justify-content:space-between;align-items:center;gap:16px}}
.box h2{{margin:0;font-size:26px;font-weight:800;letter-spacing:-.02em}}
.box h2 small{{display:block;font-size:13px;font-weight:500;color:#6B6A66;letter-spacing:0;margin-top:3px}}
.tog{{border:1px solid #0A0A0F;background:#fff;color:#0A0A0F;border-radius:6px;font-size:14px;font-weight:600;padding:8px 14px;white-space:nowrap}}
.tog[aria-expanded="true"]{{background:#0A0A0F;color:var(--onblack)}}
.body{{margin-top:20px;border-top:1px solid #D6D4CC;padding-top:6px}}
.kgrid{{display:grid;grid-template-columns:1fr 1fr;column-gap:40px}}
.ksec h3,.rsec h3{{font-size:17px;font-weight:700;margin:18px 0 8px;display:flex;align-items:baseline;gap:8px;border-bottom:1.5px solid #0A0A0F;padding-bottom:4px}}
.ksec h3 span{{margin-left:auto;font-weight:400;color:#6B6A66}}
.kex{{display:grid;grid-template-columns:30px 1fr;padding:6px 0;border-bottom:1px dashed #D6D4CC;line-height:1.5}}
.kex:last-child{{border-bottom:0}}
.kex b{{font-variant-numeric:tabular-nums}}
.kex ol{{margin:0;padding-left:20px;columns:3;column-gap:14px}}
.kex ol.one{{columns:2}}
.kex li{{break-inside:avoid}}
.kex li::marker{{font-weight:700;font-size:12px}}
.kex p{{margin:0}}
.kex i{{color:#6B6A66;font-style:normal;font-size:13px}}
.rt i{{font-style:italic;color:inherit}}
.kex ul{{margin:0;padding:0;list-style:none;columns:3;column-gap:14px}}
.kex ul.one{{columns:2}}
.map{{margin-top:16px;font-size:13px;color:#6B6A66;line-height:1.6}}
.dnote{{border-left:3px solid var(--yellow);padding:6px 0 6px 12px;margin:14px 0 18px;font-size:14px;line-height:1.55}}
.dcols{{display:grid;grid-template-columns:1fr 1.4fr;gap:34px}}
.dcols h4{{margin:0 0 8px;font-size:14px;font-weight:700}}
.dw,.ds{{margin:0;padding-left:22px;line-height:2}}
.dw em{{font-style:normal;font-size:11px;color:#6B6A66;margin-left:8px}}
.rv{{background:#EFEEE9;color:transparent;border-radius:3px;padding:1px 4px;cursor:pointer;user-select:none;transition:background .2s}}
.rv.on{{background:var(--neon);color:#0A0A0F;user-select:text}}
.dsp{{margin-top:22px;border-top:1px dashed #D6D4CC;padding-top:14px}}
.dsp h4{{margin:0 0 6px;font-size:14px;font-weight:700}}
.dhow{{margin:0 0 10px;font-size:13.5px;color:#2E2D33;line-height:1.5}}
.dsl{{margin:0;padding-left:22px;line-height:2.1}}
.dsl .qq{{display:inline-block;min-width:230px;font-weight:600;margin-right:10px}}
.dsl em{{font-style:normal;font-size:12px;color:#6B6A66;margin-left:10px}}
.dsl em{{visibility:visible}}
.hint{{font-size:12.5px;color:#6B6A66;margin-top:12px}}
.pt{{display:block;color:#6B6A66;font-size:.9em;margin-top:2px;font-weight:400}}
.pt.inl{{display:inline;margin:0 0 0 6px;font-size:14px;font-weight:500}}
.rsec h3 em{{margin-left:auto;font-style:normal;font-weight:500;color:#6B6A66;font-size:14px}}
.rules{{display:grid;grid-template-columns:1fr 1fr;gap:4px 26px;margin-top:14px}}
.rules p{{margin:0;padding-left:10px;border-left:2px solid #D6D4CC;font-size:14px;line-height:1.45}}
.rules b{{font-weight:600}}
.rt{{width:100%;border-collapse:collapse;font-size:14px;line-height:1.45;table-layout:fixed}}
.rt th{{text-align:left;font-size:12px;font-weight:600;color:#6B6A66;padding:6px 10px 6px 0;border-bottom:1px solid #D6D4CC;vertical-align:bottom}}
.rt td{{padding:8px 10px 8px 0;border-bottom:1px solid #E6E4DC;vertical-align:top}}
.rt .rn{{font-weight:800;white-space:nowrap;width:54px}}
.rt .acc{{color:#2E2D33}}
.crit .cn{{font-weight:700}}
.intro{{font-size:14px;margin:4px 0 8px}}
.wrapt{{overflow-x:auto}}
@media (max-width:640px){{
  .pgrid{{grid-template-columns:1fr}} .pbox{{padding:18px 16px}}
  .tracks .trk span{{display:none}} .back{{display:none}}
  .prow{{flex-wrap:wrap;row-gap:6px}} .track{{order:5;flex-basis:100%}} .dl{{margin-left:auto}}
  .nav{{gap:12px;font-size:12.5px}}
  .kgrid,.dcols,.rules{{grid-template-columns:1fr}}
  .box{{padding:20px 16px}} .kex ol{{columns:2}}
}}
@media (prefers-reduced-motion: reduce){{.rv{{transition:none}}}}
</style></head><body>
<div class="player"><div class="in">
  <div class="prow">
    <div class="tracks">
      <button class="trk" data-t="0" aria-pressed="true" {"" if t1 else "hidden"}><b>{LBL[0]}</b><span>ex. {EXS[0]}</span></button>
      <button class="trk" data-t="1" aria-pressed="false" {"" if t2 else "hidden"}><b>{LBL[1]}</b><span>ex. {EXS[1]}</span></button>
      <button class="trk" data-t="2" aria-pressed="false"><b>Dictation</b><span>folha à parte</span></button>
    </div>
    <button class="play" id="play" aria-label="Tocar">
      <svg id="icoPlay" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true"><path d="M5 3.5v13l11-6.5z"/></svg>
      <svg id="icoPause" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true" style="display:none"><rect x="4.5" y="3.5" width="4" height="13"/><rect x="11.5" y="3.5" width="4" height="13"/></svg>
    </button>
    <button class="small back" id="back" aria-label="Voltar 5 segundos">&minus;5 s</button>
    <div class="track">
      <div class="bar" id="bar" role="slider" tabindex="0" aria-label="Posição do áudio" aria-valuemin="0" aria-valuemax="104" aria-valuenow="0"><div class="fill" id="fill"></div><div class="knob" id="knob"></div></div>
      <div class="times"><span id="cur">0:00</span><span id="dur">{DUR0}</span></div>
    </div>
    <button class="small sbtn" id="sbtn" aria-expanded="false">Script</button>
    <button class="small tbtn" id="tbtn" aria-expanded="false">Timer</button>
    <a class="small dl" href="{V["pdf"]}" download>Prova PDF</a>
  </div>
  <p class="cast" id="cast"></p>
  <div class="spanel" id="spanel" hidden></div>
  <div class="dstrip" id="dstrip" hidden>
    <div class="drow"><span class="dl2">A · Words</span>{''.join(f'<button class="di" data-k="w{i}">{i+1}</button>' for i in range(10))}</div>
    <div class="drow"><span class="dl2">B · Sentences</span>{''.join(f'<button class="di" data-k="s{i}">{i+1}</button>' for i in range(4))}
      <span class="dl2 sp">C · Questions</span>{''.join(f'<button class="di" data-k="c{i}">{i+1}</button>' for i in range(4))}
      <button class="dstop" id="dstop">Parar</button></div>
    <p class="dmsg" id="dmsg">Toque um número para ouvir. Toque de novo para repetir. A parte D é feita pelo professor com a turma.</p>
  </div>
  <nav class="nav"><a href="#top">Conteúdo</a><a href="#p1">Prova</a><a href="#p{PG_TR[0] if t1 else PG_TR[1]}" id="goL">Listening</a><a href="#key">Answer key</a><a href="#dictation">Dictation</a><a href="#rubric">Evaluation rubric</a><a href="{DICT_PDF}" download>Folha do ditado PDF</a></nav>
</div>
<audio id="a0" preload="auto" src="{t1}"></audio><audio id="a1" preload="none" src="{t2}"></audio>
</div>

<div class="timer" id="timer" hidden>
  <div class="tring"><svg viewBox="0 0 200 200" aria-hidden="true"><circle class="tbg" cx="100" cy="100" r="86"/><circle class="tfg" id="tfg" cx="100" cy="100" r="86"/></svg>
    <div class="tread"><b id="tnum">{V["minutos"]}:00</b><span id="tlab">Prova {V["nome"]} + ditado</span></div></div>
  <div class="tctl"><button class="tgo" id="tgo">Iniciar</button><button id="treset">Zerar</button><button id="tbig">Tela cheia</button></div>
  <div class="tpre"><button data-m="{V["minutos"]}" data-l="Prova {V["nome"]} + ditado">{V["minutos"]} min</button><button data-m="12" data-l="Ditado">Ditado 12</button><button data-add="5">+5 min</button></div>
</div>
<button class="fab" id="fab" aria-expanded="false" aria-controls="guia">Como aplicar</button>
<div class="guia" id="guia" hidden role="dialog" aria-label="Como aplicar">
  <div class="ghead"><h2>Como aplicar</h2><button class="gx" id="gx" aria-label="Fechar">Fechar</button></div>
  <h3>Qual versão usar</h3>
  <table class="gt"><tr><th></th><th>● Complete</th><th>▲ Speed</th></tr>
  <tr><td>Tempo</td><td>Aula de 80 a 90 min, ou dois encontros</td><td>Uma aula de 50 min</td></tr>
  <tr><td>Writing</td><td>Quando a nota de produção escrita entra no boletim</td><td>Quando a escrita já foi avaliada em aula no mesmo ciclo</td></tr>
  <tr><td>Turma</td><td>Turma pequena ou aula individual</td><td>Turma cheia ou com ritmo de escrita mais lento</td></tr>
  <tr><td>Listening</td><td>As duas faixas</td><td>Só a faixa 1.1</td></tr>
  <tr><td>Nota</td><td>Soma direta, 100 pontos</td><td>{NSPEED} itens, convertidos pela tabela da rubrica</td></tr>
  </table>
  <ul class="gr">
    <li><b>A turma inteira faz a mesma versão.</b> Não misture versões na mesma turma.</li>
    <li><b>Registre a versão</b> (● ou ▲) junto da nota, na planilha e no boletim.</li>
    <li>Na dúvida, escolha pelo <b>tempo real</b> da aula, descontando a chegada e a entrega.</li>
    <li>As duas versões cobrem os assuntos principais das duas unidades: a Speed não é uma prova "mais fácil", é mais curta.</li>
  </ul>
  <h3>Roteiro da aula</h3>
  <ol class="gs">
    <li><b>Antes:</b> imprima a prova da versão escolhida e a folha do ditado, teste o som das faixas e deixe o timer no tempo da versão.</li>
    <li><b>Ditado primeiro</b> (cerca de 12 min), com a turma toda junto: player do topo, botão Dictation (partes A, B e C); a parte D você faz com a turma{' se sobrar tempo (opcional na Speed)' if DOPC else ''}.</li>
    <li><b>Listening em seguida</b>, ainda todos juntos. Antes de cada faixa, leia a frase que aparece sob o player (<i>Before you play · Read aloud…</i>); quando ela disser <i>Don’t read the cast</i>, não leia. Depois, toque cada faixa duas vezes. Só depois a turma segue sozinha no resto da prova.</li>
    <li><b>Esta tela pode ficar projetada:</b> sob o player só aparece o que a turma pode ver. Não abra <b>Script</b>, <b>Answer key</b> nem a aba <b>Dictation</b> com o projetor ligado: elas mostram respostas e as notas do professor.</li>
    <li><b>Resto da prova em silêncio</b>, com o timer projetado em tela cheia. Avise quando o anel ficar preto: faltam 5 minutos.</li>
    <li><b>Correção:</b> answer key e rubrica aqui embaixo; o ditado não vale nota, mas os erros vão para o plano de reforço.</li>
  </ol>
</div>
<header class="hero" id="top"><div class="in hin"><img class="selo" alt="{TURMA} · Checkpoint {CP}" src="data:image/png;base64,{b64(D.SELO)}">
<div><p class="k">Painel do professor</p><h1>{TURMA} · Checkpoint {CP}</h1><p class="u">{UN} · versão {V["nome"]} · cerca de {V["minutos"]} min com o ditado · 100 pontos</p></div>
<nav class="vers" aria-label="Versões"><span class="on">{V["marca"]} {V["nome"]}</span><a href="{OUTRA[0]}">{OUTRA[1]}</a></nav></div></header>
<section class="prog"><div class="in"><div class="pbox">
  <div class="phead"><h2>Conteúdo programático</h2><p>O que as duas unidades ensinam e onde cada item é avaliado neste checkpoint. Os itens em cinza não entram na prova.</p></div>
  <div class="pgrid">{conteudo_html()}</div></div></div></section>
<main class="pages">
{imgs}
</main>

<section class="teacher">
  <div class="box" id="key"><div class="bhead"><h2>Answer key<small>Versão {V["nome"]} · {str(NSPEED)+" itens, nota pela tabela da rubrica" if VER=="speed" else "100 pontos"}</small></h2>
    <button class="tog" aria-expanded="false" aria-controls="kbody">Mostrar respostas</button></div>
    <div class="body" id="kbody" hidden><div class="kgrid">{ak_html()}</div>
    <p class="map">Correspondência com os testes originais: {mapa_html()}.</p></div>
  </div>

  <div class="box" id="dictation"><div class="bhead"><h2>Dictation<img class="stk" alt="" src="data:image/png;base64,{b64(ICONES+'/dictation.png')}"><small>10 palavras, 4 frases, 4 perguntas e uma parte livre do professor</small></h2>
    <button class="tog" aria-expanded="false" aria-controls="dbody">Mostrar ditado</button></div>
    <div class="body" id="dbody" hidden>{dict_html()}<p class="hint">Clique em cada item para revelar. O botão acima fecha tudo de novo.</p></div>
  </div>

  <div class="box" id="rubric"><div class="bhead"><h2>Evaluation rubric<small>Bilingual · English first</small></h2>
    <button class="tog" aria-expanded="false" aria-controls="rbody">Mostrar rubrica</button></div>
    <div class="body wrapt" id="rbody" hidden>{rub_html()}</div>
  </div>
</section>

<script>
(function(){{
  var aud=[document.getElementById('a0'),document.getElementById('a1')], cur=0, a=aud[0];
  var play=document.getElementById('play'),ip=document.getElementById('icoPlay'),ipa=document.getElementById('icoPause'),
      bar=document.getElementById('bar'),fill=document.getElementById('fill'),knob=document.getElementById('knob'),
      tc=document.getElementById('cur'),td=document.getElementById('dur'),goL=document.getElementById('goL'),
      trks=[].slice.call(document.querySelectorAll('.trk'));
  var alvo=['#p{PG_TR[0]}','#p{PG_TR[1]}'];
  function fmt(s){{s=Math.max(0,Math.floor(s||0));return Math.floor(s/60)+':'+String(s%60).padStart(2,'0');}}
  function draw(){{var d=a.duration||1,p=(a.currentTime/d)*100;fill.style.width=p+'%';knob.style.left=p+'%';tc.textContent=fmt(a.currentTime);bar.setAttribute('aria-valuenow',Math.floor(a.currentTime));}}
  function icons(){{var on=!a.paused;ip.style.display=on?'none':'';ipa.style.display=on?'':'none';play.setAttribute('aria-label',on?'Pausar':'Tocar');}}
  function dur(){{if(a.duration){{td.textContent=fmt(a.duration);bar.setAttribute('aria-valuemax',Math.floor(a.duration));}}}}
  function escolher(k){{
    if(k===cur) return; a.pause(); cur=k; a=aud[k];
    goL.setAttribute('href',alvo[k]); dur(); draw(); icons();
  }}
  var player=document.querySelector('.player'), dstrip=document.getElementById('dstrip');
  function modo(k){{
    trks.forEach(function(b,i){{b.setAttribute('aria-pressed',i===k?'true':'false');}});
    var dm=(k===2); player.classList.toggle('dmode',dm); dstrip.hidden=!dm;
    if(dm){{a.pause(); goL.setAttribute('href','#dictation');}}
    else {{if(window.speechSynthesis) speechSynthesis.cancel(); var c=cur; cur=-1; a=aud[c]; escolher(k);}}
  }}
  trks.forEach(function(b,i){{b.addEventListener('click',function(){{modo(i);}});}});
  // ---------- script e elenco (cast) da faixa ----------
  var SCR={SCR_JSON}, castEl=document.getElementById('cast'), sp=document.getElementById('spanel'), sbtn=document.getElementById('sbtn');
  function esc(t){{return String(t).replace(/&/g,'&amp;').replace(/</g,'&lt;');}}
  function roteiro(k){{
    var d=SCR[k]||{{cast:[],linhas:[]}};
    // tela projetada: sob o player só o que é seguro para a turma ver (nada de nomes-resposta)
    castEl.innerHTML=!d.cast.length?'':(d.ler?'<b>Before you play</b>Read aloud: <span class="ler">“'+esc(d.ler)+'”</span>'
                                               :'<b>Before you play</b>Don’t read the cast for this track.');
    sp.innerHTML='<div class="shead"><b>Cast</b> '+esc(d.cast.join(' · '))+(d.aviso?'<span class="aviso">Teacher’s note: '+esc(d.aviso)+'</span>':'')+'</div>'+
      d.linhas.map(function(l){{return '<p class="'+(l[0]==='Narrator'?'nar':'')+'"><b>'+esc(l[0])+'</b><span>'+esc(l[1])+'</span></p>';}}).join('');
    sbtn.hidden=!d.linhas.length;
  }}
  sbtn.addEventListener('click',function(){{var on=sp.hidden; sp.hidden=!on; sbtn.setAttribute('aria-expanded',on?'true':'false');}});
  trks.forEach(function(b,i){{if(i<2) b.addEventListener('click',function(){{roteiro(i);}});}});
  roteiro(0);
  if(trks[0].hidden) modo(1);   // versão sem a primeira faixa: começa na segunda
  roteiro(trks[0].hidden?1:0);
  // ---------- guia de aplicação ----------
  var fab=document.getElementById('fab'),guia=document.getElementById('guia');
  function guiaOn(on){{guia.hidden=!on;fab.setAttribute('aria-expanded',on?'true':'false');}}
  fab.addEventListener('click',function(){{guiaOn(guia.hidden);}});
  document.getElementById('gx').addEventListener('click',function(){{guiaOn(false);}});
  document.addEventListener('keydown',function(e){{if(e.key==='Escape')guiaOn(false);}});
  // ---------- timer redondo ----------
  var tim=document.getElementById('timer'),tbtn=document.getElementById('tbtn'),tfg=document.getElementById('tfg'),
      tnum=document.getElementById('tnum'),tlab=document.getElementById('tlab'),tgo=document.getElementById('tgo');
  var C=2*Math.PI*86; tfg.style.strokeDasharray=C;
  var total={V["minutos"]}*60, resta=total, fimEm=null, raf=null;
  function mmss(x){{x=Math.max(0,Math.ceil(x));return Math.floor(x/60)+':'+String(x%60).padStart(2,'0');}}
  function pinta(){{
    tnum.textContent=mmss(resta);
    tfg.style.strokeDashoffset=C*(1-Math.max(0,resta)/total);
    tim.classList.toggle('alerta',resta>0&&resta<=300); tim.classList.toggle('fim',resta<=0);
    if(resta<=0) tlab.textContent='Tempo esgotado';
  }}
  function passo(){{resta=(fimEm-Date.now())/1000; pinta(); if(resta<=0){{parar();return;}} raf=requestAnimationFrame(passo);}}
  function parar(){{if(raf)cancelAnimationFrame(raf);raf=null;fimEm=null;tgo.textContent=resta>0?'Continuar':'Iniciar';}}
  tgo.addEventListener('click',function(){{
    if(fimEm){{parar();return;}}
    if(resta<=0) resta=total;
    fimEm=Date.now()+resta*1000; tgo.textContent='Pausar'; passo();
  }});
  document.getElementById('treset').addEventListener('click',function(){{parar();resta=total;tgo.textContent='Iniciar';pinta();}});
  [].slice.call(tim.querySelectorAll('.tpre button')).forEach(function(b){{
    b.addEventListener('click',function(){{
      if(b.dataset.add){{var d=+b.dataset.add*60; total+=d; resta+=d; if(fimEm) fimEm+=d*1000; pinta(); return;}}
      parar(); total=+b.dataset.m*60; resta=total; tlab.textContent=b.dataset.l; tgo.textContent='Iniciar'; pinta();
    }});
  }});
  document.getElementById('tbig').addEventListener('click',function(){{
    var on=!tim.classList.contains('big'); tim.classList.toggle('big',on); this.textContent=on?'Sair da tela cheia':'Tela cheia';
  }});
  tbtn.addEventListener('click',function(){{var on=tim.hidden; tim.hidden=!on; tbtn.setAttribute('aria-expanded',on?'true':'false');}});
  pinta();
  // ---------- ditado: voz do navegador (provisória) ----------
  var TXT={DICT_JSON};
  var AUD={AUD_JSON};
  var tocando=null;
  var voz=null;
  function acharVoz(){{
    if(!window.speechSynthesis) return;
    var vs=speechSynthesis.getVoices().filter(function(v){{return /^en[-_]US/i.test(v.lang);}});
    var pref=['Samantha','Aaron','Nicky','Google US English','Microsoft Aria','Microsoft Jenny','Alex'];
    voz=null;
    for(var p=0;p<pref.length&&!voz;p++) for(var q=0;q<vs.length;q++) if(vs[q].name.indexOf(pref[p])>-1){{voz=vs[q];break;}}
    if(!voz&&vs.length) voz=vs[0];
  }}
  if(window.speechSynthesis){{acharVoz(); speechSynthesis.onvoiceschanged=acharVoz;}}
  function falar(partes,rate,fim){{
    speechSynthesis.cancel();
    partes.forEach(function(t,i){{
      var u=new SpeechSynthesisUtterance(t); u.lang='en-US'; if(voz) u.voice=voz; u.rate=rate;
      if(i===partes.length-1) u.onend=fim; speechSynthesis.speak(u);
    }});
  }}
  [].slice.call(document.querySelectorAll('.di')).forEach(function(bt){{
    bt.addEventListener('click',function(){{
      var k=bt.dataset.k, t=TXT[k];
      if(tocando){{tocando.pause();tocando=null;}}
      if(AUD[k]){{
        [].slice.call(document.querySelectorAll('.di.on')).forEach(function(x){{x.classList.remove('on');}});
        if(window.speechSynthesis) speechSynthesis.cancel();
        bt.classList.add('on'); tocando=new Audio(AUD[k]);
        tocando.onended=function(){{bt.classList.remove('on');bt.classList.add('done');}};
        tocando.play(); return;
      }}
      if(!window.speechSynthesis){{document.getElementById('dmsg').textContent='Este navegador não tem voz disponível. Use o Chrome ou o Safari.';return;}}
      [].slice.call(document.querySelectorAll('.di.on')).forEach(function(x){{x.classList.remove('on');}});
      bt.classList.add('on');
      var fim=function(){{bt.classList.remove('on');bt.classList.add('done');}};
      if(k[0]==='s'||k[0]==='c') falar([t],0.82,fim);
      else falar([t],0.8,fim);
    }});
  }});
  document.getElementById('dstop').addEventListener('click',function(){{if(tocando){{tocando.pause();tocando=null;}} if(window.speechSynthesis)speechSynthesis.cancel();
    [].slice.call(document.querySelectorAll('.di.on')).forEach(function(x){{x.classList.remove('on');}});}});
  aud.forEach(function(x){{
    x.addEventListener('play',function(){{if(x===a)icons();}});x.addEventListener('pause',function(){{if(x===a)icons();}});
    x.addEventListener('timeupdate',function(){{if(x===a)draw();}});
    x.addEventListener('loadedmetadata',function(){{if(x===a)dur();}});
    x.addEventListener('ended',function(){{x.currentTime=0;if(x===a){{draw();icons();}}}});
  }});
  play.addEventListener('click',function(){{if(a.paused)a.play();else a.pause();}});
  document.getElementById('back').addEventListener('click',function(){{a.currentTime=Math.max(0,a.currentTime-5);}});
  function seek(e){{var r=bar.getBoundingClientRect();var p=Math.min(1,Math.max(0,(e.clientX-r.left)/r.width));a.currentTime=p*(a.duration||0);draw();}}
  var drag=false;
  bar.addEventListener('pointerdown',function(e){{drag=true;bar.setPointerCapture(e.pointerId);seek(e);}});
  bar.addEventListener('pointermove',function(e){{if(drag)seek(e);}});
  bar.addEventListener('pointerup',function(){{drag=false;}});
  bar.addEventListener('keydown',function(e){{
    if(e.key==='ArrowRight'){{a.currentTime=Math.min(a.duration||0,a.currentTime+5);e.preventDefault();}}
    if(e.key==='ArrowLeft'){{a.currentTime=Math.max(0,a.currentTime-5);e.preventDefault();}}
  }});
  document.addEventListener('keydown',function(e){{
    if(e.code==='Space'&&!/^(BUTTON|A)$/.test(document.activeElement.tagName)&&document.activeElement!==bar){{e.preventDefault();play.click();}}
  }});
  [].slice.call(document.querySelectorAll('.tog')).forEach(function(b){{
    var body=document.getElementById(b.getAttribute('aria-controls')), txt=b.textContent;
    b.addEventListener('click',function(){{
      var on=body.hidden; body.hidden=!on; b.setAttribute('aria-expanded',on?'true':'false');
      b.textContent=on?txt.replace('Mostrar','Ocultar'):txt;
      if(!on) [].slice.call(body.querySelectorAll('.rv.on')).forEach(function(r){{r.classList.remove('on');}});
    }});
  }});
  [].slice.call(document.querySelectorAll('.rv')).forEach(function(r){{r.addEventListener('click',function(){{r.classList.toggle('on');}});}});
}})();
</script>
</body></html>'''
open('/mnt/user-data/outputs/'+V['html'],'w',encoding='utf-8').write(HTML)
# verificação obrigatória: não entrega HTML com marcação crua, erro de JS, rubrica fora de ordem etc.
import subprocess
_v = subprocess.run([sys.executable, os.path.join(os.path.dirname(os.path.abspath(__file__)),'verificar_html.py'), '/mnt/user-data/outputs/'+V['html']], capture_output=True, text=True)
print(_v.stdout.strip())
if _v.returncode: sys.exit('HTML reprovado na verificação: corrigir antes de entregar.')
print(len(HTML)//1024,'KB')
