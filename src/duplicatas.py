"""Detecção de elementos duplicados em uma sequência.

Este módulo mantém, lado a lado, a versão original fornecida no enunciado
(O(n²)) e a primeira versão otimizada com estrutura de hash (O(n) esperado).
"""

from __future__ import annotations

from collections.abc import Hashable, Sequence


def tem_duplicata(lista: Sequence[Hashable]) -> bool:
    """Versão original: compara todos os pares possíveis.

    Complexidade de tempo: O(n²) no pior caso e no caso médio, pois no pior
    caso (sem duplicatas) são feitas n * (n - 1) / 2 comparações.
    Complexidade de espaço: O(1) adicional.

    Retorna ``True`` assim que encontra dois elementos iguais e ``False``
    caso contrário.
    """
    for i in range(len(lista)):
        for j in range(i + 1, len(lista)):
            if lista[i] == lista[j]:
                return True
    return False


def tem_duplicata_hash(lista: Sequence[Hashable]) -> bool:
    """Versão otimizada: usa um conjunto para lembrar o que já foi visto.

    Complexidade de tempo: O(n) esperado, porque cada consulta e inserção em
    ``set`` custa O(1) amortizado. No pior caso teórico, com muitas colisões
    de hash, pode degradar, mas isso não ocorre para os tipos usuais.
    Complexidade de espaço: O(n) no pior caso (todos os elementos distintos).

    Os elementos precisam ser *hashable* (int, str, tuple etc.). Para listas
    de listas, a versão original ainda funciona, mas esta versão levanta
    ``TypeError``; nesse caso seria necessário converter cada item em uma
    representação hashable.
    """
    vistos: set[Hashable] = set()
    for item in lista:
        if item in vistos:
            return True
        vistos.add(item)
    return False
