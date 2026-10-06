"""
convert_docs_to_pdf.py - Enterprise PDF Document Generator for Apex Car Rental
Converts all markdown domain documents into beautifully styled, corporate PDF documents.
"""

import os
import re
from pathlib import Path
from typing import Dict, Tuple, List

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable, KeepTogether
)
from reportlab.pdfgen import canvas

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DOCS_DIR = DATA_DIR / "documents"
PDF_DIR = DATA_DIR / "pdf_documents"
PDF_DIR.mkdir(parents=True, exist_ok=True)


class NumberedCanvas(canvas.Canvas):
    """Two-pass canvas to dynamically compute and render total page count."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count: int):
        self.saveState()
        # Top Running Header
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(colors.HexColor("#475569"))
        self.drawString(54, 755, "APEX CAR RENTAL — OPERATIONAL POLICIES & FLEET KNOWLEDGE BASE")
        
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.75)
        self.line(54, 748, 558, 748)

        # Bottom Running Footer
        self.line(54, 45, 558, 45)
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748B"))
        self.drawString(54, 32, "Confidential & Proprietary — For Apex AI & Customer Support Use Only")
        
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(558, 32, page_str)
        self.restoreState()


def parse_frontmatter(content: str) -> Tuple[Dict[str, str], str]:
    metadata = {}
    body = content
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            fm_text = parts[1].strip()
            body = parts[2].strip()
            for line in fm_text.splitlines():
                if ":" in line:
                    key, val = line.split(":", 1)
                    metadata[key.strip()] = val.strip().strip('"').strip("'")
    return metadata, body


def convert_md_to_pdf(md_path: Path, output_pdf_path: Path):
    raw_content = md_path.read_text(encoding="utf-8")
    metadata, body = parse_frontmatter(raw_content)

    doc_id = metadata.get("id", "DOC-REF")
    doc_title = metadata.get("title", md_path.stem.replace("_", " ").title())
    category = metadata.get("category", "Operations").upper()

    doc = SimpleDocTemplate(
        str(output_pdf_path),
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=64,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()

    # Custom Typography Palette
    title_style = ParagraphStyle(
        "DocTitle",
        parent=styles["Heading1"],
        fontName="Helvetica-Bold",
        fontSize=18,
        leading=22,
        textColor=colors.HexColor("#0F172A"),
        spaceAfter=4
    )

    badge_style = ParagraphStyle(
        "CategoryBadge",
        fontName="Helvetica-Bold",
        fontSize=9,
        leading=11,
        textColor=colors.HexColor("#0284C7"),
        spaceAfter=6
    )

    meta_style = ParagraphStyle(
        "MetaInfo",
        fontName="Helvetica",
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor("#64748B"),
        spaceAfter=12
    )

    h2_style = ParagraphStyle(
        "SectionH2",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=12,
        leading=16,
        textColor=colors.HexColor("#1E293B"),
        spaceBefore=12,
        spaceAfter=6,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        "BodyTextCustom",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9.5,
        leading=14,
        textColor=colors.HexColor("#334155"),
        spaceAfter=4
    )

    bullet_style = ParagraphStyle(
        "BulletCustom",
        parent=body_style,
        leftIndent=14,
        firstLineIndent=-10,
        spaceAfter=3
    )

    story = []

    # 1. Header Metadata Section
    story.append(Paragraph(f"CATEGORY: {category}", badge_style))
    story.append(Paragraph(doc_title, title_style))
    story.append(Paragraph(f"Document ID: <b>{doc_id}</b> &nbsp;|&nbsp; File Reference: <code>{md_path.name}</code> &nbsp;|&nbsp; Verification: Active Corporate Policy", meta_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#0F172A"), spaceAfter=14))

    # 2. Process Markdown Content Lines
    lines = body.splitlines()
    in_table = False
    table_lines = []

    for line in lines:
        stripped = line.strip()
        if not stripped:
            if in_table and table_lines:
                # Flush table
                story.extend(build_table_flowable(table_lines, body_style))
                table_lines = []
                in_table = False
            story.append(Spacer(1, 4))
            continue

        # Markdown Headings
        if stripped.startswith("# "):
            # Main heading already in title, render as secondary if needed
            heading_text = stripped[2:].strip()
            if heading_text.lower() != doc_title.lower():
                story.append(Paragraph(f"<b>{escape_xml(heading_text)}</b>", h2_style))
            continue

        if stripped.startswith("## "):
            section_title = stripped[3:].strip()
            story.append(Spacer(1, 6))
            story.append(Paragraph(f"<b>{escape_xml(section_title)}</b>", h2_style))
            story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#E2E8F0"), spaceAfter=6))
            continue

        if stripped.startswith("### "):
            sub_title = stripped[4:].strip()
            story.append(Paragraph(f"<b>{escape_xml(sub_title)}</b>", h2_style))
            continue

        # Tables
        if "|" in stripped and ("---" in stripped or stripped.startswith("|")):
            in_table = True
            table_lines.append(stripped)
            continue
        elif in_table:
            # End of table
            story.extend(build_table_flowable(table_lines, body_style))
            table_lines = []
            in_table = False

        # List items / Bullet points
        if stripped.startswith("- ") or stripped.startswith("* "):
            item_text = stripped[2:].strip()
            formatted_item = format_inline_markdown(item_text)
            story.append(Paragraph(f"&bull; &nbsp;{formatted_item}", bullet_style))
            continue

        # Numbered list
        numbered_match = re.match(r"^(\d+)\.\s+(.*)", stripped)
        if numbered_match:
            num = numbered_match.group(1)
            item_text = numbered_match.group(2)
            formatted_item = format_inline_markdown(item_text)
            story.append(Paragraph(f"<b>{num}.</b> &nbsp;{formatted_item}", bullet_style))
            continue

        # Normal text paragraph
        formatted_para = format_inline_markdown(stripped)
        story.append(Paragraph(formatted_para, body_style))

    if in_table and table_lines:
        story.extend(build_table_flowable(table_lines, body_style))

    doc.build(story, canvasmaker=NumberedCanvas)


def escape_xml(text: str) -> str:
    """Escapes XML entities for ReportLab Paragraphs."""
    text = text.replace("&", "&amp;")
    text = text.replace("<", "&lt;")
    text = text.replace(">", "&gt;")
    return text


def format_inline_markdown(text: str) -> str:
    """Converts **bold**, *italic*, and `code` into ReportLab XML markup."""
    # First escape XML
    text = escape_xml(text)
    # Convert bold: **text** -> <b>text</b>
    text = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', text)
    # Convert italic: *text* -> <i>\1</i>
    text = re.sub(r'\*(.+?)\*', r'<i>\1</i>', text)
    # Convert inline code: `code` -> <font name="Courier">\1</font>
    text = re.sub(r'`(.+?)`', r'<font name="Courier">\1</font>', text)
    return text


def build_table_flowable(table_lines: List[str], cell_style: ParagraphStyle) -> List:
    """Converts markdown table lines into a ReportLab Table."""
    rows = []
    for line in table_lines:
        if "---" in line:
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if cells:
            row_flowables = [Paragraph(format_inline_markdown(c), cell_style) for c in cells]
            rows.append(row_flowables)

    if not rows:
        return []

    t = Table(rows, colWidths=[504 / len(rows[0])] * len(rows[0]))
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#F1F5F9")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor("#0F172A")),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
    ]))
    return [Spacer(1, 6), t, Spacer(1, 6)]


def main():
    md_files = sorted(DOCS_DIR.glob("*.md"))
    print(f"Converting {len(md_files)} markdown documents to PDF in {PDF_DIR}...")
    success = 0
    for idx, md_file in enumerate(md_files, start=1):
        pdf_file = PDF_DIR / f"{md_file.stem}.pdf"
        try:
            convert_md_to_pdf(md_file, pdf_file)
            success += 1
            if idx % 15 == 0 or idx == len(md_files):
                print(f"  [{idx}/{len(md_files)}] Processed: {pdf_file.name}")
        except Exception as e:
            print(f"  [ERROR] Failed to convert {md_file.name}: {e}")

    print(f"\nCompleted! Successfully generated {success}/{len(md_files)} PDF documents.")


if __name__ == "__main__":
    main()
