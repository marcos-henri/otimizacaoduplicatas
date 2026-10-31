# Roteiro de apresentação (5 a 8 minutos)

Os slides estão em [`slides.md`](slides.md) e já contêm notas do apresentador
em comentários HTML. Este roteiro é uma versão compacta para ensaiar.

| Tempo | Slide | Ideia principal |
|---:|---|---|
| 0:00–0:30 | 1. Título | Tema, objetivo e integrantes. |
| 0:30–1:10 | 2. Problema | Duplicatas e anagramas são casos de detecção de equivalência. |
| 1:10–1:55 | 3. Duplicatas original | Dois laços, `n(n-1)/2` comparações, O(n²). |
| 1:55–2:40 | 4. Anagramas original | Busca linear + recálculo da chave, O(n² · k log k). |
| 2:40–3:20 | 5. Metodologia | `time.perf_counter`, aquecimento, repetições, mediana, pior caso. |
| 3:20–4:10 | 6. Duplicatas otimizada | `set` como memória do que já foi visto; O(n) esperado. |
| 4:10–5:00 | 7. Anagramas otimizada | Chave normalizada + `dict`; O(n · k log k). |
| 5:00–5:50 | 8. Resultados duplicatas | Tabela e ganho crescente; 13,13 s → 2,10 ms em n=16.000. |
| 5:50–6:30 | 9. Resultados anagramas | 17,29 s → 12,53 ms em n=1.600. |
| 6:30–7:10 | 10. Gráficos | Inclinação 2 versus 1 na escala log-log. |
| 7:10–7:40 | 11. Conclusão | Ganho comprovado e próximos passos. |

## Frase de fechamento

> “A primeira otimização não apenas deixou o código mais rápido: ela mudou a
> ordem de crescimento. O ganho cresce com o tamanho da entrada, que é
> exatamente o que a análise de complexidade previa.”

## Perguntas prováveis

- **Por que não usar `set(lista)` e comparar tamanhos?** Funciona para
  duplicatas, mas cria uma cópia O(n) e não permite retornar cedo. A versão com
  laço é O(n) e para assim que encontra a primeira duplicata.
- **O `set` não é O(1) no pior caso?** Sim, o pior caso teórico é O(n) por
  operação, mas o custo esperado é O(1) e, na prática, os tipos usados têm hash
  bem distribuído.
- **Por que a versão de anagramas não é O(n) puro?** Porque ainda ordenamos as
  letras de cada palavra, O(k log k). Com `k` fixo, isso é linear em `n`.
- **O que mudaria para O(n · k)?** Usar uma chave de contagem de caracteres em
  vez de ordenar as letras.
