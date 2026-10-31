"""Benchmarks reprodutíveis para as versões original e otimizada.

Uso:
    python -m src.benchmark                  # execução completa
    python -m src.benchmark --rapido         # execução curta, útil para testar
    python -m src.benchmark --sem-grafico
    python -m src.benchmark --publicar       # atualiza os resultados versionados

Por padrão os resultados (CSV, resumo em Markdown e gráficos PNG) são
gravados em ``resultados/local/``, que é ignorado pelo git. Assim, rodar o
benchmark não modifica os resultados de referência versionados em
``resultados/``. Use ``--publicar`` (ou ``--saida``) quando quiser
deliberadamente substituí-los.
"""

from __future__ import annotations

import argparse
import csv
import platform
import random
import statistics
import string
import time
from collections.abc import Callable, Sequence
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from .anagramas import agrupar_anagramas_hash, agrupar_anagramas_original
from .duplicatas import tem_duplicata, tem_duplicata_hash

RAIZ_PROJETO = Path(__file__).resolve().parent.parent
DIR_RESULTADOS = RAIZ_PROJETO / "resultados"
DIR_SAIDA_PADRAO = DIR_RESULTADOS / "local"


def resolver_diretorio_saida(
    saida: Path | None = None,
    publicar: bool = False,
) -> Path:
    """Decide onde os artefatos do benchmark serão gravados.

    O padrão é ``resultados/local/``, ignorado pelo git, para que uma execução
    comum não altere os resultados de referência versionados em
    ``resultados/``. Use ``publicar=True`` (ou ``--saida``) para sobrescrever
    esses arquivos de forma explícita.
    """
    if publicar:
        if saida is not None:
            raise ValueError("use --publicar ou --saida, não os dois")
        return DIR_RESULTADOS
    if saida is not None:
        return Path(saida).expanduser().resolve()
    return DIR_SAIDA_PADRAO


@dataclass(frozen=True)
class Medicao:
    """Uma medição de tempo para um par (cenário, algoritmo, tamanho)."""

    cenario: str
    algoritmo: str
    versao: str
    n: int
    tempo_mediano_s: float
    tempo_minimo_s: float
    tempo_medio_s: float
    desvio_padrao_s: float
    repeticoes: int
    numero_por_medicao: int


def medir_tempo(
    funcao: Callable[..., Any],
    *args: Any,
    repeticoes: int = 5,
    numero: int = 1,
) -> dict[str, float]:
    """Mede o tempo de ``funcao(*args)`` com aquecimento e repetições.

    Cada repetição executa a função ``numero`` vezes e divide o tempo total
    por ``numero``. Isso reduz o ruído para funções muito rápidas. O valor
    reportado nos relatórios é a mediana das repetições.
    """
    funcao(*args)  # aquecimento: aquece caches e o interpretador

    tempos: list[float] = []
    for _ in range(repeticoes):
        inicio = time.perf_counter()
        for _ in range(numero):
            funcao(*args)
        fim = time.perf_counter()
        tempos.append((fim - inicio) / numero)

    return {
        "tempo_mediano_s": statistics.median(tempos),
        "tempo_minimo_s": min(tempos),
        "tempo_medio_s": statistics.fmean(tempos),
        "desvio_padrao_s": statistics.pstdev(tempos),
    }


def _medir(
    cenario: str,
    algoritmo: str,
    versao: str,
    n: int,
    funcao: Callable[..., Any],
    *args: Any,
    repeticoes: int,
    numero: int,
) -> Medicao:
    tempos = medir_tempo(funcao, *args, repeticoes=repeticoes, numero=numero)
    return Medicao(
        cenario=cenario,
        algoritmo=algoritmo,
        versao=versao,
        n=n,
        repeticoes=repeticoes,
        numero_por_medicao=numero,
        **tempos,
    )


def gerar_lista_sem_duplicatas(n: int, semente: int = 42) -> list[int]:
    """Gera uma lista com ``n`` inteiros distintos em ordem aleatória.

    Esse é o pior caso para a versão original, pois ela precisa comparar
    todos os pares antes de concluir que não há duplicatas.
    """
    rng = random.Random(semente)
    lista = list(range(n))
    rng.shuffle(lista)
    return lista


