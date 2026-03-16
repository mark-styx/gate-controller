#!/bin/bash

# Frontend Setup Script
# Sets up and configures the Gate Controller Frontend

set -e

echo "🚀 Gate Controller Frontend Setup"
echo "=================================="
echo

# Check for Node.js
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed"
    echo "Please install Node.js 18+ from https://nodejs.org/"
    exit 1
fi

NODE_VERSION=$(node -v | cut -d 'v' -f 2 | cut -d '.' -f 1)
if [ "$NODE_VERSION" -lt 18 ]; then
    echo "❌ Node.js version 18+ required (found $(node -v))"
    exit 1
fi

echo "✅ Node.js $(node -v) found"
echo

# Check for npm/yarn/pnpm
if command -v pnpm &> /dev/null; then
    PKG_MANAGER="pnpm"
elif command -v yarn &> /dev/null; then
    PKG_MANAGER="yarn"
else
    PKG_MANAGER="npm"
fi

echo "✅ Using $PKG_MANAGER"
echo

# Install dependencies
echo "📦 Installing dependencies..."
$PKG_MANAGER install
echo "✅ Dependencies installed"
echo

# Create environment file if it doesn't exist
if [ ! -f .env.local ]; then
    echo "⚙️  Creating .env.local file..."
    cp ENV_EXAMPLE.md .env.local
    
    # Try to detect API URL
    if command -v hostname &> /dev/null; then
        PI_HOSTNAME=$(hostname -I | awk '{print $1}')
        if [ -n "$PI_HOSTNAME" ]; then
            sed -i.bak "s|http://localhost:8000|http://$PI_HOSTNAME:8000|g" .env.local
            rm -f .env.local.bak
            echo "✅ Detected Pi IP: $PI_HOSTNAME"
        fi
    fi
    
    echo "✅ .env.local created"
    echo
    echo "⚠️  IMPORTANT: Edit .env.local and add your API key!"
    echo "   Get your API key from: ../gate_control/config.py"
    echo
else
    echo "ℹ️  .env.local already exists, skipping..."
    echo
fi

# Generate PWA icons if needed
if [ ! -f public/icons/icon-512x512.png ]; then
    echo "ℹ️  Note: PWA icons are in SVG format"
    echo "   For production, convert icon.svg to PNGs at various sizes"
    echo "   Tools: https://realfavicongenerator.net/ or similar"
    echo
fi

echo "✨ Setup Complete!"
echo
echo "Next steps:"
echo "1. Edit .env.local and add your API key"
echo "2. Run: $PKG_MANAGER dev"
echo "3. Open http://localhost:3000"
echo
echo "For production build:"
echo "  $PKG_MANAGER build"
echo "  $PKG_MANAGER start"
