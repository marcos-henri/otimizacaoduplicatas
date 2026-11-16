from pathlib import Path

from docx import Document
from docx.enum.section import WD_SECTION
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Inches, Pt, RGBColor
from docx.oxml import OxmlElement
from docx.oxml.ns import qn


ROOT = Path(__file__).parents[1]
OUT = ROOT / "relatorio" / "Relatorio_Entrega_2_Otimizacao_Final.docx"


def shade(cell, fill="D9EAF7"):
    tc_pr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:fill"), fill)
    tc_pr.append(shd)


def set_cell_text(cell, text, bold=False):
    cell.text = ""
    p = cell.paragraphs[0]
    run = p.add_run(str(text))
    run.bold = bold
    run.font.size = Pt(8.5)
    cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER


def table(doc, headers, rows, widths=None):
    t = doc.add_table(rows=1, cols=len(headers))
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    t.style = "Table Grid"
    for i, header in enumerate(headers):
        set_cell_text(t.rows[0].cells[i], header, True)
        shade(t.rows[0].cells[i])
    for row in rows:
        cells = t.add_row().cells
        for i, value in enumerate(row):
            set_cell_text(cells[i], value)
    if widths:
        for row in t.rows:
            for cell, width in zip(row.cells, widths):
                cell.width = Inches(width)
    doc.add_paragraph()
    return t


def heading(doc, text, level=1):
    p = doc.add_heading(text, level=level)
    p.paragraph_format.space_before = Pt(8)
    p.paragraph_format.space_after = Pt(4)
    return p


def para(doc, text, bold_prefix=None):
    p = doc.add_paragraph()
    p.paragraph_format.line_spacing = 1.08
    p.paragraph_format.space_after = Pt(5)
    if bold_prefix and text.startswith(bold_prefix):
        p.add_run(bold_prefix).bold = True
        p.add_run(text[len(bold_prefix):])
    else:
        p.add_run(text)
    return p


def code(doc, text):
    p = doc.add_paragraph()
    p.style = "No Spacing"
    p.paragraph_format.left_indent = Inches(0.35)
    p.paragraph_format.space_after = Pt(5)
    r = p.add_run(text)
    r.font.name = "Courier New"
    r.font.size = Pt(8.2)
    return p


def page(doc):
    doc.add_page_break()


doc = Document()
section = doc.sections[0]
section.top_margin = Inches(0.65)
section.bottom_margin = Inches(0.65)
section.left_margin = Inches(0.75)
section.right_margin = Inches(0.75)

styles = doc.styles
styles["Normal"].font.name = "Arial"
styles["Normal"].font.size = Pt(10)
styles["Heading 1"].font.name = "Arial"
styles["Heading 1"].font.color.rgb = RGBColor(31, 78, 121)
styles["Heading 2"].font.name = "Arial"
styles["Heading 2"].font.color.rgb = RGBColor(31, 78, 121)

# Capa
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
p.paragraph_format.space_before = Pt(55)
r = p.add_run("ANÁLISE E OTIMIZAÇÃO DE SISTEMAS")
r.bold = True
r.font.size = Pt(18)
r.font.color.rgb = RGBColor(31, 78, 121)
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run("Projeto prático — Segunda entrega")
r.bold = True
r.font.size = Pt(15)
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
p.paragraph_format.space_before = Pt(28)
r = p.add_run("Otimização final de duplicatas e anagramas")
r.bold = True
r.font.size = Pt(20)
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
p.paragraph_format.space_before = Pt(34)
p.add_run("Evolução desde a primeira entrega, análise crítica e evidências experimentais")
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
p.paragraph_format.space_before = Pt(70)
p.add_run("William Araújo Gonçalves da Silva\nKelvin Moreira dos Santos Oliveira\nMarcos Henrique Gonçalves da Silva\n\nCiência da Computação — UNIJORGE\n2026")
page(doc)

