# Roteiro — Parte 1: apresentação principal (10 minutos)

> **Formato:** 8 a 10 minutos, dividido entre William, Kelvin e Marcos.
> **Objetivo:** mostrar o diagnóstico, as duas otimizações, a comprovação
> experimental e a conclusão, sem esgotar a discussão crítica.
> **Parte 2:** o aprofundamento e a análise dos limites do ganho estão em
> [`roteiro_aprofundamento.md`](roteiro_aprofundamento.md). O baralho completo
> fica em [`slides.md`](slides.md), com um slide de transição entre as partes.

## Divisão rápida

| Tempo | Quem | Bloco | Ideia que não pode faltar |
|---:|---|---|---|
| 0:00–0:30 | **William** | Abertura | Tema, integrantes e pergunta central. |
| 0:30–1:20 | **William** | Problema e roteiro | Equivalência; comparação ingênua × chave + hash. |
| 1:20–2:10 | **Kelvin** | Duplicatas original | Dois laços, `n(n-1)/2`, O(n²), O(1). |
| 2:10–3:00 | **Kelvin** | Anagramas original | Busca nos grupos + recálculo da chave, O(n²·k log k). |
| 3:00–3:40 | **Marcos** | Metodologia | `perf_counter`, aquecimento, repetições, mediana, pior caso. |
| 3:40–4:30 | **William** | Duplicatas otimizada | `set` como memória; O(n) esperado; O(n) de espaço. |
| 4:30–5:20 | **Kelvin** | Anagramas otimizada | Chave uma vez + `dict`; O(n·k log k). |
| 5:20–6:10 | **Marcos** | Resultados: duplicatas | 13,132 s → 2,10 ms; 6.240,9× em n=16.000. |
| 6:10–7:00 | **Marcos** | Resultados: anagramas | 17,286 s → 12,53 ms; 1.379,1× em n=1.600. |
| 7:00–7:35 | **William** | Gráficos | Inclinação 2 × 1 na escala log-log. |
| 7:35–8:15 | **Kelvin** | Como rodar e testar | `pytest` e `python -m src.benchmark`. |
| 8:15–8:55 | **Marcos** | Limites (teaser) | O ganho depende do cenário; a Parte 2 aprofunda. |
| 8:55–9:30 | **William** | Conclusão da Parte 1 | A ordem de crescimento mudou. |
| 9:30–10:00 | **William** | Transição | Anunciar o fim da Parte 1 e o início da Parte 2. |

**Tempo de fala por pessoa:** William ≈ 3 min 20 s; Kelvin ≈ 3 min 10 s;
Marcos ≈ 3 min 10 s. O restante é respiração, troca de slide e imprevisto.

## Regras de ensaio

1. Cada um ensaia o próprio bloco cronometrado, depois o grupo ensaia as
   passagens de bastão.
2. Quem termina não espera silêncio: usa a frase de passagem já escrita.
3. Não ler o slide. O slide tem a tabela ou o código; a fala explica o porquê.
4. Números redondos na fala, números exatos no slide. Exemplo: “treze segundos
   contra dois milissegundos”, não “13,132349 s”.
5. Se o tempo apertar, corte o slide de “como rodar e testar” da fala e deixe-o
   no material de apoio. Nunca corte a conclusão.

---

## Roteiro detalhado

### 0:00–0:30 — William — Abertura

**Slide 1 — Título.**

> “Boa tarde. Somos William, Kelvin e Marcos. Vamos apresentar o diagnóstico e a
> primeira otimização de dois algoritmos: detecção de duplicatas e agrupamento
> de anagramas. A pergunta que guia tudo é simples: <strong>quanto ganhamos, por que ganhamos e até onde esse ganho vai?</strong>”

**Passagem:** “Para começar, precisamos deixar claro qual é o problema.”

---

### 0:30–1:20 — William — Problema e roteiro

**Slide 2 — O problema.**

