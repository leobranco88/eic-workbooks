const fs   = require('fs');
const path = require('path');

const PUBLIC = path.join(__dirname, 'public');
const OUT    = path.join(PUBLIC, 'hub.html');
const BASE   = 'https://eic-worksheets.web.app/';

function walk(dir, base) {
  const results = [];
  fs.readdirSync(dir).forEach(f => {
    const full = path.join(dir, f);
    const rel  = path.join(base, f);
    if (fs.statSync(full).isDirectory()) {
      results.push(...walk(full, rel));
    } else {
      results.push({ full, rel });
    }
  });
  return results;
}

const allFiles = walk(PUBLIC, '');
const htmlFiles = allFiles.filter(f => f.rel.endsWith('.html') && !f.rel.includes('hub.html'));
const pdfSet    = new Set(allFiles.filter(f => f.rel.endsWith('.pdf')).map(f => f.rel));

function readHTML(full) {
  try { return fs.readFileSync(full, 'utf8'); } catch { return ''; }
}
function extractTitle(html) {
  const m = html.match(/<title[^>]*>([^<]+)<\/title>/i);
  if (!m) return null;
  return m[1].replace(/^EIC\s*[\|·]\s*/i,'').replace(/^EIC\s+[\w-]+\s*[\|·]\s*/i,'').trim();
}
function extractDesc(html) {
  const m = html.match(/class=["'][^"']*(?:hero-sub|section-desc)[^"']*["'][^>]*>([^<]{20,200})/i);
  return m ? m[1].trim() : '';
}
function guessType(rel) {
  const n = rel.toLowerCase();
  if (n.includes('diagnostico'))   return 'Diagnóstico';
  if (n.includes('desafio'))       return 'Desafio';
  if (n.includes('pratica'))       return 'Prática';
  if (n.includes('exercicio') || n.includes('set-the-scene')) return 'Exercício';
  if (n.includes('index') || n.includes('portal'))  return 'Índice';
  if (n.includes('aula') || n.includes('lesson'))   return 'Módulo';
  if (n.includes('episode') || n.includes('-ep'))   return 'Episódio';
  return 'Material';
}
function guessProject(rel, html) {
  const n = rel.toLowerCase(); const h = (html||'').toLowerCase();
  if (n.includes('neural') || n.includes('a1') || h.includes('neural english')) return 'Neural English';
  if (n.includes('carry') || n.includes('will-going') || n.includes('wh-question') || h.includes('carry-on')) return 'Carry-on';
  const folder = rel.split(path.sep)[0] || '';
  return folder.charAt(0).toUpperCase() + folder.slice(1) || 'EIC';
}
function guessLevel(html) {
  const h = (html||'').toLowerCase();
  if (h.match(/\ba1\b/)) return 'A1';
  if (h.match(/a2[–\-]b1/)) return 'A2–B1';
  if (h.match(/\bb1\b/)) return 'B1';
  if (h.match(/\ba2\b/)) return 'A2';
  return '—';
}
function findPDF(rel) {
  const base = rel.replace(/\.html$/, '');
  return [base+'-FICHA.pdf', base+'.pdf'].find(c => pdfSet.has(c)) || null;
}

const TYPE_COLORS = {
  "Módulo":{"bg":"#E7ECFC","text":"#2454E0"},"Episódio":{"bg":"#E7ECFC","text":"#2454E0"},
  "Exercício":{"bg":"#E2F5ED","text":"#0E9F6E"},"Prática":{"bg":"#E0F2FE","text":"#0891B2"},
  "Prática extensiva":{"bg":"#FEF3C7","text":"#D97706"},"Diagnóstico":{"bg":"#F2ECE0","text":"#766E61"},
  "Desafio":{"bg":"#F2ECE0","text":"#0C0C0C"},"Índice":{"bg":"#EFE7FC","text":"#7C3AED"},
  "Material":{"bg":"#F2ECE0","text":"#766E61"}
};

const materials = htmlFiles.map(({full,rel}) => {
  const html = readHTML(full);
  return {
    title:   extractTitle(html) || path.basename(rel,'.html').replace(/-/g,' '),
    desc:    extractDesc(html),
    type:    guessType(rel),
    project: guessProject(rel, html),
    level:   guessLevel(html),
    url:     BASE + rel.replace(/\\/g,'/'),
    pdf:     findPDF(rel) ? BASE + findPDF(rel).replace(/\\/g,'/') : null,
  };
}).sort((a,b) => a.project.localeCompare(b.project) || a.title.localeCompare(b.title));

const total    = materials.length;
const totalPDF = materials.filter(m=>m.pdf).length;
const projects = [...new Set(materials.map(m=>m.project))];
const DATA     = JSON.stringify(materials);

const html = `<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>EIC | Materials Hub</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
<style>
:root{--ink:#0C0C0C;--paper:#FAF6EF;--p2:#F2ECE0;--orange:#F54418;--line:#E4DCCB;--muted:#766E61;}
*{box-sizing:border-box;margin:0;padding:0;}
body{font-family:'Inter',sans-serif;background:var(--paper);color:var(--ink);min-height:100vh;-webkit-font-smoothing:antialiased;}
.hd{background:var(--ink);padding:15px 28px;display:flex;align-items:center;gap:10px;}
.hd-eic{font-size:11px;font-weight:900;letter-spacing:.1em;text-transform:uppercase;color:var(--orange);}
.hd-name{font-size:14px;font-weight:700;color:#fff;}
.hd-dot{width:4px;height:4px;border-radius:50%;background:rgba(255,255,255,.2);}
.hd-date{font-size:11px;color:rgba(255,255,255,.3);margin-left:auto;}
.hero{background:var(--ink);padding:40px 28px 36px;display:flex;align-items:flex-end;gap:40px;flex-wrap:wrap;max-width:1060px;margin:0 auto;}
.hero-title{font-size:clamp(32px,5vw,52px);font-weight:900;color:#fff;letter-spacing:-.025em;}
.hero-tag{font-size:11px;font-weight:800;letter-spacing:.1em;text-transform:uppercase;color:var(--orange);margin-bottom:8px;}
.stats{display:flex;border:1px solid rgba(255,255,255,.1);border-radius:14px;overflow:hidden;margin-left:auto;}
.stat{padding:13px 20px;text-align:center;border-right:1px solid rgba(255,255,255,.08);}
.stat:last-child{border-right:none;}
.stat-n{font-size:24px;font-weight:900;color:#fff;}
.stat-l{font-size:10px;font-weight:700;text-transform:uppercase;letter-spacing:.06em;color:rgba(255,255,255,.35);margin-top:2px;}
.toolbar{max-width:1060px;margin:20px auto 0;padding:0 28px;display:flex;gap:8px;flex-wrap:wrap;align-items:center;}
.search{flex:1;min-width:160px;border:1.5px solid var(--line);border-radius:10px;padding:9px 14px;font-family:'Inter';font-size:14px;outline:none;background:#fff;transition:border-color .2s;}
.search:focus{border-color:var(--ink);}
.pills{display:flex;gap:5px;flex-wrap:wrap;}
.pill{border:1.5px solid var(--line);background:#fff;color:var(--muted);border-radius:100px;padding:5px 12px;font-size:12px;font-weight:700;cursor:pointer;font-family:inherit;transition:all .15s;}
.pill.on-type{border-color:var(--ink);background:var(--ink);color:#fff;}
.pill.on-proj{border-color:#7C3AED;background:#EFE7FC;color:#7C3AED;}
.wrap{max-width:1060px;margin:0 auto;padding:18px 28px 60px;}
.count{font-size:12px;color:var(--muted);font-weight:600;margin-bottom:12px;}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(290px,1fr));gap:10px;}
.card{background:#fff;border:1px solid var(--line);border-radius:16px;padding:16px 18px;display:flex;flex-direction:column;gap:0;transition:box-shadow .2s;}
.card:hover{box-shadow:0 4px 18px rgba(12,12,12,.08);}
.card-top{display:flex;align-items:center;gap:6px;flex-wrap:wrap;margin-bottom:8px;}
.tb{border-radius:100px;padding:2px 9px;font-size:10px;font-weight:800;text-transform:uppercase;letter-spacing:.04em;}
.lb{border:1px solid var(--line);border-radius:100px;padding:2px 8px;font-size:10px;font-weight:700;color:var(--muted);background:var(--p2);}
.pb{font-size:10px;color:rgba(0,0,0,.22);font-weight:600;margin-left:auto;}
.ctitle{font-size:14.5px;font-weight:800;letter-spacing:-.01em;margin-bottom:4px;line-height:1.25;}
.cdesc{font-size:12px;color:#5C5648;line-height:1.55;margin-bottom:10px;flex:1;}
.actions{display:flex;gap:6px;flex-wrap:wrap;margin-top:auto;padding-top:10px;border-top:1px solid var(--line);}
.btn-o{display:inline-flex;align-items:center;gap:4px;background:var(--ink);color:#fff;border-radius:100px;padding:6px 13px;font-size:12px;font-weight:700;text-decoration:none;transition:background .2s;}
.btn-o:hover{background:var(--orange);}
.btn-d{display:inline-flex;align-items:center;gap:4px;border:1.5px solid var(--line);border-radius:100px;padding:5px 11px;font-size:12px;font-weight:600;text-decoration:none;color:var(--muted);background:#fff;transition:all .15s;}
.btn-d:hover{border-color:var(--orange);color:var(--orange);}
.empty{grid-column:1/-1;text-align:center;padding:48px 0;color:rgba(0,0,0,.2);font-size:14px;}
footer{border-top:1px solid var(--line);padding:18px 28px;font-size:11px;color:var(--muted);text-align:center;}
</style>
</head>
<body>
<div style="background:var(--ink)">
  <div class="hd">
    <span class="hd-eic">EIC</span><div class="hd-dot"></div>
    <span class="hd-name">Materials Hub</span>
    <span class="hd-date">Atualizado em ${new Date().toLocaleDateString('pt-BR')}</span>
  </div>
  <div class="hero">
    <div><div class="hero-tag">EIC · Escola de Idiomas e Cultura</div><h1 class="hero-title">Materials Hub</h1></div>
    <div class="stats">
      <div class="stat"><div class="stat-n">${total}</div><div class="stat-l">Materiais</div></div>
      <div class="stat"><div class="stat-n">${totalPDF}</div><div class="stat-l">PDFs</div></div>
      <div class="stat"><div class="stat-n">${projects.length}</div><div class="stat-l">Projetos</div></div>
    </div>
  </div>
</div>
<div class="toolbar">
  <input class="search" id="s" placeholder="Buscar título, tipo, projeto..." oninput="r()">
  <div class="pills" id="tp"></div>
  <div class="pills" id="pp"></div>
</div>
<div class="wrap">
  <div class="count" id="cnt"></div>
  <div class="grid" id="grid"></div>
</div>
<footer>Gerado automaticamente por generate-hub.cjs · ${new Date().toLocaleString('pt-BR')}</footer>
<script>
const D=${DATA};
const TC=${JSON.stringify(TYPE_COLORS)};
let at="Todos",ap="Todos";
const types=["Todos",...new Set(D.map(m=>m.type))];
const projs=["Todos",...new Set(D.map(m=>m.project))];
function f(){const q=document.getElementById('s').value.toLowerCase();return D.filter(m=>(!q||m.title.toLowerCase().includes(q)||m.desc.toLowerCase().includes(q)||m.type.toLowerCase().includes(q)||m.project.toLowerCase().includes(q))&&(at==="Todos"||m.type===at)&&(ap==="Todos"||m.project===ap));}
function r(){const l=f();
document.getElementById('cnt').textContent=l.length+' material'+(l.length!==1?'is':'')+' encontrado'+(l.length!==1?'s':'');
document.getElementById('tp').innerHTML=types.map(t=>\`<button class="pill\${at===t?' on-type':''}" onclick="at='\${t}';r()">\${t}</button>\`).join('');
document.getElementById('pp').innerHTML=projs.map(p=>\`<button class="pill\${ap===p?' on-proj':''}" onclick="ap='\${p}';r()">\${p}</button>\`).join('');
document.getElementById('grid').innerHTML=l.length===0?'<div class="empty">Nenhum material encontrado.</div>':l.map(m=>{const c=TC[m.type]||{bg:"#F2ECE0",text:"#766E61"};return\`<div class="card"><div class="card-top"><span class="tb" style="background:\${c.bg};color:\${c.text}">\${m.type}</span><span class="lb">\${m.level}</span><span class="pb">\${m.project}</span></div><div class="ctitle">\${m.title}</div><div class="cdesc">\${m.desc||'—'}</div><div class="actions"><a href="\${m.url}" target="_blank" class="btn-o">↗ Abrir</a>\${m.pdf?\`<a href="\${m.pdf}" download class="btn-d">↓ PDF</a>\`:''}</div></div>\`;}).join('');}
r();
</script>
</body>
</html>`;

fs.writeFileSync(OUT, html);
console.log(`✓ hub.html gerado com ${total} materiais (${totalPDF} PDFs) em ${projects.join(', ')}`);
