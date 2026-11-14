# Roteiro — Parte 2: aprofundamento e limites do ganho (10 minutos)

> **Quando usar:** emende depois da Parte 1, no slide de transição. Também
> serve como apresentação autônoma de 10 minutos para uma banca que queira
> discutir critérios, trade-offs e validade dos resultados.
> **Mensagem central:** *ganho é uma razão, não uma constante.* O número de
> 6.240× é verdadeiro no cenário medido, mas não é uma propriedade universal do
> algoritmo.
> **Apoio experimental:** [`src/limites.py`](../src/limites.py), que mede os
> cenários que o benchmark de pior caso não cobre.

## Divisão rápida

| Tempo | Quem | Bloco | Ideia que não pode faltar |
|---:|---|---|---|
| 0:00–0:35 | **William** | Retomada e tese | Ganho é razão; depende de `n`, entrada, memória e constantes. |
| 0:35–2:05 | **William** | Duplicatas: o ganho depende da entrada | Fórmula do ganho; duplicata cedo × tarde; memória; hash; semântica. |
| 2:05–3:35 | **Kelvin** | Anagramas: o custo que sobra | Grupos distintos × iguais; chave O(k log k) × O(k); memória. |
| 3:35–5:05 | **Marcos** | O que o experimento não prova | Uma máquina, uma semente, mediana, ruído, pior caso sintético. |
| 5:05–6:35 | **William** | Limites teóricos e quando não otimizar | Ω(n), espaço × tempo, cache, GIL, adversário. |
| 6:35–8:05 | **Kelvin** | Como rodar, testar e demonstrar | Comandos, o que cada teste prova e o que não prova. |
| 8:05–9:20 | **Marcos** | Como melhorar a análise | Múltiplas sementes, memória, profiler, chave adaptativa. |
| 9:20–10:00 | **William** | Conclusão | O ganho é real, mas condicional. |

**Tempo de fala por pessoa:** William ≈ 3 min 35 s; Kelvin ≈ 3 min;
Marcos ≈ 2 min 45 s. O restante é troca de slide.

---

## Roteiro detalhado

### 0:00–0:35 — William — Retomada e tese

**Slide 15 — Parte 2: o ganho tem limites.**

> “A Parte 1 terminou com uma conclusão clara: a otimização mudou a ordem de
> crescimento e o ganho cresceu com `n`. Agora vamos fazer a pergunta que a
> medição sozinha não responde: **esse ganho é universal?** A tese da Parte 2 é
> simples: ganho é uma **razão** entre dois tempos, não uma constante do
> algoritmo. Ele depende do tamanho, da distribuição da entrada, do custo de
> memória, das constantes do interpretador e do contrato de igualdade dos
> dados.”

**Roteiro em uma frase:** “Vamos separar o que é ganho assintótico do que é
ganho medido neste cenário.”

**Passagem:** “Começando por duplicatas: o mesmo algoritmo pode ganhar 1.800×
ou quase nada, dependendo de onde está a duplicata.”

---

### 0:35–2:05 — William — Duplicatas: o ganho depende da entrada

**Slide 16 — A fórmula do ganho.**

> “No pior caso, a versão original faz aproximadamente `c_o · n²/2`
> comparações. A versão com `set` faz `c_h · n` operações de hash, mais uma
> constante de criação do conjunto. Então o ganho é aproximadamente
> `(c_o / 2c_h) · n`. Ele **cresce linearmente com n**. Por isso 137× em
> n=500 e 6.240× em n=16.000: não são dois resultados contraditórios, são o
> mesmo resultado em pontos diferentes da mesma reta.”

**Slide 17 — Cedo × tarde.**

Mostre a tabela do `src/limites.py`:

| Cenário (n=4.000) | Original | Com `set` | Ganho |
|---|---:|---:|---:|
| duplicata no início | 0,63 µs | 0,46 µs | 1,4× |
| duplicata no fim | 781,44 ms | 429,15 µs | 1.820,9× |

