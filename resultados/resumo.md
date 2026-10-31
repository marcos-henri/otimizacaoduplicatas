# Resumo dos benchmarks

Tempos medianos obtidos com `time.perf_counter`, após aquecimento.
O ganho é a razão entre o tempo da versão original e o da versão
otimizada. Entradas de duplicatas não contêm duplicatas (pior caso
para a versão original).

**Ambiente:** Python 3.14.8 — Linux-7.2.11-arch1-1-x86_64-with-glibc2.44

### Detecção de duplicatas

| n | Original | Otimizada | Ganho |
|---:|---:|---:|---:|
| 500 | 12,63 ms | 92,0 µs | 137,2x |
| 1.000 | 54,75 ms | 191,7 µs | 285,7x |
| 2.000 | 194,06 ms | 214,7 µs | 903,9x |
| 4.000 | 757,99 ms | 430,2 µs | 1.762,1x |
| 8.000 | 2,955 s | 960,1 µs | 3.077,8x |
| 16.000 | 13,132 s | 2,10 ms | 6.240,9x |

### Agrupamento de anagramas

| n | Original | Otimizada | Ganho |
|---:|---:|---:|---:|
| 100 | 62,38 ms | 680,6 µs | 91,7x |
| 200 | 246,86 ms | 1,32 ms | 186,6x |
| 400 | 1,014 s | 2,68 ms | 378,2x |
| 800 | 4,394 s | 6,08 ms | 722,8x |
| 1.600 | 17,286 s | 12,53 ms | 1.379,1x |

> Os tempos absolutos variam conforme a máquina e a versão do Python.
> O que importa é a tendência de crescimento e a ordem de grandeza.
