FROM python:3.11-slim

WORKDIR /app

# Copy requirements
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY fearless_docx_service.py .

# Expose port
EXPOSE 5000

# Run the application
CMD ["python", "fearless_docx_service.py"]
