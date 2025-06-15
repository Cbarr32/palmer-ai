#!/bin/bash
# Test Palmer AI Complete GTM Suite

cd ~/dev/palmerai || exit 1

echo "🧪 Testing Palmer AI GTM Suite"
echo "=============================="

# Start server
echo "Starting Palmer AI server..."
python -m uvicorn src.palmer_ai.server:app --reload --host 0.0.0.0 --port 8000 > server.log 2>&1 &
SERVER_PID=$!
sleep 5

# Test health
echo ""
echo "1️⃣ Testing server health..."
curl -s http://localhost:8000/health | python -m json.tool

# Test RFP endpoint
echo ""
echo "2️⃣ Testing RFP analysis..."
echo "Sample RFP content" > test_rfp.txt
curl -X POST http://localhost:8000/api/v1/gtm/rfp/analyze \
  -F "rfp_file=@test_rfp.txt" \
  -F 'request={"company_name":"Acme Corp","industry":"industrial"}' | python -m json.tool

# Test battle cards
echo ""
echo "3️⃣ Testing battle card generation..."
curl -X POST http://localhost:8000/api/v1/gtm/battlecards/monitor \
  -H "Content-Type: application/json" \
  -d '{"domain":"grainger.com"}' | python -m json.tool

# Test opportunity monitoring
echo ""
echo "4️⃣ Testing opportunity intelligence..."
curl -X POST http://localhost:8000/api/v1/gtm/opportunities/monitor \
  -H "Content-Type: application/json" \
  -d '{"target_companies":["acme.com","widget.com"],"industries":["industrial"]}' | python -m json.tool

# Test analytics
echo ""
echo "5️⃣ Testing analytics summary..."
curl -s http://localhost:8000/api/v1/gtm/analytics/summary | python -m json.tool

# View API docs
echo ""
echo "📚 API Documentation available at: http://localhost:8000/docs"
echo ""
echo "✅ Test complete! Check server.log for details."

# Keep running
echo "Press Ctrl+C to stop server..."
wait $SERVER_PID
