"""Experimentos exploratórios sobre os limites do ganho das otimizações.

Este módulo **não substitui** o benchmark oficial de ``src.benchmark``. Ele
mede cenários que o benchmark de pior caso não cobre e que são usados na
Parte 2 da apresentação:

- duplicata no início versus no fim da lista;
- anagramas com grupos distintos versus todas as palavras iguais;
- memória adicional com ``tracemalloc``;
- chave por ordenação O(k log k) versus chave por contagem O(k);
- uma diferença de semântica entre a versão original e a versão com ``set``.

Uso:
    python3 -m src.limites
    python3 -m src.limites --rapido

Os tempos são medianos, após aquecimento, e variam conforme a máquina. O que
importa aqui é a **comparação relativa** entre cenários.
"""

from __future__ import annotations

import argparse
import platform
import random
import statistics
import string
import time
import tracemalloc
from collections.abc import Callable, Sequence
from typing import Any

from .anagramas import agrupar_anagramas_hash, agrupar_anagramas_original
from .duplicatas import tem_duplicata, tem_duplicata_hash


def medir(
    funcao: Callable[..., Any],
    *args: Any,
    repeticoes: int = 5,
    numero: int = 1,
) -> float:
    """Retorna o tempo mediano de ``funcao(*args)`` em segundos."""
    funcao(*args)  # aquecimento
    tempos: list[float] = []
    for _ in range(repeticoes):
        inicio = time.perf_counter()
        for _ in range(numero):
            funcao(*args)
        tempos.append((time.perf_counter() - inicio) / numero)
    return statistics.median(tempos)


def _formatar_tempo(segundos: float) -> str:
    if segundos < 1e-3:
        return f"{segundos * 1e6:.2f} µs".replace(".", ",")
    if segundos < 1:
        return f"{segundos * 1e3:.2f} ms".replace(".", ",")
    return f"{segundos:.3f} s".replace(".", ",")


def _ganho(original: float, otimizada: float) -> str:
    if otimizada <= 0:
        return "—"
    return f"{original / otimizada:.1f}x".replace(".", ",")


def experimento_duplicatas_cedo_tarde(
    n: int = 4_000,
    repeticoes: int = 3,
) -> list[tuple[str, float, float]]:
    """Compara o melhor caso (duplicata no início) com o pior (no fim)."""
    cedo = [1, 1] + list(range(2, n))
    tarde = list(range(n - 2)) + [n - 3, n - 3]

    resultados = []
    for rotulo, lista in [("duplicata no início", cedo), ("duplicata no fim", tarde)]:
        # No caso "cedo" a função retorna em microssegundos; repetir a chamada
        # dentro de cada medição reduz o ruído do relógio.
        numero = 100 if rotulo == "duplicata no início" else 1
        original = medir(
            tem_duplicata, lista, repeticoes=repeticoes, numero=numero
        )
        otimizada = medir(
            tem_duplicata_hash, lista, repeticoes=repeticoes, numero=numero
        )
        resultados.append((rotulo, original, otimizada))
    return resultados


def experimento_anagramas_grupos(
    n: int = 400,
    repeticoes: int = 2,
    semente: int = 42,
) -> list[tuple[str, float, float]]:
    """Compara muitos grupos distintos com um único grupo de anagramas."""
    rng = random.Random(semente)
    distintas = [
        "".join(rng.choices(string.ascii_lowercase, k=8)) for _ in range(n)
    ]
    iguais = ["abcdefgh"] * n

    resultados = []
    for rotulo, palavras in [
        ("todas em grupos distintos", distintas),
        ("todas no mesmo grupo", iguais),
    ]:
        original = medir(
            agrupar_anagramas_original, palavras, repeticoes=repeticoes
        )
        otimizada = medir(agrupar_anagramas_hash, palavras, repeticoes=repeticoes)
        resultados.append((rotulo, original, otimizada))
    return resultados


def experimento_memoria(
    n_duplicatas: int = 4_000,
    n_anagramas: int = 400,
    semente: int = 42,
) -> list[tuple[str, float, float]]:
    """Mede o pico de memória adicional com ``tracemalloc`` (em KiB)."""
    resultados: list[tuple[str, float, float]] = []

    lista = list(range(n_duplicatas))
    tracemalloc.start()
    tem_duplicata(lista)
    pico_original = tracemalloc.get_traced_memory()[1]
    tracemalloc.stop()

    tracemalloc.start()
    tem_duplicata_hash(lista)
    pico_otimizada = tracemalloc.get_traced_memory()[1]
    tracemalloc.stop()
    resultados.append(("duplicatas", pico_original / 1024, pico_otimizada / 1024))

    rng = random.Random(semente)
    palavras = [
        "".join(rng.choices(string.ascii_lowercase, k=8)) for _ in range(n_anagramas)
    ]
    tracemalloc.start()
    agrupar_anagramas_original(palavras)
    pico_original = tracemalloc.get_traced_memory()[1]
    tracemalloc.stop()

    tracemalloc.start()
    agrupar_anagramas_hash(palavras)
    pico_otimizada = tracemalloc.get_traced_memory()[1]
    tracemalloc.stop()
    resultados.append(("anagramas", pico_original / 1024, pico_otimizada / 1024))

    return resultados


def _chave_ordenada(palavra: str) -> tuple[str, ...]:
    return tuple(sorted(palavra))