# 1
heading(doc, "1. Evolução do projeto e objetivo da segunda entrega")
para(doc, "Na primeira entrega, o projeto diagnosticou duas implementações quadráticas: a detecção de duplicatas comparava todos os pares, e o agrupamento de anagramas fazia busca linear nos grupos e recalculava chaves durante cada comparação. A primeira otimização usou set para duplicatas e dict com chave normalizada para anagramas.")
para(doc, "A segunda entrega aprofunda a otimização dos anagramas. A chave anterior era construída por normalização seguida de ordenação das letras. Essa ordenação custa O(k log k), em que k é o comprimento da palavra. A otimização final implementada em src/anagramas.py usa um vetor de contagens das 26 letras do alfabeto: cada palavra é percorrida uma vez e a chave passa a custar O(k).")
para(doc, "O objetivo não é apenas apresentar uma ordem de crescimento menor. A análise verifica quando essa troca compensa, mede o custo residual, compara memória e legibilidade, verifica a correção e explicita as restrições da nova técnica. O relatório também retoma os resultados da primeira entrega para mostrar a evolução completa.")
heading(doc, "1.1 Entregas e versões comparadas", 2)
table(doc, ["Versão", "Estratégia", "Tempo", "Espaço adicional"], [
    ("Original", "Comparação de pares / busca linear nos grupos", "Duplicatas O(n²); anagramas O(n²·k log k)", "O(1) / O(n)"),
    ("1ª otimização", "set e dict com chave ordenada", "Duplicatas O(n); anagramas O(n·k log k)", "O(n) / O(n·k)"),
    ("2ª otimização", "dict com chave por contagem", "Anagramas O(n·k)", "O(n·k)"),
], [1.0, 2.1, 2.15, 1.35])
para(doc, "A segunda otimização é aplicada ao agrupamento de anagramas. A solução com set continua sendo a versão final para duplicatas, pois já atinge O(n) esperado e não há uma redução assintótica disponível sem alterar o problema.")
page(doc)

# 2
heading(doc, "2. Técnica de otimização final")
heading(doc, "2.1 Chave por ordenação", 2)
para(doc, "Na primeira versão otimizada, a chave de uma palavra é a tupla dos seus caracteres ordenados. Assim, ‘amor’ e ‘roma’ geram a mesma chave. A técnica é geral e preserva a normalização de maiúsculas, acentos, pontuação e dígitos definida no projeto, mas precisa ordenar k caracteres.")
code(doc, 'def chave_anagrama(palavra):\n    return tuple(sorted(normalizar_palavra(palavra)))')
heading(doc, "2.2 Chave por contagem", 2)
para(doc, "A otimização final explora o domínio restrito de palavras normalizadas compostas somente pelas letras a–z. Em vez de ordenar, a função cria um vetor de 26 posições e incrementa a posição correspondente a cada caractere. Duas palavras são anagramas quando produzem o mesmo vetor de frequências.")
code(doc, 'def chave_anagrama_contagem(palavra):\n    base = normalizar_palavra(palavra)\n    if any(c not in "abcdefghijklmnopqrstuvwxyz" for c in base):\n        raise ValueError("a chave por contagem aceita apenas letras a-z")\n    contagem = [0] * 26\n    for c in base:\n        contagem[ord(c) - ord("a")] += 1\n    return tuple(contagem)')
para(doc, "A função agrupar_anagramas_contagem usa essa tupla como chave de um dict. A chave tem tamanho fixo 26; por isso, para o modelo de alfabeto adotado, a comparação e a criação da chave são lineares em k. O resultado continua sendo uma lista de grupos contendo as palavras originais.")
heading(doc, "2.3 Justificativa teórica", 2)
table(doc, ["Operação", "Ordenação", "Contagem"], [
    ("Construção da chave", "O(k log k)", "O(k + σ), com σ=26"),
    ("Consulta no dict", "O(1) esperado", "O(1) esperado"),
    ("Custo total", "O(n·k log k)", "O(n·k) para σ fixo"),
    ("Domínio", "Geral após normalização", "Letras a–z"),
], [2.0, 2.0, 2.4])
para(doc, "A redução é assintótica, mas não garante ganho para toda entrada. Para palavras curtas, sorted é uma operação implementada em C com constantes pequenas; o vetor de contagem envolve criação de lista, indexação e conversão para tupla. Por isso a medição é indispensável.")
page(doc)

