#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""EIC - Speaking dos checkpoints do Kids 6.

Mesma mecanica nos quatro: o texto e identico nos dois cartoes e as lacunas sao
cruzadas, entao nenhum aluno resolve sozinho. As notas de cada um trazem
distratores, para que despejar tudo em voz alta nao entregue a resposta: so a
pergunta certa extrai a linha certa. E a ultima pergunta nao esta em cartao
nenhum, exige juntar as duas metades.

Uma decisao de desenho que vale registrar: deducao (must / can't be) e
condicional nao sao informacao que o colega tem, sao conclusao. Nesses casos o
parceiro carrega a PISTA e quem tem a lacuna produz a conclusao. Isso mantem a
producao com quem esta sendo medido, em vez de virar transmissao.

Uso: python3 build_speaking.py cp2
"""
import sys
from weasyprint import HTML

W = "/home/claude/work"

CONFIGS = {}

CONFIGS["cp1"] = dict(
    cp="Checkpoint 1", units="Units 1 &amp; 2", title="Two stories",
    kind="Boarding pass",
    # A guarda a historia da banda (Unit 1) e precisa da historia do show
    # (Unit 2). Assim cada aluno PERGUNTA na estrutura de uma unidade e
    # RESPONDE na estrutura da outra.
    own_a=[("t", "The Northern Lights have been on tour since 2019. They played in Dublin in 2023 "
                 "and they travelled there by train. They have never played in Oslo. "
                 "Their first album came out in 2018.")],
    gap_a=[
        ("t", "Our school show used to be "), ("g", "1"), ("c", "where?"),
        ("t", ". The costumes used to be made by "), ("g", "2"), ("c", "who?"),
        ("t", ". We used to rehearse on Saturdays, but now we rehearse after school. "
              "The show moved to the theater in "), ("g", "3"), ("c", "when?"), ("t", "."),
    ],
    own_b=[("t", "Our school show used to be in the gym. The costumes used to be made by the "
                 "students&rsquo; families. We used to rehearse on Saturdays, but now we rehearse "
                 "after school. The show moved to the theater in 2021.")],
    gap_b=[
        ("t", "The Northern Lights have been on tour since "), ("g", "1"), ("c", "when?"),
        ("t", ". They played in Dublin in 2023 and they travelled there "), ("g", "2"), ("c", "how?"),
        ("t", ". They have never played in "), ("g", "3"), ("c", "where?"),
        ("t", ". Their first album came out in 2018."),
    ],
    last="four things happened in different years: the first album, the start of the tour, the Dublin concert and the move to the theater. Put them in order, from the oldest to the most recent. Two of the years are gaps on your card.",
    ans_a=['in the gym', 'the students&rsquo; families', '2021'],
    ans_b=['2019', 'by train', 'Oslo'],
    ans_last="The first album came out in 2018, the tour started in 2019, the show moved to the theater in 2021, and they played in Dublin in 2023.",
    crits=[
        ("Pergunta, não só responde",
         "Faz ao menos duas perguntas ao colega. Quem só responde não fecha este ponto."),
        ("Present perfect com ever, never, for ou since",
         "Ao menos uma vez. <em>Since when have they been on tour? &middot; They have never played in Oslo.</em>"),
        ("Simple past com data fechada",
         "Ao menos uma vez. <em>They played in Dublin in 2023. &middot; When did the show move?</em>"),
        ("used to",
         "Ao menos uma vez. <em>Where did the show use to be? &middot; The costumes used to be made by the families.</em>"),
    ],
    last_crit="As três lacunas preenchidas e a ordem dita em voz alta: 2018 o álbum, 2019 a turnê, 2021 o teatro, 2023 o show em Dublin. Nenhum dos dois cartões tem as quatro datas.",
    cols=["pergunta", "present perfect", "past", "used to", "fecha"],
)

CONFIGS["cp2"] = dict(
    cp="Checkpoint 2", units="Units 3 &amp; 4", title="Two stories",
    kind="Call sheet",
    # A guarda a historia do filme (Unit 4, passiva) e precisa da historia do
    # cheiro (Unit 3, deducao e futuro).
    own_a=[("t", "The Late Bus was filmed in our school last year. One scene was filmed in the "
                 "science room, which hasn&rsquo;t been painted since 2019. The music was recorded "
                 "by Ana in her garage. The costumes were made at home by Dona Rita.")],
    gap_a=[
        ("t", "There is a strange smell in the science room. It can&rsquo;t be the food, because "),
        ("g", "1"), ("c", "why not?"),
        ("t", ". Ana said the smell "), ("g", "2"), ("c", "when?"),
        ("t", ". The teacher thinks it might be "), ("g", "3"), ("c", "what?"),
        ("t", ". Tomorrow we&rsquo;re opening the windows."),
    ],
    own_b=[("t", "There is a strange smell in the science room. It can&rsquo;t be the food, because "
                 "nobody eats there. Ana said the smell started last week. The teacher thinks it "
                 "might be the new paint. Tomorrow we&rsquo;re opening the windows.")],
    gap_b=[
        ("t", "The Late Bus was filmed in "), ("g", "1"), ("c", "where?"),
        ("t", " last year. One scene was filmed in the science room, which hasn&rsquo;t been "
              "painted since "), ("g", "2"), ("c", "when?"),
        ("t", ". The music was recorded by "), ("g", "3"), ("c", "who?"),
        ("t", " in her garage. The costumes were made at home by Dona Rita."),
    ],
    last="what does the teacher think the smell is, and can that be true? Read your two stories again and decide together, in English.",
    ans_a=['nobody eats there', 'started last week', 'the new paint'],
    ans_b=['our school', '2019', 'Ana'],
    ans_last="It can&rsquo;t be the paint. The science room hasn&rsquo;t been painted since 2019, and the smell started last week.",
    crits=[
        ("Pergunta, não só responde",
         "Faz ao menos duas perguntas ao colega. Quem só responde não fecha este ponto."),
        ("Voz passiva do passado",
         "Ao menos uma vez. <em>Where was the film filmed? &middot; The music was recorded by Ana.</em>"),
        ("Dedução com must, might ou can&rsquo;t",
         "Ao menos uma vez. <em>What might it be? &middot; It can&rsquo;t be the food.</em>"),
        ("Futuro com present continuous",
         "Ao menos uma vez. <em>Tomorrow we&rsquo;re opening the windows.</em>"),
    ],
    last_crit="As três lacunas preenchidas e a contradição resolvida em voz alta: a sala não é pintada desde 2019 e o cheiro começou semana passada, então <em>it can&rsquo;t be the paint</em>. A conclusão não está em nenhum dos dois textos.",
    cols=["pergunta", "passiva", "dedução", "futuro", "fecha"],
)

CONFIGS["cp3"] = dict(
    cp="Checkpoint 3", units="Units 5 &amp; 6", title="Two stories",
    kind="Club card",
    # A guarda o dia do acidente (Unit 6, discurso indireto) e precisa da
    # conversa sobre o novo capitao (Unit 5, condicional).
    own_a=[("t", "Yesterday Pedro fell in the gym. He said that he couldn&rsquo;t stand up. The nurse "
                 "told us that his ankle wasn&rsquo;t broken. Ana said that she had a fever, so she "
                 "went home early.")],
    gap_a=[
        ("t", "Our club needs a new captain. The new captain has to "), ("g", "1"), ("c", "do what?"),
        ("t", " on Saturday. If we had more players, we would win on Saturday. "),
        ("t", "If I were the captain, I would "), ("g", "2"), ("c", "ask for what?"),
        ("t", ". "), ("g", "3"), ("c", "who?"),
        ("t", " says she would volunteer, but she needs more time."),
    ],
    own_b=[("t", "Our club needs a new captain. The new captain has to play on Saturday. If we had "
                 "more players, we would win on Saturday. If I were the captain, I would ask for new "
                 "uniforms. Lia says she would volunteer, but she needs more time.")],
    gap_b=[
        ("t", "Yesterday Pedro fell in the gym. He said that "), ("g", "1"), ("c", "what did he say?"),
        ("t", ". The nurse told us that "), ("g", "2"), ("c", "what did she say?"),
        ("t", ". "), ("g", "3"), ("c", "who?"),
        ("t", " said that she had a fever, so she went home early."),
    ],
    last="can Pedro be the new captain this Saturday? Say yes or no, and say why, in English.",
    ans_a=['play on Saturday', 'ask for new uniforms', 'Lia'],
    ans_b=['he couldn&rsquo;t stand up', 'his ankle wasn&rsquo;t broken', 'Ana'],
    ans_last="No, he can&rsquo;t. The new captain has to play on Saturday, and Pedro said that he couldn&rsquo;t stand up.",
    crits=[
        ("Pergunta, não só responde",
         "Faz ao menos duas perguntas ao colega. Quem só responde não fecha este ponto."),
        ("Discurso indireto com said ou told",
         "Ao menos uma vez, recuando o tempo verbal. <em>What did Pedro say? &middot; He said that he couldn&rsquo;t stand up.</em>"),
        ("Segunda condicional",
         "Ao menos uma vez. <em>If I were the captain, I would ask for new uniforms.</em>"),
        ("Vocabulário das unidades",
         "Ao menos duas palavras de saúde ou de liderança. <em>ankle, fever, nurse, captain, volunteer.</em>"),
    ],
    last_crit="As três lacunas preenchidas e a conclusão dita em voz alta: o capitão tem que jogar sábado e o Pedro disse que não conseguia ficar de pé, então não. A resposta não está escrita em nenhum dos dois textos.",
    cols=["pergunta", "indireto", "condicional", "vocabulário", "fecha"],
)

CONFIGS["cp4"] = dict(
    cp="Checkpoint 4", units="Units 7 &amp; 8", title="Two stories",
    kind="Field log",
    # A guarda o diario do clube (Unit 8, present perfect progressive) e precisa
    # do relatorio (Unit 7, past perfect).
    own_a=[("t", "Our club has been watching the birds since March. The worms have been decomposing "
                 "the leaves for two months. We haven&rsquo;t been using plastic bottles this year. "
                 "The rain started in April.")],
    gap_a=[
        ("t", "Lia had already "), ("g", "1"), ("c", "done what first?"),
        ("t", " before she wrote the report. When the rain started, we hadn&rsquo;t finished "),
        ("g", "2"), ("c", "what?"),
        ("t", " yet. The plants had run out of water when we came back. "), ("g", "3"), ("c", "who?"),
        ("t", " had never used a microscope before this year."),
    ],
    own_b=[("t", "Lia had already researched vultures before she wrote the report. When the rain "
                 "started, we hadn&rsquo;t finished the experiment yet. The plants had run out of water "
                 "when we came back. Marcos had never used a microscope before this year.")],
    gap_b=[
        ("t", "Our club has been watching the birds since "), ("g", "1"), ("c", "when?"),
        ("t", ". The worms have been decomposing the leaves for "), ("g", "2"), ("c", "how long?"),
        ("t", ". We haven&rsquo;t been using plastic bottles this year. The rain started in "),
        ("g", "3"), ("c", "when?"), ("t", "."),
    ],
    last="when the rain started, the club hadn&rsquo;t finished one thing yet. What was it, and in which month did the rain start? Neither of you has both answers.",
    ans_a=['researched vultures', 'the experiment', 'Marcos'],
    ans_b=['March', 'two months', 'April'],
    ans_last="They hadn&rsquo;t finished the experiment, and the rain started in April.",
    crits=[
        ("Pergunta, não só responde",
         "Faz ao menos duas perguntas ao colega. Quem só responde não fecha este ponto."),
        ("Present perfect progressive",
         "Ao menos uma vez, com <em>for</em> ou <em>since</em>. <em>How long have the worms been decomposing the leaves?</em>"),
        ("Past perfect",
         "Ao menos uma vez. <em>Lia had already researched vultures. &middot; We hadn&rsquo;t finished the experiment.</em>"),
        ("Vocabulário das unidades",
         "Ao menos duas palavras de natureza ou de invenção. <em>decompose, experiment, report, microscope.</em>"),
    ],
    last_crit="As três lacunas preenchidas e as duas respostas ditas em voz alta: o experimento não estava terminado, e a chuva começou em abril. Uma resposta está em cada cartão, e nenhum dos dois tem as duas.",
    cols=["pergunta", "PPP", "past perfect", "vocabulário", "fecha"],
)


def checar_ultima_pergunta(cfg, key):
    """A ultima pergunta tem que depender de pelo menos uma lacuna de CADA cartao.

    O erro que este teste pega: tratar o texto com lacunas como se fosse so
    lacuna. Ele entrega tudo o que nao esta apagado, e um fato visivel ali
    conta como informacao que o aluno ja tem. Sem isso, tres das quatro
    tarefas eram resolviveis por um aluno sozinho.
    """
    import re
    limpa = lambda s: re.sub(r"&[a-z]+;", "'", s).lower()
    modelo = limpa(cfg["ans_last"])
    dep_a = [a for a in cfg["ans_a"] if limpa(a) in modelo]
    dep_b = [b for b in cfg["ans_b"] if limpa(b) in modelo]
    assert dep_a, "%s: a ultima pergunta nao depende de nenhuma lacuna do Student A" % key
    assert dep_b, "%s: a ultima pergunta nao depende de nenhuma lacuna do Student B" % key
    return dep_a, dep_b


def story_html(parts):
    out = []
    for kind, v in parts:
        if kind == "t":
            out.append(v)
        elif kind == "f":
            out.append('<span class="fill">%s</span>' % v)
        elif kind == "c":
            out.append('<span class="cue">%s</span>' % v)
        else:
            out.append('<span class="gap"><b>%s</b></span>' % v)
    return "".join(out)


def card(cfg, who, mine, theirs):
    return '''  <div class="pass">
    <div class="main">
      <div class="tag"><span class="who">Student %s</span><span class="kind">%s</span></div>
      <div class="blk mine">
        <div class="bh">Your story &middot; answer from here, only what your partner asks</div>
        <p class="story">%s</p>
      </div>
      <div class="blk theirs">
        <div class="bh">Your partner&rsquo;s story &middot; ask and fill the gaps</div>
        <p class="story">%s</p>
      </div>
    </div>
    <div class="stub">
      <div class="st">Three rules</div>
      <ol>
        <li>Don&rsquo;t show your card.</li>
        <li>Don&rsquo;t read your story out loud. Answer only the question you hear.</li>
        <li>Ask again if you did not understand.</li>
      </ol>
      <p class="ask"><b>Last question, together:</b> %s</p>
    </div>
  </div>

  <div class="art-row">
    <figure>
      <img src="%s/sp_art/print_dupla.jpg" alt="">
      <figcaption><b>Hold your card facing you. Ask as many times as you need, but never show it.</b>
      <span>Segure o seu cartão virado para você. Pergunte quantas vezes precisar, mas nunca mostre a folha.</span></figcaption>
    </figure>
    <figure>
      <img src="%s/sp_art/print_ultima.jpg" alt="">
      <figcaption><b>For the last question, put the cards down and think together.</b>
      <span>Na última pergunta, os cartões vão para a mesa: aqui vocês pensam juntos.</span></figcaption>
    </figure>
  </div>
''' % (who, cfg["kind"], story_html(mine), story_html(theirs), cfg["last"], W, W)


def build(key):
    cfg = CONFIGS[key]
    dep_a, dep_b = checar_ultima_pergunta(cfg, key)
    crits = "".join(
        '<div class="crit"><div class="n">%d</div><div class="t">%s</div><div class="d">%s</div></div>\n  '
        % (i + 1, t, d) for i, (t, d) in enumerate(cfg["crits"]))
    gab = ('<div class="gab"><div class="gh">Gabarito</div>'
           '<p><b>Student A</b> preenche: %s</p>'
           '<p><b>Student B</b> preenche: %s</p>'
           '<p class="mod"><b>Última pergunta &middot; resposta modelo</b><br>%s</p>'
           '<p class="obs">Aceite qualquer resposta que chegue ao mesmo lugar. O que fecha o ponto 5 '
           'é a conclusão certa dita em inglês, não estas palavras exatas.</p></div>'
           % (" &middot; ".join("%d. %s" % (i + 1, v) for i, v in enumerate(cfg["ans_a"])),
              " &middot; ".join("%d. %s" % (i + 1, v) for i, v in enumerate(cfg["ans_b"])),
              cfg["ans_last"]))

    crits += ('<div class="crit"><div class="n">5</div><div class="t">Fecha o texto e a última pergunta</div>'
              '<div class="d">%s Se resolveram em português, ou se um leu as notas em voz alta para o outro copiar, o ponto não sai.</div></div>'
              % cfg["last_crit"])

    rows = "".join(
        '<tr><td class="n">%d</td>%s</tr>\n    ' % (i, '<td class="c"><span></span></td>' * 5)
        for i in range(1, 13))
    cols = "".join('<th class="c">%d<br>%s</th>' % (i + 1, c) for i, c in enumerate(cfg["cols"]))

    html = TEMPLATE % dict(
        cp=cfg["cp"], units=cfg["units"], title=cfg["title"],
        card_a=card(cfg, "A", cfg["own_a"], cfg["gap_a"]),
        card_b=card(cfg, "B", cfg["own_b"], cfg["gap_b"]),
        crits=crits, gab=gab, cols=cols, rows=rows, W=W)

    src = "%s/speaking_%s_src.html" % (W, key)
    out = "%s/Speaking_%s_Kids6.pdf" % (W, cfg["cp"].replace("Checkpoint ", "CP"))
    open(src, "w", encoding="utf-8").write(html)
    HTML(src).write_pdf(out)
    from pypdf import PdfReader
    n = len(PdfReader(out).pages)
    assert n == 4, "esperava 4 paginas, saiu %d" % n
    print("OK %s · %d paginas · ultima pergunta depende de %s (A) e %s (B)"
          % (out, n, "/".join(dep_a), "/".join(dep_b)))


TEMPLATE = open("%s/speaking_template.html" % W, encoding="utf-8").read() \
    if __name__ == "__main__" else ""

if __name__ == "__main__":
    build(sys.argv[1])
