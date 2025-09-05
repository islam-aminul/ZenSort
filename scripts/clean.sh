#!/bin/bash
echo "Cleaning build artifacts..."

# Change to script's parent directory
cd "$(dirname "$0")/.."

# Remove build directories
echo "Removing build directories..."
rm -rf build/
rm -rf dist/
rm -rf *.spec

# Remove Python cache
echo "Removing Python cache..."
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find . -type f -name "*.pyc" -delete 2>/dev/null || true
find . -type f -name "*.pyo" -delete 2>/dev/null || true

# Remove logs
echo "Removing log files..."
find . -type f -name "*.log" -delete 2>/dev/null || true

echo "Clean completed!"