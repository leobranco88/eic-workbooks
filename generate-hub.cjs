/**
 * generate-hub.js
 * Roda automaticamente antes de cada `firebase deploy --only hosting`
 * via predeploy hook no firebase.json
 *
 * O que faz:
 *  1. Escaneia a pasta public/ em busca de .html e .pdf
 *  2. Extrai título e metadados de cada HTML
 *  3. Associa HTML com PDF correspondente
 *  4. Gera public/hub.html com todos os materiais listados
 */

const fs   = require('fs');
const path = require('path');

const PUBLIC = path.join(__dirname, 'public');
const OUT    = path.join(PUBLIC, 'hub.html');
const BASE   = 'https://eic-worksheets.web.app/';

// ── helpers ──────────────────────────────────────────────────────────────────

function readHTML(file) {
  try { return fs.readFileSync(path.join(PUBLIC, file), 'utf8'); }
  catch { return ''; }
}

function extractTitle(html) {
  const m = html.match(/<title[^>]*>([^<]+)<\/title>/i);
  if (!m) return null;
  return m[1]
    .replace(/^EIC\s*[\|·]\s*/i, '')
    .replace(/^EIC\s+Carry-on\s*[\|·]\s*/i, '')
    .replace(/^EIC\s+Neural\s+English\s*[\|·]\s*/i, '')
    .trim();
}

