@echo off
echo Building ZenSort for Windows...

REM Change to script's parent directory
cd /d "%~dp0.."

REM Check if virtual environment exists
if not exist "venv\Scripts\activate.bat" (
    echo Virtual environment not found. Please run setup_env.bat first.
    pause
    exit /b 1
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Create build directory
if not exist "dist" mkdir dist
if not exist "build" mkdir build

REM Build unified executable
echo Building ZenSort executable...
pyinstaller --onefile ^
    --name "ZenSort" ^
    --icon="assets/icon.ico" ^
    --add-data "src;src" ^
    --hidden-import="PIL._tkinter_finder" ^
    --hidden-import="mutagen" ^
    --collect-all="pyacoustid" ^
    --collect-all="musicbrainzngs" ^
    --exclude-module="charset_normalizer.md__mypyc" ^
    src/main.py

echo Build completed! Executables are in the dist/ folder.
pause