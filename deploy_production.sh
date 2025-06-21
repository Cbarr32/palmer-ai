#!/bin/bash

# Palmer AI Production Deployment Script
set -e

echo "🚀 Palmer AI Production Deployment"
echo "=================================="

# Environment check
if [[ ! -f ".env" ]]; then
    echo "❌ .env file not found. Creating from template..."
    cp .env.example .env
    echo "⚠️  Please update .env with production values before deploying"
    exit 1
fi

# Production environment variables
export ENVIRONMENT=production
export DEBUG=false
export LOG_LEVEL=INFO

echo "🔧 Updating dependencies for production..."
pip install -r requirements.txt

echo "🧪 Running production readiness tests..."
python -c "
import sys
sys.path.append('src')
from palmer_ai.server_production import app
from palmer_ai.utils.metrics import metrics_collector
from palmer_ai.utils.security import security_validator
print('✅ Production imports successful')
"

echo "🛡️ Security validation..."
python -c "
from src.palmer_ai.utils.security import security_validator
test_url = 'https://palmer-apps.com'
assert security_validator.validate_url(test_url), 'URL validation failed'
print('✅ Security validation passed')
"

echo "📊 Metrics system check..."
python -c "
from src.palmer_ai.utils.metrics import metrics_collector
metrics_collector.increment_counter('deployment_test')
summary = metrics_collector.get_summary()
assert 'counters' in summary, 'Metrics system failed'
print('✅ Metrics system operational')
"

echo "🎯 Starting production server..."
echo "Frontend: http://localhost:3000"
echo "Backend: http://localhost:8000"
echo "Metrics: http://localhost:8000/metrics"
echo "Health: http://localhost:8000/health"

# Start production server
python -m uvicorn src.palmer_ai.server_production:app --host 0.0.0.0 --port 8000 --workers 4
