# EIC · Guia do aluno · Writing · Kids 5 e 6

Página estática, sem build. Um HTML e uma pasta de assets.

## Estrutura

    index.html                 a home, com a lista dos guias
    writing-kids-5-6.html      o guia de Writing
    assets/img/                ilustrações (webp) e logotipos (png)
    assets/audio/              as sete faixas do diário (mp3, mono 40 kbps)
    vercel.json                cache longo nos assets

## Publicar um guia novo

Cada guia é um HTML solto na raiz. Para ligar um que estava "em breve",
abra o index.html, ache o bloco daquela habilidade e troque

    <div class="guia guia-off">          por   <a class="guia" href="arquivo.html">
    ...
    <span class="tag">...</span>          por   a seta em SVG (copie do bloco de Writing)
    </div>                                por   </a>

## Rodar localmente

    python3 -m http.server 8000

e abrir http://localhost:8000

Não abra o index.html com duplo clique: em `file://` o navegador
bloqueia o carregamento do áudio.

## Publicar

Qualquer host estático. Na Vercel, sem framework, output = raiz do projeto.

## Editar

Todo o conteúdo é HTML puro dentro do próprio index.html, em português e
inglês lado a lado, marcados com `class="pt"` e `class="en"`. Ao mexer num
texto, mexa nos dois: o botão do topo esconde um e mostra o outro, e se um
par ficar desemparelhado a página fica sem aquele trecho num dos idiomas.

## Trocar o áudio

Gere as faixas novas, comprima em mono para não pesar:

    ffmpeg -i entrada.mp3 -ac 1 -ar 24000 -b:a 40k assets/audio/dia-1.mp3

Os nomes vão de dia-1.mp3 a dia-7.mp3, na ordem dos sete dias do diário.
