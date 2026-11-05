import base64,re,os,glob
def b64(p): return base64.b64encode(open(p,'rb').read()).decode()
cav='fonts/caveat-latin-700-normal.woff2'
inter='fonts/inter-latin-wght-normal.woff2'
fonts=('<style>@font-face{font-family:Inter;font-weight:100 900;font-style:normal;font-display:swap;src:url(data:font/woff2;base64,%s) format("woff2")}'
       '@font-face{font-family:Caveat;font-weight:700;font-style:normal;font-display:swap;src:url(data:font/woff2;base64,%s) format("woff2")}</style>')%(b64(inter),b64(cav))
logo='data:image/png;base64,'+b64('eic-logo.png')
os.makedirs('dist',exist_ok=True)
def build(src,out):
    h=open(src,encoding='utf-8').read()
    h=h.replace('<!--FONTS-->',fonts).replace('<!--SCRIPTS-->','')
    h=re.sub(r'<script src="([^"]+)"></script>',lambda m:'<script>\n'+open(m.group(1),encoding='utf-8').read()+'\n</script>',h)
    h=h.replace('src="eic-logo.png"','src="%s"'%logo)
    assert 'src="config.js"' not in h and 'eic-logo.png' not in h
    open(out,'w',encoding='utf-8').write(h); print(out,len(h)//1024,'KB')
build('index.html','dist/NeuralEnglish-VerbPatterns-Part2-Vitoria.html')
build('professor.html','dist/NeuralEnglish-VerbPatterns-Part2-Vitoria-Professor.html')
D='deploy/public/vitoria/verb-patterns-part2'; os.makedirs(D,exist_ok=True)
build('index.html',D+'/pratica.html'); build('professor.html',D+'/professor.html')