# 3
heading(doc, "3. Análise de complexidade e trade-offs")
heading(doc, "3.1 Tempo", 2)
para(doc, "Na versão original, quando as palavras caem em grupos distintos, a palavra de posição i visita aproximadamente i grupos. O somatório produz O(n²) comparações. Como a chave é refeita a cada visita, o custo é O(n²·k log k). A primeira otimização remove a busca linear: cada palavra é processada uma vez e custa O(k log k), totalizando O(n·k log k). A segunda substitui a ordenação por contagem e chega a O(n·k), quando o alfabeto é fixo.")
heading(doc, "3.2 Espaço", 2)
para(doc, "As versões com dict armazenam os grupos e uma chave por grupo. O espaço adicional é O(n·k) no pior caso, considerando as chaves e as referências das palavras. A chave ordenada usa uma estrutura temporária proporcional a k; a chave por contagem usa um vetor de 26 inteiros por palavra durante a construção e uma tupla de 26 inteiros como chave persistente. Assim, a segunda otimização melhora o tempo assintótico, mas não elimina o custo de memória do agrupamento.")
heading(doc, "3.3 Trade-offs", 2)
table(doc, ["Aspecto", "Benefício", "Custo ou risco"], [
    ("Tempo", "O(n·k) em vez de O(n·k log k)", "Pode perder para k pequeno por constantes"),
    ("Espaço", "Chave de tamanho fixo", "Dict e grupos continuam O(n·k)"),
    ("Legibilidade", "Contagem é simples e explícita", "Mais código e regra de domínio"),
    ("Compatibilidade", "Excelente para a–z", "Não aceita dígitos ou outros alfabetos"),
    ("Robustez", "Valida a entrada antes de indexar", "Entrada inválida gera ValueError"),
], [1.1, 2.65, 2.65])
para(doc, "A escolha final é, portanto, contextual. Para palavras comuns curtas, a versão com ordenação é uma alternativa geral e competitiva. Para palavras longas e alfabeto conhecido, a contagem oferece melhor escalabilidade e foi incorporada como uma segunda estratégia explícita, sem esconder a restrição de entrada.")
page(doc)

# 4
heading(doc, "4. Evidências de desempenho")
para(doc, "Os experimentos foram executados com Python 3.14.7. Cada medição faz um aquecimento, usa time.perf_counter, repete a função e reporta a mediana. As palavras foram geradas com uma semente fixa. Os números absolutos dependem da máquina; a comparação relativa e a tendência com k são o foco.")
heading(doc, "4.1 Escalabilidade da primeira otimização", 2)
para(doc, "A Figura 1 retoma o benchmark da primeira entrega. A versão com dict elimina a busca quadrática pelos grupos, e o ganho cresce quando n aumenta. A versão final por contagem mantém essa estrutura e reduz o custo da chave.")
fig = ROOT / "resultados" / "grafico_anagramas.png"
if fig.exists():
    doc.add_picture(str(fig), width=Inches(6.1))
    doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER
    p = doc.add_paragraph("Figura 1 — Escalabilidade do agrupamento original versus a primeira otimização.")
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
heading(doc, "4.2 Segunda otimização: ordenação versus contagem", 2)
table(doc, ["k", "Ordenação", "Contagem", "Ordenação/contagem"], [
    ("8", "273,90 µs", "415,45 µs", "0,7×"),
    ("32", "1,18 ms", "1,15 ms", "1,0×"),
    ("128", "6,54 ms", "4,30 ms", "1,5×"),
    ("512", "31,96 ms", "17,00 ms", "1,9×"),
], [0.7, 1.55, 1.55, 1.7])
para(doc, "Com k=8, a chave por contagem foi 1,5 vez mais lenta; com k=32, as versões ficaram praticamente empatadas. A partir de k=128, a contagem foi 1,5 vez mais rápida, e com k=512 chegou a 1,9 vez. O resultado confirma a previsão: a vantagem da contagem aparece quando o custo k log k deixa de ser pequeno, mas a constante da implementação ainda domina para palavras curtas.")
page(doc)

