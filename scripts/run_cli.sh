#!/bin/bash
# Run ZenSort CLI with virtual environment

# Change to script's parent directory
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR/.."

# Check if virtual environment exists
if [ ! -f "venv/bin/activate" ]; then
    echo "Virtual environment not found. Please run setup_env.sh first."
    exit 1
fi

# Check if arguments provided
if [ $# -lt 2 ]; then
    echo "Usage: run_cli.sh \"source_directory\" \"destination_directory\" [options]"
    echo "Example: run_cli.sh \"/home/user/photos\" \"/home/user/organized\" --quiet"
    exit 1
fi

# Activate virtual environment and run CLI with all arguments
source venv/bin/activate && python src/cli.py "$@"