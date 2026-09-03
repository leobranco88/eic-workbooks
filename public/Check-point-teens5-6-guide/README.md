# Guias do Aluno · Teens 5 e 6

Cinco arquivos HTML autocontidos. Nenhum depende de servidor, banco ou build.
A única requisição externa é a fonte do Google Fonts (Inter e Caveat).

## Deploy no Firebase

Copie a pasta inteira para dentro de `public/` do repositório `eic-workbooks`:

    public/guias/index.html
    public/guias/EIC-Guia-do-Aluno-Checkpoint.html
    public/guias/EIC-Guia-do-Aluno-Grammar-Vocab.html
    public/guias/EIC-Guia-do-Aluno-Listening.html
    public/guias/EIC-Guia-do-Aluno-Writing.html

Depois:

    git add public/guias
    git commit -m "Guias do aluno: reading, grammar and vocabulary, listening, writing"
    firebase deploy --only hosting

Endereço final: https://eic-worksheets.web.app/guias/

## Estrutura

O `index.html` é a capa e linka para os quatro guias por caminho relativo.
Nos quatro guias, a marca no topo esquerdo volta para a capa.
Se renomear qualquer arquivo, corrija os links no `index.html`.

## Importante

Estes são materiais do ALUNO. Podem ir para pasta pública.
Não confundir com os HTML de prova com gabarito, que são de uso do professor
e não devem subir para o site.
