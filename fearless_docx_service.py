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
    # You'll replace this with actual logo URL from Fearless brand
    header_run = header_para.add_run()
    header_para.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    
    # Footer
    footer = section.footer
    footer_para = footer.paragraphs[0]
    footer_run = footer_para.add_run("Fearless | ")
    footer_run.font.name = 'Montserrat'
    footer_run.font.size = Pt(9)
    footer_run.font.color.rgb = RGBColor(128, 128, 128)
    
    # Add contact info or website
    contact_run = footer_para.add_run("www.fearless.com")
    contact_run.font.name = 'Montserrat'
    contact_run.font.size = Pt(9)
    contact_run.font.color.rgb = RGBColor(238, 83, 64)  # #ee5340
    footer_para.alignment = WD_ALIGN_PARAGRAPH.CENTER

def format_content(doc, text):
    """Format the main content with Fearless styling"""
    # Split content into paragraphs
    paragraphs = text.split('\n\n')
    
    for i, para_text in enumerate(paragraphs):
        if not para_text.strip():
            continue
            
        para = doc.add_paragraph()
        
        # Check if it's a heading (starts with # or all caps short line)
        if para_text.startswith('#'):
            # Remove # markers
            heading_text = para_text.lstrip('#').strip()
            level = para_text.count('#', 0, 3)
            
            run = para.add_run(heading_text)
            
            if level == 1:  # Main title
                run.font.name = 'Montserrat Alternates'
                run.font.size = Pt(18)
                run.font.bold = True
                run.font.color.rgb = RGBColor(238, 83, 64)  # #ee5340
            elif level == 2:  # Subtitle
                run.font.name = 'Montserrat'
                run.font.size = Pt(14)
                run.font.bold = True
                run.font.color.rgb = RGBColor(0, 0, 0)
            else:  # H3
                run.font.name = 'Montserrat'
                run.font.size = Pt(12)
                run.font.bold = True
                run.font.color.rgb = RGBColor(0, 0, 0)
        else:
            # Regular body text
            run = para.add_run(para_text)
            run.font.name = 'Montserrat'
            run.font.size = Pt(10)
            run.font.color.rgb = RGBColor(0, 0, 0)
        
        # Add spacing
        para.paragraph_format.space_after = Pt(12)

@app.route('/generate-document', methods=['POST'])
def generate_document():
    try:
        data = request.json
        text = data.get('text', '')
text = text.replace('\\n', '\n')  # Convert literal \n to actual newlines        
        if not text:
            return jsonify({'error': 'No text provided'}), 400
        
        # Create document
        doc = Document()
        
        # Setup margins
        sections = doc.sections
        for section in sections:
            section.top_margin = Inches(1)
            section.bottom_margin = Inches(1)
            section.left_margin = Inches(1)
            section.right_margin = Inches(1)
        
        # Add header and footer
        add_header_footer(doc)
        
        # Format content
        format_content(doc, text)
        
        # Save to BytesIO
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
