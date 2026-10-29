"""Render the working notes into the existing, simply formatted answer document."""

from pathlib import Path
import re

from docx import Document
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt, RGBColor


def build():
    root = Path(__file__).resolve().parent
    document = Document()
    section = document.sections[0]
    section.page_width, section.page_height = Inches(8.5), Inches(11)
    section.top_margin = section.bottom_margin = Inches(0.7)
    section.left_margin = section.right_margin = Inches(0.8)
    for name in ("Normal", "Title", "Heading 1", "Heading 2"):
        style = document.styles[name]
        style.font.name = "Arial"
        style.font.color.rgb = RGBColor(0, 0, 0)
    document.styles["Normal"].font.size = Pt(11)
    document.styles["Normal"].paragraph_format.space_after = Pt(7)
    document.styles["Normal"].paragraph_format.line_spacing = 1.08
    document.styles["Title"].font.size = Pt(20)
    document.styles["Heading 1"].font.size = Pt(14)
    document.styles["Heading 2"].font.size = Pt(11)
    # Remove template paragraph borders, including Word's default title rule.
    for style in document.styles:
        for border in list(style.element.iter(qn("w:pBdr"))):
            border.getparent().remove(border)
    lines = (root / "Activity 15 Working Notes.md").read_text().splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        if not line:
            i += 1
            continue
        if line.startswith("| "):
            rows = []
            while i < len(lines) and lines[i].startswith("| "):
                row = [cell.strip() for cell in lines[i].strip("|").split("|")]
                if not all(re.fullmatch(r"[-: ]+", cell) for cell in row):
                    rows.append(row)
                i += 1
            table = document.add_table(rows=0, cols=len(rows[0]))
            table.alignment = WD_TABLE_ALIGNMENT.CENTER
            table.autofit = False
            widths = [1.25, 1.85, 1.85, 0.65]
            for col, width in zip(table.columns, widths):
                col.width = Inches(width)
            for row_number, values in enumerate(rows):
                cells = table.add_row().cells
                for col_index, (cell, value) in enumerate(zip(cells, values)):
                    cell.width = Inches(widths[col_index])
                    cell.text = value
                    cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
                    props = cell._tc.get_or_add_tcPr()
                    borders = OxmlElement("w:tcBorders")
                    for edge in ("top", "left", "bottom", "right"):
                        border = OxmlElement("w:" + edge)
                        for key, val in (("val", "single"), ("sz", "4"), ("color", "D9D9D9")):
                            border.set(qn("w:" + key), val)
                        borders.append(border)
                    props.append(borders)
                    margins = OxmlElement("w:tcMar")
                    for edge in ("top", "left", "bottom", "right"):
                        margin = OxmlElement("w:" + edge)
                        margin.set(qn("w:w"), "90")
                        margin.set(qn("w:type"), "dxa")
                        margins.append(margin)
                    props.append(margins)
                    if row_number == 0:
                        shade = OxmlElement("w:shd")
                        shade.set(qn("w:fill"), "EDEDED")
                        props.append(shade)
                    for paragraph in cell.paragraphs:
                        paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
                        paragraph.paragraph_format.space_after = Pt(2)
                        for run in paragraph.runs:
                            run.font.size = Pt(10)
                            run.bold = row_number == 0
                if row_number == 0:
                    table.rows[0]._tr.get_or_add_trPr().append(OxmlElement("w:tblHeader"))
            document.add_paragraph()
            continue
        if line.startswith("# "):
            document.add_paragraph("Activity 15 Sales Commission Calculator", "Title")
        elif line.startswith("## "):
            heading = line[3:]
            paragraph = document.add_paragraph(heading, "Heading 1")
            if heading.startswith(("Part 3", "Part 4", "Part 5", "Commit comparison")):
                paragraph.paragraph_format.page_break_before = True
        elif line.startswith("### "):
            document.add_paragraph(line[4:], "Heading 2")
        else:
            document.add_paragraph(line)
        i += 1
    document.core_properties.author = "Brandon Parks"
    document.core_properties.title = "Activity 15 Sales Commission Calculator"
    document.save(root / "Answers.docx")
    print("Updated existing Answers.docx")


if __name__ == "__main__":
    build()
