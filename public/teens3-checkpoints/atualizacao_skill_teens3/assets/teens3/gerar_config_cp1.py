import json, copy
from mcq import mcq
S='/home/claude/t3/src'; SK='/mnt/skills/plugins/eic-checkpoint-juncao'; FIG='/home/claude/t3/fig'
base={
 "fontes":{"U1":f"{S}/U1.pdf","U2":f"{S}/U2.pdf"},
 "fontes_ttf":{"carb":"/usr/share/fonts/truetype/crosextra/Carlito-Bold.ttf","car":"/usr/share/fonts/truetype/crosextra/Carlito-Regular.ttf",
   "interxb":"/home/claude/fonts/inter/extras/ttf/Inter-ExtraBold.ttf","intermd":"/home/claude/fonts/inter/extras/ttf/Inter-Medium.ttf"},
 "logo":f"{SK}/assets/eic_logo_branco.png",
 "cabecalho":{"curso":"Teens 3","subtitulo":"Checkpoint 1 · Units 1-2","altura":56,"logo_altura":30,"selo":"/home/claude/t3/selo_cp1.png","selo_altura":46},
 "cores":{"faixa":"#9B4DBA","texto_faixa":"#FFFFFF","filete":None,"tinta":"#0A0A0F"},
 "area":{"x0":60,"x1":545,"topo":76,"base":778,"gap":14,"gap_titulo":18,"gap_item":6,"x_score":555,"largura_coluna":258,"x_destino":28,"passo_coluna":270,"icone_altura":30,"icone_gap":6},
 "rodape":{"fonte":"U1","pagina":1,"y0":780,"y1":841.92},
 "grupo_na_mesma_pagina":True,
}
T=lambda f,p,a,b,ic=None:dict(tipo="titulo",fonte=f,pagina=p,y0=a,y1=b,**({"icone":f"{FIG}/{ic}.png"} if ic else {}))
X=lambda f,p,a,b,**k:dict(tipo="exercicio",fonte=f,pagina=p,y0=a,y1=b,**k)
C=lambda f,p,a,b,**k:dict(tipo="continuacao",fonte=f,pagina=p,y0=a,y1=b,**k)
SC=lambda n:dict(tipo="score",texto=f"__/{n}")
TROCA_RL6={'You should do it with me.':'Great idea! Let’s do it together.','No, I wouldn’t like acting.':'No, I’m not interested in acting.','Go on.':'Go for it!'}
RL6_fix_old=[
 {"de":"You should do it with me","x_inicio":108,"segmentos":[["a.","car"],["Great idea! Let’s do it together.","car",18]]},
 {"de":"wouldn’t like acting","x_inicio":108,"segmentos":[["b.","car"],["No, I’m not interested in acting.","car",18]]},
 {"de":"Go on.","x_inicio":108,"segmentos":[["a.","car"],["Go for it!","car",18]]},
]
FIX11={"de":"Read the article again","x_inicio":90,"segmentos":[["Read the article. Choose the best answer.","carb"]]}
EX={
 'U1-2':[X("U1",1,398,556)],
 'U1-3':mcq("U1",f"{S}/U1.pdf",[(1,583,755),(2,78,312)]),
 'U2-1':[X("U2",1,153,462)],
 'U2-2':[X("U2",1,493,690)],
 'U1-4':[X("U1",2,385,563)],
 'U1-5':mcq("U1",f"{S}/U1.pdf",[(2,572,743),(3,78,312)]),
 'U1-6':[X("U1",3,349,512)],
 'U2-3':[X("U2",2,109,270)],
 'U2-4':[X("U2",2,300,461)],
 'U2-5':[X("U2",2,491,652)],
 'U1-7':[X("U1",3,574,731),C("U1",4,79,287)],
 'U2-6':[X("U2",3,104,672,corrigir=RL6_fix_old,colunas_forcar=2)],
 'U1-8':[X("U1",4,356,573,grupo="audio_U1")],
 'U1-9':mcq("U1",f"{S}/U1.pdf",[(4,605,717),(5,78,474)],max_larg=490,gap=14,grupo="audio_U1"),
 'U2-7':[X("U2",4,106,270,grupo="audio_U2")],
 'U2-8':[X("U2",4,301,545,grupo="audio_U2")],
 'U1-10':[X("U1",6,537,702)],
 'U1-11':mcq("U1",f"{S}/U1.pdf",[(7,78,552)]),
}
EX['U1-11'][0].setdefault('corrigir',[]).append(FIX11)
EX.update({
 'U2-12':[X("U2",7,353,727,inteiro=True)],
})
def monta(versao,ordem=('G','V','RL','L','R','W'),saida=None,gap_item=6):
  cfg=copy.deepcopy(base); cfg['area']['gap_item']=gap_item; speed=versao=='speed'
  cfg['cabecalho']['marca']='triangulo' if speed else 'circulo'
  nome='Checkpoint1_Teens3_U1-U2'+('_Speed' if speed else '')
  cfg['saida']=f'/home/claude/t3/cp1/{nome}.pdf'; cfg['titulo_pdf']='Teens 3 · Checkpoint 1 · Units 1-2'
  b=[T("U1",1,78,96)]
  def sec(tit,ids,pts):
    b.append(tit)
    for i in ids: b.extend(copy.deepcopy(EX[i]))
    b.append(SC(pts))
  S_={
   'G':lambda: sec(T("U1",1,128,148,'grammar'),['U1-2','U1-3','U2-1','U2-2'],20),
   'V':lambda: sec(T("U1",2,355,375,'vocabulary'),['U1-4','U1-5','U2-3','U2-5'] if speed else ['U1-4','U1-5','U1-6','U2-3','U2-4','U2-5'],20 if speed else 30),
   'RL':lambda: sec(T("U1",3,548,568,'reallife'),['U1-7','U2-6'],10),
   'L':lambda: sec(T("U1",4,328,348,'listening'),['U2-7','U2-8'] if speed else ['U1-8','U1-9','U2-7','U2-8'],10 if speed else 20),
   'R':lambda: (b.append(T("U1",6,79,99,'reading')), b.append(C("U1",6,104,502,prende=True)), b.extend(copy.deepcopy(EX['U1-10'])+copy.deepcopy(EX['U1-11'])), b.append(SC(10))),
   'W':lambda: None if speed else sec(T("U2",7,328,348,'writing'),['U2-12'],10),
  }
  for s in ordem: S_[s]()
  cfg['blocos']=b
  json.dump(cfg,open(saida or f'config_{versao}.json','w'),ensure_ascii=False,indent=1)
if __name__=='__main__':
  monta('complete'); monta('speed')
