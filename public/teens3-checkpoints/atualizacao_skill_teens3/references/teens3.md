# Teens 3 (Life 3) — regras próprias

Tudo o que vale para o Teens 1 e o Teens 2 continua valendo. Aqui só o que é novo ou diferente.

## Identidade
- Cor da turma: roxo #9B4DBA (pontas lilases da flor da capa do Life 3), texto branco na faixa.
- Selo: margarida roxa no centro (assets/teens3/selo_centro.png), gerado pelo molde oficial
  (`identidade_turma.py selo`). Selos dos CP1 a CP6 prontos em assets/teens3/selos.
- Figurinhas das seções recoloridas no roxo (assets/teens3).
- HTML do professor: COR_FUNDO '#E8E4EC', COR_LINHA '#D4CDDC' e COR_SOBRE_PRETO '#FFFFFF'.
  Regra do Leo: botão preto tem texto BRANCO (play, Mostrar/Ocultar, ● Complete, Como aplicar),
  nunca na cor da turma. O build_cp.py desta pasta aceita COR_SOBRE_PRETO no módulo de dados.

## Ordem da prova
- A prova abre SEMPRE pelo Grammar. Nunca abrir pelo Reading (texto longo no começo cansa e
  aumenta a ansiedade; a pesquisa sobre ordem de itens favorece começar pelo mais fácil).
- Writing SEMPRE no fim (Complete). A última página do writing é enchida com linhas
  (scripts/estender.py, que funciona até com uma linha só no original).
- CP1: Complete = Grammar, Vocabulary, Reading, Listening, Real Life, Writing (8 páginas);
  Speed = Grammar, Listening, Reading, Vocabulary, Real Life (6 páginas).

## Paginação: exercício pode continuar na página seguinte
O Reading do Life 3 (texto + primeiro exercício) ocupa quase uma página e abria vão antes dele.
Solução aprovada: estilo vestibular, o exercício pode começar no pé de uma página e terminar na
próxima (scripts/montar_split.py, opção "quebrar_exercicios": true no config). Continuam presos:
texto do Reading + primeiro exercício, grupo do mesmo áudio na mesma página e o writing inteiro
("inteiro": true no bloco). Testar as ordens de seção com Grammar fixo no começo e Writing no fim.

## Múltipla escolha com opções numa linha
scripts/mcq.py gera os blocos (um pedaço por item: pergunta + linha do "a.", reescrita com
todas as opções). Aceita troca de texto de opção (reescrita de item) e limite de largura.

## Rubrica
- A ordem das seções da rubrica segue a ordem da prova de CADA versão. O build padrão usa a
  ordem fixa do RUB; o dados_cp1_t3.py reordena o RUB pelo mapa da versão (ver o fim do arquivo).
- Não pôr no GRAFIA exercício cuja linha aceita erro de grafia (contradição no topo da rubrica).
- "Marque todas" com poucas certas (U2 ex. 7: 3 de 5): 1 ponto por PESSOA julgada (marcada se
  sim, em branco se não), para o exercício valer 5 e o total fechar em 100.

## Listening
- Transcrições brutas das 24 faixas das Units 1-12: references/teens3-transcricoes-brutas.json.
  Scripts limpos em references/scripts-listening-teens3.json, preenchidos a cada checkpoint.
- O nome do arquivo engana: TR 1.1 = u01_listen1_sleep; TR 2.1 = u02_listen2_plogging
  (listen1_sport não é). Conferir pelo conteúdo nas próximas unidades.
- Falante sem nome: Man / Woman quando as perguntas usam o gênero ("the woman in Conversation 1").

## Qualidade do material de origem (CP1)
- U2 Real Life: três respostas reescritas (a. Great idea! Let's do it together. / b. No, I'm not
  interested in acting. / a. Go for it!); as letras do gabarito não mudam.
- U1 ex. 11: tirado o "again" do enunciado (a ordem dos exercícios de Reading pode mudar).
- U1 Writing (formulário) é só cópia de dados: preferir o writing de produção da outra unidade.

## Ditado
- A turma já fez Life 1 e 2: vocabulário e estruturas deles valem. ESTRUTURAS_FUTURAS do Life 3
  no dados_cp1_t3.py (past continuous U4, present perfect for/since U7, conditional U8, passive e
  used to U9).
- A varredura não reconhece headword de duas palavras (sore throat): preferir palavra única.

