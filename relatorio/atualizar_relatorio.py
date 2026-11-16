from pathlib import Path
from copy import deepcopy

from docx import Document
from docx.oxml import OxmlElement


BASE = Path(__file__).with_name("Relatorio_duplicatas_anagramas_AV2.docx")
OUTPUT = Path(__file__).with_name("Relatorio_duplicatas_anagramas_AV2_atualizado.docx")


def insert_after(paragraph, text):
    new_p = OxmlElement("w:p")
    paragraph._p.addnext(new_p)
    new = paragraph._parent.add_paragraph()
    new._p.getparent().remove(new._p)
    new_p.addnext(new._p)
    new.style = paragraph.style
    new.add_run(text)
    return new


document = Document(BASE)
needle = "A função medir_tempo, de src/benchmark.py, executa a função medida uma vez para"
for paragraph in document.paragraphs:
    if paragraph.text.startswith(needle):
        explanation = (
            "Aquecimento significa executar a função uma vez antes de iniciar o cronômetro. "
            "No código, a chamada funcao(*args) ocorre antes de time.perf_counter: seu tempo "
            "não entra no resultado. Essa etapa prepara o interpretador Python e favorece o "
            "carregamento de instruções e dados nas caches, evitando que a primeira execução, "
            "frequentemente atípica, distorça a comparação. Ela não altera a complexidade dos "
            "algoritmos; apenas torna a medição mais representativa."
        )
        insert_after(paragraph, explanation)
        break
else:
    raise RuntimeError("Parágrafo da metodologia não encontrado")

document.save(OUTPUT)
print(OUTPUT)