> “Nos dois casos, o problema é decidir se dois itens são equivalentes. Em
> duplicatas, queremos saber se algum valor aparece duas vezes. Em anagramas,
> queremos agrupar palavras que têm as mesmas letras em ordem diferente.
> A solução ingênua compara todos os pares. A solução eficiente transforma cada
> item em uma **chave** e usa uma tabela de hash. Esta é a evolução desde a
> Entrega 1: saímos do código original para a primeira otimização e agora
> consolidamos a versão final com testes, benchmark e análise dos limites. O
> repositório tem as duas versões, os testes e o benchmark completo.”

**Roteiro da apresentação, em uma frase:**

> “Primeiro mostramos o código original e seu gargalo; depois a otimização;
> depois os números e os gráficos; por fim, os limites do ganho.”

**Passagem:** “Kelvin vai mostrar por que o código original é quadrático.”

---

### 1:20–2:10 — Kelvin — Versão original: duplicatas

**Slide 3 — Duplicatas original.**

> “A versão original tem dois laços. O externo fixa a posição `i`; o interno
> compara `lista[i]` com todas as posições seguintes. Se não há duplicatas, ela
> faz `(n-1) + (n-2) + ... + 1 = n(n-1)/2` comparações. Isso é O(n²). O espaço
> adicional é O(1), porque só guardamos os índices. O melhor caso é quando os
> dois primeiros elementos são iguais: a função retorna na primeira comparação.
> Mas o benchmark usa o pior caso: lista sem duplicatas.”

**Passagem:** “O mesmo padrão aparece nos anagramas, com um custo extra.”

---

### 2:10–3:00 — Kelvin — Versão original: anagramas

**Slide 4 — Anagramas original.**

> “Para cada palavra, o código percorre todos os grupos já formados. Em cada
> visita, ele normaliza e ordena as letras da palavra **e** do representante do
> grupo. Normalizar e ordenar custa O(k log k), onde `k` é o comprimento da
> palavra. No pior caso, cada palavra cria um grupo novo: são O(n²) visitas,
> cada uma com O(k log k). Total: O(n²·k log k). O espaço é O(n) para os grupos.
> O gargalo é duplo: buscar o grupo e refazer a mesma chave várias vezes.”

**Passagem:** “Antes de otimizar, precisamos medir do jeito certo.”

---

### 3:00–3:40 — Marcos — Metodologia

**Slide 5 — Como medimos.**

> “Usamos `time.perf_counter`, que é o relógio de maior resolução do Python.
> Cada função passa por aquecimento; depois medimos várias repetições e
> reportamos a **mediana**, que é menos sensível a picos de carga. Para funções
> muito rápidas, cada repetição executa a função várias vezes e divide o tempo
> total pelo número de execuções. As entradas de duplicatas são permutações sem
> repetição; as de anagramas são palavras aleatórias de oito letras. Isso força
> o pior caso das duas versões originais. A correção é verificada com `pytest`.”

**Frase de honestidade:** “Os tempos absolutos dependem da máquina; o que
interessa é a **tendência de crescimento**.”

**Passagem:** “Com o diagnóstico e a medição definidos, William mostra a
primeira otimização.”

---

### 3:40–4:30 — William — Primeira otimização: duplicatas com `set`

**Slide 6 — Duplicatas com `set`.**

> “A ideia é manter um conjunto com tudo o que já vimos. Para cada item,
> perguntamos se ele já está no conjunto; se estiver, retornamos `True` na hora.
> Caso contrário, inserimos. Consulta e inserção em `set` custam O(1)
> **amortizado esperado**, então o tempo total é O(n). O preço é o espaço: O(n)
> no pior caso, quando todos os elementos são distintos. Também há uma restrição:
> os elementos precisam ser **hashable**. Para listas de listas, a versão
> original ainda funciona, mas esta levanta `TypeError`.”

**Trade-off em uma frase:** “Trocamos memória por tempo.”

**Passagem:** “A mesma ideia se aplica aos anagramas, mas com uma chave.”

---

### 4:30–5:20 — Kelvin — Primeira otimização: anagramas com chave + `dict`

**Slide 7 — Anagramas com chave + `dict`.**

