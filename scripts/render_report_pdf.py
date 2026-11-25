"""Make a readable PDF from the reviewed Markdown analytical report."""
from pathlib import Path
import re
from xml.sax.saxutils import escape
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
ROOT=Path(__file__).resolve().parents[1]
source=ROOT/'reports/analytical_report_reviewed.md'
dest=ROOT/'reports/analytical_report.pdf'
styles=getSampleStyleSheet()
styles.add(ParagraphStyle(name='CoverTitleAlt',parent=styles['Heading1'],fontSize=18,leading=23,spaceAfter=15,textColor=colors.HexColor('#17365d')))
styles.add(ParagraphStyle(name='ReportBodyAlt',parent=styles['BodyText'],fontSize=9.3,leading=14,spaceAfter=7))
styles.add(ParagraphStyle(name='ReportSubAlt',parent=styles['Heading2'],fontSize=12,leading=16,spaceBefore=13,spaceAfter=7,textColor=colors.HexColor('#17365d')))
def inline(s):
    s=escape(s)
    s=re.sub(r'\*\*(.*?)\*\*',r'<b>\1</b>',s)
    s=re.sub(r'\*(.*?)\*',r'<i>\1</i>',s)
    s=re.sub(r'`([^`]+)`',r'<font face="Courier">\1</font>',s)
    return s
story=[]
for line in source.read_text(encoding='utf-8').splitlines():
    line=line.strip()
    if not line:
        story.append(Spacer(1,5)); continue
    if line.startswith('# '):
        story.append(Paragraph(inline(line[2:]),styles['CoverTitleAlt']))
    elif line.startswith('## '):
        story.append(Paragraph(inline(line[3:]),styles['ReportSubAlt']))
    elif line.startswith('### '):
        story.append(Paragraph(inline(line[4:]),styles['Heading3']))
    elif line.startswith('|'):
        story.append(Paragraph(inline(line.replace('|','  /  ')),styles['ReportBodyAlt']))
    elif line.startswith('- '):
        story.append(Paragraph('• '+inline(line[2:]),styles['ReportBodyAlt']))
    else:
        story.append(Paragraph(inline(line),styles['ReportBodyAlt']))
doc=SimpleDocTemplate(str(dest),pagesize=A4,rightMargin=43,leftMargin=43,topMargin=45,bottomMargin=43,title='Trading Performance Analytics Report')
doc.build(story)
print('Created',dest)
