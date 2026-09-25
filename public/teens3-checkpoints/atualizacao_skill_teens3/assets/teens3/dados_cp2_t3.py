# Dados do Checkpoint 2 (Teens 3, Life 3, Units 3-4) para build_cp.py
def P(en,pt): return f'{en}<span class="pt">{pt}</span>'
CP=2; UNITS=(3,4); DIR='/home/claude/t3/cp2'; TURMA='Teens 3'
COR='#9B4DBA'; COR_TEXTO='#FFFFFF'; COR_SOBRE_PRETO='#FFFFFF'
COR_FUNDO='#E8E4EC'; COR_LINHA='#D4CDDC'
SELO='/home/claude/t3/selo_cp2.png'; PACK='/mnt/user-data/uploads/Teens3_CP2_dictation_audios.json'
ICONES='/home/claude/t3/fig'
SCRIPTS='/home/claude/t3/scripts/scripts-listening-teens3.json'
AUD='/home/claude/t3/src/life3e_ame_L3_asmt_'
TRACKS=[('Track 3.1',AUD+'u03_listen2_travel.mp3',['U3-7','U3-8']),
        ('Track 4.1',AUD+'u04_listen1_climbing.mp3',['U4-6','U4-7'])]
PTS={'complete':{'Grammar':20,'Vocabulary':25,'Real Life':10,'Listening':20,'Reading':15,'Writing':10},
     'speed':{'Grammar':20,'Vocabulary':20,'Real Life':10,'Listening':10,'Reading':10}}
W='U4-11'
GRAFIA=['U3-1','U4-1','U4-2','U4-4']
WINTRO=("<b>Ex. {WN}.</b> A short story about an experience in the student’s town or area, 100 to 120 words. Five criteria, each scored 0 to 2. Each criterion measures one thing only. Content from Units 3 and 4.",
        "<b>Ex. {WN}.</b> Uma história curta sobre uma experiência na cidade ou região do aluno, de 100 a 120 palavras. Cinco critérios de 0 a 2, cada um mede uma coisa só.")
ANS={'U3-1':['faster','best','worse','most expensive','bigger'],
 'U3-2':['as reliable as','as expensive as','not as busy as','not as fun as','as punctual as'],
 'U4-1':['A went','B took','C Did … bring','D did … celebrate','E weren’t'],
 'U4-2':['A was writing','B were trying','C didn’t climb','D wasn’t sleeping','E Was she speaking'],
 'U3-3':['A traffic jam','B carbon emissions','C city center','D speed limit','E container ships'],
 'U3-4':['comfortable','traditional','convenient','reliable','punctual'],
 'U3-5':['fare','platform','change','gate','stop'],
 'U4-3':['a','c','b','a','c'],
 'U4-4':['A solve','B organize','C competitor','D challenge','E test'],
 'U3-6':['a','c','b','e','d'],
 'U4-5':['unfortunately','Then <i>(accept Next)</i>','That was a good idea!','What did you do?','While'],
 'U3-7':['e','d','a','b','c'],'U3-8':['A c','B b','C a','D b','E a'],
 'U4-6':['A 4','B 3','C 1','D 2','E 5'],'U4-7':['A b','B c','C b','D a','E c'],
 'U3-9':['e','c','b','a','d'],'U3-10':['c','b','c','a','b'],
 'U4-9':['repeated','smartphones','championships <i>(or competitions)</i>','exercise','work']}
LONGO={'U3-2','U3-3','U4-1','U4-2','U4-4','U4-5','U4-9'}
SECAO={'Grammar':['U3-1','U3-2','U4-1','U4-2'],'Vocabulary':['U3-3','U3-4','U3-5','U4-3','U4-4'],
       'Real Life':['U3-6','U4-5'],'Listening':['U3-7','U3-8','U4-6','U4-7'],'Reading':['U3-9','U3-10','U4-9']}
