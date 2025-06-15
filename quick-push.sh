#!/bin/bash
# Palmer AI Quick Push Script

cd ~/dev/palmerai || exit 1

echo "🚀 Palmer AI Quick Push"
echo "======================"

# Check status
echo "📊 Current changes:"
git status --short

# Add all changes
git add -A

# Commit with generated message
TIMESTAMP=$(date +"%Y-%m-%d %H:%M")
git commit -m "feat: Progress update - $TIMESTAMP

- Continued development on Palmer AI platform
- Various improvements and bug fixes
- See diff for detailed changes"

# Push to origin
git push origin main

echo ""
echo "✅ Successfully pushed to GitHub!"
echo "🎉 Another step forward in building Palmer AI!"
