from flask import Flask, request, send_file, jsonify
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from io import BytesIO
import requests

app = Flask(__name__)

def add_header_footer(doc):
    """Add Fearless branded header and footer"""
    # Header
    section = doc.sections[0]
    header = section.header
    header_para = header.paragraphs[0]
    
    # Add logo if available - placeholder for now
    header_run = header_para.add_run("Fearless Test")
    header_run.font.name = 'Montserrat'
    header_run.font.size = Pt(12)
    header_run.font.color.rgb = RGBColor(238, 83, 64)
    header_para.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    
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
    # Convert literal \n to actual newlines
    text = text.replace('\\n', '\n')
    
    # Split content into paragraphs
    paragraphs = text.split('\n\n')
    
    for para_text in paragraphs:
        if not para_text.strip():
            continue
            
        para = doc.add_paragraph()
        
        # Check if it's a heading
        if para_text.startswith('#'):
            heading_text = para_text.lstrip('#').strip()
            level = para_text.count('#', 0, 3)
            
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
            else:
                run.font.name = 'Montserrat'
                run.font.size = Pt(12)
                run.font.bold = True
        else:
            run = para.add_run(para_text)
            run.font.name = 'Montserrat'
            run.font.size = Pt(10)
        
        para.paragraph_format.space_after = Pt(12)

@app.route('/generate-document', methods=['POST'])
def generate_document():
    try:
        data = request.json
        text = data.get('text', '')
        
        if not text:
            return jsonify({'error': 'No text provided'}), 400
        
        doc = Document()
        
        sections = doc.sections
        for section in sections:
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