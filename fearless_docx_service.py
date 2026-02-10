# Force deploy: Feb 9 2026 6:30 PM
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

def download_image(url):
    """Download image from URL"""
    try:
        logger.info(f"Downloading: {url}")
        response = requests.get(url, timeout=10)
        logger.info(f"Response status: {response.status_code}")
        if response.status_code == 200:
            return BytesIO(response.content)
    except Exception as e:
        logger.error(f"Error downloading image: {e}")
    return None

def add_header_footer(doc):
    """Add Fearless header and footer"""
    logger.info("Adding header and footer...")
    section = doc.sections[0]
    
    # === HEADER (LEFT-ALIGNED) ===
    # === HEADER (FORCE LEFT) ===
    header = section.header
    
    # Clear any existing content
    for para in header.paragraphs:
        para.clear()
    
    # Create new paragraph
    header_para = header.add_paragraph()
    
    # Add logo to a run
    logo_stream = download_image(HEADER_LOGO_URL)
    if logo_stream:
        try:
            run = header_para.add_run()
            run.add_picture(logo_stream, height=Inches(0.6))
            logger.info("✅ Header logo added (left-aligned)")
        except Exception as e:
            logger.error(f"Error adding header logo: {e}")
    
    # Explicitly set paragraph alignment
    header_para.alignment = WD_ALIGN_PARAGRAPH.LEFT
    
    # === FOOTER (LOGO LEFT, TEXT RIGHT) ===
    footer = section.footer
    
    # Clear existing
    for para in footer.paragraphs:
        para.clear()
    
    # Create a paragraph with logo on left side
    footer_para = footer.add_paragraph()
    footer_para.alignment = WD_ALIGN_PARAGRAPH.LEFT
    
    # Add logo inline on the left
    logo_stream = download_image(FOOTER_LOGO_URL)
    if logo_stream:
        try:
            run = footer_para.add_run()
            run.add_picture(logo_stream, height=Inches(0.35))
            logger.info("✅ Footer logo added (left side)")
        except Exception as e:
            logger.error(f"Error adding footer logo: {e}")
    
    # Add space after logo
    footer_para.add_run("    ")
    
    # Add address and contact info on same line
    run1 = footer_para.add_run("8 Market Place, Suite 200, Baltimore, MD 21202  |  ")
    run1.font.name = 'Montserrat'
    run1.font.size = Pt(7)
    run1.font.color.rgb = RGBColor(153, 153, 153)  # Gray
    
    run2 = footer_para.add_run("(410) 394-9600  /  fax (410) 779-3706  /  ")
    run2.font.name = 'Montserrat'
    run2.font.size = Pt(7)
    run2.font.color.rgb = RGBColor(153, 153, 153)  # Gray
    
    run3 = footer_para.add_run("fearless.tech")
    run3.font.name = 'Montserrat'
    run3.font.size = Pt(7)
    run3.font.color.rgb = RGBColor(92, 57, 119)  # Purple
    
    logger.info("✅ Footer complete")

def format_content(doc, text):
    """Format content"""
    text = text.strip()
    
    if '\n' not in text and '\\n' in text:
        text = text.replace('\\r\\n', '\n')
        text = text.replace('\\n', '\n')
    
    text = text.replace('\r\n', '\n')
    text = text.replace('\r', '\n')
    
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
    """Process paragraph with exact sample document styling"""
    para = doc.add_paragraph()
    para.alignment = WD_ALIGN_PARAGRAPH.LEFT
    
    if para_text.startswith('#'):
        level = 0
        for char in para_text:
            if char == '#':
                level += 1
            else:
                break
        
        heading_text = para_text[level:].strip()
        run = para.add_run(heading_text)
        
        if level == 1:  # H1 - Titles - Orange-red
            run.font.name = 'Montserrat Alternates'
            run.font.size = Pt(16)
            run.font.bold = True
            run.font.color.rgb = RGBColor(238, 83, 64)  # #ee5340 Orange-red
        elif level == 2:  # H2 - Subtitles - Gray
            run.font.name = 'Montserrat'
            run.font.size = Pt(14)
            run.font.bold = True
            run.font.color.rgb = RGBColor(102, 102, 102)  # #666666 Gray
        else:  # H3+ - Purple
            run.font.name = 'Montserrat'
            run.font.size = Pt(12)
            run.font.bold = True
            run.font.color.rgb = RGBColor(92, 57, 119)  # #5c3977 Purple
    else:
        # Body text - Gray
        run = para.add_run(para_text)
        run.font.name = 'Montserrat'
        run.font.size = Pt(10)
        run.font.color.rgb = RGBColor(102, 102, 102)  # #666666 Gray
    
    para.paragraph_format.space_after = Pt(12)

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