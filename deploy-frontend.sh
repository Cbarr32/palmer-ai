#!/bin/bash

echo "🚀 Deploying Palmer AI Frontend to Production"
echo "============================================="

# Build the frontend
cd frontend
npm ci
npm run build

# Verify build output
if [ -d "out" ]; then
    echo "✅ Frontend build successful - static files ready"
    echo "📦 Built files located in: frontend/out/"
    echo "🔗 Ready for FastAPI static file serving"
else
    echo "❌ Build failed - no output directory found"
    exit 1
fi

# Return to project root
cd ..

# Stage deployment files
git add frontend/out/
git commit -m "build: Production frontend build for deployment"

# Push to production
git push origin main

echo "🎉 Deployment complete!"
echo "🌐 Frontend will be available via FastAPI static serving"
