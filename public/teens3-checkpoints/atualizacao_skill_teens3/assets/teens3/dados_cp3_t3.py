# Dados do Checkpoint 3 (Teens 3, Life 3, Units 5-6) para build_cp.py
def P(en,pt): return f'{en}<span class="pt">{pt}</span>'
CP=3; UNITS=(5,6); DIR='/home/claude/t3/cp3'; TURMA='Teens 3'
COR='#9B4DBA'; COR_TEXTO='#FFFFFF'; COR_SOBRE_PRETO='#FFFFFF'
COR_FUNDO='#E8E4EC'; COR_LINHA='#D4CDDC'
SELO='/home/claude/t3/selo_cp3.png'; PACK='/mnt/user-data/uploads/Teens3_CP3_dictation_audios.json'
ICONES='/home/claude/t3/fig'
SCRIPTS='/home/claude/t3/scripts/scripts-listening-teens3.json'
AUD='/home/claude/t3/src/life3e_ame_L3_asmt_'
TRACKS=[('Track 5.1',AUD+'u05_listen2_accomodation.mp3',['U5-7','U5-8']),
        ('Track 6.1',AUD+'u06_listen2_celebrations.mp3',['U6-7','U6-8'])]
PTS={'complete':{'Grammar':20,'Vocabulary':30,'Real Life':10,'Listening':20,'Reading':10,'Writing':10},
     'speed':{'Grammar':20,'Vocabulary':20,'Real Life':10,'Listening':10,'Reading':10}}
W='U6-12'
GRAFIA=['U5-4','U6-1','U6-3']
WINTRO=("<b>Ex. {WN}.</b> A description of a recent event the student attended, 100 to 120 words. Five criteria, each scored 0 to 2. Each criterion measures one thing only. Content from Units 5 and 6.",
        "<b>Ex. {WN}.</b> Descrição de um evento recente a que o aluno foi, de 100 a 120 palavras. Cinco critérios de 0 a 2, cada um mede uma coisa só.")
ANS={'U5-1':['any','much','little','few','a lot of'],
 'U5-2':['a small town … Poland','the largest river … South America','a new boat … the boat','the Great Wall of China … an ancient site','Mars … the Sun'],
 'U6-1':['plan to travel <i>(or am planning to travel)</i>','sold our car to earn','wasn’t difficult to finish <i>(or won’t be difficult to finish)</i>','would like to find','seems hard not to be'],
 'U6-2':['’ll open','’re going to see','’re meeting','Will you make','Are you going to have'],
 'U5-3':['A electronics','B metal','C paper','D glass','E plastic'],
 'U5-4':['A six million, nine hundred thousand','B six thousand, eight hundred','C two million, five hundred thousand <i>(or two and a half million)</i>','D sixteen thousand','E three hundred (and) ninety billion'],
 'U5-5':['A takes a walk','B take fourteen hours','C take a taxi','D take a break','E Take care'],
 'U6-3':['early teens','mid-twenties','late thirties','fifties','early eighties'],
 'U6-4':['d','c','a','b','e'],'U6-5':['b','a','b','a','b'],
 'U5-6':['A 5','B 1','C 3','D 4','E 2'],
 'U6-6':['do you want … that’d be great','would you like … I can’t','I’d like … I’m afraid','why don’t you … fantastic','how about … that’d be'],
 'U5-7':['A a','B b','C c','D b','E c'],'U5-8':['A marked','B marked','C blank','D marked','E blank'],
 'U6-7':['A b','B a','C c','D b','E a'],'U6-8':['A dance','B afternoon','C company','D eight <i>(or 8)</i>','E dress'],
 'U5-9':['a','c','a','c','a'],'U5-10':['False','True','Not given','False','Not given']}
LONGO={'U5-2','U6-1','U6-2','U5-3','U5-4','U5-5','U6-3','U6-6','U6-8'}
SECAO={'Grammar':['U5-1','U5-2','U6-1','U6-2'],'Vocabulary':['U5-3','U5-4','U5-5','U6-3','U6-4','U6-5'],
       'Real Life':['U5-6','U6-6'],'Listening':['U5-7','U5-8','U6-7','U6-8'],'Reading':['U5-9','U5-10']}
