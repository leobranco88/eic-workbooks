# EIC Checking Points — Blueprint

Guia de referência para criar Checking Points em HTML a partir de agora. Cobre estrutura, design, PDF, áudio, deploy e os erros que já corrigimos (pra não repetir).

---

## 1. O que é um Checking Point

Prova/avaliação de unidade (Grammar, Vocabulary, Real Life, Listening, Reading, Writing), entregue como:

- **1 arquivo `.html`** autocontido (fotos e áudio embutidos em base64, funciona offline, sem dependências externas exceto a fonte Inter do Google Fonts)
- **1 arquivo `.pdf`** gerado a partir do mesmo HTML, pra impressão e upload em outros sistemas

Os dois arquivos **sempre vivem na mesma pasta**, com o **mesmo nome base**:

```
Checking_Point_[N]_[Turma].html
Checking_Point_[N]_[Turma].pdf
```

Exemplo: `Checking_Point_1_Teens_2.html` / `Checking_Point_1_Teens_2.pdf`

---

## 2. Convenção de nomes e pastas (importante!)

**Nunca usar espaço em nome de pasta ou arquivo que vai pro Firebase Hosting.** Espaço vira `%20` na URL — funciona, mas fica feio e é fácil de errar ao compartilhar o link.

❌ `Checkingpoints/Teens 2/`
✅ `Checkingpoints/Teens-2/`

Caminho final publicado (exemplo real):
```
https://eic-worksheets.web.app/Checkingpoints/Teens-2/Checking_Point_1_Teens_2.html
```

---

## 3. Origem do conteúdo

Quando o material de origem é um `.pages`, `.docx` ou `.pdf` da editora (Cengage/Life, etc.):

1. Extrair texto com `pdfplumber` (se `.pages`, converter primeiro com LibreOffice: `soffice --headless --convert-to pdf`)
2. Extrair imagens embutidas direto da pasta `Data/` do `.pages` (é um zip) — não usar screenshot/print da página, a imagem original tem mais qualidade
3. Reproduzir o conteúdo fielmente (textos, gabaritos, numeração) — nunca inventar itens

---

## 4. Estrutura do HTML

Template de uma página única, com:

- `<head>`: fonte Inter via Google Fonts, CSS inline em `<style>`
- Barra superior (`.toolbar`) fixa no navegador com os botões **Mostrar Gabarito** e **Baixar PDF** — some na impressão (`.no-print`)
- `.page`: container central, max-width 850px, fundo branco
- `.top-bar`: badge do checkpoint + nome da escola + copyright (ver seção 8)
- `<header class="doc-header">`: logo EIC + título do documento
- `.id-fields`: campos Name / Date
- `.instructions-card`: mensagem da Flow + timer de prova (ver seção 7)
- `<section class="block">` por matéria (Grammar, Vocabulary, Real Life, Listening, Reading, Writing), cada uma com `<h2 class="section-title">`

### Identidade visual (tokens)

```css
--accent: #E63946;      /* números de exercício, eyebrow */
--highlight: #FFE89C;   /* word bank */
--ink: #0A0A0F;         /* texto, títulos de seção (fundo preto) */
--paper: #FFFFFF;
--gray-line: #E4E4E7;
--gray-text: #52525B;
```
Fonte única: **Inter** (400/500/600/700/800/900). Zero emoji, zero mono, zero em-dash decorativo — consistente com o FPFC-02 usado no resto do material EIC.

---

## 5. Como formatar cada tipo de exercício

### 5.1 Múltipla escolha (circle the word)

**Não usar mais** o formato antigo com blanks antes de cada opção (`___ Her ___ She`) — ficava confuso e estourava a largura da página.

**Usar o formato de "pílulas"**: cada opção vira um botão arredondado pra circular à mão, seguido da frase com lacuna.

```html
<div class="mc-item">
  <span class="item-num">1.</span>
  <div class="mc-body">
    <div class="mc-options"><span class="mc-option">Her</span><span class="mc-option">She</span></div>
    <p class="mc-sentence"><span class="blank"></span> name is Chiara.</p>
  </div>
</div>
```