function extractDesc(html) {
  // Try <meta name="description">
  const m = html.match(/<meta[^>]+name=["']description["'][^>]+content=["']([^"']+)["']/i)
           || html.match(/<meta[^>]+content=["']([^"']+)["'][^>]+name=["']description["']/i);
  if (m) return m[1].trim();
  // Fallback: first <p> or .hero-sub text
  const p = html.match(/class=["'][^"']*(?:hero-sub|section-desc)[^"']*["'][^>]*>([^<]{20,200})/i);
  return p ? p[1].trim() : '';
}

function guessType(name) {
  const n = name.toLowerCase();
  if (n.includes('diagnostico') || n.includes('diagnostic')) return 'Diagnóstico';
  if (n.includes('desafio')     || n.includes('challenge'))  return 'Desafio';
  if (n.includes('pratica')     || n.includes('practice'))   return 'Prática';
  if (n.includes('exercicio')   || n.includes('exercise'))   return 'Exercício';
  if (n.includes('index')       || n.includes('portal'))     return 'Índice';
  if (n.includes('set-the-scene'))                           return 'Exercício';
  if (n.includes('aula')        || n.includes('lesson'))     return 'Módulo';
  if (n.includes('episode')     || n.includes('ep'))         return 'Episódio';
  return 'Material';
}

function guessProject(name, html) {
  const n = name.toLowerCase();
  const h = (html || '').toLowerCase();
  if (n.includes('neural') || h.includes('neural english') || h.includes('a1'))    return 'Neural English';
  if (n.includes('carry')  || h.includes('carry-on'))                               return 'Carry-on';
  // Try from top-tag in header
  const tag = html && html.match(/top-tag["'][^>]*>([^<]+)</i);
  if (tag) {
    const t = tag[1].toLowerCase();
    if (t.includes('neural')) return 'Neural English';
    if (t.includes('carry'))  return 'Carry-on';
  }
  return 'EIC';
}

function guessLevel(name, html) {
  const h = (html || '').toLowerCase();
  if (h.includes('a1+') || h.includes('a1/a2'))                    return 'A1+';
  if (h.includes('b1+') || h.includes('b1/b2'))                    return 'B1+';
  if (h.match(/\ba1\b/))                                            return 'A1';
  if (h.match(/\bb1\b/))                                            return 'B1';
  if (h.match(/a2[–\-]b1/) || h.includes('a2–b1'))                 return 'A2–B1';
  if (h.match(/\ba2\b/))                                            return 'A2';
  return '—';
}

// ── scan files ────────────────────────────────────────────────────────────────

const allFiles = fs.readdirSync(PUBLIC).filter(f => !f.startsWith('.'));
const htmlFiles = allFiles.filter(f => f.endsWith('.html') && f !== 'hub.html');
const pdfSet    = new Set(allFiles.filter(f => f.endsWith('.pdf')));

function findPDF(htmlName) {
  const base = htmlName.replace(/\.html$/, '');
  const candidates = [
    base + '-FICHA.pdf',
    base + '-ficha.pdf',
    base + '.pdf',
    base + '-PDF.pdf',
  ];
  return candidates.find(c => pdfSet.has(c)) || null;
}

// ── build materials list ──────────────────────────────────────────────────────

const materials = htmlFiles.map(file => {
  const html    = readHTML(file);
  const title   = extractTitle(html) || file.replace('.html','').replace(/-/g,' ');
  const desc    = extractDesc(html);
  const type    = guessType(file);
  const project = guessProject(file, html);
  const level   = guessLevel(file, html);
  const pdf     = findPDF(file);
  return { file, title, desc, type, project, level, pdf };
});

// Sort: by project then by filename
materials.sort((a, b) => {
  if (a.project !== b.project) return a.project.localeCompare(b.project);
  return a.file.localeCompare(b.file);
});

const total     = materials.length;
const totalPDF  = materials.filter(m => m.pdf).length;
const projects  = [...new Set(materials.map(m => m.project))];

// ── generate HTML ─────────────────────────────────────────────────────────────

const DATA_JSON = JSON.stringify(materials.map((m, i) => ({
  id: i,
  file: m.file,
  title: m.title,
  desc: m.desc,
  type: m.type,
  project: m.project,
  level: m.level,
  pdf: m.pdf,
  url: BASE + m.file,
  pdfUrl: m.pdf ? BASE + m.pdf : null,
})));

const html = `<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>EIC | Materials Hub</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
<style>
:root{--ink:#0C0C0C;--paper:#FAF6EF;--p2:#F2ECE0;--orange:#F54418;--line:#E4DCCB;--muted:#766E61;}
*{box-sizing:border-box;margin:0;padding:0;}
body{font-family:'Inter',sans-serif;background:var(--paper);color:var(--ink);min-height:100vh;-webkit-font-smoothing:antialiased;}
::selection{background:var(--orange);color:#fff;}
a{color:inherit;}

/* HEADER */
.hd{background:var(--ink);padding:0;}
.hd-inner{max-width:1060px;margin:0 auto;padding:15px 28px;display:flex;align-items:center;gap:12px;}
.hd-eic{font-size:11px;font-weight:900;letter-spacing:.12em;text-transform:uppercase;color:var(--orange);}
.hd-name{font-size:14px;font-weight:700;color:#fff;}
.hd-dot{width:4px;height:4px;border-radius:50%;background:rgba(255,255,255,.2);}
.hd-sub{font-size:11px;color:rgba(255,255,255,.35);font-weight:600;margin-left:auto;}
.hd-regen{font-size:11px;color:rgba(255,255,255,.25);font-weight:500;}

/* HERO */
.hero{background:var(--ink);padding:44px 0 40px;border-bottom:1px solid rgba(255,255,255,.07);}
.hero-inner{max-width:1060px;margin:0 auto;padding:0 28px;display:flex;align-items:flex-end;gap:40px;flex-wrap:wrap;}
.hero-titles{flex:1;}
.hero-tag{font-size:11px;font-weight:800;letter-spacing:.1em;text-transform:uppercase;color:var(--orange);margin-bottom:10px;}
.hero-title{font-size:clamp(34px,5vw,54px);font-weight:900;line-height:1.04;color:#fff;letter-spacing:-.025em;}
.hero-stats{display:flex;gap:0;border:1px solid rgba(255,255,255,.1);border-radius:14px;overflow:hidden;}
.stat{padding:14px 22px;text-align:center;border-right:1px solid rgba(255,255,255,.08);}
.stat:last-child{border-right:none;}
.stat-n{font-size:26px;font-weight:900;color:#fff;letter-spacing:-.02em;}
.stat-l{font-size:10px;font-weight:700;text-transform:uppercase;letter-spacing:.06em;color:rgba(255,255,255,.35);margin-top:2px;}

/* TOOLBAR */
.toolbar{max-width:1060px;margin:24px auto 0;padding:0 28px;display:flex;gap:8px;flex-wrap:wrap;align-items:center;}
.search{flex:1;min-width:180px;border:1.5px solid var(--line);border-radius:10px;padding:9px 14px;
  font-family:'Inter';font-size:14px;outline:none;background:#fff;color:var(--ink);transition:border-color .2s;}
.search:focus{border-color:var(--ink);}
.pills{display:flex;gap:5px;flex-wrap:wrap;}
.pill{border:1.5px solid var(--line);background:#fff;color:var(--muted);border-radius:100px;
  padding:5px 12px;font-size:12px;font-weight:700;cursor:pointer;font-family:inherit;transition:all .15s;}
.pill:hover{border-color:var(--ink);color:var(--ink);}
.pill.on-type{border-color:var(--ink);background:var(--ink);color:#fff;}
.pill.on-proj{border-color:#7C3AED;background:#EFE7FC;color:#7C3AED;}

/* GRID */
.grid-wrap{max-width:1060px;margin:0 auto;padding:20px 28px 60px;}
.count-row{font-size:12px;color:var(--muted);font-weight:600;margin-bottom:14px;}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:12px;}
@media(max-width:640px){.grid{grid-template-columns:1fr;}}

/* CARD */
.card{background:#fff;border:1px solid var(--line);border-radius:18px;padding:18px 20px;
  display:flex;flex-direction:column;gap:0;transition:box-shadow .2s,border-color .2s;}
.card:hover{box-shadow:0 4px 20px rgba(12,12,12,.09);border-color:rgba(12,12,12,.12);}
.card-top{display:flex;align-items:center;gap:6px;flex-wrap:wrap;margin-bottom:9px;}
.type-b{border-radius:100px;padding:2px 9px;font-size:10px;font-weight:800;text-transform:uppercase;letter-spacing:.04em;}
.level-b{border:1px solid var(--line);border-radius:100px;padding:2px 8px;font-size:10px;
  font-weight:700;color:var(--muted);background:var(--p2);}
.proj-b{font-size:10px;color:rgba(0,0,0,.25);font-weight:600;margin-left:auto;}
.card-title{font-size:15px;font-weight:800;letter-spacing:-.01em;margin-bottom:5px;line-height:1.25;}
.card-desc{font-size:12px;color:#5C5648;line-height:1.55;margin-bottom:10px;flex:1;}
.card-actions{display:flex;gap:6px;flex-wrap:wrap;margin-top:auto;padding-top:10px;border-top:1px solid var(--line);}
.btn-open{display:inline-flex;align-items:center;gap:5px;background:var(--ink);color:#fff;
  border-radius:100px;padding:7px 13px;font-size:12px;font-weight:700;text-decoration:none;transition:background .2s;}
.btn-open:hover{background:var(--orange);}
.btn-dl{display:inline-flex;align-items:center;gap:5px;border:1.5px solid var(--line);border-radius:100px;
  padding:6px 12px;font-size:12px;font-weight:600;text-decoration:none;color:var(--muted);
  background:#fff;transition:all .15s;}
.btn-dl:hover{border-color:var(--orange);color:var(--orange);}

.empty{grid-column:1/-1;text-align:center;padding:48px 0;color:rgba(0,0,0,.25);font-size:14px;}

/* FOOTER */
footer{border-top:1px solid var(--line);padding:24px 28px;}
footer p{max-width:1060px;margin:0 auto;font-size:12px;color:var(--muted);}

.TYPE_COLORS_STYLE
</style>
</head>
<body>

<div class="hd"><div class="hd-inner">
  <span class="hd-eic">EIC</span>
  <div class="hd-dot"></div>
  <span class="hd-name">Materials Hub</span>
  <span class="hd-sub">Gerado automaticamente em ${new Date().toLocaleDateString('pt-BR')}</span>
</div></div>

<div class="hero"><div class="hero-inner">
  <div class="hero-titles">
    <div class="hero-tag">EIC · Escola de Idiomas e Cultura</div>
    <h1 class="hero-title">Materials Hub</h1>
  </div>
  <div class="hero-stats">
    <div class="stat"><div class="stat-n">${total}</div><div class="stat-l">Materiais</div></div>
    <div class="stat"><div class="stat-n">${totalPDF}</div><div class="stat-l">PDFs</div></div>
    <div class="stat"><div class="stat-n">${projects.length}</div><div class="stat-l">Projetos</div></div>
  </div>
</div></div>

<div class="toolbar">
  <input class="search" id="search" placeholder="Buscar título, tipo, projeto..." oninput="render()">
  <div class="pills" id="type-pills"></div>
  <div class="pills" id="proj-pills"></div>
</div>

<div class="grid-wrap">
  <div class="count-row" id="count"></div>
  <div class="grid" id="grid"></div>
</div>

<footer><p>Hub gerado automaticamente por generate-hub.js · ${new Date().toLocaleString('pt-BR')}</p></footer>

<script>
const DATA = ${DATA_JSON};

const TYPE_COLORS = {
  "Módulo":          {bg:"#E7ECFC",text:"#2454E0"},
  "Episódio":        {bg:"#E7ECFC",text:"#2454E0"},
  "Exercício":       {bg:"#E2F5ED",text:"#0E9F6E"},
  "Prática":         {bg:"#E0F2FE",text:"#0891B2"},
  "Prática extensiva":{bg:"#FEF3C7",text:"#D97706"},
  "Diagnóstico":     {bg:"#F2ECE0",text:"#766E61"},
  "Desafio":         {bg:"#F2ECE0",text:"#0C0C0C"},
  "Índice":          {bg:"#EFE7FC",text:"#7C3AED"},
  "Material":        {bg:"#F2ECE0",text:"#766E61"},
};

let activeType = "Todos", activeProj = "Todos";

const types    = ["Todos", ...new Set(DATA.map(m=>m.type))];
const projects = ["Todos", ...new Set(DATA.map(m=>m.project))];

function filtered(){
  const q = document.getElementById('search').value.toLowerCase();
  return DATA.filter(m=>{
    const mq = !q || m.title.toLowerCase().includes(q) || m.desc.toLowerCase().includes(q) || m.type.toLowerCase().includes(q) || m.project.toLowerCase().includes(q);
    return mq && (activeType==="Todos"||m.type===activeType) && (activeProj==="Todos"||m.project===activeProj);
  });
}

function render(){
  const list = filtered();
  document.getElementById('count').textContent = list.length + ' material' + (list.length!==1?'is':'') + ' encontrado' + (list.length!==1?'s':'');

  document.getElementById('type-pills').innerHTML = types.map(t=>
    \`<button class="pill\${activeType===t?' on-type':''}" onclick="setType('\${t}')">\${t}</button>\`
  ).join('');
  document.getElementById('proj-pills').innerHTML = projects.map(p=>
    \`<button class="pill\${activeProj===p?' on-proj':''}" onclick="setProj('\${p}')">\${p}</button>\`
  ).join('');

  document.getElementById('grid').innerHTML = list.length===0
    ? '<div class="empty">Nenhum material encontrado.</div>'
    : list.map(m=>{
        const c = TYPE_COLORS[m.type]||{bg:"#F2ECE0",text:"#766E61"};
        return \`<div class="card">
          <div class="card-top">
            <span class="type-b" style="background:\${c.bg};color:\${c.text}">\${m.type}</span>
            <span class="level-b">\${m.level}</span>
            <span class="proj-b">\${m.project}</span>
          </div>
          <div class="card-title">\${m.title}</div>
          <div class="card-desc">\${m.desc||'—'}</div>
          <div class="card-actions">
            <a href="\${m.url}" target="_blank" class="btn-open">↗ Abrir</a>
            \${m.pdfUrl?\`<a href="\${m.pdfUrl}" download class="btn-dl">↓ PDF</a>\`:''}
          </div>
        </div>\`;
      }).join('');
}

function setType(t){ activeType=t; render(); }
function setProj(p){ activeProj=p; render(); }

render();
</script>
</body>
</html>`;

fs.writeFileSync(OUT, html.replace('TYPE_COLORS_STYLE', ''));
console.log(`✓ hub.html gerado com ${total} materiais (${totalPDF} PDFs) em ${projects.join(', ')}`);