> “Se a duplicata está nas primeiras posições, a versão original retorna quase
> imediatamente. O ganho desaba de milhares de vezes para cerca de 1,5×. Em
> outra execução, a original pode até ficar alguns por cento à frente; a
> diferença está na casa de microssegundos e é dominada por constantes. Isso
> não invalida a otimização: mostra que **o pior caso é uma escolha do benchmark**, não uma propriedade de qualquer entrada real.”

**Slide 18 — O preço em memória.**

> “A versão com `set` guarda todos os elementos distintos. Com n=4.000, o pico
> medido foi de 160 KiB contra 0,1 KiB da original; a 16.000, fica na casa de
> 640 KiB. É O(n) de espaço. Em 1 milhão de inteiros, a ordem de grandeza é
> dezenas de megabytes. Em um ambiente com memória limitada ou com dados que
> chegam em fluxo, isso pode ser o fator decisivo, não o tempo.”

**Slide 19 — O pior caso do hash e a semântica.**

> “O O(1) do `set` é **esperado**, não garantido: no pior caso teórico, com
> colisões, cada operação pode custar O(n). Para strings, o Python usa hash
> aleatorizado; para inteiros, o hash é o próprio valor. Um adversário que
> controla a entrada pode tentar explorar isso. Há também uma diferença de
> semântica: `[nan, nan]` com o **mesmo objeto** `nan` retorna `False` na versão
> original, porque `nan != nan`, e `True` na versão com `set`, porque a busca
> usa identidade antes de igualdade. E listas aninhadas funcionam na original,
> mas levantam `TypeError` na otimizada. O teste automatizado cobre inteiros e
> strings; esses casos patológicos precisam ser documentados ou rejeitados.”

**Passagem:** “Nos anagramas, o limite não é a busca: é o custo que sobra.”

---

### 2:05–3:35 — Kelvin — Anagramas: o custo que sobra

**Slide 20 — Anagramas: fórmula e distribuição dos grupos.**

> “A versão original faz, no pior caso, O(n²) visitas a grupos e, em cada
> visita, refaz a chave da palavra e do representante: O(k log k). Total:
> O(n²·k log k). A versão com `dict` calcula a chave uma vez por palavra:
> O(n·k log k). O termo O(n²) desaparece, mas o O(k log k) **fica**. É por isso
> que o ganho é menor que o de duplicatas: ainda pagamos a normalização e a
> ordenação de cada palavra.”

**Ainda no slide 20 — a distribuição dos grupos importa.**

| Cenário (n=400) | Original | Com `dict` | Ganho |
|---|---:|---:|---:|
| todas em grupos distintos | 1,094 s | 3,43 ms | 318,6× |
| todas no mesmo grupo | 4,82 ms | 2,44 ms | 2,0× |

> “Se todas as palavras são anagramas entre si, a versão original encontra o
> grupo na primeira comparação e não paga o termo O(n²). Ela ainda refaz a
> chave da palavra e do representante, então o ganho cai para cerca de 2×. O
> benchmark usa palavras aleatórias de oito letras: a chance de dois grupos
> coincidirem é desprezível, então ele mede o pior caso. Em um corpus com
> muitas repetições, o ganho real seria muito menor.”

**Slide 21 — Chave: ordenar ou contar?**

> “A chave atual ordena as letras: O(k log k). A alternativa assintoticamente
> melhor é contar as letras: O(k). Mas constante importa. Em 1.000 palavras,
> com k=8, a contagem foi cerca de 1,5× **mais lenta** que o `sorted`; com
> k=128, cerca de 1,6× mais rápida; com k=512, cerca de 1,8× mais rápida.
> Ou seja: a melhoria assintótica só compensa quando k é grande. No benchmark,
> k=8, então trocar a chave não melhoraria o resultado — poderia piorá-lo. Esse
> é um exemplo claro de por que **complexidade assintótica não é a única métrica**.”

**Memória dos anagramas (slide 18).**

