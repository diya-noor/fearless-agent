# Fearless Document Formatter - Official Style Guide with Separate Functions
from flask import Flask, request, send_file, jsonify
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from io import BytesIO
import requests
import logging

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

HEADER_LOGO_URL = "https://raw.githubusercontent.com/diya-noor/fearless-agent/main/fearless_icon_logo.png"
FOOTER_LOGO_URL = "https://raw.githubusercontent.com/diya-noor/fearless-agent/main/fearless_text_logo.png"

COLORS = {
    'orange': RGBColor(238, 83, 64),
    'purple': RGBColor(92, 57, 119),
    'gray100': RGBColor(73, 79, 86),
}

def download_image(url):
    try:
        logger.info(f"Downloading: {url}")
        response = requests.get(url, timeout=10)
        logger.info(f"Response status: {response.status_code}")
        if response.status_code == 200:
            return BytesIO(response.content)
    except Exception as e:
        logger.error(f"Error downloading image: {e}")
    return None

def add_header_logo(header):
    for para in header.paragraphs:
        para.clear()
    
    header_para = header.add_paragraph()
    header_para.alignment = WD_ALIGN_PARAGRAPH.LEFT
    header_para.paragraph_format.space_after = Pt(0)
    
    logo_stream = download_image(HEADER_LOGO_URL)
    if logo_stream:
        try:
            run = header_para.add_run()
            run.add_picture(logo_stream, height=Inches(0.5))
            logger.info("✅ Header logo added")
        except Exception as e:
            logger.error(f"Error: {e}")
    
    return header_para

def add_footer_table(footer):
    """Create footer with logo and text aligned horizontally"""
    table = footer.add_table(rows=1, cols=2)
    table.alignment = WD_ALIGN_PARAGRAPH.LEFT
    
    # Remove all table borders
    for row in table.rows:
        for cell in row.cells:
            tc = cell._element
            tcPr = tc.get_or_add_tcPr()
            tcBorders = OxmlElement('w:tcBorders')
            for border_name in ['top', 'left', 'bottom', 'right', 'insideH', 'insideV']:
                border = OxmlElement(f'w:{border_name}')
                border.set(qn('w:val'), 'none')
                tcBorders.append(border)
            tcPr.append(tcBorders)
    
    # Left cell: Logo
    logo_cell = table.rows[0].cells[0]
    logo_cell.width = Inches(1.5)
    logo_cell.vertical_alignment = 1  # Center vertically
    
    logo_para = logo_cell.paragraphs[0]
    logo_para.alignment = WD_ALIGN_PARAGRAPH.LEFT
    logo_para.paragraph_format.space_after = Pt(0)
    logo_para.paragraph_format.space_before = Pt(0)
    
    logo_stream = download_image(FOOTER_LOGO_URL)
    if logo_stream:
        try:
            run = logo_para.add_run()
            run.add_picture(logo_stream, height=Inches(0.25))
            logger.info("✅ Footer logo added")
        except Exception as e:
            logger.error(f"Footer logo error: {e}")
    
    # Right cell: Text content
    text_cell = table.rows[0].cells[1]
    text_cell.width = Inches(5)
    text_cell.vertical_alignment = 1  # Center vertically
    
    # First line: Address
    addr_para = text_cell.paragraphs[0]
    addr_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    addr_para.paragraph_format.space_before = Pt(0)
    addr_para.paragraph_format.space_after = Pt(0)
    
    run1 = addr_para.add_run("8 Market Place, Suite 200, Baltimore, MD 21202")
    run1.font.name = 'Montserrat'
    run1.font.size = Pt(7)
    run1.font.color.rgb = COLORS['gray100']
    
    # Second line: Contact
    contact_para = text_cell.add_paragraph()
    contact_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    contact_para.paragraph_format.space_before = Pt(0)
    contact_para.paragraph_format.space_after = Pt(0)
    
    run2 = contact_para.add_run("(410) 394-9600  /  fax (410) 779-3706  /  ")
    run2.font.name = 'Montserrat'
    run2.font.size = Pt(7)
    run2.font.color.rgb = COLORS['gray100']
    
    run3 = contact_para.add_run("fearless.tech")
    run3.font.name = 'Montserrat'
    run3.font.size = Pt(7)
    run3.font.color.rgb = COLORS['gray100']
    
    logger.info("✅ Footer table created")

