import sys,json,subprocess,pymupdf as fitz
from PIL import Image
from gerar_config import monta
v,ordem,gi=sys.argv[1],sys.argv[2].split('-'),float(sys.argv[3])
monta(v,ordem,f'/tmp/p3_{v}.json',gi); c=json.load(open(f'/tmp/p3_{v}.json')); c['saida']=f'/tmp/p3_{v}.pdf'; json.dump(c,open(f'/tmp/p3_{v}.json','w'))
subprocess.run(['python3','montar_split.py',f'/tmp/p3_{v}.json'],capture_output=True)
d=fitz.open(f'/tmp/p3_{v}.pdf'); out=[]
for p in d:
    pix=p.get_pixmap(dpi=30,clip=fitz.Rect(0,76,595,776)); im=Image.frombytes('RGB',(pix.width,pix.height),pix.samples).convert('L')
    w,h=im.size; px=im.load(); last=0
    for y in range(h):
        if any(px[x,y]<200 for x in range(w)): last=y
    out.append(round(last/h,2))
print(gi,'-'.join(ordem),out)
