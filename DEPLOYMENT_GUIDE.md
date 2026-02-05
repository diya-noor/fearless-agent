# Fearless Document Formatter - Complete Setup Guide

## Overview
This n8n agent automatically formats any text with Fearless branding, including:
- Branded header with logo
- Styled content (titles, subtitles, body text)
- Branded footer with contact information
- Proper Montserrat font family
- Fearless color scheme (#ee5340 primary)

---

## PART 1: Deploy Python Service

### Option A: Docker (Recommended)

1. **Build the Docker image:**
```bash
docker build -t fearless-docx-service .
```

2. **Run the container:**
```bash
docker run -d -p 5000:5000 --name fearless-docx fearless-docx-service
```

3. **Test the service:**
```bash
curl http://localhost:5000/health
```

### Option B: Direct Python Installation

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Run the service:**
```bash
python fearless_docx_service.py
```

3. **Service will run on:** `http://localhost:5000`

---

## PART 2: Setup n8n Workflow

### Method 1: Import JSON (Easiest)

1. Open n8n interface
2. Click **"Import from File"** or **"Import from URL"**
3. Select `n8n_workflow.json`
4. Workflow will appear with all nodes configured

### Method 2: Manual Setup

#### Step 1: Create Webhook Trigger
1. Add "Webhook" node
2. Configure:
   - HTTP Method: `POST`
   - Path: `format-document`
   - Response Mode: "When Last Node Finishes"

#### Step 2: Extract Input
1. Add "Set" node
2. Add assignment:
   - Name: `text`
   - Value: `={{ $json.body.text }}`

#### Step 3: Call Python Service
1. Add "HTTP Request" node
2. Configure:
   - URL: `http://localhost:5000/generate-document` (or your service URL)
   - Method: `POST`
   - Headers: `Content-Type: application/json`
   - Body: 
     ```json
     {
       "text": "={{ $json.text }}"
     }
     ```
   - Response Format: **File/Binary**

#### Step 4: Check Success
1. Add "IF" node
2. Condition: `content-type` contains `application/vnd.openxmlformats`

#### Step 5: Return Document
1. Add "Respond to Webhook" node (True branch)
2. Respond With: `Binary`
3. Headers:
   - `Content-Type`: `application/vnd.openxmlformats-officedocument.wordprocessingml.document`
   - `Content-Disposition`: `attachment; filename=fearless_branded_document.docx`

#### Step 6: Error Handling
1. Add "Respond to Webhook" node (False branch)
2. Respond With: `JSON`
3. Body: `{"error": "Failed to generate document"}`
4. Status Code: `500`

---

## PART 3: Customize Branding

### Update Header/Footer in Python Service

Edit `fearless_docx_service.py`:

```python
def add_header_footer(doc):
    section = doc.sections[0]
    header = section.header
    header_para = header.paragraphs[0]
    
    # ADD LOGO
    # Download logo and add path
    header_run = header_para.add_run()
    # Uncomment when you have logo file:
    # header_run.add_picture('fearless_logo.png', width=Inches(1.5))
    header_para.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    
    # CUSTOMIZE FOOTER
    footer = section.footer
    footer_para = footer.paragraphs[0]
    
    # Update company name and info
    footer_run = footer_para.add_run("Fearless | ")
    footer_run.font.name = 'Montserrat'
    footer_run.font.size = Pt(9)
    
    # Add website/contact
    contact_run = footer_para.add_run("contact@fearless.com | +1-xxx-xxx-xxxx")
    contact_run.font.name = 'Montserrat'
    contact_run.font.size = Pt(9)
    contact_run.font.color.rgb = RGBColor(238, 83, 64)
```

### Get Actual Brand Assets

1. Visit: `https://fearless.lingoapp.com/s/Overview-oENEEv?v=0`
2. Download:
   - Fearless logo (PNG/SVG)
   - Official color codes
   - Any additional brand guidelines
3. Update the Python service with actual assets

---

## PART 4: Usage

### Test the Workflow

1. **Activate workflow** in n8n (toggle switch)
2. **Copy webhook URL** from Webhook node
3. **Test with curl:**

```bash
curl -X POST http://your-n8n-domain/webhook/format-document \
  -H "Content-Type: application/json" \
  -d '{
    "text": "# Welcome to Fearless\n\nThis is a test document.\n\n## Section 1\n\nThis is some body text that will be formatted with Fearless branding.\n\n## Section 2\n\nMore content here with proper styling."
  }' \
  --output fearless_test.docx
```

### Text Formatting Syntax

Use markdown-style headings in your text:

```
# Main Title (Montserrat Alternates Bold, #ee5340, 18pt)

## Subtitle (Montserrat Bold, 14pt)

### Sub-section (Montserrat Bold, 12pt)

Regular paragraph text (Montserrat, 10pt)

Multiple paragraphs are separated by blank lines.
```

---

## PART 5: Deploy to Client

### Option 1: Cloud Deployment (Recommended)

**Deploy Python Service:**
1. Use Railway, Render, or Heroku
2. Push Docker image
3. Get service URL (e.g., `https://fearless-docx.railway.app`)

**Update n8n:**
4. Replace `localhost:5000` with cloud URL in HTTP Request node

**Share with Client:**
5. Provide webhook URL
6. Create simple frontend form if needed

### Option 2: Docker Compose (Self-hosted)

Create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  n8n:
    image: n8nio/n8n
    ports:
      - "5678:5678"
    environment:
      - N8N_BASIC_AUTH_ACTIVE=true
      - N8N_BASIC_AUTH_USER=admin
      - N8N_BASIC_AUTH_PASSWORD=password
    volumes:
      - n8n_data:/home/node/.n8n
    networks:
      - fearless-network

  docx-service:
    build: .
    ports:
      - "5000:5000"
    networks:
      - fearless-network

volumes:
  n8n_data:

networks:
  fearless-network:
    driver: bridge
```

Deploy:
```bash
docker-compose up -d
```

### Option 3: Client Frontend Integration

Create a simple HTML form for clients:

```html
<!DOCTYPE html>
<html>
<head>
    <title>Fearless Document Generator</title>
    <style>
        body {
            font-family: 'Montserrat', sans-serif;
            max-width: 800px;
            margin: 50px auto;
            padding: 20px;
        }
        textarea {
            width: 100%;
            min-height: 300px;
            font-family: 'Montserrat', monospace;
            padding: 15px;
            border: 2px solid #ee5340;
            border-radius: 8px;
        }
        button {
            background: #ee5340;
            color: white;
            border: none;
            padding: 15px 30px;
            font-size: 16px;
            border-radius: 8px;
            cursor: pointer;
            margin-top: 20px;
        }
        button:hover {
            background: #d64a36;
        }
    </style>
</head>
<body>
    <h1 style="color: #ee5340;">Fearless Document Generator</h1>
    <p>Enter your text below. Use # for titles, ## for subtitles.</p>
    
    <textarea id="documentText" placeholder="# Your Title Here

## Subtitle

Your content goes here..."></textarea>
    
    <button onclick="generateDocument()">Generate Branded Document</button>
    
    <script>
        async function generateDocument() {
            const text = document.getElementById('documentText').value;
            
            try {
                const response = await fetch('YOUR_WEBHOOK_URL_HERE', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ text: text })
                });
                
                if (response.ok) {
                    const blob = await response.blob();
                    const url = window.URL.createObjectURL(blob);
                    const a = document.createElement('a');
                    a.href = url;
                    a.download = 'fearless_document.docx';
                    document.body.appendChild(a);
                    a.click();
                    window.URL.revokeObjectURL(url);
                    alert('Document generated successfully!');
                } else {
                    alert('Error generating document');
                }
            } catch (error) {
                alert('Error: ' + error.message);
            }
        }
    </script>