def add_header_footer(doc):
    logger.info("Adding header and footer...")
    section = doc.sections[0]
    
    header = section.header
    add_header_logo(header)
    
    footer = section.footer
    for para in footer.paragraphs:
        para.clear()
    
    add_footer_table(footer)
    
    logger.info("✅ Header and footer complete")

def format_content(doc, text):
    text = text.strip()
    if '\n' not in text and '\\n' in text:
        text = text.replace('\\r\\n', '\n').replace('\\n', '\n')
    text = text.replace('\r\n', '\n').replace('\r', '\n')
    
    lines = text.split('\n')
    current_para_lines = []
    
    for line in lines:
        line = line.strip()
        if not line:
            if current_para_lines:
                process_paragraph(doc, '\n'.join(current_para_lines))
                current_para_lines = []
            continue
        current_para_lines.append(line)
    
    if current_para_lines:
        process_paragraph(doc, '\n'.join(current_para_lines))

def process_paragraph(doc, para_text):
    para = doc.add_paragraph()
    
    if para_text.startswith('#'):
        level = 0
        for char in para_text:
            if char == '#':
                level += 1
            else:
                break
        
        heading_text = para_text[level:].strip()
        run = para.add_run(heading_text)
        
        if level == 1:
            para.alignment = WD_ALIGN_PARAGRAPH.CENTER
            para.paragraph_format.space_before = Pt(16)
            para.paragraph_format.space_after = Pt(24)
            run.font.name = 'Montserrat Alternates'
            run.font.size = Pt(28)
            run.font.bold = True
            run.font.color.rgb = COLORS['orange']
            
        elif level == 2:
            para.alignment = WD_ALIGN_PARAGRAPH.LEFT
            para.paragraph_format.space_before = Pt(26)
            para.paragraph_format.space_after = Pt(20)
            run.font.name = 'Montserrat Alternates'
            run.font.size = Pt(22)
            run.font.bold = True
            run.font.color.rgb = COLORS['purple']
            
        else:
            para.alignment = WD_ALIGN_PARAGRAPH.LEFT
            para.paragraph_format.space_before = Pt(20)
            para.paragraph_format.space_after = Pt(16)
            run.font.name = 'Montserrat'
            run.font.size = Pt(18)
            run.font.bold = True
            run.font.color.rgb = COLORS['gray100']
    else:
        para.alignment = WD_ALIGN_PARAGRAPH.LEFT
        para.paragraph_format.space_before = Pt(0)
        para.paragraph_format.space_after = Pt(16)
        para.paragraph_format.line_spacing = 1.5
        
        run = para.add_run(para_text)
        run.font.name = 'Montserrat'
        run.font.size = Pt(10)
        run.font.color.rgb = COLORS['gray100']

@app.route('/generate-document', methods=['POST'])
def generate_document():
    try:
        logger.info("📝 Generating document...")
        data = request.json
        text = data.get('text', '')
        
        if not text:
            return jsonify({'error': 'No text provided'}), 400
        
        doc = Document()
        
        for section in doc.sections:
            section.top_margin = Inches(1)
            section.bottom_margin = Inches(1)
            section.left_margin = Inches(1)
            section.right_margin = Inches(1)
        
        add_header_footer(doc)
        format_content(doc, text)
        
        file_stream = BytesIO()
        doc.save(file_stream)
        file_stream.seek(0)
        
        logger.info("✅ Document generated successfully")
        
        return send_file(
            file_stream,
            as_attachment=True,
            download_name='fearless_document.docx',
            mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        )
    
    except Exception as e:
        logger.error(f"❌ Error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)