> “O dicionário guarda uma chave por grupo e as listas de palavras. Com n=400,
> o pico foi de 52 KiB contra 24,5 KiB da original; com n=1.600, a ordem de
> grandeza é de centenas de KiB. É O(n·k), mas com fator constante maior. Para
> um corpus grande, isso pode pesar mais que o tempo economizado.”

**Passagem:** “Marcos vai mostrar o que o experimento prova e o que ele não
prova.”

---

### 3:35–5:05 — Marcos — O que o experimento não prova

**Slide 22 — Validade do experimento.**

> “O benchmark oficial mede uma máquina, uma semente, o pior caso sintético e
> reporta a mediana de poucas repetições. Ele mostra a tendência de crescimento,
> mas não dá intervalo de confiança, não varia a distribuição, não mede memória
> e não usa profiler. As inclinações log-log — 1,98 contra 0,87 em duplicatas e
> 2,04 contra 1,06 em anagramas — são **descritivas**: confirmam o formato
> previsto, mas não são uma prova estatística.”

**Ainda no slide 22 — ruído e anomalias.**

> “Entre n=1.000 e n=2.000, a versão otimizada de duplicatas cresceu só 1,12×,
> e não 2×. O relatório registra que isso não foi investigado. A explicação
> provável é ruído de medição, cache, alocação e frequência da CPU. Isso não
> muda a complexidade, mas mostra que uma única execução não basta para afirmar
> ganho com precisão. O correto seria repetir com várias sementes, alternar as
> versões, medir em mais de uma máquina e reportar dispersão.”

**Ainda no slide 22 — o que o benchmark não cobre.**

> “O benchmark não mede: melhor caso, caso médio, taxa de duplicatas, tamanho
> das palavras, distribuição dos grupos, memória, latência de cauda, custo de
> inicialização do interpretador, nem o comportamento com dados reais. O
> resultado é **externamente válido apenas dentro do cenário medido**. Para
> afirmar algo sobre produção, é preciso medir a distribuição real.”

**Passagem:** “Com isso, podemos separar os limites empíricos dos limites
teóricos.”

---

### 5:05–6:35 — William — Limites teóricos e quando não otimizar

**Slide 23 — Limites teóricos.**

> “Em duplicatas, o limite inferior é Ω(n): no pior caso, é preciso ler todos
> os elementos. A versão com `set` atinge O(n) esperado, que é ótimo a menos de
> constantes. Em anagramas, é preciso ler n palavras de comprimento k: Ω(n·k).
> A versão atual é O(n·k log k); uma chave por contagem chega a O(n·k), mas só
> compensa para k grande. Então há espaço teórico para melhorar, mas não há
> ganho infinito: o ganho é limitado pelo custo residual e pelas constantes.”

**Ainda no slide 23 — espaço, cache e paralelismo.**

> “A otimização troca tempo por espaço. Com n grande, o `set` e o `dict` não
> cabem no cache; cada acesso vira um miss de memória e a constante cresce. Em
> memória externa, o custo de I/O pode dominar. Threads não resolvem, porque o
> GIL impede paralelismo de CPU em Python puro; multiprocessing tem custo de
> serialização. O(1) assintótico não significa O(1) na prática.”

**Slide 24 — Trade-offs.**

> “A tabela resume o que trocamos: tempo por espaço, e um contrato de dados mais
> restrito. A versão otimizada continua legível; o risco não é legibilidade, é
> memória, cache e pior caso do hash. O pior caso determinístico da versão com
> `set` é O(n²) teórico; o O(n) é esperado. Essa é a letra miúda do ganho.”

**Slide 25 — Checklist: quando não otimizar.**

> “Não otimize se: n é pequeno e as constantes dominam; a duplicata aparece
> cedo; todas as palavras caem no mesmo grupo; a memória é limitada ou os dados
> são um fluxo; os elementos não são hashable; a igualdade tem casos especiais
> como NaN; ou a entrada é adversarial. Nesses casos, meça antes de trocar
> clareza por desempenho.”

