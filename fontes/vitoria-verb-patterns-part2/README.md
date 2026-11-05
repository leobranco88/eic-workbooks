# Verb Patterns · Part 2 · prática da Vitória (fonte)

Fonte da prática online com respostas gravadas no Firestore. Esta pasta NÃO vai para o ar (fica fora de `public/`).
O que vai para o ar está em `public/vitoria/verb-patterns-part2/` (gerado por `build.py`).

- `dados.js`: conteúdo (palavras, exercícios 1 a 5). Trocar aqui para outro aluno ou tema.
- `index.html`: página da aluna. `professor.html`: tela do professor.
- `config.js`, `firebase-comum.js`: gravação no Firestore (`neural_praticas/{aluna}/respostas`).
- `firestore.rules.txt`: regras completas do projeto eic-worksheets com o bloco `neural_praticas`.
- `build.py`: embute fontes, scripts e logo. Rodar `python3 build.py` aqui dentro; gera `dist/` e `deploy/public/vitoria/verb-patterns-part2/`.
- `fonts/`, `eic-logo.png`: ativos embutidos pelo build.

Para outro aluno: copiar a pasta, trocar `dados.js`, `NOMES` no `professor.html`, o texto da página, e o caminho de saída no `build.py`.
Testes do professor: usar `?aluna=teste` nos dois links.
Veja as skills `eic-pratica-online-respostas` e `eic-publicar-workbooks`.