## Exercício criado pela EIC (exceção documentada)
A regra continua: checkpoint é seleção e edição dos exercícios originais. Ponto do currículo que o
teste original não cobra fica "fora deste checkpoint" (ex.: comparative modifiers no CP2), e o Leo
aceita isso. Só se cria um exercício quando as TRÊS condições se juntam:
1. O ponto é central: está no título gramatical da unidade no currículo (não word focus nem detalhe).
2. Nenhum exercício original das duas unidades o cobre, nem de raspão.
3. Não há exercício pronto nos outros testes da Cengage do mesmo nível (Mid-course MC1 e MC2,
   testes no formato Cambridge). Se houver, usar esse: continua sendo original.
Como criar: mesmo formato e tipografia do livro (Carlito, recuo, numeração); raciocínio pedagógico
obrigatório (o que o aluno sabe, armadilhas de brasileiro, uma resposta só) e varredura; no máximo
5 itens, de preferência substituindo um exercício menos importante; a rubrica marca
"exercício da EIC". Avisar o Leo antes e mostrar o exercício para aprovação.

## CP2 (Units 3-4)
- Faixas: TR 3.1 = u03_listen2_travel (programa de rádio, Host + Cynthia, Jonathan, Brenda,
  Denise, Bill); TR 4.1 = u04_listen1_climbing (Ken e Sarah).
- Só dois exercícios de gramática por unidade: a prova chegava a 95. Para fechar 100 com 50 × 50,
  entraram os dois readings: U3 inteiro (10) e U4 texto + ex. 9 (5). Reading 15.
  Com dois textos, "ordem_livre": false (a permutação embaralhava exercício e texto) e o texto
  prende só o começo do primeiro exercício (montar_split.py já faz isso com quebrar_exercicios).
- Complete: Grammar, Vocabulary, Listening, Real Life, Reading, Writing (10 páginas).
  Speed: Grammar, Vocabulary, Real Life, Listening, Reading (7 páginas); saem listening U3,
  writing, texto do Sudoku e U3 ex. 5.
- Correções: taxi "rank" (britânico) trocado por "lane" nos distratores do U3 ex. 5, com redação
  no PDF de origem (apply_redactions), sem mexer nas caixas; U3 ex. 4 item 2 reescrito ("People in
  my village have ridden bikes for a hundred years. They're the ___ way to get around.");
  "again" tirado dos enunciados de Reading. U4 ex. 5 item 2: Then ou Next.
- U3 ex. 8 em duas colunas (colunas_forcar) para caber.

## CP3 (Units 5-6)
- Faixas: TR 5.1 = u05_listen2_accomodation (Man + Receptionist, camping); TR 6.1 =
  u06_listen2_celebrations (cinco conversas; falantes Friend/Man/Woman/Derek/Organizer pelo
  gênero das perguntas). No Life 3, a faixa do teste costuma ser a listen2: conferir sempre.
- Pontos: Grammar 20, Vocabulary 30, Reading 10 (U5), Listening 20, Real Life 10, Writing 10 (U6).
  Reading da U5 (mais claro) e writing da U6 (descrição de evento, mais próxima do adolescente).
  U5 ex. 8 "choose all" (3 de 5): 1 ponto por afirmação, como no CP1.
- Complete: Grammar, Vocabulary, Reading, Listening, Real Life, Writing (9 páginas; a página 8
  fica em 66% para o writing ter a página 9 inteira, 19 linhas; aprovado pelo Leo).
  Speed: Grammar, Listening, Vocabulary, Real Life, Reading (7 páginas).
- "grupo_na_mesma_pagina": false no CP3: o listening pode continuar na página seguinte (o próprio
  teste da U6 quebra assim). Com true, sempre sobrava uma página com 35%.
- Correções: gabarito do livro errado no U5 Real Life (C = 3, não 4); U6 ex. 1 item 5 reescrito
  ("During exam week, it ___ (seem hard / not be) stressed."); "again" tirado do U5 ex. 10.
- Britanismos do ÁUDIO ficam nas perguntas (cooker, booking, fancy-dress): trocar faria o aluno
  ler uma palavra e ouvir outra. A rubrica explica.
- Medir o preenchimento das páginas pelos pixels (render a 30 dpi), não pelos blocos de texto:
  o texto escondido fora do recorte engana a medida.
