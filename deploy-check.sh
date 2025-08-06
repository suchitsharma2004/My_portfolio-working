#!/bin/bash

echo "🚀 Preparing Django project for Vercel deployment..."

# Make sure we're in the right directory
cd "$(dirname "$0")"

# Check if .env file exists
if [ ! -f "MacOS/.env" ]; then
    echo "⚠️  Warning: No .env file found in MacOS directory"
    echo "   Copy .env.example to MacOS/.env and configure your environment variables"
fi

# Check if requirements.txt has all dependencies
echo "📦 Checking dependencies..."
if [ -f "requirements.txt" ]; then
    echo "✅ requirements.txt found"
else
    echo "❌ requirements.txt not found"
    exit 1
fi

# Test Django project locally
echo "🧪 Testing Django project..."
cd MacOS
if python manage.py check; then
    echo "✅ Django project passes checks"
else
    echo "❌ Django project has issues"
    exit 1
fi

# Collect static files
echo "📁 Collecting static files..."
if python manage.py collectstatic --noinput; then
    echo "✅ Static files collected successfully"
else
    echo "❌ Failed to collect static files"
fi

cd ..

echo ""
echo "🎉 Project is ready for Vercel deployment!"
echo ""
echo "Next steps:"
echo "1. Push your code to GitHub"
echo "2. Connect your GitHub repo to Vercel"
echo "3. Set environment variables in Vercel dashboard:"
echo "   - SECRET_KEY"
echo "   - EMAIL_HOST_PASSWORD"
echo "   - VERCEL=1"
echo "4. Deploy!"
echo ""
echo "📖 See VERCEL_DEPLOYMENT.md for detailed instructions"
