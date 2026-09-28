const fs   = require('fs');
const path = require('path');
const { execSync } = require('child_process');

// ─────────────────────────────────────────────────────────────────────────────
// CONFIGURAÇÃO — é só aqui que se mexe para organizar o hub
//
// Regra: o projeto de cada material é a PASTA de primeiro nível onde ele está.
// public/Erik/qualquer-coisa.html  →  projeto "Erik", sempre.
// Uma pasta nova que não estiver em nenhum grupo aparece em "Outros", nunca some.
// Override por arquivo continua valendo: <meta name="hub-project" content="...">
// ─────────────────────────────────────────────────────────────────────────────

// Grupos da barra lateral, na ordem em que aparecem. Chave = nome da pasta em minúsculas.
const GRUPOS = [
  { nome: 'Checkpoints Kids',  pastas: ['kids1-checkpoints','kids2-checkpoints','kids3-checkpoints','kids4-checkpoints',
                                        'kids5-checkpoints','kids6-checkpoints','speaking-kids6','kids-guide'] },
  { nome: 'Famílias',          pastas: ['familia-kids1','familia-kids2','familia-kids3','familia-kids4','familia-kids5','familia-kids6'] },
  { nome: 'Checkpoints Teens', pastas: ['teens1-checkpoints','teens2-checkpoints','teens3-checkpoints','teens4-checkpoints',
                                        'check-point-teens5-6-guide','checkpoint-teens','checkpoint-teens2-final'] },
  { nome: 'Turmas e alunos',   pastas: ['erik','rafael','toshie','deb','teens1','teens3'] },
  { nome: 'Business',          pastas: ['sales','ventix','procurement','customer-service','strategic-hr','self-development','health'] },
  { nome: 'Método',            pastas: ['neural-english','neural-english-oficial','neural-english-presentation','grammar',
                                        'verb-patterns','speaking practice'] },
  { nome: 'Viagem e temas',    pastas: ['airport','getting-around','european-garden','wh-questions-airport-hopistal','study-abroad'] },
  { nome: 'Escola',            pastas: ['eic-philosophy','eic-teacher-training','eic_curriculum_system','eic-teaching',
                                        'internal','gamefik','placement-test'] },
];

// Banco onde o botão "Organizar" do hub guarda os grupos (coleção hub, documento organizacao).
// O que for organizado no hub vale por cima da lista GRUPOS acima.
const FIREBASE = {
  apiKey: "AIzaSyDWXC2LYj4Ksa8ijTvei24EIUmWJ4uILGc",
  authDomain: "eic-worksheets.firebaseapp.com",
  projectId: "eic-worksheets",
  storageBucket: "eic-worksheets.firebasestorage.app",
  messagingSenderId: "671300791274",
  appId: "1:671300791274:web:6cdb2d7348c7f3a14ca093"
};

// Pastas que são o mesmo projeto com outro nome
const ALIAS = { 'procurement-verbpattern': 'procurement' };

// Arquivos soltos na raiz de public/ e o projeto a que pertencem
const RAIZ = {
  'manual_checkpoint_kids2.html':  'kids2-checkpoints',
  'maint-grammar-deduction.html':  'grammar',
  'procurement-verb-patterns.html':'procurement',
};

// Nomes de exibição que o formatador automático não acerta
const NOMES = {
  'check-point-teens5-6-guide': 'Teens 5–6 · Guia',
  'checkpoint-teens':           'Checkpoint Teens (antigo)',
  'checkpoint-teens2-final':    'Checkpoint Teens 2 (final)',
  'eic_curriculum_system':      'Curriculum System',
  'eic-philosophy':             'Philosophy',
  'eic-teacher-training':       'Teacher Training',
  'eic-teaching':               'Teaching',
  'kids-guide':                 'Kids · Guia',
  'speaking-kids6':             'Kids 6 · Speaking',
  'neural-english-oficial':     'Neural English · Oficial',
  'neural-english-presentation':'Neural English · Apresentação',
  'wh-questions-airport-hopistal':'Wh-questions · Airport e Hospital',
  'strategic-hr':               'Strategic HR',
};