⚠️ **Bug já corrigido**: `.item-num` genérico (usado nas listas antigas) tem `position: absolute`. Ao reusar a classe dentro de `.mc-item`, é obrigatório sobrescrever com `position: static` — senão o número fica flutuando por cima da primeira pílula.

### 5.2 Fill-in-the-blank com word bank

Word bank em pílulas amarelas (`--highlight`) acima do texto corrido, lacunas com `<span class="blank"></span>` inline no meio da frase.

### 5.3 Matching (colunas)

Grid de 2 colunas (`.match-columns`): lista numerada à esquerda, lista com blank + letra à direita.

### 5.4 Foto + legenda (ex: "look at the photo")

- Imagem sempre **com teto de altura**: `max-height: 300px`, `width: auto`, `margin: 0 auto` — nunca `width: 100%` sem limite, senão a foto sozinha ocupa a página inteira.
- Comprimir antes de embutir: redimensionar pra ~1400px de largura e salvar como JPEG qualidade ~85 (reduz de MBs pra ~150-250KB).
- Quando o número do item aparece **dentro de um parágrafo corrido** (ex: "a bed 1 ___ the left"), nunca deixar o número como texto solto — fica parecendo parte da frase. Envolver em `<span class="blank-num">1</span>` (sobrescrito, negrito, cor de destaque) pra ficar claro que é o marcador da lacuna, não conteúdo do texto.

### 5.5 Listening

- Áudio embutido em base64 dentro de `<audio controls>`, dentro de um `.audio-card` com borda esquerda vermelha.
- Player **escondido na impressão** (`.listening-player { display: none }` em `@media print`), com uma notinha substituta: *"O áudio desta faixa está disponível no arquivo HTML digital."*

### 5.6 Reading passage

Bloco com fundo levemente cinza, borda fina, título do texto em negrito. Perguntas True/False/Not enough information com as três opções em caixinhas.

### 5.7 Writing

Checklist do que incluir + linhas de resposta (`.writing-lines`, divs com `border-bottom`).

---

## 6. Regras de quebra de página (PDF)

Isso deu mais dor de cabeça, documentar bem:

- **Nunca** aplicar `break-inside: avoid` numa `<section>` inteira — se ela não couber no resto da página, o navegador empurra a seção inteira pra próxima, deixando a página atual quase em branco.
- Aplicar `break-inside: avoid` só nas unidades pequenas: `.exercise`, `.mc-item`, `.reading-passage`, `.dialogue`, `.match-columns`, `.audio-card`, `.photo-frame`, `.instructions-card`.
- Pra impedir título de seção "órfão" (título sozinho no fim da página, exercício pulando pra próxima com espaço em branco enorme):
  ```css
  h2.section-title { break-after: avoid; }
  h2.section-title + .exercise { break-before: avoid; }
  ```
- Margens mais enxutas **na impressão** (`@media print`) do que na tela — aperta o conteúdo pra caber mais por página sem ficar apertado na visualização web.
- **`.no-print` precisa de uma regra CSS de verdade.** Não basta colocar a classe no elemento — se `@media print { .no-print { display: none !important; } }` não existir explicitamente, a classe não faz nada (bug que já caímos: o timer aparecia no PDF porque só o `.toolbar` tinha a regra, e `.no-print` sozinho não).

Checklist rápido antes de entregar um PDF novo:
1. Primeira página não pode terminar vazia ou quase vazia
2. Nenhum título de seção sozinho no fim de uma página
3. Nenhum exercício cortado no meio entre duas páginas
4. Foto de exercício cabe junto com o texto na mesma página
5. Rodapé com paginação aparece em **todas** as páginas (ver seção 6.1)

### 6.1 Cabeçalho/rodapé repetindo em todas as páginas (importante!)

O conteúdo dentro do `<body>` do HTML só imprime **uma vez**, no fluxo normal — não existe "rodapé fixo" nativo em HTML/CSS puro que se repita em cada página impressa. Pra isso, usa-se os parâmetros nativos do Playwright na hora de gerar o PDF, **não** um elemento `<footer>` no HTML:

```python
footer_html = '''
<div style="font-family:Arial,Helvetica,sans-serif;font-size:8px;color:#52525B;width:100%;padding:0 12mm;display:flex;align-items:center;justify-content:space-between;">
  <div style="display:flex;align-items:center;gap:6px;">
    <span style="background:#E63946;color:#fff;font-weight:700;padding:2px 8px;border-radius:999px;font-size:8px;">Nº 1</span>
    <span>EIC &middot; Escola de Idiomas e Cultura</span>
  </div>
  <div>Checking Point 1 &mdash; Teens 2 &middot; &copy; 2025 Cengage Learning, Inc. &middot; Página <span class="pageNumber"></span>/<span class="totalPages"></span></div>
</div>
'''

page.pdf(
    path='Checking_Point_X.pdf',
    format='A4',
    margin={'top': '14mm', 'bottom': '20mm', 'left': '12mm', 'right': '12mm'},  # bottom maior pra caber o rodapé
    print_background=True,
    display_header_footer=True,
    header_template='<span></span>',   # vazio, senão o Chromium mostra título/URL da página
    footer_template=footer_html
)
```

⚠️ Esse `header_template`/`footer_template` roda isolado, **sem acesso** ao CSS/fontes do documento — por isso usa fonte web-safe (`Arial, Helvetica`) só nesse trechinho, e estilo inline. `<span class="pageNumber"></span>` e `<span class="totalPages"></span>` são classes especiais que o Chromium preenche sozinho.

**No HTML**, como a página é um scroll único (não existe "página 2, 3..."), esse mesmo bloco de identificação (badge + nome da escola + copyright) fica só **uma vez, no topo do documento** (`.top-bar`), antes do cabeçalho — não faz sentido repetir.

---

## 7. Mensagem da Flow + timer (padrão a partir de agora)

Todo Checking Point deve ter, entre o campo Name/Date e o início dos exercícios, um card de orientação com a personagem **Flow** dando as boas-vindas e o tempo de prova.

```html
<div class="instructions-card">
  <img class="flow-avatar" src="data:image/jpeg;base64,..." alt="Flow">
  <div class="instructions-body">
    <p class="instructions-name">Flow diz</p>
    <p class="instructions-message">Antes de começar: leia cada questão com calma, circule suas respostas com clareza e revise antes de entregar. Você tem <strong>45 minutos</strong> pra essa prova — dá pra fazer com tranquilidade.</p>
    <div class="timer-widget no-print">
      <span class="timer-display" id="timerDisplay">45:00</span>
      <div class="timer-controls">
        <button class="timer-btn" onclick="startTimer()" type="button">Começar</button>
        <button class="timer-btn timer-btn-ghost" onclick="pauseTimer()" type="button">Pausar</button>
        <button class="timer-btn timer-btn-ghost" onclick="resetTimer()" type="button">Reiniciar</button>
      </div>
    </div>
    <p class="print-only" style="font-size:12.5px; color:var(--gray-text); margin-top:4px;">Você tem 45 minutos para completar esta prova.</p>
  </div>
</div>
```

Regras:
- **O tempo (45 min) é o padrão**, mas ajustável por prova — trocar o número no texto e em `timerSeconds = 45 * 60` no JS.
- **Avatar da Flow**: recortar em quadrado centrado no rosto, redimensionar pra ~500px, salvar como JPEG qualidade ~88, aplicar como círculo via `border-radius: 50%` + `object-fit: cover`.
- **O timer é HTML-only** — some na impressão (`.no-print`) e vira uma frase estática (`.print-only`): "Você tem 45 minutos para completar esta prova." Faz sentido: um cronômetro interativo não funciona no papel.
- Cor da moldura/destaque do card usa `--teacher` (roxo `#534AB7`), consistente com o resto do material voltado a orientação/professor.
- Zero emoji na mensagem da Flow — segue a mesma regra do FPFC-02 pro resto do documento.
- ⚠️ **O card inteiro da Flow (`.instructions-card`) é escondido no PDF** (`display: none !important` em `@media print`), não só o timer. Ele existe só pra dar boas-vindas na tela — no papel ele empurrava os exercícios pra baixo e criava espaço em branco na página 1. Regra geral: qualquer bloco novo "só HTML" deve ser escondido inteiro no print, não parcialmente.

