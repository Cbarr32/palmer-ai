#!/bin/bash
# Palmer AI Development Manager - Windows Git Bash Edition

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
BACKEND_PORT=8000
FRONTEND_PORT=3000
PROJECT_ROOT="$HOME/dev/palmerai"

# Change to project directory
cd "$PROJECT_ROOT" || exit 1

case "$1" in
    start)
        echo -e "${BLUE}🚀 Starting Palmer AI Development Environment${NC}"
        echo "============================================="
        
        # Kill any existing processes
        echo -e "${YELLOW}Cleaning up existing processes...${NC}"
        taskkill //F //IM python.exe 2>/dev/null || true
        taskkill //F //IM node.exe 2>/dev/null || true
        sleep 2
        
        # Start backend
        echo -e "${GREEN}Starting Backend...${NC}"
        python -m uvicorn src.palmer_ai.server:app --reload --host 0.0.0.0 --port $BACKEND_PORT > backend.log 2>&1 &
        BACKEND_PID=$!
        echo "Backend PID: $BACKEND_PID" > .palmer-pids
        
        # Wait for backend
        echo -n "Waiting for backend to start"
        for i in {1..10}; do
            if curl -s http://localhost:$BACKEND_PORT/health > /dev/null; then
                echo -e " ${GREEN}✓${NC}"
                break
            fi
            echo -n "."
            sleep 1
        done
        
        # Start frontend
        echo -e "${GREEN}Starting Frontend...${NC}"
        cd frontend
        npm run dev > ../frontend.log 2>&1 &
        FRONTEND_PID=$!
        echo "Frontend PID: $FRONTEND_PID" >> ../.palmer-pids
        cd ..
        
        # Wait for frontend
        echo -n "Waiting for frontend to start"
        for i in {1..10}; do
            if curl -s http://localhost:$FRONTEND_PORT > /dev/null 2>&1; then
                echo -e " ${GREEN}✓${NC}"
                break
            fi
            echo -n "."
            sleep 1
        done
        
        echo ""
        echo -e "${GREEN}✅ Palmer AI is running!${NC}"
        echo "========================"
        echo "🎨 Frontend: http://localhost:$FRONTEND_PORT"
        echo "🔧 Backend:  http://localhost:$BACKEND_PORT"
        echo "📚 API Docs: http://localhost:$BACKEND_PORT/docs"
        echo ""
        echo "📝 Commands:"
        echo "   ./palmer-dev-manager.sh status  # Check status"
        echo "   ./palmer-dev-manager.sh logs    # View logs"
        echo "   ./palmer-dev-manager.sh stop    # Stop all"
        echo "   ./palmer-dev-manager.sh test    # Run tests"
        ;;
        
    stop)
        echo -e "${RED}🛑 Stopping Palmer AI...${NC}"
        taskkill //F //IM python.exe 2>/dev/null || true
        taskkill //F //IM node.exe 2>/dev/null || true
        rm -f .palmer-pids
        echo "✅ All services stopped"
        ;;
        
    status)
        echo -e "${BLUE}📊 Palmer AI Status${NC}"
        echo "==================="
        echo -n "Backend:  "
        if curl -s http://localhost:$BACKEND_PORT/health > /dev/null 2>&1; then
            echo -e "${GREEN}✓ Running${NC}"
        else
            echo -e "${RED}✗ Stopped${NC}"
        fi
        echo -n "Frontend: "
        if curl -s http://localhost:$FRONTEND_PORT > /dev/null 2>&1; then
            echo -e "${GREEN}✓ Running${NC}"
        else
            echo -e "${RED}✗ Stopped${NC}"
        fi
        ;;
        
    logs)
        echo -e "${BLUE}📝 Palmer AI Logs${NC}"
        echo "================="
        echo -e "${YELLOW}Backend (last 10 lines):${NC}"
        tail -10 backend.log
        echo ""
        echo -e "${YELLOW}Frontend (last 10 lines):${NC}"
        tail -10 frontend.log
        ;;
        
    test)
        echo -e "${BLUE}🧪 Running Palmer AI Tests${NC}"
        echo "=========================="
        echo -e "${YELLOW}Testing backend health...${NC}"
        curl -s http://localhost:$BACKEND_PORT/health | python -m json.tool
        echo ""
        echo -e "${YELLOW}Testing API endpoints...${NC}"
        curl -s -X POST http://localhost:$BACKEND_PORT/api/v1/analyze \
            -H "Content-Type: application/json" \
            -d '{"url":"https://example.com","analysis_type":"quick"}' | python -m json.tool || echo "⚠️ Analyze endpoint needs implementation"
        ;;
        
    *)
        echo "Usage: $0 {start|stop|status|logs|test}"
        exit 1
        ;;
esac