# 5
heading(doc, "5. Correção, limitações e validade")
heading(doc, "5.1 Correção", 2)
para(doc, "Foram adicionados testes automatizados para comparar a partição produzida pela chave por contagem com a versão original. Os testes cobrem palavras repetidas, anagramas em grupos diferentes, entrada vazia, maiúsculas e acentos. O teste de ‘Ação!’ e ‘acao’ verifica que a normalização continua preservada antes da contagem.")
code(doc, 'assert particionar(agrupar_anagramas_contagem(palavras)) == \\\n+       particionar(agrupar_anagramas_original(palavras))')
para(doc, "A correção da nova chave depende do contrato declarado: após a normalização, cada caractere precisa pertencer a a–z. Em vez de produzir uma posição inválida para outro caractere, a implementação levanta ValueError. Isso torna a limitação observável e evita resultados silenciosamente incorretos.")
heading(doc, "5.2 Limitações experimentais", 2)
table(doc, ["Limitação", "Impacto", "Melhoria futura"], [
    ("Uma máquina e poucas repetições", "Ruído e baixa generalização", "Mais repetições, sementes e máquinas"),
    ("k sintético", "Não representa todos os textos", "Medir distribuição real de comprimentos"),
    ("Alfabeto a–z", "Restringe a aplicabilidade", "Contagem Unicode ou chave adaptativa"),
    ("Sem profiler", "Não separa todos os custos", "Usar cProfile e medir alocações"),
    ("Memória medida separadamente", "Não há curva completa de pico", "Registrar memória por n e k"),
], [1.55, 2.3, 2.3])
para(doc, "O benchmark de k mede apenas a construção da chave, enquanto o benchmark de n mede o agrupamento. Portanto, não se deve somar diretamente os tempos das tabelas. A conclusão segura é que a segunda chave reduz o custo por palavra para k grande; o ganho total do agrupamento também depende do número de palavras, da distribuição dos grupos e do custo do dict.")
heading(doc, "5.3 Melhorias futuras", 2)
para(doc, "As próximas melhorias seriam: escolher automaticamente entre ordenação e contagem conforme o alfabeto e o tamanho de k; generalizar a contagem para Unicode com uma estrutura esparsa; medir pico de memória para cada versão em vários tamanhos; alternar a ordem das medições para reduzir viés térmico; e avaliar entradas reais com diferentes taxas de repetição. Também seria possível comparar uma chave baseada em Counter, observando o custo de seus objetos e a legibilidade.")
page(doc)

# 6
heading(doc, "6. Conclusão")
para(doc, "A segunda entrega consolidou a evolução do projeto. A primeira otimização trocou comparações repetidas por hashing: duplicatas passaram de O(n²) para O(n) esperado, e anagramas passaram de O(n²·k log k) para O(n·k log k). A otimização final atacou o custo residual dos anagramas, substituindo a ordenação por uma assinatura de contagem e reduzindo o custo teórico da chave para O(k), ou O(n·k) no agrupamento com alfabeto fixo.")
para(doc, "Os dados mostram que a melhoria final não deve ser apresentada como um ganho universal. Para k=8, ordenar foi mais rápido; para k=128 e k=512, contar foi respectivamente 1,5 e 1,9 vez mais rápido. Portanto, a análise crítica é parte do resultado: a melhor técnica depende do tamanho da palavra, do domínio dos caracteres, das constantes da linguagem e do contrato de entrada.")
para(doc, "A versão final mantém a correção verificada por testes e explicita o trade-off entre desempenho, generalidade e legibilidade. O trabalho atende ao foco da segunda entrega ao combinar evolução, justificativa teórica, análise de tempo e espaço, evidências de escalabilidade, limitações e propostas de continuidade.")
heading(doc, "Referências")
para(doc, "CORMEN, T. H. et al. Introduction to algorithms. 3. ed. Cambridge: MIT Press, 2009.")
para(doc, "PYTHON SOFTWARE FOUNDATION. Python 3 documentation: dict, set, time.perf_counter e unicodedata. Disponível em: https://docs.python.org/3/. Acesso em: 15 nov. 2026.")
para(doc, "SEDGEWICK, R.; WAYNE, K. Algorithms. 4. ed. Addison-Wesley, 2011.")
para(doc, "Repositório do projeto: https://github.com/marcos-henri/otimizacaoduplicatas.")

doc.save(OUT)
print(OUT)
