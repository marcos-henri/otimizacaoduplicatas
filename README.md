# AV2 — Diagnóstico e Primeira Otimização: Duplicatas e Anagramas

Projeto da disciplina de Análise de Algoritmos. O objetivo é diagnosticar e
otimizar um código ineficiente, comprovando os ganhos com medições
reprodutíveis.

O repositório contém duas frentes do mesmo tema:

1. **Detecção de duplicatas** — versão original O(n²) e primeira versão
   otimizada O(n) com `set` (hashing).
2. **Agrupamento de anagramas** — versão original que refaz a normalização e
   a ordenação a cada comparação e versão otimizada que calcula uma chave
   normalizada uma única vez e usa `dict`.

## Ambiente de desenvolvimento (devcontainer)

O projeto foi preparado para que ninguém precise instalar Python na máquina.
O Python 3.12 e as dependências ficam dentro do container.

### Pré-requisitos

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) (ou Docker
  Engine) instalado e em execução.
- [Visual Studio Code](https://code.visualstudio.com/) com a extensão
  **Dev Containers** (`ms-vscode-remote.remote-containers`).

### Como abrir

1. Abra a pasta do projeto no VS Code.
2. Pressione `Ctrl+Shift+P` (ou `Cmd+Shift+P` no macOS).
3. Execute **Dev Containers: Reopen in Container**.
4. Aguarde a criação do container. O comando `postCreateCommand` instala
   automaticamente `pytest` e `matplotlib`.
5. Abra o terminal integrado e rode os comandos abaixo.

Também é possível usar o GitHub Codespaces: basta abrir o repositório e
escolher **Code → Codespaces → Create codespace** (no branch desejado). O
arquivo `.devcontainer/devcontainer.json` é usado automaticamente.

> O container usa a imagem oficial
> `mcr.microsoft.com/devcontainers/python:1-3.12-bookworm`. A primeira criação
> baixa a imagem; depois disso, o ambiente fica em cache.

## Comandos úteis

```bash
# Testes
python3 -m pytest

# Benchmark completo (grava CSV, resumo e gráficos em resultados/local/)
python3 -m src.benchmark

# Benchmark curto, para testar rapidamente
python3 -m src.benchmark --rapido

# Benchmark sem gerar gráficos
python3 -m src.benchmark --sem-grafico

# Atualizar os resultados de referência versionados em resultados/
python3 -m src.benchmark --publicar
```

> Rodar o benchmark sem `--publicar` não altera os arquivos versionados em
> `resultados/`: a saída vai para `resultados/local/`, que está no
> `.gitignore`. Use `--saida DIR` para escolher outro diretório.

Com `make`:

```bash
make test
make bench
make bench-rapido
make bench-publicar
```

## Estrutura

```text
.
├── .devcontainer/
│   └── devcontainer.json       # Python 3.12 + dependências
├── .vscode/
│   └── extensions.json         # extensões recomendadas
├── src/
│   ├── duplicatas.py           # versão original e versão com set
│   ├── anagramas.py            # versão original e versão com dict
│   └── benchmark.py            # medição, CSV, resumo e gráficos
├── tests/
│   ├── test_duplicatas.py
│   ├── test_anagramas.py
│   └── test_benchmark.py
├── resultados/
│   ├── README.md
│   ├── benchmark_duplicatas.csv
│   ├── benchmark_anagramas.csv
│   ├── resumo.md
│   ├── grafico_duplicatas.png
│   ├── grafico_anagramas.png
│   └── local/                  # saída das execuções locais (ignorado pelo git)
├── relatorio/
│   └── relatorio.md            # relatório de 3 a 5 páginas
├── apresentacao/
│   ├── slides.md               # slides no formato Marp (5 a 8 min)
│   └── roteiro.md              # roteiro compacto com tempos
├── requirements.txt
├── pyproject.toml
└── Makefile
```

## O que o benchmark mede

- **Duplicatas:** lista com `n` inteiros distintos embaralhados. É o pior caso
  da versão original, pois ela só termina depois de comparar todos os pares.
- **Anagramas:** `n` palavras aleatórias de 8 letras. Com alta probabilidade,
  cada palavra cai em um grupo diferente, o que também caracteriza o pior caso
  da versão original.

As medições usam `time.perf_counter`, com aquecimento, repetições e mediana.
Para funções muito rápidas, cada repetição executa a função várias vezes e
divide o tempo total pelo número de execuções.

## Resultados

Os números da execução de referência estão em
[`resultados/resumo.md`](resultados/resumo.md) e no
[`relatorio/relatorio.md`](relatorio/relatorio.md). Como os tempos absolutos
dependem da máquina, o mais importante é a tendência de crescimento: ao dobrar
`n`, a versão original aproximadamente quadruplica o tempo (O(n²)), enquanto a
versão otimizada aproximadamente dobra (O(n)).

## Relatório e apresentação

- Relatório: [`relatorio/relatorio.md`](relatorio/relatorio.md)
- Slides: [`apresentacao/slides.md`](apresentacao/slides.md)
- Roteiro de apresentação: [`apresentacao/roteiro.md`](apresentacao/roteiro.md)

Para exportar o relatório em PDF, abra o Markdown no VS Code e use uma
extensão de exportação (por exemplo, *Markdown PDF*) ou, se tiver `pandoc`
instalado, rode:

```bash
pandoc relatorio/relatorio.md -o relatorio/relatorio.pdf
```

Para apresentar os slides, abra `apresentacao/slides.md` no VS Code com a
extensão **Marp for VS Code** (já incluída no devcontainer) e use
**Marp: Export Slide Deck** ou **Marp: Start Presentation**.
