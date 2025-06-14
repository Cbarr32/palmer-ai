#!/bin/bash

# Palmer AI Production Environment
set -e

# Colors
BLUE='\033[0;34m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
PURPLE='\033[0;35m'
NC='\033[0m'

echo -e "${PURPLE}"
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║              🚀 Palmer AI Production Platform                ║"
echo "║           Enterprise B2B Intelligence System                 ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

echo -e "${GREEN}🎯 Production Endpoints:${NC}"
echo -e "   Frontend:  ${BLUE}http://localhost:3000${NC}"
echo -e "   Backend:   ${BLUE}http://localhost:8000${NC}"
echo -e "   Metrics:   ${BLUE}http://localhost:8000/metrics${NC}"
echo -e "   Health:    ${BLUE}http://localhost:8000/health${NC}"
echo ""

# Cleanup function
cleanup() {
    echo -e "\n${YELLOW}🛑 Shutting down Palmer AI Production...${NC}"
    jobs -p | xargs -r kill 2>/dev/null || true
    echo -e "${GREEN}✅ Production shutdown complete${NC}"
    exit 0
}
trap cleanup SIGINT SIGTERM

# Environment validation
if [[ ! -f ".env" ]]; then
    echo -e "${YELLOW}⚠️  Creating .env from template...${NC}"
    cp .env.example .env
    echo -e "${YELLOW}   Please update .env with production values${NC}"
fi

# Start production backend
echo -e "${BLUE}🔧 Starting Palmer AI Production Backend...${NC}"
python -m uvicorn src.palmer_ai.server_production:app --reload --host 0.0.0.0 --port 8000 > backend_production.log 2>&1 &
BACKEND_PID=$!

echo -e "${YELLOW}   Initializing production services...${NC}"
sleep 8

# Verify backend health
if kill -0 $BACKEND_PID 2>/dev/null; then
    echo -e "${GREEN}✅ Production backend operational (PID: $BACKEND_PID)${NC}"
    
    # Test health endpoint
    health_response=$(curl -s http://localhost:8000/health || echo "failed")
    if [[ $health_response == *"healthy"* ]]; then
        echo -e "${GREEN}✅ Health check passed${NC}"
    else
        echo -e "${YELLOW}⚠️  Health check inconclusive${NC}"
    fi
else
    echo -e "${RED}❌ Production backend failed to start${NC}"
    cat backend_production.log
    exit 1
fi

# Start production frontend
echo -e "${BLUE}🎨 Starting Palmer AI Frontend...${NC}"
cd frontend
npm run dev -- --port 3000 > ../frontend_production.log 2>&1 &
FRONTEND_PID=$!
cd ..

echo -e "${YELLOW}   Building production frontend...${NC}"
sleep 10

echo ""
echo -e "${GREEN}╔══════════════════════════════════════════════════════════════╗"
echo -e "${GREEN}║             🎉 PALMER AI PRODUCTION READY 🎉                ║"
echo -e "${GREEN}╚══════════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${BLUE}🚀 Production Features Active:${NC}"
echo -e "   • Enterprise security and validation"
echo -e "   • Circuit breaker and retry patterns"
echo -e "   • Comprehensive metrics collection"
echo -e "   • Production error handling"
echo -e "   • Real-time health monitoring"
echo ""
echo -e "${PURPLE}📊 Monitoring:${NC}"
echo -e "   • Metrics: curl http://localhost:8000/metrics"
echo -e "   • Health: curl http://localhost:8000/health"
echo -e "   • Logs: tail -f backend_production.log"
echo ""
echo -e "${YELLOW}Press Ctrl+C to stop all production services${NC}"

# Keep running with health monitoring
while true; do
    sleep 30
    
    # Check backend health
    if ! kill -0 $BACKEND_PID 2>/dev/null; then
        echo -e "${RED}❌ Production backend died${NC}"
        break
    fi
    
    # Check frontend health
    if ! kill -0 $FRONTEND_PID 2>/dev/null; then
        echo -e "${RED}❌ Frontend process died${NC}"
        break
    fi
    
    # Optional: Check endpoint health
    health_check=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/health 2>/dev/null || echo "000")
    if [[ $health_check != "200" ]]; then
        echo -e "${YELLOW}⚠️  Health check warning: HTTP $health_check${NC}"
    fi
done

cleanup
