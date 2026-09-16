from pathlib import Path
from datetime import date
from xml.sax.saxutils import escape
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_RIGHT, TA_CENTER
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from app.database.models import Letter, Organization

FONT_PATH = Path("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf")
FONT_NAME = "DejaVuSans"

def _font() -> str:
    if FONT_NAME not in pdfmetrics.getRegisteredFontNames() and FONT_PATH.exists():
        pdfmetrics.registerFont(TTFont(FONT_NAME, str(FONT_PATH)))
    return FONT_NAME if FONT_NAME in pdfmetrics.getRegisteredFontNames() else "Helvetica"

def create_pdf(letter: Letter, org: Organization | None, out: Path) -> Path:
    out.parent.mkdir(parents=True, exist_ok=True)
    font = _font(); base = getSampleStyleSheet()
    normal = ParagraphStyle("UzNormal", parent=base["Normal"], fontName=font, leading=15)
    center = ParagraphStyle("UzCenter", parent=normal, alignment=TA_CENTER)
    right = ParagraphStyle("UzRight", parent=normal, alignment=TA_RIGHT)
    heading = ParagraphStyle("UzHeading", parent=center, fontSize=13, leading=16)
    story = []
    if org:
        if org.logo_path and Path(org.logo_path).exists():
            story.append(Image(org.logo_path, width=25*mm, height=25*mm))
        story.append(Paragraph(f"<b>{escape(org.full_name)}</b>", heading))
        details = " | ".join(x for x in [org.address, org.phone, org.email, org.website] if x)
        if details: story.append(Paragraph(escape(details), center))
    story += [Spacer(1, 8*mm), Paragraph(f"Sana: {date.today():%d.%m.%Y} &nbsp;&nbsp; № {escape(letter.letter_number or '—')}", normal), Spacer(1, 5*mm)]
    story.append(Paragraph(f"<b>{escape(letter.recipient)}</b>", right))
    if letter.recipient_person: story.append(Paragraph(escape(letter.recipient_person), right))
    if letter.recipient_position: story.append(Paragraph(escape(letter.recipient_position), right))
    story += [Spacer(1, 5*mm), Paragraph(f"<b>Mavzu: {escape(letter.subject)}</b>", normal), Spacer(1, 5*mm)]
    for block in letter.content.splitlines():
        if block.strip(): story += [Paragraph(escape(block.strip()), normal), Spacer(1, 3*mm)]
    story += [Spacer(1, 8*mm), Paragraph(f"{escape(letter.signer_position or '')} &nbsp;&nbsp;&nbsp;&nbsp; {escape(letter.signer_name or '')}", normal)]
    if letter.attachments: story.append(Paragraph(f"Ilova: {escape(letter.attachments)}", normal))
    SimpleDocTemplate(str(out), pagesize=A4, rightMargin=20*mm, leftMargin=25*mm, topMargin=18*mm, bottomMargin=18*mm).build(story)
    return out