def _chave_contagem(palavra: str) -> tuple[int, ...]:
    """Chave O(k) para palavras minúsculas sem acento (a-z)."""
    contagem = [0] * 26
    for caractere in palavra:
        contagem[ord(caractere) - ord("a")] += 1
    return tuple(contagem)


def experimento_chave(
    palavras_por_tamanho: int = 1_000,
    repeticoes: int = 3,
    semente: int = 42,
) -> list[tuple[int, float, float]]:
    """Compara a chave por ordenação com a chave por contagem para vários k."""
    rng = random.Random(semente)
    resultados = []
    for k in (8, 32, 128, 512):
        palavras = [
            "".join(rng.choices(string.ascii_lowercase, k=k))
            for _ in range(palavras_por_tamanho)
        ]
        ordenada = medir(
            lambda lista: [_chave_ordenada(p) for p in lista],
            palavras,
            repeticoes=repeticoes,
        )
        contagem = medir(
            lambda lista: [_chave_contagem(p) for p in lista],
            palavras,
            repeticoes=repeticoes,
        )
        resultados.append((k, ordenada, contagem))
    return resultados


def experimento_semantica() -> list[tuple[str, str, str]]:
    """Mostra casos em que a versão com ``set`` não é equivalente à original."""
    nan = float("nan")
    casos = [
        (
            "[nan, nan] (mesmo objeto)",
            str(tem_duplicata([nan, nan])),
            str(tem_duplicata_hash([nan, nan])),
        ),
        (
            "[nan, nan] (objetos distintos)",
            str(tem_duplicata([float("nan"), float("nan")])),
            str(tem_duplicata_hash([float("nan"), float("nan")])),
        ),
    ]
    try:
        resultado = str(tem_duplicata_hash([[1], [1]]))
    except TypeError as erro:
        resultado = f"TypeError: {erro}"
    casos.append(("[[1], [1]] (não hashable)", str(tem_duplicata([[1], [1]])), resultado))
    return casos


def _imprimir_tabela(
    titulo: str,
    cabecalho: tuple[str, ...],
    linhas: Sequence[tuple[str, ...]],
) -> None:
    print()
    print(titulo)
    print(" | ".join(cabecalho))
    print("-+-".join("-" * len(coluna) for coluna in cabecalho))
    for linha in linhas:
        print(" | ".join(linha))


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Experimentos exploratórios sobre os limites do ganho."
    )
    parser.add_argument(
        "--rapido",
        action="store_true",
        help="usa tamanhos e repetições menores",
    )
    args = parser.parse_args(argv)

    if args.rapido:
        n_dup, rep_dup = 2_000, 2
        n_ana, rep_ana = 200, 1
        n_mem_dup, n_mem_ana = 2_000, 200
        palavras_por_tamanho, rep_chave = 400, 2
    else:
        n_dup, rep_dup = 4_000, 3
        n_ana, rep_ana = 400, 2
        n_mem_dup, n_mem_ana = 4_000, 400
        palavras_por_tamanho, rep_chave = 1_000, 3

    print("Experimentos de limites — resultados exploratórios")
    print(f"Python {platform.python_version()}")

    linhas = [
        (
            rotulo,
            _formatar_tempo(original),
            _formatar_tempo(otimizada),
            _ganho(original, otimizada),
        )
        for rotulo, original, otimizada in experimento_duplicatas_cedo_tarde(
            n_dup, rep_dup
        )
    ]
    _imprimir_tabela(
        f"Duplicatas, n={n_dup}",
        ("cenário", "original", "com set", "ganho"),
        linhas,
    )

    linhas = [
        (
            rotulo,
            _formatar_tempo(original),
            _formatar_tempo(otimizada),
            _ganho(original, otimizada),
        )
        for rotulo, original, otimizada in experimento_anagramas_grupos(
            n_ana, rep_ana
        )
    ]
    _imprimir_tabela(
        f"Anagramas, n={n_ana}",
        ("cenário", "original", "com dict", "ganho"),
        linhas,
    )

    linhas = [
        (rotulo, f"{original:.1f} KiB", f"{otimizada:.1f} KiB")
        for rotulo, original, otimizada in experimento_memoria(n_mem_dup, n_mem_ana)
    ]
    _imprimir_tabela(
        "Pico de memória adicional (tracemalloc)",
        ("cenário", "original", "otimizada"),
        linhas,
    )

    linhas = [
        (f"k={k}", _formatar_tempo(ordenada), _formatar_tempo(contagem), _ganho(ordenada, contagem))
        for k, ordenada, contagem in experimento_chave(
            palavras_por_tamanho, rep_chave
        )
    ]
    _imprimir_tabela(
        f"Chave de anagrama ({palavras_por_tamanho} palavras)",
        ("comprimento", "sorted O(k log k)", "contagem O(k)", "sorted/contagem"),
        linhas,
    )

    linhas = [
        (caso, original, otimizada)
        for caso, original, otimizada in experimento_semantica()
    ]
    _imprimir_tabela(
        "Semântica: onde as versões divergem",
        ("caso", "original", "com set"),
        linhas,
    )

    print()
    print("Observação: 'ganho' é a razão entre a primeira e a segunda coluna")
    print("de tempo; valores < 1 indicam que a primeira coluna foi mais rápida.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
