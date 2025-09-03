#!/bin/bash
# Run ZenSort GUI with virtual environment

# Change to script's parent directory
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR/.."

# Check if virtual environment exists
if [ ! -f "venv/bin/activate" ]; then
    echo "Virtual environment not found. Please run setup_env.sh first."
    exit 1
fi

# Activate virtual environment and run GUI
source venv/bin/activate && python src/gui.py