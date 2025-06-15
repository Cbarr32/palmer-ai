#!/bin/bash

case "$1" in
  check)
    echo "🔍 Checking Palmer AI privacy status..."
    echo "Files in .gitignore:"
    cat .gitignore | grep -E "^\w" | tail -10
    echo ""
    echo "Sensitive files that would be exposed:"
    find . -name "*.env" -o -name "*secret*" -o -name "*key*" | grep -v node_modules
    ;;
    
  protect)
    echo "🔒 Adding file to .gitignore: $2"
    echo "$2" >> .gitignore
    git rm --cached "$2" 2>/dev/null
    echo "✅ Protected from public repo"
    ;;
    
  test-private)
    echo "🧪 Testing what private would look like..."
    echo "Your repo would disappear from:"
    echo "- https://github.com/Cbarr32/palmer-ai (404 for others)"
    echo "- Google search results"
    echo "- Your public profile"
    echo "- GitHub explore/trending"
    ;;
    
  *)
    echo "Palmer AI Privacy Tools:"
    echo "  ./privacy-tools.sh check        - Check current privacy"
    echo "  ./privacy-tools.sh protect FILE - Add file to .gitignore"
    echo "  ./privacy-tools.sh test-private - Preview private mode"
    ;;
esac
