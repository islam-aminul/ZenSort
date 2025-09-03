#!/usr/bin/env python3
"""
Clean build artifacts and temporary files
"""

import shutil
import os
from pathlib import Path

def clean_directory(path, description):
    """Remove directory if it exists."""
    if Path(path).exists():
        print(f"Removing {description}...")
        shutil.rmtree(path)
        print(f"✓ Removed {path}")
    else:
        print(f"✓ {description} already clean")

def clean_files(pattern, description):
    """Remove files matching pattern."""
    files = list(Path(".").glob(pattern))
    if files:
        print(f"Removing {description}...")
        for file in files:
            file.unlink()
            print(f"✓ Removed {file}")
    else:
        print(f"✓ {description} already clean")

def main():
    """Main clean function."""
    print("Cleaning ZenSort build artifacts...")
    
    # Change to script's parent directory
    script_dir = Path(__file__).parent
    project_dir = script_dir.parent
    os.chdir(project_dir)
    
    # Remove build directories
    clean_directory("build", "build directory")
    clean_directory("dist", "distribution directory")
    clean_directory("__pycache__", "Python cache")
    
    # Remove PyInstaller spec files
    clean_files("*.spec", "PyInstaller spec files")
    
    # Remove Python cache directories recursively
    for cache_dir in Path(".").rglob("__pycache__"):
        clean_directory(cache_dir, f"cache directory {cache_dir}")
    
    # Remove .pyc files
    for pyc_file in Path(".").rglob("*.pyc"):
        pyc_file.unlink()
    
    print("\nClean completed!")

if __name__ == "__main__":
    main()