RUB=[('Grammar','Gramática',[
 (['U3-1'],P('The comparative or superlative form of the word in bold.','A forma comparativa ou superlativa da palavra em negrito.'),P('Spelling counts (<i>bigger</i>, <i>worse</i>). Item 2: <i>the best</i> scores; item 4: <i>the most expensive</i> scores.','A grafia conta. Com <i>the</i> vale igual.')),
 (['U3-2'],P('<i>as … as</i> or <i>not as … as</i>, as the sentence needs.','<i>as … as</i> ou <i>not as … as</i>, como a frase pede.'),P('Full forms do not apply here. <i>isn’t as busy as</i> scores in item 3.','<i>isn’t as busy as</i> vale no item 3.')),
 (['U4-1'],P('The past simple of the verb from the box.','O past simple do verbo do quadro.'),P('Items C and D: both words right for the point. Item E: <i>were not</i> scores.','Itens C e D: as duas palavras certas para o ponto. Item E: forma cheia vale.')),
 (['U4-2'],P('Past simple or past continuous, as the sentence needs.','Past simple ou past continuous, como a frase pede.'),P('Full forms (<i>did not climb</i>, <i>was not sleeping</i>) score.','Forma cheia vale.'))]),
 ('Vocabulary','Vocabulário',[
 (['U3-3'],P('The compound noun made of two words from the box.','O substantivo composto com duas palavras do quadro.'),P('Item E: <i>container ship</i> without -s still scores.','Item E: sem -s vale.')),
 (['U3-4'],P('The right adjective.','O adjetivo certo.'),P('Item 2 was rewritten from the book so that <i>traditional</i> fits.','O item 2 foi reescrito para <i>traditional</i> fazer sentido.')),
 (['U3-5'],P('The right word.','A palavra certa.'),P('<i>rank</i> (British) was replaced by <i>lane</i> in the options; the answers are the same.','<i>rank</i> foi trocado por <i>lane</i> nas opções; as respostas não mudam.')),
 (['U4-3'],P('The right option.','A opção certa.'),P('Two options marked score zero.','Duas opções marcadas não pontuam.')),
 (['U4-4'],P('The right form of the word from the box (verb or noun).','A forma certa da palavra do quadro (verbo ou substantivo).'),P('Spelling counts: <i>organise</i> (British) still scores.','A grafia conta; <i>organise</i> vale.'))]),
 ('Real Life','Situações reais',[
 (['U3-6'],P('The right letter.','A letra certa.'),P('Matching.','Associação.')),
 (['U4-5'],P('The right option.','A opção certa.'),P('Item 2: <i>Then</i> or <i>Next</i> (both work after <i>First</i>).','Item 2: <i>Then</i> ou <i>Next</i> (os dois funcionam depois de <i>First</i>).'))]),
 ('Listening','Compreensão auditiva',[
 (['U3-7'],P('The right letter.','A letra certa.'),P('Track 3.1, played twice.','Faixa 3.1, tocada duas vezes.')),
 (['U3-8'],P('The right option.','A opção certa.'),P('Track 3.1.','Faixa 3.1.')),
 (['U4-6'],P('The order number, 1 to 5.','O número da ordem, de 1 a 5.'),P('Track 4.1, played twice.','Faixa 4.1, tocada duas vezes.')),
 (['U4-7'],P('The right option.','A opção certa.'),P('Track 4.1.','Faixa 4.1.'))]),
 ('Reading','Leitura',[
 (['U3-9'],P('The right letter.','A letra certa.'),P('Matching.','Associação.')),
 (['U3-10'],P('The right option.','A opção certa.'),P('Two options marked score zero.','Duas opções marcadas não pontuam.')),
 (['U4-9'],P('One word from the article.','Uma palavra do texto.'),P('Item 3: <i>championships</i> or <i>competitions</i>. Small spelling slips that keep the word clear score.','Item 3: as duas valem. Erro pequeno de grafia que mantém a palavra clara vale.'))]),
]
WCRIT=[('Task','Tarefa','All four parts: an introduction, the background and what happened first, an important moment, and an ending.','As quatro partes: introdução, contexto e o que aconteceu primeiro, um momento importante e um final.','Two or three.','Duas ou três.'),
 ('Unit vocabulary','Vocabulário da unidade','Three or more words from Units 3 and 4 (<i>traffic jam</i>, <i>challenge</i>, <i>risk</i>, <i>adventure</i>, <i>dangerous</i>).','Três ou mais palavras das Units 3 e 4.','One or two.','Uma ou duas.'),
 ('Unit grammar','Gramática da unidade','Past simple used correctly, and at least two sentences with the past continuous for the background (<i>It was raining when…</i>).','Past simple correto e pelo menos duas frases com past continuous para o contexto.','One sentence with the past continuous, or several past simple mistakes.','Uma frase com past continuous, ou vários erros de past simple.'),
 ('Subskill: structuring your writing','Subskill: estruturar o texto','Time words that order the story (<i>First</i>, <i>Then</i>, <i>While</i>, <i>In the end</i>) and a new paragraph for each part.','Palavras de tempo que ordenam a história e um parágrafo para cada parte.','Some time words, but no paragraphs, or the reverse.','Algumas palavras de tempo, mas sem parágrafos, ou o contrário.'),
 ('Organization and length','Organização e tamanho','Complete sentences and a clear ending, 90 words or more.','Frases completas e final claro, 90 palavras ou mais.','Loose fragments, or a very short text.','Frases soltas ou texto muito curto.')]
