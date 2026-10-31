"""Testes do agrupamento e da verificação de anagramas."""

from __future__ import annotations

import random
import string

import pytest

from src.anagramas import (
    agrupar_anagramas_hash,
    agrupar_anagramas_original,
    chave_anagrama,
    normalizar_palavra,
    sao_anagramas,
)


def particionar(grupos: list[list[str]]) -> set[frozenset[str]]:
    """Converte grupos em uma partição comparável, ignorando a ordem."""
    return {frozenset(grupo) for grupo in grupos}


@pytest.mark.parametrize(
    ("palavra", "esperado"),
    [
        ("Árvore", "arvore"),
        ("Ação!", "acao"),
        ("  Olá, Mundo  ", "olamundo"),
        ("Python3", "python3"),
        ("", ""),
    ],
)
def test_normalizacao(palavra: str, esperado: str) -> None:
    assert normalizar_palavra(palavra) == esperado


def test_normalizacao_pode_preservar_acentos() -> None:
    assert normalizar_palavra("Ação", ignorar_acentos=False) == "ação"


def test_chave_de_anagrama() -> None:
    assert chave_anagrama("amor") == tuple(sorted("amor"))
    assert chave_anagrama("amor") == chave_anagrama("roma")
    assert chave_anagrama("Ação") == chave_anagrama("acao")


@pytest.mark.parametrize(
    ("a", "b", "esperado"),
    [
        ("amor", "roma", True),
        ("Amor", "ROMA", True),
        ("dorme", "morde", True),
        ("ação", "acao", True),
        ("abc", "ab", False),
        ("a", "b", False),
        ("", "", True),
    ],
)
def test_sao_anagramas(a: str, b: str, esperado: bool) -> None:
    assert sao_anagramas(a, b) is esperado


def test_agrupamento_fixo() -> None:
    palavras = ["amor", "roma", "ramo", "mora", "carro", "arco", "orca", "Caro"]
    grupos = agrupar_anagramas_hash(palavras)

    assert particionar(grupos) == {
        frozenset({"amor", "roma", "ramo", "mora"}),
        frozenset({"carro"}),
        frozenset({"arco", "orca", "Caro"}),
    }


def test_agrupamento_preserva_palavras_originais() -> None:
    assert agrupar_anagramas_hash(["Ação", "acao", "cao", "coa"]) == [
        ["Ação", "acao"],
        ["cao", "coa"],
    ]


def test_lista_vazia() -> None:
    assert agrupar_anagramas_original([]) == []
    assert agrupar_anagramas_hash([]) == []


def test_versoes_concordam_em_casos_fixos() -> None:
    casos = [
        [],
        ["a"],
        ["a", "a", "a"],
        ["amor", "roma", "carro", "arco", "orca"],
        ["Ação", "cao", "coa", "AÇÃO"],
    ]
    for palavras in casos:
        assert particionar(agrupar_anagramas_original(palavras)) == particionar(
            agrupar_anagramas_hash(palavras)
        )


def test_versoes_concordam_em_palavras_aleatorias() -> None:
    rng = random.Random(7)
    for _ in range(30):
        quantidade = rng.randint(0, 25)
        palavras = [
            "".join(rng.choices(string.ascii_lowercase, k=rng.randint(0, 6)))
            for _ in range(quantidade)
        ]
        assert particionar(agrupar_anagramas_original(palavras)) == particionar(
            agrupar_anagramas_hash(palavras)
        )
