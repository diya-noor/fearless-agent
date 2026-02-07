from flask import Flask, request, send_file, jsonify
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from io import BytesIO

app = Flask(__name__)

def add_header_footer(doc):
    """Add Fearless branded header and footer"""
    section = doc.sections[0]
    
    # Header
    header = section.header
    header_para = header.paragraphs[0]
    header_run = header_para.add_run("[FEARLESS LOGO]")
    header_run.font.name = 'Montserrat'
    header_run.font.size = Pt(10)
    header_run.font.color.rgb = RGBColor(238, 83, 64)
    header_para.alignment = WD_ALIGN_PARAGRAPH.LEFT
    
    # Footer
    footer = section.footer
    footer_para = footer.paragraphs[0]
    footer_run = footer_para.add_run("Fearless | ")
    footer_run.font.name = 'Montserrat'
    footer_run.font.size = Pt(9)
    footer_run.font.color.rgb = RGBColor(128, 128, 128)
    
    contact_run = footer_para.add_run("www.fearless.com")
    contact_run.font.name = 'Montserrat'
    contact_run.font.size = Pt(9)
    contact_run.font.color.rgb = RGBColor(238, 83, 64)
    footer_para.alignment = WD_ALIGN_PARAGRAPH.CENTER

def format_content(doc, text):
    """Format the main content with Fearless styling"""
    # Strip any leading/trailing whitespace
    text = text.strip()
    
    # The text might have actual newlines OR literal \n strings
    # First check if it has actual newlines (from webhook)
    if '\n' not in text and '\\n' in text:
        # Has literal \n strings, convert them
        text = text.replace('\\r\\n', '\n')
        text = text.replace('\\n', '\n')
    
    # Normalize Windows line endings to Unix
    text = text.replace('\r\n', '\n')
    text = text.replace('\r', '\n')
    
    # Split by single newlines first
    lines = text.split('\n')
    
    # Process each line
    current_para_lines = []
    
    for line in lines:
        line = line.strip()
        
        if not line:
            # Empty line - end current paragraph
            if current_para_lines:
                process_paragraph(doc, '\n'.join(current_para_lines))
                current_para_lines = []
            continue
        
        current_para_lines.append(line)
    
    # Process last paragraph
    if current_para_lines:
        process_paragraph(doc, '\n'.join(current_para_lines))

def process_paragraph(doc, para_text):
    """Process a single paragraph with heading detection"""
    para = doc.add_paragraph()
    para.alignment = WD_ALIGN_PARAGRAPH.LEFT
    
    # Check for heading
    if para_text.startswith('#'):
        # Count heading level
        level = 0
        for char in para_text:
            if char == '#':
                level += 1
            else:
                break
        
        # Remove # symbols and spaces
        heading_text = para_text[level:].strip()
        run = para.add_run(heading_text)
        
        # Apply formatting based on level
        if level == 1:  # H1
            run.font.name = 'Montserrat Alternates'
            run.font.size = Pt(18)
            run.font.bold = True
            run.font.color.rgb = RGBColor(238, 83, 64)  # Orange-red
        elif level == 2:  # H2
            run.font.name = 'Montserrat'
            run.font.size = Pt(14)
            run.font.bold = True
            run.font.color.rgb = RGBColor(238, 83, 64)  # Also orange-red
        else:  # H3+
            run.font.name = 'Montserrat'
            run.font.size = Pt(12)
            run.font.bold = True
            run.font.color.rgb = RGBColor(0, 0, 0)  # Black
    else:
        # Regular text
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
        
        # Set margins
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