def gerar_palavras(n: int, comprimento: int = 8, semente: int = 42) -> list[str]:
    """Gera ``n`` palavras aleatórias de letras minúsculas.

    Com alfabeto de 26 letras e comprimento 8, a chance de duas palavras
    caírem no mesmo grupo de anagramas é desprezível; assim, a versão
    original tende ao pior caso (um grupo novo por palavra).
    """
    rng = random.Random(semente)
    return [
        "".join(rng.choices(string.ascii_lowercase, k=comprimento))
        for _ in range(n)
    ]


def benchmark_duplicatas(
    tamanhos: Sequence[int],
    semente: int = 42,
    rapido: bool = False,
) -> list[Medicao]:
    """Executa o benchmark de detecção de duplicatas."""
    repeticoes_original = 2 if rapido else 3
    repeticoes_hash = 5 if rapido else 7
    numero_hash = 5 if rapido else 10

    medicoes: list[Medicao] = []
    for n in tamanhos:
        lista = gerar_lista_sem_duplicatas(n, semente)
        medicoes.append(
            _medir(
                "duplicatas",
                "tem_duplicata",
                "original",
                n,
                tem_duplicata,
                lista,
                repeticoes=repeticoes_original,
                numero=1,
            )
        )
        medicoes.append(
            _medir(
                "duplicatas",
                "tem_duplicata_hash",
                "otimizada",
                n,
                tem_duplicata_hash,
                lista,
                repeticoes=repeticoes_hash,
                numero=numero_hash,
            )
        )
    return medicoes


def benchmark_anagramas(
    tamanhos: Sequence[int],
    semente: int = 42,
    rapido: bool = False,
) -> list[Medicao]:
    """Executa o benchmark de agrupamento de anagramas."""
    repeticoes_original = 2 if rapido else 3
    repeticoes_hash = 5 if rapido else 7
    numero_hash = 3 if rapido else 5

    medicoes: list[Medicao] = []
    for n in tamanhos:
        palavras = gerar_palavras(n, semente=semente)
        medicoes.append(
            _medir(
                "anagramas",
                "agrupar_anagramas_original",
                "original",
                n,
                agrupar_anagramas_original,
                palavras,
                repeticoes=repeticoes_original,
                numero=1,
            )
        )
        medicoes.append(
            _medir(
                "anagramas",
                "agrupar_anagramas_hash",
                "otimizada",
                n,
                agrupar_anagramas_hash,
                palavras,
                repeticoes=repeticoes_hash,
                numero=numero_hash,
            )
        )
    return medicoes


def salvar_csv(medicoes: Sequence[Medicao], caminho: Path) -> None:
    """Grava as medições em CSV."""
    caminho.parent.mkdir(parents=True, exist_ok=True)
    campos = list(asdict(medicoes[0]).keys())
    with caminho.open("w", newline="", encoding="utf-8") as arquivo:
        escritor = csv.DictWriter(arquivo, fieldnames=campos)
        escritor.writeheader()
        for medicao in medicoes:
            escritor.writerow(asdict(medicao))


def _formatar_tempo(segundos: float) -> str:
    if segundos < 1e-3:
        return f"{segundos * 1e6:.1f} µs".replace(".", ",")
    if segundos < 1:
        return f"{segundos * 1e3:.2f} ms".replace(".", ",")
    return f"{segundos:.3f} s".replace(".", ",")


def _formatar_inteiro(valor: int) -> str:
    return f"{valor:,}".replace(",", ".")


def _formatar_ganho(original: float, otimizada: float) -> str:
    if otimizada <= 0:
        return "—"
    ganho = original / otimizada
    texto = f"{ganho:,.1f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return f"{texto}x"


