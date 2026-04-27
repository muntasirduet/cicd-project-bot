#!/bin/bash
# Manual Deploy Script for my-cicd-project
# Usage: ./deploy.sh [staging|production]

set -e

ENV=${1:-staging}
PROJECT_DIR="/home/devuser/my-cicd-project"
PUBLISH_DIR="$PROJECT_DIR/App/publish"

echo "=========================================="
echo "🚀 Deploying my-cicd-project to $ENV"
echo "=========================================="

cd "$PROJECT_DIR"

echo "📦 Publishing .NET project..."
dotnet publish "$PROJECT_DIR/App/App.csproj" -c Release -o "$PUBLISH_DIR"

echo "✅ Published to $PUBLISH_DIR"
echo ""
echo "📝 Next steps:"
echo "   1. Copy files to server: rsync -avz $PUBLISH_DIR/ user@server:/var/www/api/"
echo "   2. Restart service: ssh user@server 'sudo systemctl restart my-api'"
echo "   3. Verify: curl https://your-domain.com/health"
