# Resultados dos benchmarks

Esta pasta é gerada por `python3 -m src.benchmark`.

| Arquivo | Conteúdo |
|---|---|
| `benchmark_duplicatas.csv` | Medições de `tem_duplicata` e `tem_duplicata_hash` |
| `benchmark_anagramas.csv` | Medições de `agrupar_anagramas_original` e `agrupar_anagramas_hash` |
| `resumo.md` | Tabelas com tempos medianos e ganho relativo |
| `grafico_duplicatas.png` | Gráfico em escala linear e log-log |
| `grafico_anagramas.png` | Gráfico em escala linear e log-log |

## Como interpretar

- `tempo_mediano_s` é a mediana das repetições e é o valor usado nas tabelas.
- `tempo_minimo_s` é a menor medição; ajuda a ver o melhor caso observado.
- `repeticoes` e `numero_por_medicao` documentam como o tempo foi obtido.
- O ganho é calculado como `tempo_original / tempo_otimizada`.

Os tempos absolutos variam com a máquina, a carga do sistema e a versão do
Python. Para comparar execuções, use a mesma máquina e evite outros processos
pesados rodando ao mesmo tempo.

## Reprodução

```bash
python3 -m src.benchmark
```

Para uma execução rápida:

```bash
python3 -m src.benchmark --rapido
```
