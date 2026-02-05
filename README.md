# Fearless Document Formatter Agent

Automated n8n agent that transforms plain text into professionally branded Fearless documents with proper headers, footers, fonts, and styling.

## 🎯 What It Does

- Takes any text input via webhook
- Applies Fearless brand styling:
  - Montserrat font family
  - Primary color (#ee5340) for titles
  - Professional header with logo
  - Branded footer with contact info
- Returns formatted DOCX file
- Zero manual formatting needed

## 📋 Requirements

- Docker (recommended) OR Python 3.11+
- n8n instance (local or cloud)
- 2GB RAM minimum
- 500MB disk space

## 🚀 Quick Start (5 minutes)

```bash
# Make script executable
chmod +x quick_start.sh

# Run setup
./quick_start.sh
```

This will:
1. Build Docker image
2. Start Python service
3. Test health endpoint
4. Generate sample document

## 📦 Project Structure

```
fearless-document-formatter/
├── fearless_docx_service.py   # Python Flask service
├── requirements.txt            # Python dependencies
├── Dockerfile                  # Docker configuration
├── n8n_workflow.json          # n8n workflow (import this)
├── DEPLOYMENT_GUIDE.md        # Complete setup guide
├── quick_start.sh             # Automated setup script
└── README.md                  # This file
```

## 🔧 Manual Setup

### 1. Start Python Service

**Option A: Docker**
```bash
docker build -t fearless-docx-service .
docker run -d -p 5000:5000 --name fearless-docx fearless-docx-service
```

**Option B: Python**
```bash
pip install -r requirements.txt
python fearless_docx_service.py
```

### 2. Import n8n Workflow

1. Open n8n
2. Click "Import from File"
3. Select `n8n_workflow.json`
4. Update HTTP Request node:
   - URL: `http://localhost:5000/generate-document`
   - (Or your deployed service URL)
5. Activate workflow

## 💡 Usage

### API Request

```bash
curl -X POST http://your-n8n-webhook-url/format-document \
  -H "Content-Type: application/json" \
  -d '{
    "text": "# Company Report\n\n## Q4 Summary\n\nRevenue increased by 25%..."
  }' \
  --output branded_document.docx
```

### Text Formatting

Use markdown-style headings:

```
# Main Title
(Montserrat Alternates Bold, #ee5340, 18pt)

## Section Title  
(Montserrat Bold, 14pt)

### Subsection
(Montserrat Bold, 12pt)

Regular paragraph text.
(Montserrat, 10pt)
```

## 🎨 Customization

### Update Branding

Edit `fearless_docx_service.py`:

**Change Colors:**
```python
# Line 57: Primary color
run.font.color.rgb = RGBColor(238, 83, 64)  # #ee5340
```

**Add Logo:**
```python
# Line 21: Uncomment and add logo file
header_run.add_picture('fearless_logo.png', width=Inches(1.5))
```

**Update Footer:**
```python
# Line 32: Customize contact info
contact_run = footer_para.add_run("your-email@fearless.com | +1-xxx-xxx-xxxx")
```

### Rebuild After Changes

```bash
docker stop fearless-docx
docker rm fearless-docx
docker build -t fearless-docx-service .
docker run -d -p 5000:5000 --name fearless-docx fearless-docx-service
```

## 🌐 Deployment Options

### Cloud Deployment (Recommended for Production)

**Railway.app:**
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login and deploy
railway login
railway init
railway up
```

**Render.com:**
1. Connect GitHub repo
2. Select "Docker" deployment
3. Auto-deploys on push

**Heroku:**
```bash
heroku create fearless-docx-service
heroku container:push web
heroku container:release web
```

### Self-Hosted with Docker Compose

See `DEPLOYMENT_GUIDE.md` for complete `docker-compose.yml` setup.

## 🔍 Testing

### Test Python Service Directly

```bash
# Health check
curl http://localhost:5000/health

# Generate document
curl -X POST http://localhost:5000/generate-document \
  -H "Content-Type: application/json" \
  -d '{"text": "# Test\n\nHello World"}' \
  --output test.docx
```

### Test n8n Workflow

1. Activate workflow in n8n
2. Copy webhook URL from Webhook node
3. Send POST request with JSON body:
   ```json
   {
     "text": "# Your Content Here"
   }
   ```

## 📊 Workflow Architecture

```
User Request
    ↓
Webhook Trigger (n8n)
    ↓
Extract Text Input
    ↓
Call Python Service → Generate DOCX
    ↓
Check Success?
    ├─ Yes → Return Document
    └─ No → Return Error
```

## 🛠️ Troubleshooting

### Service Won't Start

```bash
# Check if port 5000 is in use
lsof -i :5000

# Kill existing process
kill -9 <PID>

# Or use different port
docker run -d -p 5001:5000 --name fearless-docx fearless-docx-service
```

### Font Not Found

Install Montserrat fonts on the server:
```bash
# Ubuntu/Debian
sudo apt-get install fonts-montserrat

# Or download from Google Fonts
wget https://fonts.google.com/download?family=Montserrat
```

### Document Not Generating

Check service logs:
```bash
docker logs fearless-docx
```

Common issues:
- Missing text in request body
- Invalid JSON format
- Font files not accessible
- Memory/disk space limitations

## 📖 API Documentation

### POST /generate-document

**Request:**
```json
{
  "text": "string (required)"
}
```

**Response:**
- Success: Binary DOCX file
- Error: 
  ```json
  {
    "error": "string"
  }
  ```

**Status Codes:**
- 200: Success
- 400: Bad request (missing text)
- 500: Server error

### GET /health

**Response:**
```json
{
  "status": "healthy"
}
```

## 🔐 Security Considerations

For production deployment:

1. **Add Authentication:**
   ```python
   from functools import wraps
   
   def require_api_key(f):
       @wraps(f)
       def decorated_function(*args, **kwargs):
           api_key = request.headers.get('X-API-Key')
           if api_key != 'your-secret-key':
               return jsonify({'error': 'Invalid API key'}), 401
           return f(*args, **kwargs)
       return decorated_function
   
   @app.route('/generate-document', methods=['POST'])
   @require_api_key
   def generate_document():
       # ...
   ```

2. **Add Rate Limiting:**
   ```python
   from flask_limiter import Limiter
   
   limiter = Limiter(app, key_func=lambda: request.remote_addr)
   
   @app.route('/generate-document', methods=['POST'])
   @limiter.limit("10 per minute")
   def generate_document():
       # ...
   ```

3. **Input Validation:**
   ```python
   if len(text) > 100000:  # 100KB limit
       return jsonify({'error': 'Text too long'}), 400
   ```

## 📈 Performance Optimization

### Caching

Add Redis caching for frequently generated documents:
```python
import redis
import hashlib

cache = redis.Redis(host='localhost', port=6379)

def generate_document():
    text = request.json.get('text')
    cache_key = hashlib.md5(text.encode()).hexdigest()
    
    cached = cache.get(cache_key)
    if cached:
        return send_file(BytesIO(cached), ...)
    
    # Generate document
    # Cache result
    cache.setex(cache_key, 3600, file_stream.getvalue())
```

### Async Processing

For large documents, use background jobs:
```python
from celery import Celery

celery = Celery('tasks', broker='redis://localhost:6379')

@celery.task
def generate_document_task(text):
    # Generate document asynchronously
    pass
```

## 🧪 Testing Suite

Run automated tests:
```bash
# Install test dependencies
pip install pytest requests-mock

# Run tests
pytest tests/
```

## 📞 Client Delivery

### What to Provide Client

1. **Webhook URL** - The n8n endpoint they'll call
2. **API Documentation** - How to format text
3. **Sample Requests** - Example curl commands
4. **Frontend Integration** (optional) - HTML form or React component
5. **Support Contact** - Your contact for issues

### Sample Client Package

```
client-package/
├── API_DOCS.md           # How to use the API
├── EXAMPLES.md           # Sample requests/responses
├── frontend_form.html    # Ready-to-use HTML form
└── webhook_url.txt       # The actual URL to call
```

## 📝 License

MIT License - Free to use and modify

## 🤝 Support

- **Issues:** Check `DEPLOYMENT_GUIDE.md` troubleshooting section
- **Updates:** Rebuild Docker image and redeploy
- **Questions:** Document issues encountered for future reference

## 🎉 Success Checklist

Before delivering to client:

- [ ] Python service deployed and accessible
- [ ] n8n workflow activated
- [ ] Test document generated successfully
- [ ] Webhook URL working
- [ ] Branding assets (logo, colors) updated
- [ ] Footer contact info customized
- [ ] Documentation provided
- [ ] Client tested successfully
- [ ] Monitoring/logging enabled
- [ ] Backup plan in place

## 🔄 Version History

- **v1.0** - Initial release with core functionality
- **v1.1** - Add header/footer customization (planned)
- **v1.2** - Multiple template support (planned)
- **v2.0** - Cloud-native deployment (planned)

---

**Ready to format documents with Fearless branding! 🚀**
