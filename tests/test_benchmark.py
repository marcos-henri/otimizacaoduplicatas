"""Testes auxiliares do gerador de entradas e do medidor de tempo."""

from __future__ import annotations

from src.benchmark import gerar_lista_sem_duplicatas, gerar_palavras, medir_tempo


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
