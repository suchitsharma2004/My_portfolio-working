#!/bin/bash

# Build script for Vercel deployment
echo "Starting Django build process..."

# Install dependencies
pip install -r requirements.txt

# Collect static files
cd MacOS
python manage.py collectstatic --noinput

echo "Build process completed!"
