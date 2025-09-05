#!/bin/bash
echo "Setting up ZenSort development environment..."

# Change to script's parent directory
cd "$(dirname "$0")/.."

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "Python 3 is not installed. Please install Python 3.8+ first."
    exit 1
fi

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo "Installing requirements..."
pip install -r requirements.txt

# Install PyInstaller for building
echo "Installing PyInstaller..."
pip install pyinstaller

echo "Setup completed successfully!"
echo "To activate the environment, run: source venv/bin/activate"