def _tabela_markdown(medicoes: Sequence[Medicao], titulo: str) -> str:
    por_n: dict[int, dict[str, Medicao]] = {}
    for medicao in medicoes:
        por_n.setdefault(medicao.n, {})[medicao.versao] = medicao

    linhas = [
        f"### {titulo}",
        "",
        "| n | Original | Otimizada | Ganho |",
        "|---:|---:|---:|---:|",
    ]
    for n in sorted(por_n):
        original = por_n[n]["original"].tempo_mediano_s
        otimizada = por_n[n]["otimizada"].tempo_mediano_s
        linhas.append(
            f"| {_formatar_inteiro(n)} "
            f"| {_formatar_tempo(original)} "
            f"| {_formatar_tempo(otimizada)} "
            f"| {_formatar_ganho(original, otimizada)} |"
        )
    return "\n".join(linhas)


def gerar_resumo(
    medicoes_duplicatas: Sequence[Medicao],
    medicoes_anagramas: Sequence[Medicao],
    caminho: Path,
) -> str:
    """Gera um resumo em Markdown e o grava em disco."""
    texto = "\n".join(
        [
            "# Resumo dos benchmarks",
            "",
            "Tempos medianos obtidos com `time.perf_counter`, após aquecimento.",
            "O ganho é a razão entre o tempo da versão original e o da versão",
            "otimizada. Entradas de duplicatas não contêm duplicatas (pior caso",
            "para a versão original).",
            "",
            f"**Ambiente:** Python {platform.python_version()} — "
            f"{platform.platform()}",
            "",
            _tabela_markdown(medicoes_duplicatas, "Detecção de duplicatas"),
            "",
            _tabela_markdown(medicoes_anagramas, "Agrupamento de anagramas"),
            "",
            "> Os tempos absolutos variam conforme a máquina e a versão do Python.",
            "> O que importa é a tendência de crescimento e a ordem de grandeza.",
            "",
        ]
    )
    caminho.write_text(texto, encoding="utf-8")
    return texto


def _dados_por_versao(
    medicoes: Sequence[Medicao],
    versao: str,
) -> tuple[list[int], list[float]]:
    itens = sorted(
        (medicao.n, medicao.tempo_mediano_s)
        for medicao in medicoes
        if medicao.versao == versao
    )
    return [n for n, _ in itens], [tempo for _, tempo in itens]


