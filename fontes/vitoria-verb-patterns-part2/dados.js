/* Conteúdo da página. A página da aluna e a tela do professor leem o mesmo arquivo. */
var WORDS = [
  { w: 'enrollment fee', ipa: '/ɪnˈroʊl.mənt fiː/', cls: 'subst.', pt: 'taxa de matrícula; taxa de inscrição', ex: 'The enrollment fee for the English course is paid once a year.', expt: 'A taxa de matrícula do curso de inglês é paga uma vez por ano.' },
  { w: 'lower prices', ipa: '/ˈloʊ.ər ˈpraɪ.sɪz/', cls: 'expr.', pt: 'preços mais baixos; reduzir preços', ex: 'The store has lower prices than the mall on weekends.', expt: 'A loja tem preços mais baixos que o shopping nos fins de semana.' },
  { w: 'be worth (it)', ipa: '/bi wɜːrθ (ɪt)/', cls: 'expr.', pt: 'valer a pena', ex: 'The movie was long, but it was worth it.', expt: 'O filme era longo, mas valeu a pena.' },
  { w: 'crowded', ipa: '/ˈkraʊ.dɪd/', cls: 'adj.', pt: 'lotado; cheio de gente; cheio (de pessoas ou coisas)', ex: 'The subway is always crowded during rush hour.', expt: 'O metrô fica sempre lotado no horário de pico.' },
  { w: 'exchange rate', ipa: '/ɪksˈtʃeɪndʒ reɪt/', cls: 'subst.', pt: 'taxa de câmbio; câmbio', ex: 'The exchange rate for the dollar went up today.', expt: 'A taxa de câmbio do dólar subiu hoje.' },
  { w: 'fee', ipa: '/fiː/', cls: 'subst.', pt: 'taxa; tarifa; mensalidade', ex: 'There is a small fee for using the ATM.', expt: 'Há uma pequena taxa para usar o caixa eletrônico.' },
  { w: 'Go up', ipa: '/ɡoʊ ʌp/', cls: 'phrasal verb', pt: 'subir; aumentar', ex: 'The price of coffee went up again this month.', expt: 'O preço do café subiu de novo este mês.' }
];

/* Exercício 1: escrever a lacuna. fam = família do verbo (1 = com to, 2 = sem to). */
var EX1 = {
  example: { pre: 'The shop owner had the clerk', post: 'the window.', answer: 'clean', pt: 'O dono da loja pediu para o funcionário limpar a vitrine.', fam: 2 },
  items: [
    { pre: 'The trade fair requires exhibitors', post: 'the enrollment fee by March.', accept: ['to pay'], pt: 'A feira exige que os expositores paguem a taxa de inscrição até março.', fam: 1 },
    { pre: 'My manager made me', post: 'the quote, but it was worth it.', accept: ['redo'], pt: 'Meu gerente me fez refazer a cotação, mas valeu a pena.', fam: 2 },
    { pre: 'The new supplier enabled us', post: 'prices for paint makers.', accept: ['to lower'], pt: 'O novo fornecedor nos permitiu baixar os preços para os fabricantes de tintas.', fam: 1 },
    { pre: 'We watched the stand', post: 'crowded within minutes.', accept: ['get'], pt: 'Vimos o estande ficar lotado em poucos minutos.', fam: 2 },
    { pre: 'The price news inspired many clients', post: 'before prices went up.', accept: ['to buy'], pt: 'A notícia dos preços inspirou muitos clientes a comprar antes que os preços subissem.', fam: 1 },
    { pre: 'I had my assistant', post: 'the exchange rate before the quote.', accept: ['check'], pt: 'Pedi para minha assistente conferir a taxa de câmbio antes da cotação.', fam: 2 },
    { pre: 'We saw the exchange rate', post: 'up last week.', accept: ['go'], pt: 'Vimos a taxa de câmbio subir na semana passada.', fam: 2 }
  ]
};

/* Exercício 2: escolher. Posição da certa por item: 2,3,1,3,2,1,3. */
var EX2 = {
  example: { pre: 'The video helped me', post: 'the offer.', opts: ['understanding', 'understand', 'to understand'], right: 1, note: '“Help” aceita os dois: “understand” ou “to understand”', pt: 'O vídeo me ajudou a entender a oferta.' },
  items: [
    { pre: 'The supplier requires clients', post: 'a fee for small orders.', opts: ['paying', 'to pay', 'pay'], right: 1, fam: 1, pt: 'O fornecedor exige que os clientes paguem uma taxa por pedidos pequenos.' },
    { pre: 'My manager urged us', post: 'prices before the quarter ended.', opts: ['lowering', 'lower', 'to lower'], right: 2, fam: 1, pt: 'Meu gerente insistiu para que baixássemos os preços antes do fim do trimestre.' },
    { pre: 'I would love you', post: 'the sample on Friday.', opts: ['to test', 'testing', 'test'], right: 0, fam: 1, pt: 'Eu adoraria que você testasse a amostra na sexta.' },
    { pre: 'Please don\u2019t make the client', post: 'twice for the same sample.', opts: ['to wait', 'waiting', 'wait'], right: 2, fam: 2, pt: 'Por favor, não faça o cliente esperar duas vezes pela mesma amostra.' },
    { pre: 'The discount got buyers', post: 'the booth, even on a crowded day.', opts: ['visit', 'to visit', 'that visit'], right: 1, fam: 1, pt: 'O desconto levou os compradores a visitar o estande, mesmo num dia lotado.' },
    { pre: 'The manager had the team', post: 'the exchange rate.', opts: ['check', 'to check', 'that check'], right: 0, fam: 2, pt: 'O gerente pediu para a equipe conferir a taxa de câmbio.' },
    { pre: 'Her presentation inspired the team', post: 'harder.', opts: ['work', 'working', 'to work'], right: 2, fam: 1, pt: 'A apresentação dela inspirou a equipe a trabalhar mais.' }
  ]
};