// Linhas do método: atravessam as pastas (um material do Erik pode ser Neural English)
function linhasDe(rel, html) {
  const n = rel.toLowerCase(); const h = (html || '').slice(0, 30000).toLowerCase();
  const l = [];
  if (n.includes('neural') || h.includes('neural english')) l.push('Neural English');
  if (n.includes('carry') || n.includes('will-going') || n.includes('wh-question') || h.includes('carry-on')) l.push('Carry-on');
  return l;
}
// ─────────────────────────────────────────────────────────────────────────────

const ROOTS = [
  { dir: 'public',         base: 'https://eic-worksheets.web.app/', site: 'worksheets' },
  { dir: 'public-familia', base: 'https://eic-familia.web.app/',    site: 'familia'    },
];
const OUT = path.join(__dirname, 'public', 'hub.html');

function walk(dir, base) {
  const out = [];
  fs.readdirSync(dir).forEach(f => {
    if (f.startsWith('.') || f === 'node_modules') return;
    const full = path.join(dir, f), rel = path.join(base, f);
    if (fs.statSync(full).isDirectory()) out.push(...walk(full, rel));
    else out.push({ full, rel });
  });
  return out;
}

const allFiles = [];
ROOTS.forEach(root => {
  const dir = path.join(__dirname, root.dir);
  if (!fs.existsSync(dir)) { console.log(`- ${root.dir} nao existe, ignorado`); return; }
  walk(dir, '').forEach(f => allFiles.push({ ...f, root }));
});
const htmlFiles = allFiles.filter(f => f.rel.endsWith('.html') && path.basename(f.rel) !== 'hub.html');
const pdfSet = new Set(allFiles.filter(f => f.rel.endsWith('.pdf')).map(f => f.root.site + '::' + f.rel));

// Data de entrada de cada arquivo = o commit mais recente que o ADICIONOU (git).
// Arquivo ainda não commitado: data de criação no disco.
function datasGit() {
  const mapa = {};
  try {
    const out = execSync('git log --no-renames --diff-filter=A --name-only --format=@@%aI -- public public-familia',
                         { cwd: __dirname, encoding: 'utf8', maxBuffer: 64 * 1024 * 1024, stdio: ['ignore', 'pipe', 'ignore'] });
    let data = null;
    out.split('\n').forEach(l => {
      if (l.startsWith('@@')) data = l.slice(2).trim();
      else if (l.trim() && data && !mapa[l.trim()]) mapa[l.trim()] = data;   // log vem do mais novo para o mais velho
    });
  } catch (e) { console.log('- git indisponivel, usando a data dos arquivos'); }
  return mapa;
}
const DATAS = datasGit();
function dataDe(full) {
  const relRepo = path.relative(__dirname, full).split(path.sep).join('/');
  if (DATAS[relRepo]) return DATAS[relRepo];
  const st = fs.statSync(full);
  return new Date(st.birthtimeMs || st.mtimeMs).toISOString();
}

const readHTML = full => { try { return fs.readFileSync(full, 'utf8'); } catch { return ''; } };
const ENT = { '&middot;':'·','&amp;':'&','&nbsp;':' ','&ndash;':'–','&mdash;':'—','&rsquo;':'’','&lsquo;':'‘',
              '&quot;':'"','&eacute;':'é','&aacute;':'á','&atilde;':'ã','&ccedil;':'ç','&oacute;':'ó','&iacute;':'í','&ecirc;':'ê' };
