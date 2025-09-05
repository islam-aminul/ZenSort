#!/bin/bash
echo "Building ZenSort for macOS..."

# Change to script's parent directory
cd "$(dirname "$0")/.."

# Check if virtual environment exists
if [ ! -f "venv/bin/activate" ]; then
    echo "Virtual environment not found. Please run setup_env.sh first."
    exit 1
fi

# Activate virtual environment
source venv/bin/activate

# Create build directory
mkdir -p dist
mkdir -p build

# Build unified executable
echo "Building ZenSort executable..."
pyinstaller --onefile \
    --name "ZenSort" \
    --icon="assets/icon.icns" \
    --add-data "src:src" \
    --hidden-import="PIL._tkinter_finder" \
    --hidden-import="mutagen" \
    --hidden-import="exifread" \
    --hidden-import="av" \
    --hidden-import="pyacoustid" \
    --collect-all="musicbrainzngs" \
    src/main.py

echo "Build completed! Executables are in the dist/ folder."