⚠️ **Pegadinha ao medir se o conteúdo cabe numa página**: nunca meça a altura do conteúdo usando o viewport padrão do navegador (ex: 1280px) — a `.page` tem `max-width: 850px`, então qualquer viewport maior que isso mede errado. Na hora de gerar o PDF de verdade, o Chromium usa a largura **real do papel A4 menos as margens** (~703px pra margens de 12mm), que é bem mais estreita — o texto quebra em mais linhas e fica mais alto do que parece no navegador normal. Pra medir corretamente antes de gerar o PDF:
```python
page = b.new_page(viewport={'width': 703, 'height': 1200})  # largura real do conteúdo em A4 com margens de 12mm
page.goto('file:///caminho/Checking_Point_X.html')
page.emulate_media(media='print')
# agora sim getBoundingClientRect() bate com o que vai sair no PDF
```

---

## 8. Identidade visual dos Checkpoints (badge numerado)

O Basecamp (`eic-basecamp.web.app`) já usa pílulas coloridas "Nº 1" a "Nº 6" nos cards de cada checkpoint. Replicamos a mesma cor no documento do Checking Point correspondente, dentro da `.top-bar`:

```html
<div class="top-bar" style="--cp-color:#E63946;">
  <div class="footer-left">
    <span class="cp-badge-footer">Nº 1</span>
    <span>EIC &middot; Escola de Idiomas e Cultura</span>
  </div>
  <span>Checking Point 1 — Teens 2 · Life, Level 2, Unit 2 · © 2025 Cengage Learning, Inc.</span>
</div>
```

⚠️ **Não colocar o badge no cabeçalho** (`.doc-header`) — já tentamos, ele fica absoluto e corta o texto "UNIT 2" do eyebrow em telas menores. O lugar seguro é dentro da `.top-bar`, que tem espaço de sobra.

| Checkpoint | Cor (`--cp-color`) |
|---|---|
| Nº 1 | `#E63946` (vermelho) |
| Nº 2 | a confirmar (dourado/mostarda no Basecamp) |
| Nº 3 | a confirmar (verde-azulado) |
| Nº 4 | a confirmar (verde) |
| Nº 5 | a confirmar (rosa/magenta) |
| Nº 6 | a confirmar (roxo/índigo) |

Mesma cor entra também no `footer_template` do PDF (seção 6.1), então repetir o hex nos dois lugares ao gerar cada checkpoint.

---

## 9. Campos de nota (total geral + total por seção)

Todo Checking Point deve ter dois níveis de campo pra pontuação, ambos em branco (sem presumir valor máximo que não esteja no material original):

**Total geral**, ao lado de Name/Date:
```html
<div class="total-field">
  <label>Total</label>
  <div class="total-box"><span class="blank"></span> / <span class="blank"></span></div>
</div>
```

**Total por seção**, no final de cada uma das 6 seções (Grammar, Vocabulary, Real Life, Listening, Reading, Writing), antes do `</section>`:
```html
<div class="section-total">
  <span>Total Grammar</span>
  <span class="blank"></span> / <span class="blank"></span>
</div>
```

Regra: como nem todo exercício do material original vem com pontuação declarada (`___ / 10` etc.), os campos ficam **totalmente em branco** — não inventamos denominador. O professor preenche os dois números (acertos e total) conforme o próprio critério de correção.

⚠️ Cada campo novo desses adiciona altura real ao documento — depois de adicionar, sempre remedir com o método da seção 6.1 (viewport 703px) pra conferir se não estourou o encaixe de nenhuma página. Foi exatamente o que aconteceu ao adicionar os 6 campos de seção: a Listening passou a não caber mais na página 3 por 21pt. Resolvido apertando margens de `.audio-card`, `.ex-head` e `.section-total` só na impressão.

