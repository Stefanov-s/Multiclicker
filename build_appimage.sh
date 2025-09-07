#!/bin/bash
# Simple shell script to build AppImage

echo "🚀 Building Multi-Clicker Autoclicker AppImage..."

# Check if we're on Linux
if [[ "$OSTYPE" != "linux-gnu"* ]]; then
    echo "❌ AppImage can only be built on Linux"
    exit 1
fi

# Check for required tools
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 is required but not installed"
    exit 1
fi

if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 is required but not installed"
    exit 1
fi

# Run the Python build script
python3 build_appimage.py

echo "✅ Build complete!"
echo "📦 Run the AppImage with: ./MultiClickerAutoclicker-x86_64.AppImage"
