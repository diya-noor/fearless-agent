# Fearless Document Formatter - Final Version with All Headings
from flask import Flask, request, send_file, jsonify
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from io import BytesIO
import requests
import logging

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

HEADER_LOGO_URL = "https://raw.githubusercontent.com/diya-noor/fearless-agent/main/fearless_icon_logo.png"
FOOTER_LOGO_URL = "https://raw.githubusercontent.com/diya-noor/fearless-agent/main/fearless_text_logo.png"

# Fearless Color Palette
COLORS = {
    'orange': RGBColor(238, 83, 64),      # #EE5340 - Main Title
    'purple': RGBColor(92, 57, 119),      # #5C3977 - Subtitle
    'gray100': RGBColor(73, 79, 86),      # #494F56 - Headings & Body
}

def download_image(url):
    """Download image from URL"""
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return BytesIO(response.content)
    except:
        pass
    return None

def add_header_footer(doc):
    """Add Fearless header and footer"""
    section = doc.sections[0]
    
    # === HEADER ===
    header = section.header
    for para in header.paragraphs:
        para.clear()
    
    header_para = header.add_paragraph()
    header_para.alignment = WD_ALIGN_PARAGRAPH.LEFT
    header_para.paragraph_format.space_after = Pt(0)
    
    logo_stream = download_image(HEADER_LOGO_URL)
    if logo_stream:
        try:
            header_para.add_run().add_picture(logo_stream, height=Inches(0.5))
            logger.info("✅ Header logo added")
        except Exception as e:
            logger.error(f"Header logo error: {e}")
    
    # === FOOTER ===
    footer = section.footer
    for para in footer.paragraphs:
        para.clear()
    
    # Logo - Small, left aligned, independent
    logo_para = footer.add_paragraph()
    logo_para.alignment = WD_ALIGN_PARAGRAPH.LEFT
    logo_para.paragraph_format.space_after = Pt(1)
    
    logo_stream = download_image(FOOTER_LOGO_URL)
    if logo_stream:
        try:
            logo_para.add_run().add_picture(logo_stream, height=Inches(0.2))
            logger.info("✅ Footer logo added")
        except Exception as e:
            logger.error(f"Footer logo error: {e}")
    
    # Address - Centered, separate from logo
    addr_para = footer.add_paragraph()
    addr_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    addr_para.paragraph_format.space_before = Pt(0)
    addr_para.paragraph_format.space_after = Pt(0)
    
    run1 = addr_para.add_run("8 Market Place, Suite 200, Baltimore, MD 21202")
    run1.font.name = 'Montserrat'
    run1.font.size = Pt(7)
    run1.font.color.rgb = COLORS['gray100']
    
    # Contact - Centered
    contact_para = footer.add_paragraph()
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
    
    logger.info("✅ Footer complete")

def format_content(doc, text):
    """Format markdown content"""
    text = text.strip()
    
    # Handle escaped newlines
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
    """Process paragraph with Fearless styling"""
    para = doc.add_paragraph()
    
    if para_text.startswith('#'):
        # Count heading level
        level = 0
        for char in para_text:
            if char == '#':
                level += 1
            else:
                break
        
        heading_text = para_text[level:].strip()
        run = para.add_run(heading_text)
        
        if level == 1:
            # H1 - Main Title: Orange, 28pt, Centered, Bold
            para.alignment = WD_ALIGN_PARAGRAPH.LEFT
            para.paragraph_format.space_before = Pt(16)
            para.paragraph_format.space_after = Pt(24)
            run.font.name = 'Montserrat Alternates'
            run.font.size = Pt(28)
            run.font.bold = True
            run.font.color.rgb = COLORS['orange']  # #EE5340
            
        elif level == 2:
            # H2 - Subtitle: Purple, 22pt, Left, Bold
            para.alignment = WD_ALIGN_PARAGRAPH.LEFT
            para.paragraph_format.space_before = Pt(26)
            para.paragraph_format.space_after = Pt(20)
            run.font.name = 'Montserrat Alternates'
            run.font.size = Pt(22)
            run.font.bold = True
            run.font.color.rgb = COLORS['purple']  # #5C3977
            
        elif level == 3:
            # H3 - Heading 3: Gray, 18pt, Left, Bold
            para.alignment = WD_ALIGN_PARAGRAPH.LEFT
            para.paragraph_format.space_before = Pt(20)
            para.paragraph_format.space_after = Pt(16)
            run.font.name = 'Montserrat'
            run.font.size = Pt(18)
            run.font.bold = True
            run.font.color.rgb = COLORS['gray100']  # #494F56
            
        elif level == 4:
            # H4 - Heading 4: Gray, 14pt, Left, Bold
            para.alignment = WD_ALIGN_PARAGRAPH.LEFT
            para.paragraph_format.space_before = Pt(16)
            para.paragraph_format.space_after = Pt(12)
            run.font.name = 'Montserrat'
            run.font.size = Pt(14)
            run.font.bold = True
            run.font.color.rgb = COLORS['gray100']  # #494F56
            
        else:
            # H5+ - Smaller headings: Gray, 12pt, Left, Bold
            para.alignment = WD_ALIGN_PARAGRAPH.LEFT
            para.paragraph_format.space_before = Pt(12)
            para.paragraph_format.space_after = Pt(10)
            run.font.name = 'Montserrat'
            run.font.size = Pt(12)
            run.font.bold = True
            run.font.color.rgb = COLORS['gray100']  # #494F56
    else:
        # Body text: Gray, 10pt, Left, Regular, Line height 1.5
        para.alignment = WD_ALIGN_PARAGRAPH.LEFT
        para.paragraph_format.space_before = Pt(0)
        para.paragraph_format.space_after = Pt(16)
        para.paragraph_format.line_spacing = 1.5
        
        run = para.add_run(para_text)
        run.font.name = 'Montserrat'
        run.font.size = Pt(10)
        run.font.color.rgb = COLORS['gray100']  # #494F56

@app.route('/generate-document', methods=['POST'])
def generate_document():
    try:
        logger.info("📝 Generating document...")
        data = request.json
        text = data.get('text', '')
        
        if not text:
            return jsonify({'error': 'No text provided'}), 400
        
        doc = Document()
        
        # Page margins and footer positioning
        for section in doc.sections:
            section.top_margin = Inches(1)
            section.bottom_margin = Inches(0.5)      # Reduced - footer moves up
            section.left_margin = Inches(1)
            section.right_margin = Inches(1)
            section.footer_distance = Inches(0.3)    # Footer closer to content
        
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