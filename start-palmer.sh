#!/bin/bash

# Palmer AI Integrated Development Environment
# Optimized for rapid development and testing

set -e

# Colors for beautiful output
BLUE='\033[0;34m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
PURPLE='\033[0;35m'
NC='\033[0m'

echo -e "${PURPLE}"
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║                    🚀 Palmer AI Platform                     ║"
echo "║              Conversational B2B Intelligence                ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

echo -e "${GREEN}🎯 System Endpoints:${NC}"
echo -e "   Frontend: ${BLUE}http://localhost:3000${NC}"
echo -e "   Backend:  ${BLUE}http://localhost:8000${NC}"
echo -e "   API Docs: ${BLUE}http://localhost:8000/docs${NC}"
echo ""

# Environment check
if [[ ! -f ".env" ]]; then
    echo -e "${YELLOW}⚠️  Creating .env file from template...${NC}"
    cp .env.example .env
    echo -e "${YELLOW}   Please update .env with your ANTHROPIC_API_KEY${NC}"
    echo ""
fi

# Cleanup function
cleanup() {
    echo -e "\n${YELLOW}🛑 Shutting down Palmer AI...${NC}"
    jobs -p | xargs -r kill 2>/dev/null || true
    echo -e "${GREEN}✅ Cleanup complete${NC}"
    exit 0
}
trap cleanup SIGINT SIGTERM

# Start backend
echo -e "${BLUE}🔧 Starting Palmer AI Backend...${NC}"
python -m uvicorn src.palmer_ai.server:app --reload --host 0.0.0.0 --port 8000 > backend.log 2>&1 &
BACKEND_PID=$!

# Wait for backend
echo -e "${YELLOW}   Initializing backend services...${NC}"
sleep 5

# Check backend health
if kill -0 $BACKEND_PID 2>/dev/null; then
    echo -e "${GREEN}✅ Backend running (PID: $BACKEND_PID)${NC}"
else
    echo -e "${RED}❌ Backend failed to start${NC}"
    cat backend.log
    exit 1
fi

# Start frontend
echo -e "${BLUE}🎨 Starting Palmer AI Frontend...${NC}"
cd frontend
npm run dev > ../frontend.log 2>&1 &
FRONTEND_PID=$!
cd ..

# Wait for frontend
echo -e "${YELLOW}   Building frontend application...${NC}"
sleep 8

echo ""
echo -e "${GREEN}╔══════════════════════════════════════════════════════════════╗"
echo -e "${GREEN}║                   🎉 PALMER AI READY 🎉                     ║"
echo -e "${GREEN}╚══════════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${BLUE}🚀 Quick Start Guide:${NC}"
echo -e "   1. Open: ${GREEN}http://localhost:3000${NC}"
echo -e "   2. Try: ${YELLOW}'I have 500 HVAC products with terrible descriptions'${NC}"
echo -e "   3. Upload: ${YELLOW}Excel/CSV files for AI enhancement${NC}"
echo -e "   4. Test: ${YELLOW}B2B product intelligence features${NC}"
echo ""
echo -e "${PURPLE}💡 Pro Tips:${NC}"
echo -e "   • Drag & drop files directly into the chat"
echo -e "   • Use suggested actions for quick workflows"
echo -e "   • Monitor system status in the header"
echo ""
echo -e "${YELLOW}Press Ctrl+C to stop all services${NC}"

# Keep running
while true; do
    sleep 10
    # Check if processes are still running
    if ! kill -0 $BACKEND_PID 2>/dev/null; then
        echo -e "${RED}❌ Backend process died${NC}"
        break
    fi
    if ! kill -0 $FRONTEND_PID 2>/dev/null; then
        echo -e "${RED}❌ Frontend process died${NC}"
        break
    fi
done

cleanup
