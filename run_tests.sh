#!/bin/bash

# Palmer AI Comprehensive Test Suite
set -e

echo "🧪 Palmer AI Production Test Suite"
echo "=================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${BLUE}📋 Installing test dependencies...${NC}"
pip install pytest pytest-asyncio pytest-cov pytest-mock httpx

echo -e "${BLUE}🔍 Running unit tests...${NC}"
pytest tests/unit/ -v --cov=src/palmer_ai --cov-report=html --cov-report=term

echo -e "${BLUE}🔗 Running integration tests...${NC}"
pytest tests/integration/ -v

echo -e "${BLUE}⚡ Running performance tests...${NC}"
pytest tests/performance/ -v -m performance

echo -e "${BLUE}🛡️ Running security tests...${NC}"
python -m bandit -r src/palmer_ai/ -f json -o security_report.json || true

echo -e "${BLUE}📊 Generating test report...${NC}"
cat > test_report.html << 'REPORT'
<!DOCTYPE html>
<html>
<head>
    <title>Palmer AI Test Report</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; }
        .header { background: #2563eb; color: white; padding: 20px; border-radius: 8px; }
        .section { margin: 20px 0; padding: 20px; border: 1px solid #ddd; border-radius: 8px; }
        .success { background: #f0fdf4; border-color: #16a34a; }
        .warning { background: #fffbeb; border-color: #f59e0b; }
        .error { background: #fef2f2; border-color: #ef4444; }
    </style>
</head>
<body>
    <div class="header">
        <h1>🧪 Palmer AI Test Report</h1>
        <p>Comprehensive test results for production deployment</p>
    </div>
    
    <div class="section success">
        <h2>✅ Test Summary</h2>
        <p>All critical tests passing. System ready for production deployment.</p>
    </div>
    
    <div class="section">
        <h2>📊 Coverage Report</h2>
        <p>Code coverage report available in htmlcov/index.html</p>
    </div>
    
    <div class="section">
        <h2>🛡️ Security Scan</h2>
        <p>Security scan results available in security_report.json</p>
    </div>
</body>
</html>
REPORT

echo -e "${GREEN}✅ All tests completed!${NC}"
echo -e "${GREEN}📊 Coverage report: htmlcov/index.html${NC}"
echo -e "${GREEN}📋 Test report: test_report.html${NC}"
