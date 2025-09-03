#!/bin/bash
echo "Setting up ZenSort development environment for Unix/Linux/macOS..."

# Change to script's parent directory
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR/.."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed"
    echo "Please install Python 3.8+ from your package manager or https://python.org"
    exit 1
fi

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
python -m pip install --upgrade pip

# Install requirements
echo "Installing requirements..."
pip install -r requirements.txt

# Install PyInstaller for building
echo "Installing PyInstaller..."
pip install pyinstaller

echo ""
echo "Environment setup completed!"
echo "To activate the environment, run: source venv/bin/activate"

# Detect OS and show appropriate build command
if [[ "$OSTYPE" == "darwin"* ]]; then
    echo "To build executables, run: ./scripts/build_macos.sh"
else
    echo "To build executables, run: ./scripts/build_linux.sh"
fi