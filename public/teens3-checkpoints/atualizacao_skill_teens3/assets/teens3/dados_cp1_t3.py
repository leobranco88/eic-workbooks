# Dados do Checkpoint 1 (Teens 3, Life 3, Units 1-2) para build_cp.py
def P(en,pt): return f'{en}<span class="pt">{pt}</span>'
CP=1; UNITS=(1,2); DIR='/home/claude/t3/cp1'; TURMA='Teens 3'
COR='#9B4DBA'; COR_TEXTO='#FFFFFF'; COR_SOBRE_PRETO='#FFFFFF'
COR_FUNDO='#E8E4EC'; COR_LINHA='#D4CDDC'
SELO='/home/claude/t3/selo_cp1.png'; PACK='/mnt/user-data/uploads/Teens3_CP1_dictation_audios.json'
ICONES='/home/claude/t3/fig'
SCRIPTS='/home/claude/t3/scripts/scripts-listening-teens3.json'
AUD='/home/claude/t3/src/life3e_ame_L3_asmt_'
TRACKS=[('Track 1.1',AUD+'u01_listen1_sleep.mp3',['U1-8','U1-9']),
        ('Track 2.1',AUD+'u02_listen2_plogging.mp3',['U2-7','U2-8'])]
PTS={'complete':{'Grammar':20,'Vocabulary':30,'Real Life':10,'Listening':20,'Reading':10,'Writing':10},
     'speed':{'Grammar':20,'Vocabulary':20,'Real Life':10,'Listening':10,'Reading':10}}
W='U2-12'
GRAFIA=['U1-2','U2-2','U2-5']
WINTRO=("<b>Ex. {WN}.</b> Ad for a photography competition, 100 to 120 words, written from the assistant’s notes after correcting their mistakes. Five criteria, each scored 0 to 2. Each criterion measures one thing only. Content from Units 1 and 2.",
        "<b>Ex. {WN}.</b> Anúncio de um concurso de fotografia, de 100 a 120 palavras, a partir das anotações do assistente, corrigindo os erros delas. Cinco critérios de 0 a 2, cada um mede uma coisa só.")
ANS={'U1-2':['often watch','sometimes get','don’t usually have','go running three times a week','Do you always stay up'],
 'U1-3':['a','b','a','b','a'],
 'U2-1':['can’t','can’t','doesn’t have to','can','have to'],
 'U2-2':['A Learning','B being','C Watching','D skiing','E Taking'],
 'U1-4':['A stay up','B do exercise','C fall asleep','D feel tired','E get up'],
 'U1-5':['a','b','a','b','a'],
 'U1-6':['A fever','B headache','C stomachache','D backache','E bad cough'],
 'U2-3':['b','a','e','c','d'],'U2-4':['like','would like','look like','like','would like'],
 'U2-5':['surfer','driver','boxer','swimmer','player'],
 'U1-7':['hot water with honey and lemon','fever','You should','see me again','Why don’t you'],
 'U2-6':['a','a','b','a','b'],
 'U1-8':['b','d','e','c','a'],'U1-9':['A c','B b','C a','D b','E a'],
 'U2-7':['A marked','B blank','C marked','D blank','E marked'],
 'U2-8':['A trash bag <i>(or bag)</i>','B flags','C car','D hill','E kilograms <i>(or kilos, kg)</i>'],
 'U1-10':['True','False','True','False','False'],'U1-11':['b','c','b','a','b']}
LONGO={'U1-2','U1-7','U2-8','U1-4','U1-6','U2-2'}
SECAO={'Grammar':['U1-2','U1-3','U2-1','U2-2'],'Vocabulary':['U1-4','U1-5','U1-6','U2-3','U2-4','U2-5'],
       'Real Life':['U1-7','U2-6'],'Listening':['U1-8','U1-9','U2-7','U2-8'],'Reading':['U1-10','U1-11']}
