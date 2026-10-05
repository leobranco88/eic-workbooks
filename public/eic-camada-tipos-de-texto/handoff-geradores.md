# Handoff para o projeto do eic-writing: camada de tipo de texto (gerador 1 e gerador 2)

Este texto resume o raciocínio de uma conversa longa. Lê tudo antes de mexer no site. Ele separa o que o Leo decidiu do que só foi recomendado e do que não foi verificado.

## 1. Por que mudar

O gerador de tema do eic-writing só oferecia "Opinião" e "Os dois lados". O Leo estranhou que o Teens 1 não tivesse email nem outros tipos. A análise das 60 tarefas de Writing do livro (Life 1 a 5, arquivo `writing_raw.json`) confirmou: o livro ensina muitos tipos de texto, e opinion essay aparece só em Teens 4 unidade 11 e Teens 5 unidade 6. Dar opinião aparece em Teens 3 unidade 9 e Teens 5 unidade 8. For-and-against, que seria "dois lados", não aparece em nenhum nível. Ou seja, o gerador atual só cobre dois tipos que o livro quase não ensina nos primeiros níveis.

Tipo de texto muda a folha: cada um tem um layout próprio de página. Por isso a solução não é só um sorteio de tema, é um material com templates por tipo.

## 2. O que o Leo decidiu (dito por ele)

1. Criar templates impressos, um por tipo de texto, para o aluno escrever à mão. Feito: PDF de 22 páginas (`eic-writing-templates-completo.pdf`), aprovado visualmente por ele.
2. Regra de layout dos templates: espaço livre para escrever e desenhar, instruções na coluna lateral, nunca dentro das molduras. Sobra de espaço vira linha de escrever. Caixas com linha fina.
3. Ter um segundo gerador (gerador 2, de situações), além do atual.
4. O gerador atual (gerador 1) passa a ter só opinião e dois lados. Os outros tipos saem dele.
5. Topic sentences continuam servindo ao gerador 1. Filtro por unidade: o aluno sorteia temas da unidade atual e das anteriores, nunca de unidades à frente (decidido numa etapa anterior).
6. Mesmo com o tema fiel à unidade, o gerador 2 pode ter mais de uma situação por unidade, inclusive de gêneros diferentes do que o livro ensina na unidade, para dar mais prática.
7. Tradução nas situações: Teens 1 com a frase inteira em português e palavras-chave traduzidas. Teens 2 e 3 só com palavras-chave.

## 3. O que foi recomendado e ainda NÃO decidido

- Nível mínimo do gerador 1: recomendei oferecer opinião e dois lados só a partir do Teens 3 ou 4, porque muitas frases do Teens 1 e 2 não dão debate ("A friendly hello makes a new student feel welcome"). Não contei quantas frases dos níveis baixos são debatíveis.
- Teens 4 e 5: os arquivos trazem só palavras raras com tradução, por dedução da regra acima. O Leo não falou desses níveis. Teens 6 não existe.
- Tamanho da caixa "Topic or question": com inglês, português e palavras-chave, no Teens 1 ela precisa de uns 24 mm em vez de 17 mm. Ainda não decidido.
- Como o gerador 2 se liga aos templates (por exemplo, mostrar o botão de imprimir a página do tipo sorteado): é sugestão minha de implementação, não pedido dele.
- Narrativa: eu disse que cabe no gerador 2 e não no 1 (não parte de uma tese). O Leo seguiu em frente e pediu o gerador 2, mas não confirmou isso em palavras.

## 4. Arquivos

- `eic-writing-templates-completo.pdf`: 22 páginas A4. 1 email informal, 2 email formal, 3 post de rede social, 4 fórum ou blog de viagem, 5 mensagens, 6 resenha, 7 anúncio, 8 notícia, 9 agradecimento, 10 perfil, 11 formulário, 12 descrição, 13 história, 14 história de vida, 15 instruções ou conselho, 16 anotações, 17 relatório curto, 18 currículo, 19 carta formal, 20 artigo, 21 opinion essay (plano), 22 dois lados (plano).
- `topic-sentences-eic.json` e `.csv`: 299 frases para o gerador 1. Campos: id, teens, book, unit, unit_title, lesson, source_kind, source_description, theme_code, theme_pt, theme_en, topic_sentence, grounding (book, unit_theme ou theme_only). As 27 frases do Teens 6 são só de tema, sem base do livro.
- `situacoes-teens1.json` a `situacoes-teens5.json` (e `.md` de cada um): situações do gerador 2. Teens 1: 43, Teens 2: 45, Teens 3: 48, Teens 4: 48, Teens 5: 47 (231 no total). Campos: id, teens, unit, unit_title, genre, kind (book_genre ou extra), template_page, situation_en, situation_pt, words (lista de en e pt).
- `mapa-niveis.md`: tipos de texto que o livro ensina por nível, fonte `writing_raw.json`.

