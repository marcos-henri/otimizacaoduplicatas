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

# Experimentos exploratórios de limites (duplicata cedo, grupos iguais, memória)
python3 -m src.limites
python3 -m src.limites --rapido
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
make limites
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
│   ├── benchmark.py            # medição, CSV, resumo e gráficos
│   └── limites.py              # experimentos de limites do ganho
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
│   ├── Relatorio_duplicatas_anagramas_AV2.pdf   # relatório final
│   └── Relatorio_duplicatas_anagramas_AV2.docx  # versão editável
├── apresentacao/
│   ├── slides.md               # baralho Marp com Parte 1 + Parte 2
│   ├── slides.pdf              # baralho exportado (31 slides)
│   ├── roteiro.md              # roteiro da Parte 1 (10 min, 3 pessoas)
│   ├── roteiro.pdf             # roteiro da Parte 1 em PDF (7 páginas)
│   ├── roteiro_aprofundamento.md  # roteiro da Parte 2 (limites do ganho)
│   └── roteiro_aprofundamento.pdf # roteiro da Parte 2 em PDF (8 páginas)
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

## Experimentos de limites

O benchmark oficial mede o pior caso. Para a Parte 2 da apresentação, o script
[`src/limites.py`](src/limites.py) mede cenários que mostram quando o ganho
muda: duplicata no início × no fim, anagramas em grupos distintos × no mesmo
grupo, pico de memória com `tracemalloc`, chave por ordenação × por contagem e
a diferença de semântica com `NaN` e tipos não hashable.

```bash
python3 -m src.limites
python3 -m src.limites --rapido
make limites
```

Os números são exploratórios e variam com a máquina; eles não substituem os
resultados versionados em `resultados/`.

## Resultados

Os números da execução de referência estão em
[`resultados/resumo.md`](resultados/resumo.md) e no
[`relatório final`](relatorio/Relatorio_duplicatas_anagramas_AV2.pdf). Como os tempos absolutos
dependem da máquina, o mais importante é a tendência de crescimento: ao dobrar
`n`, a versão original aproximadamente quadruplica o tempo (O(n²)), enquanto a
versão otimizada aproximadamente dobra (O(n)).

## Relatório e apresentação

- Relatório: [`relatorio/Relatorio_duplicatas_anagramas_AV2.pdf`](relatorio/Relatorio_duplicatas_anagramas_AV2.pdf)
  (versão editável em
  [`relatorio/Relatorio_duplicatas_anagramas_AV2.docx`](relatorio/Relatorio_duplicatas_anagramas_AV2.docx))
- Slides: [`apresentacao/slides.pdf`](apresentacao/slides.pdf) (fonte em
  [`apresentacao/slides.md`](apresentacao/slides.md), 31 slides com as duas partes)
- Roteiro da Parte 1 (10 min, dividido entre William, Kelvin e Marcos):
  [`apresentacao/roteiro.pdf`](apresentacao/roteiro.pdf) (fonte em
  [`apresentacao/roteiro.md`](apresentacao/roteiro.md))
- Roteiro da Parte 2 (aprofundamento e limites do ganho):
  [`apresentacao/roteiro_aprofundamento.pdf`](apresentacao/roteiro_aprofundamento.pdf)
  (fonte em
  [`apresentacao/roteiro_aprofundamento.md`](apresentacao/roteiro_aprofundamento.md))

O baralho de slides contém as duas partes: a Parte 1 termina no slide de
transição “Fim da Parte 1 — início da Parte 2”. Para uma apresentação de 10
minutos, use apenas a Parte 1; para um bloco maior, emende a Parte 2.

Para editar o relatório, abra o arquivo `.docx` no Word ou no LibreOffice e
exporte novamente em PDF. O PDF versionado é o resultado final.

Para apresentar os slides, abra `apresentacao/slides.md` no VS Code com a
extensão **Marp for VS Code** (já incluída no devcontainer) e use
**Marp: Export Slide Deck** ou **Marp: Start Presentation**.

Para regerar os PDFs a partir das fontes:

```bash
# slides (Marp CLI via npx)
npx --yes @marp-team/marp-cli@latest apresentacao/slides.md \
  -o apresentacao/slides.pdf --allow-local-files

# roteiros (md-to-pdf via npx; renderiza com Chromium headless)
for f in roteiro roteiro_aprofundamento; do
  npx --yes md-to-pdf "apresentacao/$f.md" \
    --pdf-options '{"format":"A4","printBackground":true}'
done
```

Se o Chromium do `md-to-pdf` não for encontrado, aponte o executável com
`--launch-options '{"executablePath":"/caminho/para/chrome"}'`.