</body>
</html>
```

---

## PART 6: Advanced Customization

### Add Logo to Header

1. Download Fearless logo from brand portal
2. Place in same directory as Python script
3. Uncomment logo code in `add_header_footer()`:

```python
header_run.add_picture('fearless_logo.png', width=Inches(1.5))
```

### Custom Styling Rules

Add more heading levels or custom styles:

```python
# In format_content() function
if para_text.startswith('**'):  # Custom callout
    run.font.name = 'Montserrat'
    run.font.size = Pt(11)
    run.font.color.rgb = RGBColor(238, 83, 64)
    run.font.bold = True
```

### Multiple Brand Templates

Add template parameter:

```python
@app.route('/generate-document', methods=['POST'])
def generate_document():
    data = request.json
    text = data.get('text', '')
    template = data.get('template', 'default')  # New parameter
    
    if template == 'letterhead':
        # Use letterhead styling
        pass
    elif template == 'report':
        # Use report styling
        pass
```

---

## Troubleshooting

### Python Service Issues

**Port already in use:**
```bash
# Kill existing process
lsof -ti:5000 | xargs kill -9
# Or use different port
python fearless_docx_service.py --port 5001
```

**Font not found:**
- Install Montserrat fonts on server
- Or embed fonts in DOCX (modify python-docx usage)

### n8n Issues

**Webhook not responding:**
- Ensure workflow is activated
- Check webhook URL is correct
- Verify n8n is publicly accessible

**Binary data not downloading:**
- Confirm Response Format is set to "File"
- Check Content-Type header in response

---

## Cost & Scaling

### Free Tier Options:
- Railway: 500 hours/month free
- Render: Free tier available
- n8n Cloud: Free plan (limited executions)

### Production Recommendations:
- Use managed services for reliability
- Add rate limiting
- Implement authentication
- Cache generated documents
- Add monitoring (Sentry, LogRocket)

---

## Support & Maintenance

### Update Brand Assets:
1. Edit `fearless_docx_service.py`
2. Rebuild Docker image
3. Redeploy service

### Monitor Usage:
- Add logging to Python service
- Use n8n's execution history
- Track document generation metrics

---

## Client Handoff Checklist

- [ ] Python service deployed and tested
- [ ] n8n workflow imported and activated  
- [ ] Webhook URL shared with client
- [ ] Documentation provided
- [ ] Sample documents generated
- [ ] Client tested successfully
- [ ] Backup/disaster recovery plan in place
- [ ] Support contact information shared
