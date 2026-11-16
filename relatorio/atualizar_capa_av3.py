from io import BytesIO
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).parents[1]
DOCX = ROOT / "relatorio" / "Relatorio_Entrega_2_Otimizacao_Final.docx"
TMP = DOCX.with_suffix(".tmp.docx")


def font(name, size):
    return ImageFont.truetype(f"/usr/share/fonts/liberation/{name}.ttf", size)


with ZipFile(DOCX) as zin:
    cover = Image.open(BytesIO(zin.read("word/media/image1.png"))).convert("RGB")
    draw = ImageDraw.Draw(cover)
    bold = font("LiberationSans-Bold", 34)
    regular = font("LiberationSans-Regular", 27)
    white = (255, 255, 255)
    black = (0, 0, 0)

    # Replace the AV2 title block while preserving the original institutional
    # artwork, authors, spacing and visual hierarchy.
    draw.rectangle((80, 1080, 1370, 1395), fill=white)
    title = "OTIMIZAÇÃO FINAL E ANÁLISE CRÍTICA\nDE DUPLICATAS E ANAGRAMAS"
    bbox = draw.multiline_textbbox((0, 0), title, font=bold, spacing=10, align="center")
    draw.multiline_text(
        ((cover.width - (bbox[2] - bbox[0])) / 2, 1120),
        title,
        font=bold,
        fill=black,
        spacing=10,
        align="center",
    )

    # Update the AV2 description to the AV3 delivery description.
    draw.rectangle((735, 1300, 1390, 1780), fill=white)
    description = (
        "Relatório da Avaliação 3 (Av3) apresentado à\n"
        "disciplina Análise e Otimização de Sistemas, do\n"
        "curso de Ciência da Computação, como parte da\n"
        "avaliação do semestre.\n\n"
        "Professor: Igor Gonzalez"
    )
    draw.multiline_text((760, 1480), description, font=regular, fill=black, spacing=9)

    output = BytesIO()
    cover.save(output, format="PNG")
    cover_bytes = output.getvalue()

    with ZipFile(TMP, "w", ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            data = cover_bytes if item.filename == "word/media/image1.png" else zin.read(item.filename)
            zout.writestr(item, data)

TMP.replace(DOCX)
print(DOCX)
