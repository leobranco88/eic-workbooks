/**
 * setup.js — rode UMA VEZ na raiz do projeto
 * Uso: node setup.js
 *
 * O que faz automaticamente:
 *  1. Verifica que está na pasta certa (firebase.json existe)
 *  2. Lê o firebase.json atual
 *  3. Adiciona o predeploy hook (sem apagar nada existente)
 *  4. Salva o firebase.json atualizado
 *  5. Testa o generate-hub.cjs
 *  6. Mostra o resultado
 */

const fs   = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const ROOT      = __dirname;
const FIREBASE  = path.join(ROOT, 'firebase.json');
const HUB_GEN   = path.join(ROOT, 'generate-hub.cjs');

const green  = s => `\x1b[32m${s}\x1b[0m`;
const red    = s => `\x1b[31m${s}\x1b[0m`;
const yellow = s => `\x1b[33m${s}\x1b[0m`;
const bold   = s => `\x1b[1m${s}\x1b[0m`;

console.log('\n' + bold('EIC Hub — Configuração automática') + '\n');

// ── Passo 1: verificar pasta ──────────────────────────────────────────────────
process.stdout.write('1. Verificando pasta do projeto... ');

if (!fs.existsSync(FIREBASE)) {
  console.log(red('✗'));
  console.log(red('\nErro: firebase.json não encontrado.'));
  console.log(yellow('Certifique-se de rodar este script na raiz do projeto eic-workbooks:'));
  console.log('   cd ~/Downloads/eic-workbooks');
  console.log('   node setup.js\n');
  process.exit(1);
}
console.log(green('✓  firebase.json encontrado'));

// ── Passo 2: verificar generate-hub.cjs ───────────────────────────────────────
process.stdout.write('2. Verificando generate-hub.cjs... ');

if (!fs.existsSync(HUB_GEN)) {
  console.log(red('✗'));
  console.log(red('\nErro: generate-hub.cjs não encontrado.'));
  console.log(yellow('Baixe o generate-hub.cjs e coloque na mesma pasta do firebase.json.'));
  console.log('Deve estar em: ' + ROOT + '\n');
  process.exit(1);
}
console.log(green('✓  generate-hub.cjs encontrado'));

// ── Passo 3: ler e atualizar firebase.json ────────────────────────────────────
process.stdout.write('3. Atualizando firebase.json... ');

let config;
try {
  config = JSON.parse(fs.readFileSync(FIREBASE, 'utf8'));
} catch(e) {
  console.log(red('✗'));
  console.log(red('\nErro ao ler firebase.json: ' + e.message + '\n'));
  process.exit(1);
}

// Garante que hosting existe
if (!config.hosting) config.hosting = {};

// Verifica se predeploy já existe
const existing = config.hosting.predeploy;
const HOOK = 'node generate-hub.cjs';

if (existing) {
  const hooks = Array.isArray(existing) ? existing : [existing];
  if (hooks.includes(HOOK)) {
    console.log(yellow('já configurado  (nenhuma alteração necessária)'));
  } else {
    // Adiciona sem remover o que já existe
    config.hosting.predeploy = [...hooks, HOOK];
    fs.writeFileSync(FIREBASE, JSON.stringify(config, null, 2));
    console.log(green('✓  predeploy adicionado'));
  }
} else {
  config.hosting.predeploy = [HOOK];
  fs.writeFileSync(FIREBASE, JSON.stringify(config, null, 2));
  console.log(green('✓  predeploy configurado'));
}

// ── Passo 4: testar o generate-hub.cjs ────────────────────────────────────────
process.stdout.write('4. Gerando hub.html pela primeira vez... ');

try {
  const output = execSync('node generate-hub.cjs', { cwd: ROOT, encoding: 'utf8' });
  console.log(green('✓'));
  console.log('   ' + output.trim());
} catch(e) {
  console.log(red('✗'));
  console.log(red('\nErro ao gerar hub.html:'));
  console.log(e.stderr || e.message);
  process.exit(1);
}

// ── Passo 5: verificar que hub.html foi criado ────────────────────────────────
const hubPath = path.join(ROOT, 'public', 'hub.html');
process.stdout.write('5. Verificando public/hub.html... ');

if (fs.existsSync(hubPath)) {
  const size = (fs.statSync(hubPath).size / 1024).toFixed(0);
  console.log(green(`✓  criado (${size} KB)`));
} else {
  console.log(red('✗  hub.html não foi criado'));
  process.exit(1);
}

// ── Resumo ────────────────────────────────────────────────────────────────────
console.log('\n' + '─'.repeat(52));
console.log(green(bold('✓  Tudo configurado com sucesso!')));
console.log('─'.repeat(52));
console.log('\nA partir de agora, seu fluxo normal já funciona:');
console.log(bold('\n   git add .'));
console.log(bold('   git commit -m "novo material"'));
console.log(bold('   git push origin main'));
console.log(bold('   firebase deploy --only hosting'));
console.log('\nO hub se gera automaticamente antes de cada deploy.');
console.log('URL do hub: ' + bold('https://eic-worksheets.web.app/hub.html'));
console.log('');