RUB=[('Grammar','Gramática',[
 (['U5-1'],P('The right quantifier.','O quantificador certo.'),P('Two options marked score zero.','Duas opções marcadas não pontuam.')),
 (['U5-2'],P('Both blanks with the right article (or no article).','As duas lacunas com o artigo certo (ou sem artigo).'),P('One point per item, only with both blanks right. Capital letters don’t matter.','Um ponto por item, só com as duas lacunas certas.')),
 (['U6-1'],P('The verb + infinitive (or base form), as the sentence needs.','Verbo + infinitivo (ou forma base), como a frase pede.'),P('Item 1: <i>plan to</i> or <i>am planning to</i>. Item 3: past or future. Item 5 was rewritten from the book (<i>During exam week…</i>); the answer is the same.','Item 1 e item 3 aceitam as duas formas. O item 5 foi reescrito; a resposta é a mesma.')),
 (['U6-2'],P('The right future form.','A forma de futuro certa.'),P('Full forms (<i>I will open</i>) score.','Forma cheia vale.'))]),
 ('Vocabulary','Vocabulário',[
 (['U5-3'],P('The material from the box.','O material do quadro.'),P('Copied from the box, so spelling must match.','Copiada do quadro: grafia igual.')),
 (['U5-4'],P('The number written out in words.','O número escrito por extenso.'),P('Spelling counts. With or without <i>and</i> and commas. Item C: <i>two and a half million</i> scores.','A grafia conta. Com ou sem <i>and</i> e vírgulas.')),
 (['U5-5'],P('<i>take</i> in the right form + the phrase from the box.','<i>take</i> na forma certa + a expressão do quadro.'),P('Item A: <i>took a walk</i> scores if the rest is right.','Item A: <i>took a walk</i> vale.')),
 (['U6-3'],P('The age phrase from the box.','A expressão de idade do quadro.'),P('Copied from the box, so spelling must match.','Copiada do quadro: grafia igual.')),
 (['U6-4'],P('The right letter.','A letra certa.'),P('Matching.','Associação.')),
 (['U6-5'],P('The right synonym.','O sinônimo certo.'),P('Two options marked score zero.','Duas opções marcadas não pontuam.'))]),
 ('Real Life','Situações reais',[
 (['U5-6'],P('The number of the right sentence.','O número da frase certa.'),P('The book’s key has a mistake: C is 3, not 4.','O gabarito do livro erra: C é 3, não 4.')),
 (['U6-6'],P('Both words in the right blanks.','As duas expressões nas lacunas certas.'),P('One point per dialog, only with both right.','Um ponto por diálogo, só com as duas certas.'))]),
 ('Listening','Compreensão auditiva',[
 (['U5-7'],P('The right option.','A opção certa.'),P('Track 5.1, played twice. The audio says <i>cooker</i> and <i>booking</i> (British), so the questions keep them.','Faixa 5.1, tocada duas vezes. O áudio usa <i>cooker</i> e <i>booking</i>, e as perguntas mantêm.')),
 (['U5-8'],P('One point per statement, A to E: marked if true (A, B, D), left blank if not (C, E).','Um ponto por afirmação: marcada se verdadeira (A, B, D), em branco se não (C, E).'),P('Five points in total.','Cinco pontos no total.')),
 (['U6-7'],P('The right option.','A opção certa.'),P('Track 6.1, played twice.','Faixa 6.1, tocada duas vezes.')),
 (['U6-8'],P('One word.','Uma palavra.'),P('Item D: <i>eight</i> or <i>8</i>. Small spelling slips that keep the word clear score.','Item D: <i>eight</i> ou <i>8</i>. Erro pequeno de grafia que mantém a palavra clara vale.'))]),
 ('Reading','Leitura',[
 (['U5-9'],P('The right option.','A opção certa.'),P('Two options marked score zero.','Duas opções marcadas não pontuam.')),
 (['U5-10'],P('True, False or Not given.','Verdadeiro, falso ou não informado.'),P('<i>T</i>, <i>F</i> or <i>NG</i>.','<i>T</i>, <i>F</i> ou <i>NG</i>.'))]),
]
WCRIT=[('Task','Tarefa','All four parts: what the event was and who was there, the details in order, how they felt, and an ending.','As quatro partes: o evento e quem estava, os detalhes em ordem, como se sentiu e um final.','Two or three.','Duas ou três.'),
 ('Unit vocabulary','Vocabulário da unidade','Three or more words from Units 5 and 6 (<i>fireworks</i>, <i>costume</i>, <i>decorations</i>, <i>in their teens</i>, <i>take a break</i>).','Três ou mais palavras das Units 5 e 6.','One or two.','Uma ou duas.'),
 ('Unit grammar','Gramática da unidade','Two or more correct verb + infinitive patterns (<i>decided to</i>, <i>wanted to</i>, <i>it was easy to</i>) and past forms used correctly.','Dois ou mais padrões certos de verbo + infinitivo e passado correto.','One.','Um.'),
 ('Subskill: descriptive adjectives','Subskill: adjetivos descritivos','Three or more varied adjectives instead of <i>good</i>, <i>nice</i>, <i>big</i> (<i>wonderful</i>, <i>huge</i>, <i>delicious</i>).','Três ou mais adjetivos variados no lugar de <i>good</i>, <i>nice</i>, <i>big</i>.','One or two.','Um ou dois.'),
 ('Organization and length','Organização e tamanho','Events in a clear order with an ending, 90 words or more.','Eventos em ordem clara com um final, 90 palavras ou mais.','Loose fragments, or a very short text.','Frases soltas ou texto muito curto.')]