RUB=[('Grammar','Gramática',[
 (['U1-2'],P('The words in the right order, with the verb in the right form.','As palavras na ordem certa, com o verbo na forma certa.'),P('Full forms (<i>do not usually have</i>) score. The adverb in the wrong place scores zero: the order is what the item measures.','Forma cheia vale. Advérbio fora do lugar não pontua: a ordem é o que o item mede.')),
 (['U1-3'],P('The right option.','A opção certa.'),P('Two options marked score zero.','Duas opções marcadas não pontuam.')),
 (['U2-1'],P('The right option from the box.','A opção certa do quadro.'),P('Full forms (<i>cannot</i>, <i>does not have to</i>) score.','Forma cheia vale.')),
 (['U2-2'],P('The -ing form of the verb from the box.','A forma -ing do verbo do quadro.'),P('Spelling counts (<i>skiing</i>, <i>taking</i>). A small letter at the start still scores.','A grafia conta. Minúscula no início vale.'))]),
 ('Vocabulary','Vocabulário',[
 (['U1-4'],P('The phrase from the box.','A expressão do quadro.'),P('The verb in any correct form (<i>fall asleep</i> / <i>falls asleep</i>).','O verbo em qualquer forma certa.')),
 (['U1-5'],P('The right verb: <i>do</i>, <i>play</i> or <i>go</i>.','O verbo certo: <i>do</i>, <i>play</i> ou <i>go</i>.'),P('No alternatives.','Nenhuma alternativa.')),
 (['U1-6'],P('The medical problem from the box.','O problema de saúde do quadro.'),P('Copied from the box, so spelling must match.','Copiada do quadro: grafia igual.')),
 (['U2-3'],P('The right letter.','A letra certa.'),P('Matching.','Associação.')),
 (['U2-4'],P('<i>like</i>, <i>look like</i> or <i>would like</i>, as the sentence needs.','<i>like</i>, <i>look like</i> ou <i>would like</i>, como a frase pede.'),P('Item 2: <i>’d like</i> scores.','Item 2: <i>’d like</i> vale.')),
 (['U2-5'],P('The person word with the right suffix.','A palavra da pessoa com o sufixo certo.'),P('Spelling counts: double letters in <i>swimmer</i>, no <i>e</i> twice in <i>driver</i>.','A grafia conta.'))]),
 ('Real Life','Situações reais',[
 (['U1-7'],P('The phrase from the box.','A expressão do quadro.'),P('Capital letter doesn’t matter.','Maiúscula não desconta.')),
 (['U2-6'],P('The right response.','A resposta certa.'),P('Items 1, 3 and 4 were rewritten from the book; the letters are the same.','Os itens 1, 3 e 4 foram reescritos; as letras não mudaram.'))]),
 ('Listening','Compreensão auditiva',[
 (['U1-8'],P('The right letter.','A letra certa.'),P('Track 1.1, played twice.','Faixa 1.1, tocada duas vezes.')),
 (['U1-9'],P('The right option.','A opção certa.'),P('Track 1.1.','Faixa 1.1.')),
 (['U2-7'],P('One point per person, A to E: marked if they want to take part (A, C, E), left blank if not (B, D).','Um ponto por pessoa: marcada se quer participar (A, C, E), em branco se não (B, D).'),P('Track 2.1, played twice. Five points in total.','Faixa 2.1, tocada duas vezes. Cinco pontos no total.')),
 (['U2-8'],P('The missing word.','A palavra que falta.'),P('Small spelling slips that keep the word clear score (<i>flaggs</i>).','Erro pequeno de grafia que mantém a palavra clara vale.'))]),
 ('Reading','Leitura',[
 (['U1-10'],P('True or False.','Verdadeiro ou falso.'),P('<i>T</i> or <i>F</i>.','<i>T</i> ou <i>F</i>.')),
 (['U1-11'],P('The right option.','A opção certa.'),P('Two options marked score zero.','Duas opções marcadas não pontuam.'))]),
]
WCRIT=[('Task','Tarefa','All the information from the notes: the competition, when and where, the prizes and how to contact Amanda.','Todas as informações das anotações: o concurso, quando e onde, os prêmios e o contato da Amanda.','Three or four of the five.','Três ou quatro das cinco.'),
 ('Unit vocabulary','Vocabulário da unidade','Three or more words or phrases from the units (<i>competition</i>, <i>interested in</i>, <i>would like</i>, <i>winner</i>, <i>photographer</i>).','Três ou mais palavras ou expressões das unidades.','One or two.','Uma ou duas.'),
 ('Unit grammar','Gramática da unidade','Two or more correct sentences with <i>can</i> / <i>have to</i> / <i>don’t have to</i> or the -ing form (<i>Taking photos is fun.</i>).','Duas ou mais frases certas com <i>can</i> / <i>have to</i> / <i>don’t have to</i> ou a forma -ing.','One.','Uma.'),
 ('Subskill: checking your writing','Subskill: revisar o texto','The five mistakes in the notes are corrected (<i>photography</i>, <i>Enter…!</i>, <i>at the Civic Center at 3 p.m.</i>, <i>We offer</i>, <i>Amanda</i>).','Os cinco erros das anotações corrigidos.','Three or four.','Três ou quatro.'),
 ('Organization and length','Organização e tamanho','Organized like an ad (a catchy opening, the details, how to contact), 90 words or more.','Organizado como anúncio (abertura chamativa, detalhes, contato), 90 palavras ou mais.','Loose fragments, or a very short text.','Frases soltas ou texto muito curto.')]
