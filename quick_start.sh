#!/bin/bash

# Fearless Document Formatter - Quick Start Script

echo "========================================="
echo "Fearless Document Formatter Setup"
echo "========================================="
echo ""

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    echo "Visit: https://docs.docker.com/get-docker/"
    exit 1
fi

echo "✓ Docker found"
echo ""

# Step 1: Build Docker image
echo "Step 1: Building Docker image..."
docker build -t fearless-docx-service . || {
    echo "❌ Failed to build Docker image"
    exit 1
}
echo "✓ Docker image built successfully"
echo ""

# Step 2: Stop existing container if running
echo "Step 2: Checking for existing container..."
if docker ps -a | grep -q fearless-docx; then
    echo "Stopping and removing existing container..."
    docker stop fearless-docx 2>/dev/null
    docker rm fearless-docx 2>/dev/null
fi
echo "✓ Ready to start fresh"
echo ""

# Step 3: Start the container
echo "Step 3: Starting Python service..."
docker run -d -p 5000:5000 --name fearless-docx fearless-docx-service || {
    echo "❌ Failed to start container"
    exit 1
}
echo "✓ Service started on http://localhost:5000"
echo ""

# Step 4: Wait for service to be ready
echo "Step 4: Waiting for service to be ready..."
sleep 3

# Step 5: Test the service
echo "Step 5: Testing service health..."
HEALTH_CHECK=$(curl -s http://localhost:5000/health)
if [[ $HEALTH_CHECK == *"healthy"* ]]; then
    echo "✓ Service is healthy and ready!"
else
    echo "❌ Service health check failed"
    echo "Response: $HEALTH_CHECK"
    exit 1
fi
echo ""

# Step 6: Generate test document
echo "Step 6: Generating test document..."
curl -X POST http://localhost:5000/generate-document \
  -H "Content-Type: application/json" \
  -d '{
    "text": "# Fearless Document Test\n\nThis is a test document to verify the branding system is working correctly.\n\n## Features\n\nThe document includes:\n- Branded header\n- Proper font styling\n- Fearless color scheme\n- Professional footer\n\n## Next Steps\n\nIntegrate this service with n8n and start formatting documents with Fearless branding!"
  }' \
  --output fearless_test.docx

if [ -f fearless_test.docx ]; then
    echo "✓ Test document generated: fearless_test.docx"
else
    echo "❌ Failed to generate test document"
    exit 1
fi
echo ""

echo "========================================="
echo "✓ Setup Complete!"
echo "========================================="
echo ""
echo "Service URL: http://localhost:5000"
echo "Test Document: ./fearless_test.docx"
echo ""
echo "Next Steps:"
echo "1. Open n8n"
echo "2. Import n8n_workflow.json"
echo "3. Update HTTP Request node URL to: http://localhost:5000/generate-document"
echo "4. Activate the workflow"
echo "5. Test with the webhook URL"
echo ""
echo "To view logs: docker logs -f fearless-docx"
echo "To stop service: docker stop fearless-docx"
echo "To restart: docker start fearless-docx"
echo ""