**Passagem:** “Kelvin mostra como rodar e testar tudo o que apresentamos.”

---

### 6:35–8:05 — Kelvin — Como rodar, testar e demonstrar

**Slide 26 — Comandos de reprodução.**

```bash
# dependências (ou use o devcontainer)
python3 -m pip install -r requirements.txt

# testes de correção
python3 -m pytest -q
python3 -m pytest tests/test_duplicatas.py -q
python3 -m pytest tests/test_anagramas.py -q
python3 -m pytest tests/test_benchmark.py -q

# benchmark oficial
python3 -m src.benchmark --rapido --sem-grafico   # rápido
python3 -m src.benchmark                          # completo
python3 -m src.benchmark --publicar               # atualiza referência

# experimentos de limites (Parte 2)
python3 -m src.limites
python3 -m src.limites --rapido
```

Com `make`:

```bash
make test
make bench-rapido
make bench
make limites
```

**Ainda no slide 26 — o que cada coisa prova.**

> “`pytest` prova que as duas versões concordam em casos fixos e em entradas
> aleatórias: listas vazias, um elemento, `None`, strings, acentos, 10.000
> elementos, e que a entrada não é alterada. O benchmark mede tempo; ele **não**
> é um teste de correção. O `src.limites` mede os cenários de limite: duplicata
> cedo, todos os anagramas iguais, memória e chave por contagem. Nenhum deles
> prova que o código está correto para todo contrato de igualdade; por isso a
> discussão de NaN e de tipos não hashable importa.”

**Slide 27 — Demo segura (roteiro de palco).**

1. Antes de entrar: rode `python3 -m src.benchmark --rapido` e deixe
   `resultados/local/` aberto.
2. No palco: `python3 -m pytest -q` (rápido) e `python3 -m src.limites
   --rapido` (alguns segundos).
3. Mostre `resultados/local/resumo.md` e um CSV.
4. Não rode o benchmark completo ao vivo: são dezenas de segundos e o efeito
   visual já está nos gráficos.

> “Se a máquina da apresentação não tiver pytest, use o devcontainer ou
> `pip install -r requirements.txt`. O benchmark grava em `resultados/local/`
> por padrão, então a demonstração não altera os resultados versionados.”

**Passagem:** “Marcos fecha com o que faríamos para melhorar a análise.”

---

### 8:05–9:20 — Marcos — Como melhorar a análise e a implementação

**Slide 28 — Próximos experimentos.**

> “Para aumentar a validade: várias sementes, várias máquinas, intervalo de
> confiança, alternância entre versões para reduzir deriva térmica, e medição
> de memória com `tracemalloc` em todos os tamanhos. Para entender o gargalo:
> `cProfile` e `line_profiler`. Para testar a chave: comparar `sorted` e
> contagem em função de k e escolher um limiar adaptativo. Para testar a
> distribuição: variar a posição da duplicata e o número de grupos de
> anagramas.”

**Slide 29 — Próximas implementações.**

> “Chave adaptativa: `sorted` para k pequeno, contagem para k grande. Para
> memória: processar em fluxo, usar ordenação externa ou um filtro de Bloom
> (com falsos positivos) quando duplicatas aproximadas bastarem. Para dados
> numéricos, `array`/NumPy reduzem o custo por elemento. Para paralelismo,
> multiprocessing por blocos, com cuidado no custo de junção. E, antes de
> tudo, medir o cenário real: o benchmark sintético é um ponto de partida, não
> a resposta final.”

**Passagem:** “William fecha com a conclusão.”

---

### 9:20–10:00 — William — Conclusão da Parte 2

**Slide 30 — Conclusão.**

> “O ganho é real, mas é condicional. Ele é grande no pior caso, com `n`
> grande, entradas sintéticas e memória disponível. Ele encolhe quando a
> duplicata aparece cedo, quando todas as palavras são anagramas, quando `k` é
> pequeno ou quando a memória é o recurso escasso. A otimização muda a ordem de
> crescimento, mas não elimina o custo residual nem o custo de espaço. A lição
> prática é: **meça o cenário real**, **entenda o contrato dos dados** e **trate o ganho como uma razão — não como um número mágico**.”