> “A versão otimizada calcula a chave uma única vez por palavra: normaliza,
> ordena as letras e converte em tupla. Duas palavras são anagramas se, e
> somente se, têm a mesma chave. Um dicionário associa cada chave ao grupo
> correspondente. A busca linear pelos grupos desaparece. O custo dominante
> passa a ser a ordenação das letras: O(k log k) por palavra, O(n·k log k) no
> total. Com `k` fixo, como no benchmark, isso é linear em `n`. O espaço é
> O(n·k) para chaves e grupos.”

**Detalhe que mostra domínio:** “A normalização usa `casefold`, remove acentos
com NFD e descarta pontuação; por isso `Ação!` e `acao` caem no mesmo grupo.”

**Passagem:** “Agora os números. Marcos mostra duplicatas e anagramas.”

---

### 5:20–6:10 — Marcos — Resultados: duplicatas

**Slide 8 — Tabela de duplicatas.**

Mostre a tabela com `n = 500`, `4.000` e `16.000` e diga:

> “Em 500 elementos, a original leva 12,63 ms e a otimizada 92 µs: 137 vezes.
> Em 16.000, a original leva 13,132 segundos e a otimizada 2,10 ms: **6.240,9 vezes**. A cada dobra de `n`, a original cresce cerca de 4 vezes; a otimizada,
> cerca de 2. No log-log, as inclinações são aproximadamente 2,0 e 0,9. O ganho
> não é uma constante: ele cresce com `n`, exatamente como a razão entre uma
> função quadrática e uma linear prevê.”

**Comentário de rigor:** “Entre 1.000 e 2.000 a versão otimizada cresceu só
1,12×; isso é ruído de medição e efeito de cache/alocação, não uma mudança de
complexidade.”

**Passagem:** “Nos anagramas, o comportamento se repete, mas com um custo
residual.”

---

### 6:10–7:00 — Marcos — Resultados: anagramas

**Slide 9 — Tabela de anagramas.**

> “Em 1.600 palavras, a original leva 17,286 segundos e a otimizada 12,53 ms:
> **1.379,1 vezes**. As inclinações log-log são aproximadamente 2,0 e 1,1. O
> ganho é menor que o de duplicatas porque a normalização e a ordenação de cada
> palavra continuam existindo; o que desaparece é o fator O(n²) da busca nos
> grupos. A cada dobra de `n`, a original cresce de 3,9 a 4,3 vezes; a
> otimizada, de 1,9 a 2,3.”

**Passagem:** “Os gráficos mostram isso de forma mais direta.”

---

### 7:00–7:35 — William — Gráficos

**Slide 10 — Gráficos em escala linear e log-log.**

> “À esquerda, a escala linear mostra a explosão da versão original. À direita,
> a escala log-log transforma potências em retas: a inclinação da original fica
> próxima de 2; a da otimizada, próxima de 1. As linhas tracejadas são
> referências O(n²) e linear, não ajustes aos dados. O importante não é o valor
> absoluto, que muda de máquina para máquina, mas a **mudança de inclinação**.”

**Passagem:** “Kelvin mostra como reproduzir e testar tudo isso.”

---

### 7:35–8:15 — Kelvin — Como rodar e testar

**Slide 11 — Comandos.**

```bash
# instalar dependências (ou usar o devcontainer)
python3 -m pip install -r requirements.txt

# todos os testes
python3 -m pytest -q

# testes de cada otimização
python3 -m pytest tests/test_duplicatas.py -q
python3 -m pytest tests/test_anagramas.py -q

# benchmark rápido, sem gráficos
python3 -m src.benchmark --rapido --sem-grafico

# benchmark completo; grava em resultados/local/
python3 -m src.benchmark

# atualizar os resultados de referência versionados
python3 -m src.benchmark --publicar
```

Fale:

> “Os testes comparam as duas versões em casos fixos e em entradas aleatórias.
> Eles provam que a otimização **não muda o resultado** nesses casos, mas não
> provam desempenho: para isso existe o benchmark. O benchmark completo demora;
> para uma demonstração ao vivo, use `--rapido`. A saída padrão vai para
> `resultados/local/`, que é ignorada pelo git, para não sobrescrever a
> referência.”

**Passagem:** “Com tudo reproduzível, Marcos fecha a Parte 1 com os limites.”

---