const dec = t => t.replace(/&[a-z]+;/gi, e => ENT[e.toLowerCase()] ?? e).replace(/&#(\d+);/g, (_, n) => String.fromCharCode(n));
function extractTitle(html) {
  const m = html.match(/<title[^>]*>([^<]+)<\/title>/i);
  return m ? dec(m[1]).replace(/^EIC\s*[\|·]\s*/i, '').replace(/^EIC\s+[\w-]+\s*[\|·]\s*/i, '').trim() : null;
}
function meta(html, nome) {
  const m = html.match(new RegExp('<meta\\s+name=["\']hub-' + nome + '["\']\\s+content=["\']([^"\']+)["\']', 'i'));
  return m ? dec(m[1]).trim() : null;
}
function extractDesc(html) {
  const m = html.match(/class=["'][^"']*(?:hero-sub|section-desc)[^"']*["'][^>]*>([^<]{20,200})/i);
  return m ? dec(m[1]).trim() : '';
}
function guessType(rel) {
  const n = rel.toLowerCase();
  if (n.includes('diagnostico')) return 'Diagnóstico';
  if (n.includes('desafio'))     return 'Desafio';
  if (n.includes('pratica'))     return 'Prática';
  if (n.includes('exercicio') || n.includes('set-the-scene')) return 'Exercício';
  if (n.includes('index') || n.includes('portal')) return 'Índice';
  if (n.includes('aula') || n.includes('lesson'))  return 'Módulo';
  if (n.includes('episode') || n.includes('-ep'))  return 'Episódio';
  return 'Material';
}
function guessLevel(html) {
  const h = (html || '').slice(0, 30000).toLowerCase();
  if (h.match(/\ba1\b/)) return 'A1';
  if (h.match(/a2[–\-]b1/)) return 'A2–B1';
  if (h.match(/\bb1\b/)) return 'B1';
  if (h.match(/\ba2\b/)) return 'A2';
  return '';
}
function findPDF(rel, root, html) {
  const marcado = meta(html, 'pdf');
  if (marcado) { const c = path.join(path.dirname(rel), marcado); if (pdfSet.has(root.site + '::' + c)) return c; }
  const base = rel.replace(/\.html$/, '');
  return [base + '-FICHA.pdf', base + '.pdf'].find(c => pdfSet.has(root.site + '::' + c)) || null;
}

// chave do projeto = pasta de primeiro nível, normalizada
function chaveProjeto(rel, root) {
  const partes = rel.split(path.sep);
  if (root.site === 'familia') {
    const turma = partes.find(p => /^kids\d/i.test(p));
    return turma ? 'familia-' + turma.toLowerCase().match(/^kids\d/)[0] : 'familia';
  }
  let k = partes.length > 1 ? partes[0] : (RAIZ[partes[0].toLowerCase()] || 'avulsos');
  k = k.trim().toLowerCase();
  return ALIAS[k] || k;
}
function nomeProjeto(k) {
  if (NOMES[k]) return NOMES[k];
  let m;
  if ((m = k.match(/^familia-kids(\d)$/))) return `Kids ${m[1]} · Famílias`;
  if ((m = k.match(/^(kids|teens)(\d)-checkpoints$/))) return `${m[1][0].toUpperCase() + m[1].slice(1)} ${m[2]} · Checkpoints`;
  return k.replace(/[-_]+/g, ' ').replace(/\b(eic|hr)\b/g, s => s.toUpperCase())
          .replace(/\b([a-z])/g, s => s.toUpperCase()).replace(/(Kids|Teens)(\d)/g, '$1 $2');
}
const grupoDe = {};
GRUPOS.forEach(g => g.pastas.forEach(p => grupoDe[p] = g.nome));

const materials = htmlFiles.map(({ full, rel, root }) => {
  const html = readHTML(full);
  const pdf  = findPDF(rel, root, html);
  const forcado = meta(html, 'project');
  const k = forcado ? forcado.trim().toLowerCase() : chaveProjeto(rel, root);
  return {
    title:   meta(html, 'title') || extractTitle(html) || path.basename(rel, '.html').replace(/-/g, ' '),
    desc:    meta(html, 'desc')  || extractDesc(html),
    type:    meta(html, 'type')  || guessType(rel),
    project: forcado || nomeProjeto(k),
    group:   grupoDe[k] || 'Outros',
    lines:   linhasDe(rel, html),
    level:   meta(html, 'level') || guessLevel(html),
    date:    dataDe(full),
    url:     root.base + rel.split(path.sep).join('/'),
    pdf:     pdf ? root.base + pdf.split(path.sep).join('/') : null,
  };
}).sort((a, b) => b.date.localeCompare(a.date) || a.title.localeCompare(b.title));

const total    = materials.length;
const totalPDF = materials.filter(m => m.pdf).length;
const projects = [...new Set(materials.map(m => m.project))];
const ORDEM_GRUPOS = [...GRUPOS.map(g => g.nome), 'Outros'];
const agora = new Date();
const carimbo = agora.toLocaleDateString('pt-BR') + ' ' + agora.toLocaleTimeString('pt-BR', { hour: '2-digit', minute: '2-digit' });
const json = o => JSON.stringify(o).replace(/</g, '\\u003c');

const html = `<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>EIC | Materials Hub</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
<style>
:root{--ink:#0C0C0C;--paper:#FAF6EF;--p2:#F2ECE0;--orange:#F54418;--line:#E4DCCB;--muted:#766E61;--soft:#A59C8C;}
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:'Inter',system-ui,sans-serif;background:var(--paper);color:var(--ink);-webkit-font-smoothing:antialiased;font-variant-numeric:tabular-nums}
button{font:inherit;color:inherit;background:none;border:0;cursor:pointer;text-align:left}
a{color:inherit}
.top{background:var(--ink);color:#fff;padding:14px 28px;display:flex;align-items:baseline;gap:12px;flex-wrap:wrap}
.top b{font-size:11px;font-weight:900;letter-spacing:.12em;color:var(--orange)}
.top h1{font-size:15px;font-weight:800;letter-spacing:-.01em}
.top .st{margin-left:auto;font-size:12px;color:rgba(255,255,255,.45)}
.top .st strong{color:#fff;font-weight:700}
.shell{max-width:1240px;margin:0 auto;display:grid;grid-template-columns:260px minmax(0,1fr);gap:0 48px;padding:0 28px}
aside{position:sticky;top:0;align-self:start;max-height:100vh;overflow:auto;padding:28px 4px 40px 0;scrollbar-width:thin}
.search{width:100%;border:0;border-bottom:1.5px solid var(--ink);background:transparent;padding:8px 0;font:inherit;font-size:15px;outline:none}
.search::placeholder{color:var(--soft)}
.blk{margin-top:26px}
.lbl{font-size:10.5px;font-weight:800;letter-spacing:.14em;text-transform:uppercase;color:var(--muted);margin-bottom:6px;display:flex;justify-content:space-between;align-items:center}
.lbl button{font-size:10.5px;letter-spacing:.14em;color:var(--soft);font-weight:800;text-transform:uppercase}
.lbl button:hover{color:var(--ink)}
.types{display:flex;flex-wrap:wrap;gap:4px 14px}
.types button{font-size:13px;color:var(--muted);padding:2px 0;border-bottom:1.5px solid transparent}
.types button:hover{color:var(--ink)}
.types button.on{color:var(--ink);font-weight:700;border-color:var(--orange)}
.proj{display:flex;justify-content:space-between;gap:10px;width:100%;padding:4px 0 4px 10px;font-size:13.5px;color:#3B372F;border-left:2px solid transparent;line-height:1.3}
.proj:hover{color:var(--ink);background:rgba(12,12,12,.03)}
.proj.on{border-left-color:var(--orange);font-weight:700;color:var(--ink)}
.proj i{font-style:normal;color:var(--soft);font-size:12px}
details.grp summary{list-style:none;cursor:pointer}
details.grp summary::-webkit-details-marker{display:none}
details.grp summary .lbl:after{content:'+';font-size:13px;letter-spacing:0;color:var(--soft)}
details.grp[open] summary .lbl:after{content:'–'}
main{padding:28px 0 80px;min-width:0}
.mh{display:flex;align-items:flex-end;gap:16px;flex-wrap:wrap;padding-bottom:18px;border-bottom:1.5px solid var(--ink)}
.mh h2{font-size:clamp(30px,4.2vw,46px);font-weight:900;letter-spacing:-.035em;line-height:1}
.mh .cnt{font-size:13px;color:var(--muted);margin-bottom:4px}
.sort{margin-left:auto;display:flex;gap:14px;font-size:13px;margin-bottom:4px}
.sort button{color:var(--soft)}
.sort button.on{color:var(--ink);font-weight:700}
.fbtn{display:none;font-size:13px;font-weight:700;border:1.5px solid var(--ink);padding:6px 12px;margin-bottom:2px}
.bucket{font-size:11px;font-weight:800;letter-spacing:.14em;text-transform:uppercase;color:var(--muted);padding:30px 0 8px;border-bottom:1px solid var(--line)}
.row{display:grid;grid-template-columns:62px minmax(0,1fr) auto;gap:18px;align-items:start;padding:14px 0;border-bottom:1px solid var(--line)}
.row:hover{background:linear-gradient(90deg,transparent,rgba(242,236,224,.55) 12%,rgba(242,236,224,.55) 88%,transparent)}
.dt{font-size:12.5px;color:var(--muted);padding-top:2px;position:relative}
.dt.new:before{content:'';position:absolute;left:-12px;top:8px;width:6px;height:6px;border-radius:50%;background:var(--orange)}
.t{font-size:15.5px;font-weight:700;letter-spacing:-.01em;line-height:1.3}
.t a{text-decoration:none}
.t a:hover{text-decoration:underline;text-decoration-thickness:1.5px;text-underline-offset:3px}
.m{font-size:12.5px;color:var(--muted);margin-top:3px;display:flex;flex-wrap:wrap;gap:0 10px}
.m .pj{color:var(--ink);font-weight:600}
.m .ln{color:var(--orange);font-weight:600}
.d{font-size:13px;color:#5C5648;margin-top:5px;line-height:1.5;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden;max-width:68ch}
.act{display:flex;gap:16px;font-size:13px;font-weight:600;padding-top:2px;white-space:nowrap}
.act a,.act button{color:var(--muted);text-decoration:none}
.act a:hover,.act button:hover{color:var(--ink)}
.act .open{color:var(--ink)}
.act .ok{color:#0E7A52}
.org{margin-top:30px;padding-top:14px;border-top:1px solid var(--line);font-size:12.5px;color:var(--muted)}
.org button{font-weight:700;color:var(--ink);border-bottom:1.5px solid var(--ink)}
.org #orgst{display:block;margin-top:6px;min-height:1em}
.org #orgst.err{color:#B3261E}
body.orgm aside{background:var(--p2);margin-left:-14px;padding-left:14px;padding-right:14px}
.gh{display:flex;align-items:center;gap:6px;margin-bottom:6px}
.gh .lbl{margin:0;flex:1}
.gh button{font-size:12px;color:var(--muted);padding:0 3px}
.gh button:hover{color:var(--ink)}
.pr{display:flex;align-items:center;justify-content:space-between;gap:8px;padding:3px 0 3px 10px;font-size:13px}
.pr select{font:inherit;font-size:12px;max-width:128px;border:1px solid var(--line);background:#fff;padding:2px 4px;color:var(--ink)}
.newg{font-size:12.5px;font-weight:700;margin-top:18px;border-bottom:1.5px solid var(--ink)}
.empty{padding:60px 0;color:var(--muted);font-size:15px}
.empty button{text-decoration:underline;font-weight:700;color:var(--ink)}
footer{max-width:1240px;margin:0 auto;padding:18px 28px 30px;font-size:11px;color:var(--soft)}
@media (max-width:860px){
  .shell{grid-template-columns:1fr;padding:0 16px}
  .top{padding:12px 16px}
  aside{display:none;position:static;max-height:none;padding:8px 0 20px;border-bottom:1.5px solid var(--ink)}
  body.fo aside{display:block}
  .fbtn{display:inline-block}
  .row{grid-template-columns:48px minmax(0,1fr);gap:12px}
  .act{grid-column:2;padding-top:0}
  .dt.new:before{left:-9px}
  footer{padding:18px 16px 30px}
}
</style>
</head>
<body>
<header class="top">
  <b>EIC</b><h1>Materials Hub</h1>
  <span class="st"><strong>${total}</strong> materiais · <strong>${totalPDF}</strong> PDFs · <strong>${projects.length}</strong> projetos · atualizado ${carimbo}</span>
</header>
<div class="shell">
  <aside id="side">
    <input class="search" id="s" placeholder="Buscar título, projeto, pasta" autocomplete="off">
    <div class="blk"><div class="lbl">Tipo</div><div class="types" id="tp"></div></div>
    <div class="blk" id="all"></div>
    <div class="blk" id="ln"></div>
    <div id="gp"></div>
    <div class="org"><button id="orgb">Organizar grupos</button><span id="orgst"></span></div>
  </aside>
  <main>
    <div class="mh">
      <div><h2 id="ttl">Tudo</h2><div class="cnt" id="cnt"></div></div>
      <div class="sort" id="sort"><button data-s="d" class="on">Mais recentes</button><button data-s="a">A–Z</button></div>
      <button class="fbtn" id="fb">Filtros</button>
    </div>
    <div id="list"></div>
  </main>
</div>
<footer>Gerado por generate-hub.cjs em ${carimbo}. Projeto = pasta de primeiro nível; data = quando o arquivo entrou no repositório.</footer>
<script>
const D=${json(materials)};
const GR=${json(ORDEM_GRUPOS)};
const HOJE=new Date();
let st={q:'',t:'Todos',p:'',l:'',s:'d'};
const $=id=>document.getElementById(id);
const esc=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const dia=iso=>{const d=new Date(iso);return new Date(d.getFullYear(),d.getMonth(),d.getDate());};
const H0=dia(HOJE.toISOString());
const MES=['janeiro','fevereiro','março','abril','maio','junho','julho','agosto','setembro','outubro','novembro','dezembro'];
function balde(iso){const n=Math.round((H0-dia(iso))/864e5);
  if(n<=0)return'Hoje';if(n===1)return'Ontem';if(n<7)return'Últimos 7 dias';
  const d=new Date(iso);return MES[d.getMonth()]+' de '+d.getFullYear();}
const curto=iso=>{const d=new Date(iso);return String(d.getDate()).padStart(2,'0')+'/'+String(d.getMonth()+1).padStart(2,'0');};
function hash(){const p=new URLSearchParams(location.hash.slice(1));st.p=p.get('p')||'';st.l=p.get('l')||'';st.t=p.get('t')||'Todos';}
function sethash(){const p=new URLSearchParams();if(st.p)p.set('p',st.p);if(st.l)p.set('l',st.l);if(st.t!=='Todos')p.set('t',st.t);
  history.replaceState(null,'',p.toString()?'#'+p:location.pathname);}
function filtra(){const q=st.q.toLowerCase();return D.filter(m=>(!st.p||m.project===st.p)&&(!st.l||m.lines.includes(st.l))&&(st.t==='Todos'||m.type===st.t)&&
  (!q||(m.title+' '+m.desc+' '+m.project+' '+m.type+' '+m.url).toLowerCase().includes(q)));}
function lado(){
  const tipos=['Todos',...[...new Set(D.map(m=>m.type))].sort()];
  $('tp').innerHTML=tipos.map(t=>'<button data-t="'+esc(t)+'"'+(st.t===t?' class="on"':'')+'>'+esc(t)+'</button>').join('');
  const lns=[...new Set(D.flatMap(m=>m.lines))];
  $('ln').innerHTML=lns.length?'<div class="lbl">Linha do método</div>'+lns.map(l=>'<button class="proj'+(st.l===l?' on':'')+'" data-l="'+esc(l)+'"><span>'+esc(l)+'</span><i>'+D.filter(m=>m.lines.includes(l)).length+'</i></button>').join(''):'';
  $('all').innerHTML='<button class="proj'+(!st.p&&!st.l?' on':'')+'" data-p=""><span>Tudo</span><i>'+D.length+'</i></button>';
  $('gp').innerHTML=ORG?ladoOrg():ordemEf().map(g=>{const ps=projsDe(g);
    if(!ps.length)return'';const aberto=ps.includes(st.p)||(innerWidth>860&&g!==gname('Outros'));
    return'<details class="blk grp"'+(aberto?' open':'')+'><summary><div class="lbl">'+esc(g)+'</div></summary>'+
     ps.map(p=>'<button class="proj'+(st.p===p?' on':'')+'" data-p="'+esc(p)+'"><span>'+esc(p)+'</span><i>'+D.filter(m=>m.project===p).length+'</i></button>').join('')+'</details>';}).join('');
  $('orgb').textContent=ORG?'Concluir':'Organizar grupos';
}
// ── organização (grupos editáveis, guardados no Firestore) ──
let CFG={mover:{},ordem:[],renomear:{}},ORG=false;
const gname=g=>CFG.renomear[g]||g;
const grupoEf=p=>{if(CFG.mover[p])return CFG.mover[p];const m=D.find(x=>x.project===p);return gname(m?m.group:'Outros');};
const PROJS=[...new Set(D.map(m=>m.project))];
function ordemEf(){const outros=gname('Outros');let o=[...new Set((CFG.ordem||[]).map(gname))];
  GR.map(gname).forEach(g=>{if(!o.includes(g))o.push(g);});
  PROJS.map(grupoEf).forEach(g=>{if(!o.includes(g))o.push(g);});
  o=o.filter(g=>g!==outros);o.push(outros);return o;}
const projsDe=g=>PROJS.filter(p=>grupoEf(p)===g).sort((a,b)=>a.localeCompare(b,'pt',{numeric:true}));
function ladoOrg(){const gs=ordemEf();
  return gs.map((g,i)=>'<div class="blk"><div class="gh"><div class="lbl">'+esc(g)+'</div>'+
    (i>0&&i<gs.length-1?'<button data-up="'+i+'" title="Subir">↑</button>':'')+(i<gs.length-2?'<button data-dn="'+i+'" title="Descer">↓</button>':'')+
    (i<gs.length-1?'<button data-rn="'+esc(g)+'">Renomear</button>':'')+'</div>'+
    (projsDe(g).map(p=>'<div class="pr"><span>'+esc(p)+'</span><select data-mv="'+esc(p)+'">'+
      gs.map(x=>'<option'+(x===g?' selected':'')+'>'+esc(x)+'</option>').join('')+'<option value="__novo">+ Novo grupo…</option></select></div>').join('')||
     '<div class="pr" style="color:var(--soft)">Vazio</div>')+'</div>').join('')+
    '<button class="newg" id="ng">+ Novo grupo</button>';}
function aplicaCfg(c){CFG={mover:c.mover||{},ordem:c.ordem||[],renomear:c.renomear||{}};lado();}
async function grava(){const e=$('orgst');e.className='';e.textContent='Salvando…';
  if(!window.salvaCfg){e.className='err';e.textContent='Sem conexão com o banco. A mudança vale só nesta aba.';return;}
  try{CFG.ordem=ordemEf();await window.salvaCfg(CFG);e.textContent='Salvo. Vale para todos.';}
  catch(err){e.className='err';e.textContent=/permission/i.test(String(err))?'O banco recusou (permissão). Falta liberar a coleção hub nas regras do Firestore.':'Não salvou: '+err.message;}}
function novoGrupo(){const n=(prompt('Nome do novo grupo:')||'').trim();if(!n)return null;
  if(ordemEf().includes(n)){alert('Já existe um grupo com esse nome.');return null;}
  const o=ordemEf();o.splice(o.length-1,0,n);CFG.ordem=o;return n;}
function mexe(ev){const x=ev.target;
  if(x.dataset.mv!==undefined){let g=x.value;if(g==='__novo'){g=novoGrupo();if(!g){lado();return;}}
    CFG.mover[x.dataset.mv]=g;lado();grava();}}
function ordemTroca(i,j){const o=ordemEf();[o[i],o[j]]=[o[j],o[i]];CFG.ordem=o;lado();grava();}
function renomeia(g){const n=(prompt('Novo nome para "'+g+'":',g)||'').trim();if(!n||n===g)return;
  const antes=ordemEf();if(antes.includes(n)){alert('Já existe um grupo com esse nome.');return;}
  Object.keys(CFG.renomear).forEach(k=>{if(CFG.renomear[k]===g)CFG.renomear[k]=n;});
  if(GR.includes(g))CFG.renomear[g]=n;
  Object.keys(CFG.mover).forEach(p=>{if(CFG.mover[p]===g)CFG.mover[p]=n;});
  CFG.ordem=antes.map(x=>x===g?n:x);lado();grava();}
function linha(m){
  const novo=(H0-dia(m.date))/864e5<7;
  return'<div class="row"><div class="dt'+(novo?' new':'')+'">'+curto(m.date)+'</div><div>'+
   '<div class="t"><a href="'+esc(m.url)+'" target="_blank" rel="noopener">'+esc(m.title)+'</a></div>'+
   '<div class="m">'+(st.p?'':'<span class="pj">'+esc(m.project)+'</span>')+'<span>'+esc(m.type)+'</span>'+(m.level?'<span>'+esc(m.level)+'</span>':'')+
   m.lines.map(l=>'<span class="ln">'+esc(l)+'</span>').join('')+'</div>'+
   (m.desc?'<div class="d">'+esc(m.desc)+'</div>':'')+'</div>'+
   '<div class="act"><a class="open" href="'+esc(m.url)+'" target="_blank" rel="noopener">Abrir ↗</a>'+
   '<button data-cp="'+esc(m.url)+'">Copiar link</button>'+(m.pdf?'<a href="'+esc(m.pdf)+'" download>PDF</a>':'')+'</div></div>';
}
function r(){
  const l=filtra();if(st.s==='a')l.sort((a,b)=>a.title.localeCompare(b.title,'pt',{numeric:true}));
  $('ttl').textContent=st.p||st.l||'Tudo';
  $('cnt').textContent=l.length+(l.length===1?' material':' materiais')+(st.t!=='Todos'?' · '+st.t:'')+(st.q?' · busca "'+st.q+'"':'');
  document.querySelectorAll('#sort button').forEach(b=>b.classList.toggle('on',b.dataset.s===st.s));
  if(!l.length){$('list').innerHTML='<div class="empty">Nenhum material com esses filtros. <button id="lim">Limpar filtros</button></div>';return;}
  let out='',b=null;
  l.forEach(m=>{if(st.s==='d'){const k=balde(m.date);if(k!==b){b=k;out+='<div class="bucket">'+k+'</div>';}}out+=linha(m);});
  $('list').innerHTML=out;
}
function tudo(){lado();r();sethash();}
document.addEventListener('click',e=>{
  const x=e.target.closest('button');if(!x)return;
  if(x.id==='fb'){document.body.classList.toggle('fo');return;}
  if(x.id==='orgb'){ORG=!ORG;document.body.classList.toggle('orgm',ORG);$('orgst').textContent='';$('orgst').className='';return lado();}
  if(x.id==='ng'){if(novoGrupo()){lado();grava();}return;}
  if(x.dataset.up){const i=+x.dataset.up;return ordemTroca(i,i-1);}
  if(x.dataset.dn){const i=+x.dataset.dn;return ordemTroca(i,i+1);}
  if(x.dataset.rn){return renomeia(x.dataset.rn);}
  if(x.id==='lim'){st={...st,q:'',t:'Todos',p:'',l:''};$('s').value='';return tudo();}
  if('t' in x.dataset){st.t=x.dataset.t;return tudo();}
  if('p' in x.dataset){st.p=x.dataset.p;st.l='';document.body.classList.remove('fo');tudo();return window.scrollTo({top:0});}
  if('l' in x.dataset){st.l=st.l===x.dataset.l?'':x.dataset.l;st.p='';document.body.classList.remove('fo');tudo();return window.scrollTo({top:0});}
  if('s' in x.dataset){st.s=x.dataset.s;return r();}
  if(x.dataset.cp){copia(x,x.dataset.cp);}
});
document.addEventListener('change',mexe);
$('s').addEventListener('input',e=>{st.q=e.target.value.trim();r();});
function copia(btn,url){
  const ok=()=>{const t=btn.textContent;btn.textContent='Copiado';btn.classList.add('ok');setTimeout(()=>{btn.textContent=t;btn.classList.remove('ok');},1500);};
  const alt=()=>{const ta=document.createElement('textarea');ta.value=url;ta.style.position='fixed';ta.style.opacity='0';document.body.appendChild(ta);ta.select();
    try{document.execCommand('copy');ok();}catch(e){window.prompt('Copie o link:',url);}ta.remove();};
  if(navigator.clipboard&&window.isSecureContext)navigator.clipboard.writeText(url).then(ok,alt);else alt();
}
hash();tudo();
</script>
<script type="module">
import{initializeApp}from'https://www.gstatic.com/firebasejs/10.12.2/firebase-app.js';
import{getFirestore,doc,getDoc,setDoc}from'https://www.gstatic.com/firebasejs/10.12.2/firebase-firestore.js';
try{
  const db=getFirestore(initializeApp(${JSON.stringify(FIREBASE)}));
  const ref=doc(db,'hub','organizacao');
  window.salvaCfg=c=>setDoc(ref,{mover:c.mover,ordem:c.ordem,renomear:c.renomear,atualizado:new Date().toISOString()});
  const snap=await getDoc(ref);if(snap.exists())aplicaCfg(snap.data());
}catch(e){console.warn('hub: organizacao nao carregada',e);}
</script>
</body>
</html>`;

fs.writeFileSync(OUT, html);
console.log(`✓ hub.html gerado com ${total} materiais (${totalPDF} PDFs) em ${projects.length} projetos`);
const soltos = [...new Set(materials.filter(m => m.group === 'Outros').map(m => m.project))];
if (soltos.length) console.log(`  Em "Outros" (pastas sem grupo): ${soltos.join(', ')}`);
console.log(`  ${OUT}`);