def gerar_graficos(
    medicoes_duplicatas: Sequence[Medicao],
    medicoes_anagramas: Sequence[Medicao],
    dir_saida: Path = DIR_SAIDA_PADRAO,
) -> None:
    """Gera gráficos comparativos em escala linear e log-log."""
    try:
        import matplotlib

        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        print("matplotlib não instalado: gráficos não foram gerados.")
        return

    def desenhar(
        medicoes: Sequence[Medicao],
        titulo: str,
        arquivo: Path,
        rotulo_original: str,
        rotulo_otimizada: str,
    ) -> None:
        ns_original, tempos_original = _dados_por_versao(medicoes, "original")
        ns_otimizada, tempos_otimizada = _dados_por_versao(medicoes, "otimizada")

        figura, (eixo_linear, eixo_log) = plt.subplots(
            1, 2, figsize=(11.5, 4.4)
        )

        eixo_linear.plot(
            ns_original,
            tempos_original,
            marker="o",
            linewidth=2,
            label=rotulo_original,
        )
        eixo_linear.plot(
            ns_otimizada,
            tempos_otimizada,
            marker="s",
            linewidth=2,
            label=rotulo_otimizada,
        )
        eixo_linear.set_title("Escala linear")
        eixo_linear.set_xlabel("Tamanho da entrada (n)")
        eixo_linear.set_ylabel("Tempo mediano (s)")
        eixo_linear.grid(True, alpha=0.3)
        eixo_linear.legend()

        eixo_log.plot(
            ns_original,
            tempos_original,
            marker="o",
            linewidth=2,
            label=rotulo_original,
        )
        eixo_log.plot(
            ns_otimizada,
            tempos_otimizada,
            marker="s",
            linewidth=2,
            label=rotulo_otimizada,
        )

        # Linhas de referência para comparação visual das inclinações.
        if ns_original and tempos_original[0] > 0:
            n0 = ns_original[0]
            t0 = tempos_original[0]
            eixo_log.plot(
                ns_original,
                [t0 * (n / n0) ** 2 for n in ns_original],
                linestyle="--",
                color="gray",
                linewidth=1,
                label="referência O(n²)",
            )
        if ns_otimizada and tempos_otimizada[0] > 0:
            n0 = ns_otimizada[0]
            t0 = tempos_otimizada[0]
            eixo_log.plot(
                ns_otimizada,
                [t0 * (n / n0) for n in ns_otimizada],
                linestyle=":",
                color="gray",
                linewidth=1.2,
                label="referência linear",
            )

        eixo_log.set_xscale("log")
        eixo_log.set_yscale("log")
        eixo_log.set_title("Escala log-log")
        eixo_log.set_xlabel("Tamanho da entrada (n)")
        eixo_log.set_ylabel("Tempo mediano (s)")
        eixo_log.grid(True, which="both", alpha=0.3)
        eixo_log.legend(fontsize=8)

        figura.suptitle(titulo, fontsize=13, fontweight="bold")
        figura.tight_layout(rect=(0, 0, 1, 0.95))
        figura.savefig(arquivo, dpi=150, bbox_inches="tight")
        plt.close(figura)

    desenhar(
        medicoes_duplicatas,
        "Detecção de duplicatas",
        dir_saida / "grafico_duplicatas.png",
        "Original O(n²)",
        "Otimizada com set O(n)",
    )
    desenhar(
        medicoes_anagramas,
        "Agrupamento de anagramas",
        dir_saida / "grafico_anagramas.png",
        "Original O(n² · k log k)",
        "Otimizada com dict O(n · k log k)",
    )


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Executa os benchmarks de duplicatas e anagramas."
    )
    parser.add_argument(
        "--rapido",
        action="store_true",
        help="usa tamanhos menores e menos repetições",
    )
    parser.add_argument(
        "--sem-grafico",
        action="store_true",
        help="não gera os gráficos PNG",
    )
    parser.add_argument(
        "--semente",
        type=int,
        default=42,
        help="semente do gerador aleatório (padrão: 42)",
    )
    parser.add_argument(
        "--saida",
        type=Path,
        default=None,
        metavar="DIR",
        help=(
            "diretório onde os resultados serão gravados "
            f"(padrão: {DIR_SAIDA_PADRAO.relative_to(RAIZ_PROJETO)})"
        ),
    )
    parser.add_argument(
        "--publicar",
        action="store_true",
        help=(
            "grava em resultados/ e sobrescreve os resultados versionados "
            "(use apenas quando quiser atualizar a referência do repositório)"
        ),
    )
    args = parser.parse_args(argv)

    if args.publicar and args.saida is not None:
        parser.error("use --publicar ou --saida, não os dois")

    dir_saida = resolver_diretorio_saida(args.saida, args.publicar)

    if args.rapido:
        tamanhos_duplicatas = [200, 400, 800, 1600]
        tamanhos_anagramas = [50, 100, 200, 400]
    else:
        tamanhos_duplicatas = [500, 1000, 2000, 4000, 8000, 16000]
        tamanhos_anagramas = [100, 200, 400, 800, 1600]

    dir_saida.mkdir(parents=True, exist_ok=True)

    if dir_saida == DIR_RESULTADOS:
        print("Atenção: os resultados de referência em resultados/ serão sobrescritos.")
    print("Gravando resultados em:", dir_saida)
    print()

    print("Executando benchmark de detecção de duplicatas...")
    medicoes_duplicatas = benchmark_duplicatas(
        tamanhos_duplicatas, args.semente, args.rapido
    )
    salvar_csv(
        medicoes_duplicatas,
        dir_saida / "benchmark_duplicatas.csv",
    )

    print("Executando benchmark de agrupamento de anagramas...")
    medicoes_anagramas = benchmark_anagramas(
        tamanhos_anagramas, args.semente, args.rapido
    )
    salvar_csv(
        medicoes_anagramas,
        dir_saida / "benchmark_anagramas.csv",
    )

    resumo = gerar_resumo(
        medicoes_duplicatas,
        medicoes_anagramas,
        dir_saida / "resumo.md",
    )
    print()
    print(resumo)

    if not args.sem_grafico:
        gerar_graficos(medicoes_duplicatas, medicoes_anagramas, dir_saida)
        print("Gráficos salvos em:", dir_saida)

    print("Benchmarks concluídos. Resultados em:", dir_saida)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
