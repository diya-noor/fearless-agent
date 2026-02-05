# API Usage Examples

## Basic Request

### Simple Document

**Request:**
```bash
curl -X POST https://your-webhook-url/format-document \
  -H "Content-Type: application/json" \
  -d '{
    "text": "# Welcome to Fearless\n\nWe are excited to work with you."
  }' \
  --output welcome.docx
```

**Output:** `welcome.docx` with:
- "Welcome to Fearless" as title (18pt, #ee5340, Montserrat Alternates Bold)
- Body text (10pt, Montserrat)
- Fearless header and footer

---

## Business Report

### Quarterly Report

**Request:**
```bash
curl -X POST https://your-webhook-url/format-document \
  -H "Content-Type: application/json" \
  -d '{
    "text": "# Q4 2025 Performance Report\n\n## Executive Summary\n\nFearless achieved record growth in Q4 2025, with revenue increasing 45% year-over-year.\n\n## Financial Highlights\n\n### Revenue\n\nTotal revenue: $2.5M\nGrowth rate: 45% YoY\n\n### Key Metrics\n\nCustomer acquisition increased by 60%.\nChurn rate decreased to 2.1%.\n\n## Strategic Initiatives\n\nWe launched three major product features in Q4:\n\n- Advanced analytics dashboard\n- API integrations marketplace  \n- Mobile app for iOS and Android\n\n## Looking Ahead\n\nQ1 2026 will focus on expanding our enterprise offerings and strengthening customer success operations."
  }' \
  --output q4_report.docx
```

**Output:** Professional report with:
- Title: "Q4 2025 Performance Report" (main title styling)
- Section headers: "Executive Summary", "Financial Highlights" (subtitle styling)
- Subsections: "Revenue", "Key Metrics" (H3 styling)
- Body text with proper spacing
- Branded header/footer

---

## Marketing Materials

### Product Launch Announcement

**Request:**
```bash
curl -X POST https://your-webhook-url/format-document \
  -H "Content-Type: application/json" \
  -d '{
    "text": "# Introducing Fearless Pro\n\n## The Next Evolution in Brand Management\n\nWe are thrilled to announce Fearless Pro, our most powerful brand management platform yet.\n\n## What'\''s New\n\n### AI-Powered Brand Guidelines\n\nAutomatically generate brand guidelines from your existing assets.\n\n### Real-Time Collaboration\n\nWork together with your team in real-time, no matter where they are.\n\n### Advanced Analytics\n\nTrack brand consistency across all channels with detailed metrics.\n\n## Pricing & Availability\n\nFearless Pro is available now starting at $99/month.\n\nVisit fearless.com/pro to learn more and start your free trial."
  }' \
  --output product_launch.docx
```

---

## Client Proposals

### Partnership Proposal

**Request:**
```bash
curl -X POST https://your-webhook-url/format-document \
  -H "Content-Type: application/json" \
  -d '{
    "text": "# Strategic Partnership Proposal\n\n## Prepared for: ABC Corporation\n\n## Overview\n\nFearless is excited to propose a strategic partnership that will help ABC Corporation strengthen its brand presence and streamline marketing operations.\n\n## Partnership Benefits\n\n### For ABC Corporation\n\n- Reduce brand inconsistency by 80%\n- Accelerate content creation by 3x\n- Improve team collaboration\n\n### For Fearless\n\n- Access to enterprise market insights\n- Co-marketing opportunities\n- Case study and testimonial content\n\n## Investment & Timeline\n\n### Phase 1: Discovery (Month 1)\n\nBrand audit and requirements gathering.\n\n### Phase 2: Implementation (Months 2-3)\n\nPlatform setup and team training.\n\n### Phase 3: Optimization (Month 4+)\n\nOngoing support and feature enhancement.\n\n## Next Steps\n\nWe propose a 30-minute call to discuss this opportunity further.\n\nLet'\''s schedule a time that works for you."
  }' \
  --output partnership_proposal.docx
```

---

## Internal Communications

### Team Memo

**Request:**
```bash
curl -X POST https://your-webhook-url/format-document \
  -H "Content-Type: application/json" \
  -d '{
    "text": "# Important Update: New Brand Guidelines\n\n## To: All Team Members\n\n## Date: February 5, 2026\n\n## Overview\n\nEffective immediately, all team members should use the updated Fearless brand guidelines when creating any external-facing materials.\n\n## What'\''s Changed\n\n### Logo Usage\n\nWe now have three approved logo variations:\n- Full color (primary)\n- White (for dark backgrounds)\n- Monochrome (for special applications)\n\n### Color Palette\n\nOur primary brand color (#ee5340) should be used more prominently in all designs.\n\n### Typography\n\nMontserrat is now our exclusive font family for all materials.\n\n## Action Items\n\n- Review the updated guidelines at fearless.com/brand\n- Update any templates you'\''re currently using\n- Attend the brand training session next Tuesday at 2pm\n\n## Questions\n\nContact the marketing team at brand@fearless.com with any questions."
  }' \
  --output team_memo.docx
```

---

## Meeting Minutes

### Board Meeting

**Request:**
```bash
curl -X POST https://your-webhook-url/format-document \
  -H "Content-Type: application/json" \
  -d '{
    "text": "# Board Meeting Minutes\n\n## January 30, 2026\n\n## Attendees\n\n- Jane Smith, CEO\n- John Doe, CFO\n- Sarah Johnson, CMO\n- Michael Chen, CTO\n\n## Agenda Items\n\n### Financial Review\n\nCFO presented Q4 financial results. Revenue exceeded projections by 12%.\n\nBoard approved FY2026 budget.\n\n### Strategic Planning\n\nDiscussed expansion into European market. Timeline: Q3 2026.\n\nCEO to prepare detailed market analysis for next meeting.\n\n### Product Roadmap\n\nCTO presented 2026 product roadmap. Key highlights:\n- Mobile app launch (Q1)\n- Enterprise features (Q2)\n- API marketplace (Q3)\n\nBoard provided feedback on prioritization.\n\n## Action Items\n\n- Jane: Prepare European market analysis (Due: Feb 15)\n- John: Finalize FY2026 budget documentation (Due: Feb 10)\n- Sarah: Launch Q1 marketing campaign (Due: Feb 5)\n- Michael: Begin mobile app development (Due: Ongoing)\n\n## Next Meeting\n\nMarch 15, 2026 at 10:00 AM"
  }' \
  --output board_minutes.docx
```

---

## JavaScript/Node.js Example

### Using Fetch API

```javascript
async function generateDocument(text) {
    try {
        const response = await fetch('https://your-webhook-url/format-document', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ text })
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const blob = await response.blob();
        
        // Download in browser
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'fearless_document.docx';
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        a.remove();
        
        console.log('Document generated successfully!');
    } catch (error) {
        console.error('Error generating document:', error);
    }
}

// Usage
const sampleText = `# My Document

## Introduction

This is sample content.`;

generateDocument(sampleText);
```

---

## Python Example

### Using Requests Library

```python
import requests

def generate_fearless_document(text, output_filename='fearless_document.docx'):
    """
    Generate a Fearless-branded document from text
    
    Args:
        text (str): The content to format
        output_filename (str): Output file name
    
    Returns:
        bool: True if successful, False otherwise
    """
    url = 'https://your-webhook-url/format-document'
    
    try:
        response = requests.post(
            url,
            json={'text': text},
            headers={'Content-Type': 'application/json'},
            timeout=30
        )
        
        response.raise_for_status()
        
        # Save the document
        with open(output_filename, 'wb') as f:
            f.write(response.content)
        
        print(f"✓ Document saved: {output_filename}")
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"✗ Error: {e}")
        return False

# Usage
sample_text = """# Project Proposal

## Overview

This is a sample project proposal document.

## Budget

Total: $50,000

## Timeline

Duration: 3 months
"""

generate_fearless_document(sample_text, 'proposal.docx')
```

---

## PHP Example

### Using cURL

```php
<?php

function generateFearlessDocument($text, $outputFilename = 'fearless_document.docx') {
    $url = 'https://your-webhook-url/format-document';
    
    $data = json_encode(['text' => $text]);
    
    $ch = curl_init($url);
    curl_setopt($ch, CURLOPT_POST, true);
    curl_setopt($ch, CURLOPT_POSTFIELDS, $data);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_HTTPHEADER, [
        'Content-Type: application/json',
        'Content-Length: ' . strlen($data)
    ]);
    
    $response = curl_exec($ch);
    $httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
    curl_close($ch);
    
    if ($httpCode === 200) {
        file_put_contents($outputFilename, $response);
        echo "✓ Document saved: $outputFilename\n";
        return true;
    } else {
        echo "✗ Error: HTTP $httpCode\n";
        return false;
    }
}

// Usage
$sampleText = "# Annual Report\n\n## Financial Results\n\nRevenue: $5M";
generateFearlessDocument($sampleText, 'annual_report.docx');

?>
```

---

## Common Text Formatting Patterns

### Headers

```
# Main Title (Level 1)
## Section Title (Level 2)
### Subsection Title (Level 3)
```

### Lists

```
Items to include:
- First item
- Second item
- Third item

Numbered lists:
1. Step one
2. Step two
3. Step three
```

### Emphasis

```
Standard paragraph text flows naturally.

To create a new paragraph, use double line breaks.

Each paragraph gets proper spacing automatically.
```

### Long Documents

```
# Report Title

## Executive Summary

Brief overview here.

## Section 1: Introduction

Detailed content...

## Section 2: Analysis

### Subsection 2.1

Content here...

### Subsection 2.2

More content...

## Section 3: Conclusions

Final thoughts...
```

---

## Error Handling

### Invalid Request

**Request with missing text:**
```bash
curl -X POST https://your-webhook-url/format-document \
  -H "Content-Type: application/json" \
  -d '{}' 
```

**Response:**
```json
{
  "error": "No text provided"
}
```
**Status:** 400

### Service Error

**Response when service is down:**
```json
{
  "error": "Failed to generate document",
  "details": "Connection timeout"
}
```
**Status:** 500

---

## Best Practices

### 1. Keep Text Structured

✅ **Good:**
```
# Main Title

## Section 1

Content here.

## Section 2

More content.
```

❌ **Avoid:**
```
Main TitleSection 1Content hereSection 2More content
```

### 2. Use Consistent Heading Levels

✅ **Good:**
```
# Title
## Section
### Subsection
```

❌ **Avoid:**
```
### Small Header
# Big Header After Small
```

### 3. Separate Paragraphs Properly

✅ **Good:**
```
First paragraph here.

Second paragraph here.
```

❌ **Avoid:**
```
First paragraph here.
Second paragraph here.
```

### 4. Test with Sample Content First

Always test with a small document before generating large reports.

---

## Limitations

- Maximum text length: 100,000 characters
- Supported format: Plain text with markdown-style headers
- Images: Not currently supported in text input (header/footer images supported via branding)
- Tables: Not supported (coming in v2.0)
- Custom fonts: Montserrat family only

---

## Need Help?

Contact support with:
- The text you're trying to format
- The error message received
- When the issue started occurring

Response time: Within 24 hours
