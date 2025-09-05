#!/usr/bin/env python3
"""Cross-platform build script for ZenSort."""

import os
import sys
import platform
import subprocess
from pathlib import Path

def run_command(cmd, shell=False):
    """Run command and return success status."""
    try:
        result = subprocess.run(cmd, shell=shell, check=True, capture_output=True, text=True)
        print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        print(f"Output: {e.stdout}")
        print(f"Error: {e.stderr}")
        return False

def build_for_platform():
    """Build ZenSort for current platform."""
    system = platform.system().lower()
    
    # Change to project root
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    os.chdir(project_root)
    
    print(f"Building ZenSort for {system}...")
    
    # Check virtual environment
    if system == 'windows':
        venv_activate = "venv\\Scripts\\activate.bat"
        python_cmd = "python"
    else:
        venv_activate = "venv/bin/activate"
        python_cmd = "python3"
    
    if not Path(venv_activate).exists():
        print("Virtual environment not found. Please run setup script first.")
        return False
    
    # Create build directories
    Path("dist").mkdir(exist_ok=True)
    Path("build").mkdir(exist_ok=True)
    
    # Build command
    if system == 'windows':
        icon = "assets/icon.ico"
    else:
        icon = "assets/icon.icns" if system == 'darwin' else "assets/icon.ico"
    
    build_cmd = [
        python_cmd, "-m", "PyInstaller", "--onefile",
        "--name", "ZenSort",
        "--icon", icon,
        "--add-data", "src:src" if system != 'windows' else "src;src",
        "--hidden-import", "PIL._tkinter_finder",
        "--hidden-import", "mutagen",
        "--hidden-import", "exifread", 
        "--hidden-import", "av",
        "--hidden-import", "pyacoustid",
        "--collect-all", "musicbrainzngs",
        "src/main.py"
    ]
    
    # Activate virtual environment and run build
    if system == 'windows':
        full_cmd = f'call {venv_activate} && {" ".join(build_cmd)}'
        success = run_command(full_cmd, shell=True)
    else:
        full_cmd = f'source {venv_activate} && {" ".join(build_cmd)}'
        success = run_command(full_cmd, shell=True)
    
    if success:
        print("Build completed! Executables are in the dist/ folder.")
    else:
        print("Build failed!")
    
    return success

if __name__ == "__main__":
    success = build_for_platform()
    sys.exit(0 if success else 1)