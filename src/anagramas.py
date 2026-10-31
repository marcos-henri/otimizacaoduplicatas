"""Agrupamento de anagramas com normalização de chaves.

A versão original compara cada palavra com o representante de cada grupo já
formado, refazendo a normalização e a ordenação das letras a cada comparação.
A versão otimizada calcula uma única chave normalizada por palavra e usa um
dicionário para agrupar palavras que produzem a mesma chave.
"""

from __future__ import annotations

import unicodedata
from collections.abc import Iterable


def normalizar_palavra(palavra: str, ignorar_acentos: bool = True) -> str:
    """Normaliza uma palavra para servir de base à chave de anagrama.

    A normalização aplica ``casefold`` (equivalente a minúsculas para a
    maioria dos alfabetos), remove acentos quando ``ignorar_acentos=True`` e
    descarta caracteres que não sejam letras ou dígitos (espaços, pontuação
    etc.). Assim, ``"Ação!"`` e ``"acao"`` produzem a mesma base.
    """
    texto = palavra.casefold()
    if ignorar_acentos:
        texto = "".join(
            caractere
            for caractere in unicodedata.normalize("NFD", texto)
            if unicodedata.category(caractere) != "Mn"
        )
    return "".join(caractere for caractere in texto if caractere.isalnum())


def chave_anagrama(palavra: str, ignorar_acentos: bool = True) -> tuple[str, ...]:
    """Retorna a chave normalizada de uma palavra.

    Duas palavras são anagramas se, e somente se, suas chaves são iguais.
    A chave é uma tupla ordenada de caracteres, que é hashable e pode ser
    usada diretamente como chave de dicionário.
    """
    return tuple(sorted(normalizar_palavra(palavra, ignorar_acentos)))


def sao_anagramas(a: str, b: str, ignorar_acentos: bool = True) -> bool:
    """Verifica se duas palavras são anagramas após a normalização."""
    return chave_anagrama(a, ignorar_acentos) == chave_anagrama(b, ignorar_acentos)


def agrupar_anagramas_original(
    palavras: Iterable[str],
    ignorar_acentos: bool = True,
) -> list[list[str]]:
    """Versão original: compara cada palavra com cada grupo já existente.

    Para cada palavra, percorre todos os grupos e refaz a normalização e a
    ordenação tanto da palavra quanto do representante do grupo. No pior caso
    (todas as palavras em grupos distintos), o custo é O(n² · k log k), onde
    ``k`` é o comprimento típico das palavras.
    """
    grupos: list[list[str]] = []

    for palavra in palavras:
        for grupo in grupos:
            chave_palavra = tuple(
                sorted(normalizar_palavra(palavra, ignorar_acentos))
            )
            chave_grupo = tuple(
                sorted(normalizar_palavra(grupo[0], ignorar_acentos))
            )
            if chave_palavra == chave_grupo:
                grupo.append(palavra)
                break
        else:
            grupos.append([palavra])

    return grupos


def agrupar_anagramas_hash(
    palavras: Iterable[str],
    ignorar_acentos: bool = True,
) -> list[list[str]]:
    """Versão otimizada: calcula a chave uma vez e usa um dicionário.

    O custo dominante é a ordenação das letras de cada palavra: O(n · k log k)
    no total. Como ``k`` (comprimento da palavra) costuma ser pequeno e fixo
    nos problemas práticos, o comportamento observado é linear em ``n``.
    O espaço adicional é O(n · k) para armazenar as chaves e os grupos.
    """
    grupos: dict[tuple[str, ...], list[str]] = {}

    for palavra in palavras:
        chave = chave_anagrama(palavra, ignorar_acentos)
        grupos.setdefault(chave, []).append(palavra)

    return list(grupos.values())
