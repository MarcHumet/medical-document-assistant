#!/bin/bash
# Test script para funcionalidad de carga de documentos PDF

echo "🧪 Testing PDF Document Upload Functionality"
echo "=============================================="

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuración
API_URL="http://localhost:8000"
USERNAME="medical_researcher"
PASSWORD="demo_password_123"

echo -e "${BLUE}📍 Step 1: Getting authentication token...${NC}"

# Obtener token de autenticación
TOKEN_RESPONSE=$(curl -s -X POST "$API_URL/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=$USERNAME&password=$PASSWORD")

if [[ $? -ne 0 ]]; then
    echo -e "${RED}❌ Failed to connect to API${NC}"
    exit 1
fi

# Extraer token del response JSON
TOKEN=$(echo $TOKEN_RESPONSE | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    print(data['access_token'])
except:
    print('ERROR')
")

if [[ "$TOKEN" == "ERROR" ]]; then
    echo -e "${RED}❌ Failed to get authentication token${NC}"
    echo "Response: $TOKEN_RESPONSE"
    exit 1
fi

echo -e "${GREEN}✅ Authentication token obtained${NC}"

echo -e "${BLUE}📍 Step 2: Using existing PDF document...${NC}"

# Usar el documento PDF existente
TEST_FILE="../DA Technical Challenge.pdf"

if [[ -f "$TEST_FILE" ]]; then
    echo -e "${GREEN}✅ Found PDF document: $TEST_FILE${NC}"
    echo -e "${BLUE}   File size: $(du -h "$TEST_FILE" | cut -f1)${NC}"
else
    echo -e "${RED}❌ PDF document not found: $TEST_FILE${NC}"
    exit 1
fi

echo -e "${BLUE}📍 Step 3: Uploading document to API...${NC}"

# Subir documento
UPLOAD_RESPONSE=$(curl -s -X POST "$API_URL/upload" \
  -H "Authorization: Bearer $TOKEN" \
  -F "file=@$TEST_FILE")

if [[ $? -ne 0 ]]; then
    echo -e "${RED}❌ Failed to upload document${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Upload response:${NC}"
echo "$UPLOAD_RESPONSE" | python3 -m json.tool 2>/dev/null || echo "$UPLOAD_RESPONSE"

echo -e "${BLUE}📍 Step 4: Listing uploaded documents...${NC}"

# Listar documentos
DOCS_RESPONSE=$(curl -s -X GET "$API_URL/documents" \
  -H "Authorization: Bearer $TOKEN")

echo -e "${GREEN}✅ Documents list:${NC}"
echo "$DOCS_RESPONSE" | python3 -m json.tool 2>/dev/null || echo "$DOCS_RESPONSE"

echo -e "${BLUE}📍 Step 5: Testing question about the document...${NC}"

# Hacer una pregunta sobre el documento
QUESTION_RESPONSE=$(curl -s -X POST "$API_URL/ask" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"question": "What is this document about? Can you summarize the main content?"}')

echo -e "${GREEN}✅ Question response:${NC}"
echo "$QUESTION_RESPONSE" | python3 -m json.tool 2>/dev/null || echo "$QUESTION_RESPONSE"

echo -e "${BLUE}📍 Step 6: Cleanup...${NC}"

# No eliminar el archivo original, solo archivos temporales
echo -e "${GREEN}✅ Test completed! (Original PDF preserved)${NC}"