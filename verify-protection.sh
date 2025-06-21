#!/bin/bash
echo "=== 🔍 Palmer AI IP Protection Status ==="
echo ""

# Check if private files exist
echo "Protected files:"
[ -f "private_core/prompts/palmer_ai_elite.py" ] && echo "✅ Elite prompts (SECURED)" || echo "❌ Elite prompts"
[ -f "private_core/services/business_analyzer.py" ] && echo "✅ MPB algorithm (SECURED)" || echo "❌ MPB algorithm"
[ -d "private_core/agents" ] && echo "✅ Agent intelligence (SECURED)" || echo "❌ Agent intelligence"

echo ""
echo "Public stubs in place:"
grep -q "PROPRIETARY" src/palmer_ai/prompts/palmer_ai_elite.py && echo "✅ Prompt interface" || echo "❌ Prompt interface"
grep -q "PUBLIC_INTERFACE" src/palmer_ai/services/business_analyzer.py && echo "✅ Analyzer interface" || echo "❌ Analyzer interface"

echo ""
echo "Git status (ensure no private_core/):"
git status --porcelain | grep -E "private_core|proprietary" || echo "✅ No private files staged"