WORDS=[('ferry','U3'),('commute','U3'),('aisle','U3'),('headphones','U3'),('freeze','U3'),
       ('adventure','U4'),('earthquake','U4'),('dangerous','U4'),('architecture','U4'),('mountaineer','U4')]
SENT=['Riding a bike is cheaper than taking a taxi.',
      'The subway isn’t as crowded as the bus in the morning.',
      'We didn’t bring enough water on our trip.',
      'I was walking home when it started to rain.']
QUEST=[('What’s the fastest way to get to school?','By car. / The fastest way is by bus.','U3 · superlatives'),
       ('Which is more comfortable, the bus or the car?','The car is more comfortable.','U3 · comparatives'),
       ('What did you do last weekend?','I went to the beach.','U4 · past simple'),
       ('What were you doing at eight o’clock last night?','I was watching TV.','U4 · past continuous')]
DICT_ERROS="<i>s</i> mudo em <i>aisle</i>, <i>ph</i> em <i>headphones</i>, <i>ea</i> e <i>qu</i> em <i>earthquake</i>, <i>ch</i> com som de k em <i>architecture</i>, <i>rr</i> em <i>ferry</i>, <i>cheaper</i> (não <i>more cheap</i>) em B1, <i>isn’t as … as</i> em B2, <i>was walking</i> em B4, resposta com past continuous em C4"
ESTRUTURAS_FUTURAS={r"\bused to\b":9, r"\b(is|are|was|were) \w+ed by\b":9, r"\b(have|has) \w+ed (for|since)\b":7, r"\bif .* will\b":8}
CONTEUDO=[
 ('Unit 3 · Transportation',[
  ('Grammar',[('comparatives and superlatives',['U3-1'],''),('as … as',['U3-2'],''),('comparative modifiers',[],'')]),
  ('Vocabulary',[('compound nouns',['U3-3'],''),('transportation adjectives',['U3-4'],''),('taking transportation',['U3-5','U3-6'],''),('word focus: understand',[],'')]),
  ('Real life',[('going on a journey',['U3-6'],'')]),
  ('Listening',[('a radio show about travel problems',['U3-7','U3-8'],'')]),
  ('Reading',[('an article about drone deliveries',['U3-9','U3-10'],'')]),
  ('Writing',[('a short report; summarizing results',[],'')]),
 ]),
 ('Unit 4 · Challenges',[
  ('Grammar',[('past simple',['U4-1'],''),('past continuous and past simple',['U4-2'],'')]),
  ('Vocabulary',[('personal qualities',['U4-3'],''),('verbs and nouns',['U4-4'],'')]),
  ('Real life',[('telling a story',['U4-5'],'')]),
  ('Listening',[('a rock climbing lesson',['U4-6','U4-7'],'')]),
  ('Reading',[('an article about Sudoku',['U4-9'],'')]),
  ('Writing',[('a short story; structuring your writing',['U4-11'],'')]),
 ]),
]
import sys, re as _re
_VER=sys.argv[2] if len(sys.argv)>2 and sys.argv[2] in ('complete','speed') else 'complete'
_NUM={}
for _l in open(f'{DIR}/map_{_VER}.txt'):
    _m=_re.match(r'ex\s+(\d+) = (U\d+) ex (\d+)',_l)
    if _m: _NUM[f'{_m.group(2)}-{_m.group(3)}']=int(_m.group(1))
RUB.sort(key=lambda sec: min([_NUM[o] for r in sec[2] for o in r[0] if o in _NUM] or [999]))