### 8:15–8:55 — Marcos — Limites (teaser)

**Slide 12 — O ganho tem limites.**

> “O benchmark mede o pior caso sintético. Se a duplicata está nas primeiras
> posições, a versão original retorna em microssegundos e a vantagem cai para
> cerca de 1,5×, podendo inverter dependendo das constantes. Se todas as palavras
> são anagramas entre si, o termo O(n²)
> da versão original desaparece e o ganho cai para cerca de 2 vezes. E a versão
> otimizada usa O(n) de memória. Ou seja: **6.240× é o ganho neste cenário, não uma propriedade universal do algoritmo**. É exatamente isso que a Parte 2
> aprofunda.”

**Passagem:** “William fecha a Parte 1.”

---

### 8:55–9:30 — William — Conclusão da Parte 1

**Slide 13 — Conclusão da Parte 1.**

> “A primeira otimização elimina comparações repetidas. O `set` e o `dict` levam
> o custo esperado de O(n²) para O(n), no caso de duplicatas, e de
> O(n²·k log k) para O(n·k log k), no caso de anagramas. A mudança não é só de
> constante: a **ordem de crescimento** mudou. Por isso o ganho cresce com `n`.
> O código final, os testes e o benchmark estão no repositório, e os números são
> reprodutíveis.”

**Frase de fechamento da Parte 1:**

> “A primeira otimização não apenas deixou o código mais rápido: ela mudou a
> inclinação da curva. O ganho cresce com o tamanho da entrada, que é
> exatamente o que a análise de complexidade previa.”

---

### 9:30–10:00 — William — Transição para a Parte 2

**Slide 14 — Transição.**

> “**A Parte 1 termina aqui.** Até agora respondemos: funciona, é mais rápido e
> o ganho aparece nos gráficos. A Parte 2 começa com a pergunta mais difícil:
> **quando esse ganho desaparece?** Vamos aprofundar as duas otimizações,
> separar ganho assintótico de ganho medido e analisar criticamente os limites:
> distribuição da entrada, memória, pior caso do hash, custo residual da chave e
> validade do experimento.”

Se o slot terminar aqui, acrescente:

> “Obrigado. Ficamos à disposição para perguntas.”

Se a Parte 2 for apresentada em seguida, não agradeça ainda; emende a primeira
frase do roteiro de aprofundamento.

---

## Perguntas prováveis da Parte 1

- **Por que não usar `set(lista)` e comparar tamanhos?** Funciona para
  duplicatas, mas cria uma cópia O(n) e não retorna cedo. O laço com `set` para
  na primeira duplicata.
- **O `set` não é O(1) no pior caso?** O pior caso teórico é O(n) por operação;
  o custo esperado é O(1) amortizado. Na prática, os tipos usuais têm hash bem
  distribuído.
- **Por que a versão de anagramas não é O(n) puro?** Porque ainda ordenamos as
  letras de cada palavra, O(k log k). Com `k` fixo, isso é linear em `n`.
- **O que mudaria para O(n·k)?** Uma chave de contagem de caracteres em vez de
  ordenar as letras. Na Parte 2 mostramos por que isso não compensa para
  `k = 8`.
- **O ganho de 6.240× é garantido?** Não. Ele vale para o pior caso, nesta
  máquina, com esta distribuição de entrada. A Parte 2 discute os limites.

## Cola de números

| Cenário | Original | Otimizada | Ganho |
|---|---:|---:|---:|
| Duplicatas, n=500 | 12,63 ms | 92,0 µs | 137,2× |
| Duplicatas, n=4.000 | 757,99 ms | 430,2 µs | 1.762,1× |
| Duplicatas, n=16.000 | 13,132 s | 2,10 ms | 6.240,9× |
| Anagramas, n=100 | 62,38 ms | 680,6 µs | 91,7× |
| Anagramas, n=400 | 1,014 s | 2,68 ms | 378,2× |
| Anagramas, n=1.600 | 17,286 s | 12,53 ms | 1.379,1× |

**Inclinações log-log:** duplicatas ≈2,0 (original) e ≈0,9 (otimizada);
anagramas ≈2,0 (original) e ≈1,1 (otimizada).
