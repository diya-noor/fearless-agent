from flask import Flask, request, send_file, jsonify
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from io import BytesIO
import requests

app = Flask(__name__)

# LOGO URLs - GitHub raw URLs
HEADER_LOGO_URL = "https://raw.githubusercontent.com/diya-noor/fearless-agent/main/fearless_icon_logo.png"
FOOTER_LOGO_URL = "https://raw.githubusercontent.com/diya-noor/fearless-agent/main/fearless_text_logo.png"

def download_image(url):
    """Download image from URL and return as BytesIO stream"""
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return BytesIO(response.content)
    except:
        pass
    return None

def add_header_footer(doc):
    """Add Fearless branded header and footer with logos"""
    section = doc.sections[0]
    
    # === HEADER ===
    header = section.header
    header_para = header.paragraphs[0]
    header_para.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    
    # Add icon logo to header
    logo_stream = download_image(HEADER_LOGO_URL)
    if logo_stream:
        header_para.add_run().add_picture(logo_stream, height=Inches(0.6))
    else:
        # Placeholder if logo can't be downloaded
        run = header_para.add_run("[FEARLESS ICON]")
        run.font.name = 'Montserrat'
        run.font.size = Pt(10)
        run.font.color.rgb = RGBColor(92, 57, 119)
    
    # === FOOTER ===
    footer = section.footer
    
    # Clear existing paragraphs
    for para in footer.paragraphs:
        para.clear()
    
    # Line 1: Text logo (centered)
    logo_para = footer.add_paragraph()
    logo_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    logo_stream = download_image(FOOTER_LOGO_URL)
    if logo_stream:
        logo_para.add_run().add_picture(logo_stream, width=Inches(1.5))
    else:
        # Placeholder if logo can't be downloaded
        run = logo_para.add_run("fearless")
        run.font.name = 'Montserrat'
        run.font.size = Pt(14)
        run.font.bold = True
        run.font.color.rgb = RGBColor(92, 57, 119)
    
    # Line 2: Address
    address_para = footer.add_paragraph()
    address_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    address_run = address_para.add_run("8 Market Place, Suite 200, Baltimore, MD 21202")
    address_run.font.name = 'Montserrat'
    address_run.font.size = Pt(7)
    address_run.font.color.rgb = RGBColor(153, 153, 153)
    address_para.paragraph_format.space_before = Pt(6)
    
    # Line 3: Contact info
    contact_para = footer.add_paragraph()
    contact_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    # Phone and fax (gray)
    contact_run1 = contact_para.add_run("(410) 394-9600  /  fax (410) 779-3706  /  ")
    contact_run1.font.name = 'Montserrat'
    contact_run1.font.size = Pt(7)
    contact_run1.font.color.rgb = RGBColor(153, 153, 153)
    
    # Website (purple)
    contact_run2 = contact_para.add_run("fearless.tech")
    contact_run2.font.name = 'Montserrat'
    contact_run2.font.size = Pt(7)
    contact_run2.font.color.rgb = RGBColor(92, 57, 119)

def format_content(doc, text):
    """Format the main content with Fearless styling"""
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
    """Process a single paragraph with heading detection"""
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
        
        if level == 1:
            run.font.name = 'Montserrat Alternates'
            run.font.size = Pt(18)
            run.font.bold = True
            run.font.color.rgb = RGBColor(238, 83, 64)
        elif level == 2:
            run.font.name = 'Montserrat'
            run.font.size = Pt(14)
            run.font.bold = True
            run.font.color.rgb = RGBColor(238, 83, 64)
        else:
            run.font.name = 'Montserrat'
            run.font.size = Pt(12)
            run.font.bold = True
            run.font.color.rgb = RGBColor(0, 0, 0)
    else:
        run = para.add_run(para_text)
        run.font.name = 'Montserrat'
        run.font.size = Pt(10)
        run.font.color.rgb = RGBColor(0, 0, 0)
    
    para.paragraph_format.space_after = Pt(12)

@app.route('/generate-document', methods=['POST'])
def generate_document():
    try:
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
        
        return send_file(
            file_stream,
            as_attachment=True,
            download_name='fearless_document.docx',
            mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        )
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)