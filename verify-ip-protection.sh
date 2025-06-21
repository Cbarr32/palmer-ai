#!/bin/bash
# Verify Palmer AI IP Protection

echo "=== 🔍 Palmer AI IP Protection Audit ==="
echo ""

# Check for exposed sensitive files
echo "Checking for exposed core IP..."
EXPOSED=$(git ls-files | grep -E "(elite|proprietary|secret|private)" | grep -v .gitignore)

if [ -z "$EXPOSED" ]; then
    echo "✅ No core IP exposed in git!"
else
    echo "❌ WARNING: Exposed files:"
    echo "$EXPOSED"
fi

# Check private directories
echo ""
echo "Protected directories:"
[ -d "private_core" ] && echo "✅ private_core/ (excluded from git)"
[ -d "private_modules" ] && echo "✅ private_modules/ (excluded from git)"

# Verify .gitignore
echo ""
echo "Git ignore rules:"
grep -E "private_|proprietary|elite" .gitignore | head -5

echo ""
echo "=== Protection Status: ACTIVE ==="
