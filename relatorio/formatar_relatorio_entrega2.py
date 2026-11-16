from copy import deepcopy
from pathlib import Path

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Cm, Pt
from docx.text.paragraph import Paragraph
from docx.table import Table
from docx.oxml.ns import qn


ROOT = Path(__file__).parents[1]
TEMPLATE = ROOT / "relatorio" / "Relatorio_duplicatas_anagramas_AV2.docx"
SOURCE = ROOT / "relatorio" / "Relatorio_Entrega_2_Otimizacao_Final.docx"
OUTPUT = SOURCE
GRAPH = ROOT / "resultados" / "grafico_anagramas.png"


def set_font(run, name="Times New Roman", size=11, bold=None, italic=None):
    run.font.name = name
    run._element.get_or_add_rPr().rFonts.set(qn("w:eastAsia"), name)
    run.font.size = Pt(size)
    if bold is not None:
        run.bold = bold
    if italic is not None:
        run.italic = italic


def normalize_paragraph(p, kind="body"):
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    pf = p.paragraph_format
    pf.line_spacing = 1.0
    pf.space_before = Pt(0)
    pf.space_after = Pt(6)
    pf.left_indent = Cm(0)
    pf.right_indent = Cm(0)
    pf.first_line_indent = Cm(1.25)
    if kind == "heading1":
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        pf.first_line_indent = Cm(0)
        pf.space_after = Pt(6)
    elif kind == "heading2":
        pf.first_line_indent = Cm(0)
        pf.space_before = Pt(6)
        pf.space_after = Pt(4)
    elif kind in {"code", "caption", "reference"}:
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT if kind != "caption" else WD_ALIGN_PARAGRAPH.CENTER
        pf.first_line_indent = Cm(0)
        pf.left_indent = Cm(0 if kind != "code" else 1.25)
        pf.space_after = Pt(4 if kind != "reference" else 10)
        pf.line_spacing = 1.0
    for run in p.runs:
        if kind == "code":
            set_font(run, "Courier New", 9)
        else:
            set_font(run, "Times New Roman", 11, bold=(kind.startswith("heading")))


def add_text(doc, text):
    p = doc.add_paragraph()
    p.style = doc.styles["normal"]
    kind = "body"
    stripped = text.strip()
    if stripped == "Referências" or stripped.upper() == "REFERÊNCIAS":
        kind = "heading1"
        p.add_run("REFERÊNCIAS")
    elif stripped[:1].isdigit() and ("." in stripped[:4] or " " in stripped[:4]):
        parts = stripped.split(" ", 1)
        number = parts[0]
        title = parts[1] if len(parts) > 1 else ""
        level = 2 if not number.endswith(".") else 1
        kind = "heading2" if level == 2 else "heading1"
        p.add_run(f"{number.replace('.', '.') } {title}".strip())
    elif stripped.startswith(("def ", "    ", "assert ", "for ", "    ")) or "\n" in text and stripped.startswith("def "):
        kind = "code"
        p.add_run(text)
    elif stripped.startswith("Figura ") or stripped.startswith("Tabela ") or stripped.startswith("Fonte:"):
        kind = "caption"
        p.add_run(text)
    elif stripped.startswith(("CORMEN,", "PYTHON SOFTWARE", "SEDGEWICK,", "Repositório")):
        kind = "reference"
        p.add_run(text)
    else:
        p.add_run(text)
    normalize_paragraph(p, kind)
    return p, kind


def copy_table(doc, source_table):
    target = doc.add_table(rows=0, cols=len(source_table.columns))
    for source_row in source_table.rows:
        row = target.add_row()
        for source_cell, target_cell in zip(source_row.cells, row.cells):
            target_cell.text = source_cell.text
            for p in target_cell.paragraphs:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                p.paragraph_format.space_after = Pt(0)
                p.paragraph_format.line_spacing = 1.0
                for run in p.runs:
                    set_font(run, "Times New Roman", 9, bold=(p is target.rows[0].cells[0].paragraphs[0]))
    doc.add_paragraph().paragraph_format.space_after = Pt(0)


template = Document(TEMPLATE)
source = Document(SOURCE)

# Keep the original cover paragraph, which contains the institutional artwork.
body = template._element.body
for child in list(body)[1:]:
    if child.tag.endswith("sectPr"):
        continue
    body.remove(child)

# ABNT-style A4 page setup for the body: 3 cm left/top and 2 cm right/bottom.
section = template.sections[0]
section.page_width = Cm(21)
section.page_height = Cm(29.7)
section.top_margin = Cm(3)
section.bottom_margin = Cm(2)
section.left_margin = Cm(3)
section.right_margin = Cm(2)
section.header_distance = Cm(1.5)
section.footer_distance = Cm(1.5)

# Insert a page break after the preserved cover.
break_p = template.add_paragraph()
break_p.add_run().add_break()

# Copy the second-delivery content, omitting the generated cover and explicit
# page breaks so that pagination follows the ABNT body layout.
started = False
for child in source._element.body:
    if child.tag.endswith("sectPr"):
        continue
    if child.tag.endswith("p"):
        original_p = Paragraph(child, source)
        text = original_p.text
        if not started:
            if text.startswith("1. Evolução"):
                started = True
            else:
                continue
        if not text.strip():
            continue
        # Captions and paragraphs are rebuilt to remove direct formatting from
        # the previous report while preserving the actual content.
        p, kind = add_text(template, text)
        if text.startswith("Figura 1") and GRAPH.exists():
            image_p = template.add_paragraph()
            image_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            image_p.add_run().add_picture(str(GRAPH), width=Cm(15.5))
            caption = template.add_paragraph("Fonte: Elaborado pelos autores (2026).")
            normalize_paragraph(caption, "caption")
    elif child.tag.endswith("tbl") and started:
        source_table = Table(child, source)
        copy_table(template, source_table)

# Apply Times New Roman 11 to the preserved institutional cover's text runs
# without disturbing its logo drawing.
for run in template.paragraphs[0].runs:
    set_font(run, "Arial", 10)

template.save(OUTPUT)
print(OUTPUT)
