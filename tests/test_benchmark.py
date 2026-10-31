"""Testes auxiliares do gerador de entradas e do medidor de tempo."""

from __future__ import annotations

from pathlib import Path

import pytest

from src.benchmark import (
    DIR_RESULTADOS,
    DIR_SAIDA_PADRAO,
    gerar_lista_sem_duplicatas,
    gerar_palavras,
    medir_tempo,
    resolver_diretorio_saida,
)


def test_lista_gerada_nao_tem_duplicatas() -> None:
    lista = gerar_lista_sem_duplicatas(1_000)
    assert len(lista) == 1_000
    assert len(set(lista)) == 1_000
    assert set(lista) == set(range(1_000))


def test_lista_gerada_e_reprodutivel() -> None:
    assert gerar_lista_sem_duplicatas(50, semente=7) == gerar_lista_sem_duplicatas(
        50, semente=7
    )


def test_palavras_geradas_tem_o_comprimento_pedido() -> None:
    palavras = gerar_palavras(20, comprimento=6)
    assert len(palavras) == 20
    assert all(len(palavra) == 6 for palavra in palavras)
    assert all(palavra.islower() for palavra in palavras)


def test_medir_tempo_retorna_valores_positivos() -> None:
    resultado = medir_tempo(sum, range(100), repeticoes=3, numero=2)
    assert resultado["tempo_mediano_s"] > 0
    assert resultado["tempo_minimo_s"] > 0
    assert resultado["tempo_medio_s"] > 0
    assert resultado["desvio_padrao_s"] >= 0


def test_saida_padrao_nao_sobrescreve_resultados_versionados() -> None:
    assert resolver_diretorio_saida() == DIR_SAIDA_PADRAO
    assert DIR_SAIDA_PADRAO != DIR_RESULTADOS
    assert DIR_RESULTADOS in DIR_SAIDA_PADRAO.parents


def test_publicar_grava_nos_resultados_versionados() -> None:
    assert resolver_diretorio_saida(publicar=True) == DIR_RESULTADOS


def test_saida_customizada_e_resolvida(tmp_path: Path) -> None:
    assert resolver_diretorio_saida(tmp_path) == tmp_path.resolve()


def test_publicar_e_saida_sao_exclusivos(tmp_path: Path) -> None:
    with pytest.raises(ValueError):
        resolver_diretorio_saida(tmp_path, publicar=True)
