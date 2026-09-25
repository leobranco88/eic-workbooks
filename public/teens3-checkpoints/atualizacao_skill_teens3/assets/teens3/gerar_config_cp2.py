import json, copy
from mcq import mcq
S='/home/claude/t3/src'; SK='/mnt/skills/plugins/eic-checkpoint-juncao'; FIG='/home/claude/t3/fig'
base={
 "fontes":{"U3":f"{S}/U3.pdf","U4":f"{S}/U4.pdf"},
 "fontes_ttf":{"carb":"/usr/share/fonts/truetype/crosextra/Carlito-Bold.ttf","car":"/usr/share/fonts/truetype/crosextra/Carlito-Regular.ttf",
   "interxb":"/home/claude/fonts/inter/extras/ttf/Inter-ExtraBold.ttf","intermd":"/home/claude/fonts/inter/extras/ttf/Inter-Medium.ttf"},
 "logo":f"{SK}/assets/eic_logo_branco.png",
 "cabecalho":{"curso":"Teens 3","subtitulo":"Checkpoint 2 · Units 3-4","altura":56,"logo_altura":30,"selo":"/home/claude/t3/selo_cp2.png","selo_altura":46},
 "cores":{"faixa":"#9B4DBA","texto_faixa":"#FFFFFF","filete":None,"tinta":"#0A0A0F"},
 "area":{"x0":60,"x1":545,"topo":76,"base":778,"gap":14,"gap_titulo":18,"gap_item":6,"x_score":555,"largura_coluna":258,"x_destino":28,"passo_coluna":270,"icone_altura":30,"icone_gap":6},
 "rodape":{"fonte":"U3","pagina":1,"y0":780,"y1":841.92},
 "grupo_na_mesma_pagina":True, "quebrar_exercicios":True, "ordem_livre":False,
}
T=lambda f,p,a,b,ic=None:dict(tipo="titulo",fonte=f,pagina=p,y0=a,y1=b,**({"icone":f"{FIG}/{ic}.png"} if ic else {}))
X=lambda f,p,a,b,**k:dict(tipo="exercicio",fonte=f,pagina=p,y0=a,y1=b,**k)
C=lambda f,p,a,b,**k:dict(tipo="continuacao",fonte=f,pagina=p,y0=a,y1=b,**k)
SC=lambda n:dict(tipo="score",texto=f"__/{n}")
SEM_AGAIN=lambda n,resto:{"de":"Read the article again","x_inicio":90,"segmentos":[[f"Read the article. {resto}","carb"]]}
FIX_V4={"de":"Because the streets","x_inicio":108,"segmentos":[["People in my village have ridden bikes for a hundred years. They’re the __________ way to get around.","car"]]}
EX={
 'U3-1':[X("U3",1,154,305)], 'U3-2':[X("U3",1,332,525)],
 'U4-1':[X("U4",1,150,305)], 'U4-2':[X("U4",1,336,506)],
 'U3-3':[X("U3",2,110,290)], 'U3-4':[X("U3",2,318,617,corrigir=[FIX_V4])], 'U3-5':[X("U3",3,78,380)],
 'U4-3':mcq("U4",f"{S}/U4.pdf",[(1,567,755),(2,78,352)]), 'U4-4':[X("U4",2,392,580)],
 'U3-6':[X("U3",3,448,600)], 'U4-5':[X("U4",3,104,740)],
 'U3-7':[X("U3",4,106,265,grupo="audio_U3")], 'U3-8':[X("U3",4,300,692,grupo="audio_U3",colunas_forcar=2),C("U3",5,78,158)],
 'U4-6':[X("U4",4,105,253,grupo="audio_U4")], 'U4-7':[X("U4",4,286,690,grupo="audio_U4"),C("U4",5,78,157)],
 'U3-9':[X("U3",6,78,372)], 'U3-10':[X("U3",6,404,660,corrigir=[SEM_AGAIN(10,"Choose the best answer.")]),C("U3",7,78,430)],
 'U4-9':[X("U4",6,275,482,corrigir=[SEM_AGAIN(9,"Complete the sentences with one word from the article.")])],
 'U4-11':[X("U4",7,104,556,inteiro=True)],
}
def monta(versao,ordem=('G','V','R','L','RL','W'),saida=None,gap_item=6):
  cfg=copy.deepcopy(base); cfg['area']['gap_item']=gap_item; speed=versao=='speed'
  cfg['cabecalho']['marca']='triangulo' if speed else 'circulo'
  nome='Checkpoint2_Teens3_U3-U4'+('_Speed' if speed else '')
  cfg['saida']=f'/home/claude/t3/cp2/{nome}.pdf'; cfg['titulo_pdf']='Teens 3 · Checkpoint 2 · Units 3-4'
  b=[T("U3",1,78,96)]
  def sec(tit,ids,pts):
    b.append(tit)
    for i in ids: b.extend(copy.deepcopy(EX[i]))
    b.append(SC(pts))
  def R():
    b.append(T("U3",5,202,222,'reading')); b.append(C("U3",5,228,650,prende=True))
    b.extend(copy.deepcopy(EX['U3-9'])+copy.deepcopy(EX['U3-10']))
    if not speed:
      b.append(T("U4",5,228,700)); b.extend(copy.deepcopy(EX['U4-9']))
    b.append(SC(10 if speed else 15))
  S_={'G':lambda: sec(T("U3",1,128,148,'grammar'),['U3-1','U3-2','U4-1','U4-2'],20),
   'V':lambda: sec(T("U3",2,79,99,'vocabulary'),['U3-3','U3-4','U4-3','U4-4'] if speed else ['U3-3','U3-4','U3-5','U4-3','U4-4'],20 if speed else 25),
   'RL':lambda: sec(T("U3",3,423,443,'reallife'),['U3-6','U4-5'],10),
   'L':lambda: sec(T("U3",4,79,99,'listening'),['U4-6','U4-7'] if speed else ['U3-7','U3-8','U4-6','U4-7'],10 if speed else 20),
   'R':R,
   'W':lambda: None if speed else sec(T("U4",7,79,99,'writing'),['U4-11'],10)}
  for s in ordem: S_[s]()
  cfg['blocos']=b
  json.dump(cfg,open(saida or f'config_{versao}.json','w'),ensure_ascii=False,indent=1)
