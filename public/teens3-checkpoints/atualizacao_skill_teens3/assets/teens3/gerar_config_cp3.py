import json, copy
from mcq import mcq
S='/home/claude/t3/src'; SK='/mnt/skills/plugins/eic-checkpoint-juncao'; FIG='/home/claude/t3/fig'
base={
 "fontes":{"U5":f"{S}/U5.pdf","U6":f"{S}/U6.pdf"},
 "fontes_ttf":{"carb":"/usr/share/fonts/truetype/crosextra/Carlito-Bold.ttf","car":"/usr/share/fonts/truetype/crosextra/Carlito-Regular.ttf",
   "interxb":"/home/claude/fonts/inter/extras/ttf/Inter-ExtraBold.ttf","intermd":"/home/claude/fonts/inter/extras/ttf/Inter-Medium.ttf"},
 "logo":f"{SK}/assets/eic_logo_branco.png",
 "cabecalho":{"curso":"Teens 3","subtitulo":"Checkpoint 3 · Units 5-6","altura":56,"logo_altura":30,"selo":"/home/claude/t3/selo_cp3.png","selo_altura":46},
 "cores":{"faixa":"#9B4DBA","texto_faixa":"#FFFFFF","filete":None,"tinta":"#0A0A0F"},
 "area":{"x0":60,"x1":545,"topo":76,"base":778,"gap":14,"gap_titulo":18,"gap_item":6,"x_score":555,"largura_coluna":258,"x_destino":28,"passo_coluna":270,"icone_altura":30,"icone_gap":6},
 "rodape":{"fonte":"U5","pagina":1,"y0":780,"y1":841.92},
 "grupo_na_mesma_pagina":False, "quebrar_exercicios":True, "ordem_livre":False,
}
T=lambda f,p,a,b,ic=None:dict(tipo="titulo",fonte=f,pagina=p,y0=a,y1=b,**({"icone":f"{FIG}/{ic}.png"} if ic else {}))
X=lambda f,p,a,b,**k:dict(tipo="exercicio",fonte=f,pagina=p,y0=a,y1=b,**k)
C=lambda f,p,a,b,**k:dict(tipo="continuacao",fonte=f,pagina=p,y0=a,y1=b,**k)
SC=lambda n:dict(tipo="score",texto=f"__/{n}")
FIX_G5={"de":"In general, it","x_inicio":108,"segmentos":[["During exam week, it ____________________ (seem hard / not be) stressed.","car"]]}
FIX_R10={"de":"Read the article again","x_inicio":90,"segmentos":[["Read the article. Are these statements True, False, or Not given?","carb"]]}
EX={
 'U5-1':[X("U5",1,150,378)], 'U5-2':[X("U5",1,408,568)],
 'U6-1':[X("U6",1,150,312,corrigir=[FIX_G5])], 'U6-2':[X("U6",1,343,610)],
 'U5-3':[X("U5",2,110,265)], 'U5-4':[X("U5",2,296,560)], 'U5-5':[X("U5",3,75,250)],
 'U6-3':[X("U6",2,110,325)], 'U6-4':[X("U6",2,364,516)], 'U6-5':mcq("U6",f"{S}/U6.pdf",[(3,78,465)]),
 'U5-6':[X("U5",3,300,598)], 'U6-6':[X("U6",3,527,755),C("U6",4,78,212)],
 'U5-7':[X("U5",4,105,592,grupo="audio_U5")], 'U5-8':[X("U5",5,80,206,grupo="audio_U5")],
 'U6-7':[X("U6",4,270,715,grupo="audio_U6"),C("U6",5,78,157)], 'U6-8':[X("U6",5,199,325,grupo="audio_U6")],
 'U5-9':mcq("U5",f"{S}/U5.pdf",[(6,78,565)],max_larg=490,gap=16), 'U5-10':[X("U5",7,78,270,corrigir=[FIX_R10])],
 'U6-12':[X("U6",10,104,364,inteiro=True)],
}
RLO=['U6-6','U5-6']
def monta(versao,ordem=('G','V','L','RL','R','W'),saida=None,gap_item=6):
  cfg=copy.deepcopy(base); cfg['area']['gap_item']=gap_item; speed=versao=='speed'
  cfg['cabecalho']['marca']='triangulo' if speed else 'circulo'
  nome='Checkpoint3_Teens3_U5-U6'+('_Speed' if speed else '')
  cfg['saida']=f'/home/claude/t3/cp3/{nome}.pdf'; cfg['titulo_pdf']='Teens 3 · Checkpoint 3 · Units 5-6'
  b=[T("U5",1,78,96)]
  def sec(tit,ids,pts):
    b.append(tit)
    for i in ids: b.extend(copy.deepcopy(EX[i]))
    b.append(SC(pts))
  def R():
    b.append(T("U5",5,233,253,'reading')); b.append(C("U5",5,260,625,prende=True))
    b.extend(copy.deepcopy(EX['U5-9'])+copy.deepcopy(EX['U5-10'])); b.append(SC(10))
  S_={'G':lambda: sec(T("U5",1,126,146,'grammar'),['U5-1','U5-2','U6-1','U6-2'],20),
   'V':lambda: sec(T("U5",2,79,99,'vocabulary'),['U5-4','U5-5','U6-3','U6-5'] if speed else ['U5-3','U5-4','U5-5','U6-3','U6-4','U6-5'],20 if speed else 30),
   'RL':lambda: sec(T("U5",3,276,296,'reallife'),(RLO if not speed else ['U5-6','U6-6']),10),
   'L':lambda: sec(T("U5",4,79,99,'listening'),['U6-7','U6-8'] if speed else ['U5-7','U5-8','U6-7','U6-8'],10 if speed else 20),
   'R':R,
   'W':lambda: None if speed else sec(T("U6",10,79,99,'writing'),['U6-12'],10)}
  for s in ordem: S_[s]()
  cfg['blocos']=b
  json.dump(cfg,open(saida or f'config_{versao}.json','w'),ensure_ascii=False,indent=1)