WORDS=[('scissors','U5'),('pollution','U5'),('garbage','U5'),('receive','U5'),('weight','U5'),
       ('teenager','U6'),('ceremony','U6'),('festival','U6'),('invitation','U6'),('community','U6')]
SENT=['We don’t have many recycling bins at school.',
      'The moon is smaller than the Earth.',
      'I’m planning to travel to the beach next summer.',
      'We’re meeting our friends at six o’clock tomorrow.']
QUEST=[('How much water do you drink every day?','I drink a lot of water. / Not much.','U5 · quantifiers'),
       ('What’s the largest city in Brazil?','It’s São Paulo.','U5 · articles (the + superlative)'),
       ('What are you going to do this weekend?','I’m going to visit my friends.','U6 · future forms'),
       ('What would you like to do after high school?','I’d like to travel.','U6 · verb + infinitive')]
DICT_ERROS="<i>sc</i> e <i>ss</i> em <i>scissors</i>, <i>ei</i> depois de <i>c</i> em <i>receive</i>, <i>eigh</i> em <i>weight</i>, <i>c</i> com som de s em <i>ceremony</i>, <i>mm</i> em <i>community</i>, <i>many</i> (não <i>much</i>) em B1, <i>the</i> em B2, <i>planning to</i> em B3, <i>I’d like to</i> (não <i>like travel</i>) em C4"
ESTRUTURAS_FUTURAS={r"\bused to\b":9, r"\b(is|are|was|were) \w+ed by\b":9, r"\b(have|has) \w+ed (for|since)\b":7, r"\bif .* will\b":8}
CONTEUDO=[
 ('Unit 5 · The environment',[
  ('Grammar',[('quantifiers',['U5-1'],''),('articles',['U5-2'],'')]),
  ('Vocabulary',[('recycling',['U5-3','U5-9','U5-10'],''),('large numbers',['U5-4'],''),('word focus: take',['U5-5'],'')]),
  ('Real life',[('communicating about an order',['U5-6'],'')]),
  ('Listening',[('a call to a campsite',['U5-7','U5-8'],'')]),
  ('Reading',[('an article about a school recycling project',['U5-9','U5-10'],'')]),
  ('Writing',[('formal emails; using formal language',[],'')]),
 ]),
 ('Unit 6 · Stages in life',[
  ('Grammar',[('verb + infinitive',['U6-1'],''),('future forms',['U6-2'],'')]),
  ('Vocabulary',[('describing age',['U6-3'],''),('celebrations',['U6-4','U6-7','U6-8'],''),('synonyms',['U6-5'],''),('word focus: get',[],'')]),
  ('Real life',[('inviting, accepting and declining',['U6-6'],'')]),
  ('Listening',[('five conversations about celebrations',['U6-7','U6-8'],'')]),
  ('Reading',[('an email about getting married',[],'')]),
  ('Writing',[('a description; descriptive adjectives',['U6-12'],'')]),
 ]),
]
import sys, re as _re
_VER=sys.argv[2] if len(sys.argv)>2 and sys.argv[2] in ('complete','speed') else 'complete'
_NUM={}
for _l in open(f'{DIR}/map_{_VER}.txt'):
    _m=_re.match(r'ex\s+(\d+) = (U\d+) ex (\d+)',_l)
    if _m: _NUM[f'{_m.group(2)}-{_m.group(3)}']=int(_m.group(1))
RUB.sort(key=lambda sec: min([_NUM[o] for r in sec[2] for o in r[0] if o in _NUM] or [999]))
