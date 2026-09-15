"""PDF practical report builder using ReportLab.

One generic builder handles every practical: it lays out the practical's
static content (aim/objectives/theory/algorithm/code) alongside the
student's submitted result (input image(s), output image(s)/values/tables).
"""
from __future__ import annotations

import base64
import io
import re
from datetime import date
from typing import Any

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import (
    Image as RLImage,
    ListFlowable,
    ListItem,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

MAX_IMAGE_WIDTH = 8 * cm


def _data_url_to_image_flowable(data_url: str, max_width: float = MAX_IMAGE_WIDTH) -> RLImage | None:
    if not data_url or "," not in data_url:
        return None
    header, b64data = data_url.split(",", 1)
    try:
        raw = base64.b64decode(b64data)
    except Exception:
        return None
    buf = io.BytesIO(raw)
    try:
        img = RLImage(buf)
    except Exception:
        return None
    if img.drawWidth > max_width:
        scale = max_width / img.drawWidth
        img.drawWidth *= scale
        img.drawHeight *= scale
    return img


def _styles():
    styles = getSampleStyleSheet()
    styles.add(
        ParagraphStyle(
            name="LabTitle",
            fontSize=20,
            leading=24,
            spaceAfter=4,
            textColor=colors.HexColor("#1e1b4b"),
            fontName="Helvetica-Bold",
        )
    )
    styles.add(
        ParagraphStyle(
            name="SectionHeading",
            fontSize=13,
            leading=16,
            spaceBefore=14,
            spaceAfter=6,
            textColor=colors.HexColor("#312e81"),
            fontName="Helvetica-Bold",
        )
    )
    styles.add(
        ParagraphStyle(name="Body", fontSize=10, leading=14, spaceAfter=4, fontName="Helvetica")
    )
    styles.add(
        ParagraphStyle(
            name="CodeBlock",
            fontSize=8,
            leading=10.5,
            fontName="Courier",
            backColor=colors.HexColor("#0f172a"),
            textColor=colors.HexColor("#e2e8f0"),
            leftIndent=6,
            spaceBefore=4,
            spaceAfter=8,
        )
    )
    return styles


def _strip_code_fence(code: str) -> str:
    return re.sub(r"^```[a-zA-Z]*\n|\n```$", "", code.strip())


def _page_footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(colors.HexColor("#64748b"))
    canvas.drawString(2 * cm, 1.2 * cm, "Image Processing Lab — Practical Report")
    canvas.drawRightString(A4[0] - 2 * cm, 1.2 * cm, f"Page {doc.page}")
    canvas.restoreState()


def build_report(practical: dict[str, Any], result: dict[str, Any], student_info: dict[str, Any], input_images: dict[str, str]) -> bytes:
    styles = _styles()
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        topMargin=2 * cm,
        bottomMargin=2 * cm,
        leftMargin=2 * cm,
        rightMargin=2 * cm,
        title=f"{practical.get('title', 'Practical')} — Report",
    )

    story: list = []

    story.append(Paragraph("Image Processing Lab", styles["LabTitle"]))
    story.append(
        Paragraph(
            f"Practical {practical.get('number', '')}: {practical.get('title', '')}",
            styles["SectionHeading"],
        )
    )

    info_rows = [
        ["Student Name", student_info.get("name", "")],
        ["Roll Number", student_info.get("rollNumber", "")],
        ["USN", student_info.get("usn", "")],
        ["Semester", student_info.get("semester", "")],
        ["Section", student_info.get("section", "")],
        ["Date", student_info.get("date") or date.today().isoformat()],
    ]
    info_table = Table(info_rows, colWidths=[4 * cm, 10 * cm])
    info_table.setStyle(
        TableStyle(
            [
                ("FONTSIZE", (0, 0), (-1, -1), 9),
                ("TEXTCOLOR", (0, 0), (0, -1), colors.HexColor("#4338ca")),
                ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
                ("TOPPADDING", (0, 0), (-1, -1), 3),
                ("LINEBELOW", (0, 0), (-1, -1), 0.3, colors.HexColor("#e2e8f0")),
            ]
        )
    )
    story.append(info_table)
    story.append(Spacer(1, 10))

    def section(title: str, body: str):
        story.append(Paragraph(title, styles["SectionHeading"]))
        for para in (body or "").split("\n\n"):
            clean = para.strip()
            if clean:
                story.append(Paragraph(clean.replace("\n", "<br/>"), styles["Body"]))

    section("Aim", practical.get("aim", ""))

    if practical.get("objectives"):
        story.append(Paragraph("Objectives", styles["SectionHeading"]))
        story.append(
            ListFlowable(
                [ListItem(Paragraph(obj, styles["Body"])) for obj in practical["objectives"]],
                bulletType="1",
            )
        )

    section("Theory", practical.get("theory", ""))

    if practical.get("algorithm"):
        story.append(Paragraph("Algorithm", styles["SectionHeading"]))
        story.append(
            ListFlowable(
                [ListItem(Paragraph(step, styles["Body"])) for step in practical["algorithm"]],
                bulletType="1",
            )
        )

    if practical.get("referenceCode"):
        story.append(Paragraph("Python Implementation (Reference)", styles["SectionHeading"]))
        code = _strip_code_fence(practical["referenceCode"])
        # Break very long code blocks across paragraphs so ReportLab can page-break safely.
        for chunk_start in range(0, len(code), 3000):
            chunk = code[chunk_start : chunk_start + 3000]
            escaped = chunk.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace("\n", "<br/>")
            story.append(Paragraph(escaped, styles["CodeBlock"]))

    story.append(PageBreak())

    if input_images:
        story.append(Paragraph("Input Image(s)", styles["SectionHeading"]))
        row = []
        for role, data_url in input_images.items():
            flow = _data_url_to_image_flowable(data_url)
            if flow:
                row.append([flow, Paragraph(role.capitalize(), styles["Body"])])
        if row:
            table = Table([row], colWidths=[MAX_IMAGE_WIDTH + 0.5 * cm] * len(row))
            story.append(table)
            story.append(Spacer(1, 10))

    outputs = result.get("outputs", [])
    image_outputs = [o for o in outputs if o.get("type") == "image"]
    other_outputs = [o for o in outputs if o.get("type") != "image"]

    if image_outputs:
        story.append(Paragraph("Output Image(s)", styles["SectionHeading"]))
        cells = []
        for out in image_outputs:
            flow = _data_url_to_image_flowable(out.get("data", ""))
            if flow:
                cells.append([flow, Paragraph(out.get("name", ""), styles["Body"])])
        # Two images per row so the report stays readable and doesn't overflow.
        for i in range(0, len(cells), 2):
            pair = cells[i : i + 2]
            row_table = Table([pair], colWidths=[MAX_IMAGE_WIDTH + 0.5 * cm] * len(pair))
            story.append(row_table)
            story.append(Spacer(1, 8))

    if other_outputs:
        story.append(Paragraph("Numerical / Tabular Results", styles["SectionHeading"]))
        for out in other_outputs:
            story.append(Paragraph(f"<b>{out.get('name','')}</b>", styles["Body"]))
            if out.get("type") == "value":
                story.append(Paragraph(str(out.get("data")), styles["Body"]))
            elif out.get("type") == "table":
                rows = out.get("data") or []
                if rows:
                    headers = list(rows[0].keys())
                    table_data = [headers] + [[str(r.get(h, "")) for h in headers] for r in rows]
                    t = Table(table_data, hAlign="LEFT")
                    t.setStyle(
                        TableStyle(
                            [
                                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#4338ca")),
                                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                                ("FONTSIZE", (0, 0), (-1, -1), 8),
                                ("GRID", (0, 0), (-1, -1), 0.3, colors.HexColor("#cbd5e1")),
                                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
                                ("TOPPADDING", (0, 0), (-1, -1), 4),
                            ]
                        )
                    )
                    story.append(t)
                    story.append(Spacer(1, 8))

    section("Observation", practical.get("observation", ""))
    section("Conclusion", practical.get("conclusion", ""))

    if practical.get("postLab"):
        story.append(Paragraph("Post-Lab Questions", styles["SectionHeading"]))
        story.append(
            ListFlowable(
                [ListItem(Paragraph(q, styles["Body"])) for q in practical["postLab"]],
                bulletType="1",
            )
        )

    doc.build(story, onFirstPage=_page_footer, onLaterPages=_page_footer)
    return buffer.getvalue()