WORDS=[('lifestyle','U1'),('stressed','U1'),('gardening','U1'),('pharmacy','U1'),('earache','U1'),
       ('athlete','U2'),('championship','U2'),('goalkeeper','U2'),('referee','U2'),('crowd','U2')]
SENT=['I usually get up early on school days.',
      'She’s playing tennis at the moment.',
      'You don’t have to wear a helmet in this game.',
      'Swimming is good for your health.']
QUEST=[('How often do you play video games?','Once a week. / I never play video games.','U1 · adverbs and expressions of frequency'),
       ('What are you doing right now?','I’m doing a test.','U1 · present continuous'),
       ('Do you have to do homework on weekends?','Yes, I do. / No, I don’t.','U2 · verbs for rules'),
       ('Which sport do you like playing?','I like playing soccer.','U2 · like + -ing')]
DICT_ERROS="<i>ph</i> em <i>pharmacy</i>, <i>ea</i> e <i>ch</i> em <i>earache</i>, <i>th</i> e três sílabas em <i>athlete</i> (não <i>atlete</i>), <i>ss</i> em <i>stressed</i>, <i>mm</i> em <i>swimming</i>, advérbio antes do verbo em B1, <i>like playing</i> (não <i>like play</i>) em C4"
ESTRUTURAS_FUTURAS={r"\b(was|were|wasn't|weren't) \w+ing\b":4, r"\bused to\b":9,
    r"\b(is|are|was|were) \w+ed by\b":9, r"\b(have|has) \w+ed (for|since)\b":7, r"\bif .* will\b":8}
CONTEUDO=[
 ('Unit 1 · Lifestyle',[
  ('Grammar',[('present simple and adverbs of frequency',['U1-2'],''),('present simple and present continuous',['U1-3'],'')]),
  ('Vocabulary',[('everyday routines',['U1-4'],''),('collocations with do, play and go',['U1-5'],''),('word focus: feel',['U1-4'],', item D'),('medical problems',['U1-6','U1-7'],'')]),
  ('Real life',[('talking about illness',['U1-7'],'')]),
  ('Listening',[('five conversations about sleep',['U1-8','U1-9'],'')]),
  ('Reading',[('an article about how nature is good for you',['U1-10','U1-11'],'')]),
  ('Writing',[('a form; filling out forms',[],'')]),
 ]),
 ('Unit 2 · Competitions',[
  ('Grammar',[('verbs for rules',['U2-1'],''),('-ing form',['U2-2'],'')]),
  ('Vocabulary',[('sports',['U2-3'],''),('suffixes',['U2-5'],''),('word focus: like',['U2-4','U2-6'],'')]),
  ('Real life',[('talking about interests',['U2-6'],'')]),
  ('Listening',[('a talk about plogging',['U2-7','U2-8'],'')]),
  ('Reading',[('an article about two unusual sports',[],'')]),
  ('Writing',[('an ad or notice; checking your writing',['U2-12'],'')]),
 ]),
]

# Rubrica e seções na ordem da prova de cada versão (as ordens de seção da Complete e da Speed diferem)
import sys, re as _re
_VER=sys.argv[2] if len(sys.argv)>2 and sys.argv[2] in ('complete','speed') else 'complete'
_NUM={}
for _l in open(f'{DIR}/map_{_VER}.txt'):
    _m=_re.match(r'ex\s+(\d+) = (U\d+) ex (\d+)',_l)
    if _m: _NUM[f'{_m.group(2)}-{_m.group(3)}']=int(_m.group(1))
RUB.sort(key=lambda sec: min([_NUM[o] for r in sec[2] for o in r[0] if o in _NUM] or [999]))