---

## 10. Geração do PDF

**Não usar** WeasyPrint pra esse tipo de documento (o layout usa flexbox/grid pesado, e o WeasyPrint não renderiza sempre igual ao Chrome).

**Usar Playwright** (Chromium headless) — ele imprime exatamente o que aparece no navegador. Já incluindo o rodapé fixo com paginação (ver seção 6.1):

```python
from playwright.sync_api import sync_playwright

footer_html = '''...'''  # ver template completo na seção 6.1

with sync_playwright() as p:
    b = p.chromium.launch()
    page = b.new_page()
    page.goto('file:///caminho/Checking_Point_X.html')
    page.emulate_media(media='print')
    page.pdf(
        path='Checking_Point_X.pdf',
        format='A4',
        margin={'top': '14mm', 'bottom': '20mm', 'left': '12mm', 'right': '12mm'},
        print_background=True,
        display_header_footer=True,
        header_template='<span></span>',
        footer_template=footer_html
    )
    b.close()
```

Depois de gerar, validar com `pdfplumber` (texto de cada página) antes de considerar pronto — mais confiável que só olhar print de tela.

---

## 11. Botão "Baixar PDF"

⚠️ **Bug já corrigido**: o botão **não deve** chamar `window.print()`. Isso pula direto pra caixa de impressão do sistema operacional, sem deixar o usuário ler o PDF primeiro — diferente do padrão dos outros projetos EIC (onde o PDF abre no visualizador nativo do navegador).

**Certo**: link direto pro arquivo `.pdf`, mesma pasta, abrindo em nova aba:

```html
<a class="download-btn" href="Checking_Point_X.pdf" target="_blank" rel="noopener">
  Baixar PDF
</a>
```

Isso abre o visualizador de PDF nativo do Chrome — zoom, leitura, e o próprio botão de imprimir/baixar dele.

---

## 12. Deploy (Firebase Hosting)

```bash
cd ~/Downloads/eic-workbooks
git add .
git commit -m "checking point: [descrição]"
git push origin main
firebase deploy --only hosting
```

Se der erro de autenticação (`Your credentials are no longer valid`):
```bash
firebase login --reauth
```

Confirmar sempre qual conta está logada — `leobranco88@gmail.com` (pessoal) ou `leobranco@eicschool.com.br` (Workspace) — dependendo de qual projeto Firebase hospeda aquele site.

Depois do deploy, testar o link publicado com **Cmd+Shift+R** (recarrega ignorando cache) antes de considerar no ar — cache de navegador é a causa mais comum de "não é a última versão".

---

## 13. Checklist final antes de entregar um Checking Point novo

- [ ] Conteúdo confere 100% com o material de origem (sem inventar item)
- [ ] Logo preta (não a cinza-clara, que é a versão para fundo escuro)
- [ ] Fotos com teto de altura, comprimidas
- [ ] Áudio embutido, com fallback de texto na versão impressa
- [ ] Nenhuma página do PDF vazia ou quase vazia
- [ ] Nenhum título de seção órfão
- [ ] Nenhum exercício cortado entre páginas
- [ ] Botão "Baixar PDF" aponta pro arquivo `.pdf` real, mesma pasta, mesmo nome base
- [ ] Pasta e arquivo sem espaço no nome
- [ ] Rodapé com paginação em todas as páginas do PDF (`header_template`/`footer_template`)
- [ ] Badge do checkpoint (`.top-bar`) com a cor certa, batendo com o card do Basecamp
- [ ] Card da Flow com o tempo de prova certo, timer testado (começar/pausar/reiniciar)
- [ ] Timer some no PDF e vira frase estática
- [ ] Card da Flow inteiro (não só o timer) escondido no PDF
- [ ] Campo de Total geral (Name/Date) presente
- [ ] Campo de Total por seção presente nas 6 seções
- [ ] Testado o link publicado com reload forçado