## 5. Mudança no gerador 1

- Deixar só opinião e dois lados. Remover todo outro tipo de texto. Não revisei quais tipos o gerador tem hoje além do que a tela mostrava para o Teens 1.
- Manter o filtro por nível e por unidade (unidade atual e anteriores).
- As páginas de plano (21 e 22 do PDF) combinam com este gerador.
- A decisão do nível mínimo (seção 3) está em aberto.

## 6. Gerador 2: especificação

- Entrada: nível (Teens) e unidade. Mostra situações com nível menor ou igual e unidade até a atual.
- Cada situação já carrega o gênero e a página de template. O gênero permitido está nos dados: as situações extras de uma unidade só usam gêneros que o livro ensinou até aquela unidade. Quem escrever situações novas precisa seguir essa regra.
- Em cada unidade, a situação "livro" (kind book_genre) segue o gênero que o livro ensina na seção Writing daquela unidade. As "extra" são prática variada, com o tema da unidade.
- Teens 1 a 5: escritos e revisados por leitores cegos (Teens 1 e 2 em duas passagens; Teens 3 a 5 em duas passagens com professor/editor, e aluno só na primeira). Gêneros novos nos níveis altos e a página do PDF: relatório 17, currículo 18, carta de apresentação ou reclamação 19, artigo 20, notícia 8, biografia 14, descrição de evento 12, parágrafo de opinião 21, blog post 4. Nos Teens 4 (unidade 11) e 5 (unidade 6), onde o livro ensina opinion essay, as situações são só extras. Cada situação 'a' segue o livro; marcado em `kind`. Teens 6: o Life 6 não foi extraído, então não há base do livro. Marcar as situações do Teens 6 como "sem base do livro" ou esperar o Life 6.
- Mostrar: situação em inglês, português embaixo em cinza (só Teens 1), linha de palavras-chave. Palavras verbais aparecem na forma base com a flexão entre parênteses quando precisa (ex.: “felt (feel)”).
- Linha fixa em toda folha (ainda não está nos arquivos de situação, é para a interface/PDF): “You can invent names, numbers and details. Do not write your real address or phone number.” (Teens 1 em português.) Ela cobre tarefas que pedem dados, números ou contato. Verbos de instrução do Teens 1, uma vez na folha: write = escrever, ask = perguntar, say = dizer, send = mandar, fill out = preencher, invite = convidar, describe = descrever, choose = escolher, post = publicar.

## 7. Regras da casa para qualquer texto novo

Inglês americano. Primeira letra de linha ou frase maiúscula. Aspas curvas. Parte escrita à mão em inglês, português cinza embaixo. Impressora da escola é preto e branco, então linhas de escrever são elementos reais (nunca gradiente). Sem Nexus City. Evitar tema de família. Não inventar fatos nem números. Zip de deploy só depois que o Leo aprovar os arquivos. O site não foi alterado ainda: tudo até aqui são arquivos soltos.

## 8. O que NÃO foi verificado

- As situações nunca foram conferidas contra as páginas do livro, só contra os títulos das tarefas de Writing.
- A ordem dos gêneros por unidade não foi confrontada com o que cada professor ensina em sala.
- As frases "Useful chunks" de cada template e os rótulos da estrutura de cada gênero são escolha nossa, não do livro.
- As traduções das palavras-chave não foram checadas com o vocabulário que o Leo ensina (por exemplo "post = publicação").
- Nenhuma página foi impressa na impressora preto e branco da escola. Linha fina e clara pode sair fraca no papel.
- Das 22 páginas, só algumas foram vistas na tela depois do último ajuste de espaço. O resto foi conferido por medida.
- Revisão cega: feita nas situações dos Teens 1 a 5 (leitores sem contexto, só o texto). Os templates novos (páginas 12 a 22) ainda não passaram por ela. Os revisores contestaram alguns pontos que não apliquei (ex.: “film” por “movie”, quase-duplicados leves entre unidades distantes, rótulos 'poster' e 'notice').
- Teens 3 a 5: gêneros marcados 'notes' (T3 u4-d) e o rótulo de página de cada situação não passaram pelo olho de um professor da escola.
- Teens 6: sem situações (Life 6 não extraído).

## 9. Próximos passos sugeridos

1. Leo decide as pendências da seção 3.
2. Mudar o gerador 1 e criar o gerador 2 com o Teens 1.
3. Teens 6: extrair o Life 6 e escrever as situações.
4. Revisão cega dos templates das páginas 12 a 22.
5. Teste de impressão preto e branco antes da gráfica.