**Frase de fechamento:**

> “Não perguntamos apenas ‘é mais rápido?’. Perguntamos ‘mais rápido para quê,
> em qual entrada, com qual memória e com qual garantia?’. É essa pergunta que
> separa uma otimização de um benchmark bonito.”

---

## Perguntas difíceis e respostas curtas

- **“Então a versão otimizada é pior no melhor caso?”** No cenário de
  duplicata imediata, o ganho cai para ~1,5× e pode empatar ou inverter por
  constantes; ela não é assintoticamente pior. O custo é o espaço O(n).
- **“Por que não usar contagem de letras sempre?”** Porque em k=8 a contagem
  foi ~1,5× mais lenta que `sorted`. O ganho assintótico não aparece no regime
  pequeno.
- **“O `set` não é O(1)?”** É O(1) esperado/amortizado. O pior caso teórico é
  O(n) por operação, e entradas adversariais podem se aproximar disso.
- **“Os testes provam que está correto?”** Provam nos casos testados. NaN,
  objetos com `__eq__`/`__hash__` inconsistentes e tipos mutáveis exigem
  decisão explícita de contrato.
- **“Qual é a maior limitação do trabalho?”** O benchmark cobre só o pior caso
  sintético, em uma máquina e uma semente; não mede memória nem distribuição
  real.
- **“Como saber o ganho no meu caso?”** Rode o benchmark com a distribuição
  real; varie a posição da duplicata, o número de grupos e o comprimento das
  palavras; meça memória e use profiler.
- **“Por que o ganho de anagramas é menor que o de duplicatas?”** Porque o
  custo O(k log k) da chave continua; em duplicatas, a operação de hash é O(1)
  esperado e o termo quadrático desaparece por completo.

## Tabela de números — execução exploratória

Medições de `python3 -m src.limites` (Python 3.14.8, mesma máquina do
benchmark). São **exploratórias**: não substituem os resultados versionados do
benchmark oficial.

| Cenário | Original | Otimizada | Ganho |
|---|---:|---:|---:|
| Duplicata no início, n=4.000 | 0,63 µs | 0,46 µs | 1,4× |
| Duplicata no fim, n=4.000 | 781,44 ms | 429,15 µs | 1.820,9× |
| Anagramas distintos, n=400 | 1,094 s | 3,43 ms | 318,6× |
| Anagramas no mesmo grupo, n=400 | 4,82 ms | 2,44 ms | 2,0× |
| Memória: duplicatas, n=4.000 | 0,1 KiB | 160,2 KiB | — |
| Memória: anagramas, n=400 | 24,5 KiB | 52,0 KiB | — |
| Chave ordenada × contagem, k=8 | 1,29 ms | 1,91 ms | 0,7× |
| Chave ordenada × contagem, k=512 | 147,73 ms | 80,87 ms | 1,8× |

Na última seção, “ganho” é `tempo da chave ordenada / tempo da chave por
contagem`; valores menores que 1 indicam que a contagem foi mais lenta.

## Cola de fórmulas

- Duplicatas original: `T_o(n) ≈ c_o · n²/2` → **O(n²)**.
- Duplicatas com `set`: `T_h(n) ≈ c_h · n + c_s` → **O(n) esperado**.
- Ganho em duplicatas: `S(n) ≈ (c_o / 2c_h) · n` → cresce com `n`.
- Anagramas original: `T_o(n) ≈ c_o · n²/2 · k log k` → **O(n²·k log k)**.
- Anagramas com `dict`: `T_h(n) ≈ c_h · n · k log k` → **O(n·k log k)**.
- Anagramas com contagem: `T_c(n) ≈ c_c · n · k` → **O(n·k)**, mas com
  constante maior; só compensa para `k` grande.
