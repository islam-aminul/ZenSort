#!/usr/bin/env python3
"""
Cross-platform build script for ZenSort
Builds executables for the current platform
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

def run_command(cmd, shell=False):
    """Run command and return success status."""
    try:
        result = subprocess.run(cmd, shell=shell, check=True, 
                              capture_output=True, text=True)
        print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        print(f"Output: {e.stdout}")
        print(f"Error: {e.stderr}")
        return False

def build_executable(name, script, windowed=False, icon=None):
    """Build executable using PyInstaller."""
    cmd = [
        "pyinstaller", "--onefile",
        "--name", name,
        "--add-data", f"src{os.pathsep}src",
        "--hidden-import", "mutagen",
        "--hidden-import", "acoustid", 
        "--hidden-import", "musicbrainzngs",
        "--hidden-import", "duckdb"
    ]
    
    if windowed:
        cmd.append("--windowed")
        cmd.extend(["--hidden-import", "PIL._tkinter_finder"])
    
    if icon and Path(icon).exists():
        cmd.extend(["--icon", icon])
    
    if platform.system() == "Darwin":
        cmd.extend(["--osx-bundle-identifier", "com.zensort.app"])
    
    cmd.append(script)
    
    print(f"Building {name}...")
    return run_command(cmd)

def main():
    """Main build function."""
    system = platform.system()
    print(f"Building ZenSort for {system}...")
    
    # Change to script's parent directory
    script_dir = Path(__file__).parent
    project_dir = script_dir.parent
    os.chdir(project_dir)
    
    # Create directories
    Path("dist").mkdir(exist_ok=True)
    Path("build").mkdir(exist_ok=True)
    
    # Determine icon file
    icon_map = {
        "Windows": "assets/icon.ico",
        "Darwin": "assets/icon.icns", 
        "Linux": "assets/icon.png"
    }
    icon = icon_map.get(system)
    
    # Build GUI executable
    gui_success = build_executable("ZenSort", "src/gui.py", windowed=True, icon=icon)
    
    # Build CLI executable  
    cli_success = build_executable("ZenSort-CLI", "src/cli.py", icon=icon)
    
    # Set executable permissions on Unix systems
    if system in ["Linux", "Darwin"]:
        os.chmod("dist/ZenSort", 0o755)
        os.chmod("dist/ZenSort-CLI", 0o755)
    
    if gui_success and cli_success:
        print("\nBuild completed successfully!")
        print("Executables are in the dist/ folder.")
        return 0
    else:
        print("\nBuild failed!")
        return 1

if __name__ == "__main__":
    sys.exit(main())