/* Exercício 3: dizer em inglês. Cada item aceita o trecho-chave (regex), não a frase exata. */
var EX3 = {
  example: { pt: 'Eu vi o cliente sair.', model: 'I saw the client leave.', fam: 2 },
  items: [
    { pt: 'A feira exige que os expositores paguem a taxa de inscrição.', model: 'The fair requires exhibitors to pay the enrollment fee.', fam: 1, ok: ['requires? exhibitors to pay (the )?enrollment fee'] },
    { pt: 'O gerente fez a equipe baixar os preços.', model: 'The manager made the team lower prices.', fam: 2, ok: ['made (the )?team lower (the )?prices'] },
    { pt: 'O cliente me fez esperar, mas valeu a pena.', model: 'The client made me wait, but it was worth it.', fam: 2, ok: ['made me wait.*worth it'] },
    { pt: 'Eu adoraria que você conferisse a taxa de câmbio.', model: 'I would love you to check the exchange rate.', fam: 1, ok: ["(i would|i'd) love you to check (the )?exchange rate"] },
    { pt: 'Consegui que o fornecedor reduzisse a taxa.', model: 'I got the supplier to lower the fee.', fam: 1, ok: ['got (the )?supplier to (lower|reduce|cut|drop) (the )?fee'] },
    { pt: 'Vimos os preços subirem.', model: 'We saw prices go up.', fam: 2, ok: ['(saw|watched) (the )?prices go up'] },
    { pt: 'Vimos o showroom ficar lotado.', model: 'We watched the showroom get crowded.', fam: 2, ok: ['(saw|watched) (the )?showroom get crowded'] }
  ]
};

/* Exercício 4: perguntas dissertativas. Ninguém corrige sozinho: o professor lê. */
var EX4 = {
  min: 25,
  items: [
    { q: 'A client says: \u201CYour prices are too high.\u201D What do you ask your manager to do? What can you get the client to do?', pt: 'Um cliente diz: \u201CSeus preços estão altos demais.\u201D O que você pede para o seu gerente fazer? O que você consegue que o cliente faça?', hint: 'Ask him to… · get the client to…' },
    { q: 'Think about a time the exchange rate or a fee upset a client. What did you make or have the team do?', pt: 'Pense numa vez em que o câmbio ou uma taxa chateou um cliente. O que você fez a equipe fazer ou pediu para ela fazer?', hint: 'Made the team… · had my assistant…' },
    { q: 'What would you love your company to do for paint makers next year? Why would it be worth it?', pt: 'O que você adoraria que a sua empresa fizesse pelos fabricantes de tintas no ano que vem? Por que valeria a pena?', hint: 'I would love the company to… · it would be worth it' }
  ]
};

/* Exercício 5: responder ao e-mail de um cliente. A página da aluna e o painel do professor leem este objeto. */
var EX5 = {
  min: 70, max: 130,
  title: 'Reply to the client',
  pt: 'Responda ao cliente',
  mail: {
    subject: 'Price update for January?',
    from: 'Marcos Teixeira <marcos.teixeira@alvorada-paints.example>',
    to: 'Vitória · Midland',
    date: 'Monday, 9:14 AM',
    paras: [
      'Hi Vitória,',
      'A colleague told me your prices will go up next month because of the exchange rate. <span class="ask">Is that true?<sup>1</sup></span>',
      'We are planning our January production and we need raw materials for it. I would love to know if there is any way to keep the current price.',
      'Also, the fee on our last invoice was higher than usual. <span class="ask">Can you explain why?<sup>2</sup></span>',
      'If it is worth it for both sides, we can place the order this week.'
    ],
    sig: ['Best regards,', 'Marcos Teixeira', 'Purchasing · Alvorada Paints'],
    note: 'Marcos asked two questions. Answer both!'
  },
  steps: [
    { en: 'Tell him yes: the prices go up next month.', pt: 'Diga que sim: os preços sobem no mês que vem, por causa do câmbio.' },
    { en: 'Ask him to place the order before that.', pt: 'Peça que ele faça o pedido antes disso.' },
    { en: 'Explain what you got your supplier to do for him.', pt: 'Explique o que você conseguiu que o fornecedor fizesse por ele.' }
  ],
  hint: 'Use structures from today and two lesson words.',
  hintpt: 'Use estruturas de hoje e duas palavras da aula.',
  quote: 'On Monday, 9:14 AM, Marcos Teixeira wrote:<br>A colleague told me your prices will go up next month because of the exchange rate. Is that true? […]'
};

/* Palavras da aula que aparecem no texto da aluna (para o painel e para a dica abaixo da caixa). */
var LESSON_RX = [
  ['enrollment fee', /enrollment fees?/i],
  ['lower prices', /lower\b.{0,12}\bprices?/i],
  ['worth it', /\bworth\b/i],
  ['crowded', /\bcrowded\b/i],
  ['exchange rate', /exchange rate/i],
  ['fee', /(?<!enrollment )\bfees?\b/i],
  ['go up', /\b(?:go|goes|going|went|gone) up\b/i]
];
