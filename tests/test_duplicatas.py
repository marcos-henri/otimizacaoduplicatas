"""Testes da detecção de duplicatas."""

from __future__ import annotations

import random

import pytest

from src.duplicatas import tem_duplicata, tem_duplicata_hash


@pytest.mark.parametrize(
    ("lista", "esperado"),
    [
        ([], False),
        ([1], False),
        ([1, 2, 3, 4], False),
        ([1, 2, 3, 1], True),
        ([1, 1, 2, 3], True),
        ([1, 2, 3, 3], True),
        (["a", "b", "c", "a"], True),
        ([None, None], True),
        ([0, -1, 2, -1], True),
    ],
)
def test_casos_fixos(lista: list[object], esperado: bool) -> None:
    assert tem_duplicata(lista) is esperado
    assert tem_duplicata_hash(lista) is esperado


def test_versoes_concordam_em_listas_aleatorias() -> None:
    rng = random.Random(123)
    for _ in range(200):
        n = rng.randint(0, 40)
        lista = [rng.randint(0, 12) for _ in range(n)]
        assert tem_duplicata(lista) == tem_duplicata_hash(lista)


def test_lista_grande_sem_duplicatas() -> None:
    # A versão original seria O(n²); aqui validamos apenas a versão O(n).
    lista = list(range(10_000))
    assert tem_duplicata_hash(lista) is False


def test_nao_altera_a_entrada() -> None:
    lista = [3, 1, 2, 1]
    copia = lista.copy()
    assert tem_duplicata_hash(lista) is True
    assert lista == copia
