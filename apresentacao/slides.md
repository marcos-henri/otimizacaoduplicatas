---
marp: true
theme: default
paginate: true
header: 'AV2 — Duplicatas e Anagramas'
footer: 'Análise de Algoritmos — 30/10/2026'
---

# Detecção de duplicatas e anagramas

## Diagnóstico e primeira otimização

**Integrantes:** _preencher com os nomes do grupo_

<!--
Tempo: 30 s.
Apresentar o tema e o objetivo: sair de uma solução O(n²) e comprovar o ganho
com medições, não apenas com argumentos teóricos.
-->

---

## O problema

- **Duplicatas:** existe algum valor repetido em uma sequência?
- **Anagramas:** quais palavras têm as mesmas letras em ordem diferente?

Em ambos os casos, precisamos detectar **equivalência** entre itens.

A solução ingênua compara todos os pares. A solução eficiente transforma cada
item em uma **chave** e usa uma tabela de hash.

<!--
Tempo: 40 s.
Destacar a ideia comum: comparação direta repetida versus chave + hash.
-->

---

## Versão original: duplicatas

```python
def tem_duplicata(lista):
    for i in range(len(lista)):
        for j in range(i + 1, len(lista)):
            if lista[i] == lista[j]:
                return True
    return False
```

- Pior caso: `n(n-1)/2` comparações
- Complexidade: **O(n²)**
- Espaço adicional: O(1)

<!--
Tempo: 45 s.
Mostrar a contagem de comparações. Se não há duplicatas, todos os pares são
comparados. O melhor caso é O(1), mas o pior caso domina para entradas grandes.
-->

---

## Versão original: anagramas

```python
for palavra in palavras:
    for grupo in grupos:
        chave_palavra = tuple(sorted(normalizar(palavra)))
        chave_grupo = tuple(sorted(normalizar(grupo[0])))
        if chave_palavra == chave_grupo:
            grupo.append(palavra)
            break
    else:
        grupos.append([palavra])
```

- Busca linear nos grupos: O(n²) comparações
- Normalização + ordenação refeitas a cada comparação: O(k log k)
- Total: **O(n² · k log k)**

<!--
Tempo: 45 s.
O gargalo é duplo: buscar o grupo e recalcular a chave da mesma palavra várias
vezes. A normalização é necessária, mas pode ser feita uma única vez.
-->

---

## Como medimos

- `time.perf_counter`, após aquecimento
- Várias repetições; reportamos a **mediana**
- Funções rápidas: várias execuções por medição
- Pior caso: listas sem duplicatas e palavras com chaves distintas
- Correção verificada com `pytest`

<!--
Tempo: 40 s.
Explicar que medir uma vez é ruído. A mediana reduz o efeito de picos de carga.
Os testes garantem que a versão otimizada não altera o resultado.
-->

---

## Primeira otimização: duplicatas com `set`

```python
def tem_duplicata_hash(lista):
    vistos = set()
    for item in lista:
        if item in vistos:
            return True
        vistos.add(item)
    return False
```

- Consulta e inserção em `set`: O(1) amortizado esperado
- Tempo: **O(n)**
- Espaço: O(n)
- Trade-off: troca memória por tempo

<!--
Tempo: 50 s.
O conjunto funciona como memória do que já foi visto. Cada elemento entra uma
vez e é consultado uma vez. O custo de espaço é o preço da linearidade.
-->

---

## Primeira otimização: anagramas com chave + `dict`

```python
def chave_anagrama(palavra):
    return tuple(sorted(normalizar_palavra(palavra)))

def agrupar_anagramas_hash(palavras):
    grupos = {}
    for palavra in palavras:
        grupos.setdefault(chave_anagrama(palavra), []).append(palavra)
    return list(grupos.values())
```

- Normalização: `casefold`, sem acentos, apenas letras/dígitos
- Chave calculada **uma vez** por palavra
- Tempo: **O(n · k log k)**; com `k` fixo, linear em `n`

<!--
Tempo: 50 s.
A chave normalizada é o ponto central: "Ação" e "acao" produzem a mesma tupla
ordenada. O dicionário faz a busca do grupo em tempo constante esperado.
-->

---

## Resultados: duplicatas

| n | Original | Otimizada | Ganho |
|---:|---:|---:|---:|
| 500 | 12,63 ms | 92,0 µs | 137,2× |
| 4.000 | 757,99 ms | 430,2 µs | 1.762,1× |
| 16.000 | 13,132 s | 2,10 ms | 6.240,9× |

- Ao dobrar `n`, o original cresce ~4×; a versão com `set` cresce ~2×
- O ganho cresce com o tamanho da entrada

<!--
Tempo: 50 s.
Apontar a última linha: 13 segundos contra 2 milissegundos. Não é só uma
constante melhor; a inclinação da curva mudou.
-->

---

## Resultados: anagramas

| n | Original | Otimizada | Ganho |
|---:|---:|---:|---:|
| 100 | 62,38 ms | 680,6 µs | 91,7× |
| 400 | 1,014 s | 2,68 ms | 378,2× |
| 1.600 | 17,286 s | 12,53 ms | 1.379,1× |

- O original refaz a chave a cada comparação
- A versão com `dict` calcula a chave uma vez e agrupa

<!--
Tempo: 40 s.
Aqui o ganho é menor que em duplicatas porque a normalização e a ordenação
continuam custando O(k log k), mas o fator O(n²) desaparece.
-->

---

## Gráficos: linear e log-log

![w:680](../resultados/grafico_duplicatas.png)

![w:680](../resultados/grafico_anagramas.png)

<!--
Tempo: 40 s.
Na escala log-log, a inclinação da curva original fica próxima de 2 e a da
otimizada próxima de 1. As linhas de referência ajudam a visualizar isso.
-->

---

## Conclusão e próximos passos

- A primeira otimização elimina as comparações repetidas
- `set` e `dict` levam de O(n²) para O(n) esperado
- O ganho medido cresce com `n` (até **6.240,9×** em duplicatas)

**Próximos passos:**

1. Chave de contagem de caracteres: O(k log k) → O(k)
2. Medir memória com `tracemalloc`
3. Usar `cProfile` para encontrar o novo gargalo
4. Testar mais cenários de melhor caso, caso médio e pior caso

<!--
Tempo: 30 s.
Fechar com a mensagem principal: medimos, identificamos o gargalo e
comprovamos o ganho. As próximas etapas refinam a solução e o diagnóstico.
-->
