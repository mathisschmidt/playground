#!/bin/bash

# Exit on any error
set -e

echo "🚀 Starting deployment..."

# Pull latest changes from GitHub
echo "📥 Pulling latest changes..."
git pull origin your-special-branch-name

# Rebuild and restart the container
echo "🔨 Building and restarting container..."
docker compose down
docker compose up -d --build

# Clean up old images
echo "🧹 Cleaning up old images..."
docker image prune -f

echo "✅ Deployment complete!"