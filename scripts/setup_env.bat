@echo off
echo Setting up ZenSort development environment for Windows...

REM Change to script's parent directory
cd /d "%~dp0.."

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://python.org
    pause
    exit /b 1
)

REM Create virtual environment
echo Creating virtual environment...
python -m venv venv

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip

REM Install requirements
echo Installing requirements...
pip install -r requirements.txt

REM Install PyInstaller for building
echo Installing PyInstaller...
pip install pyinstaller

echo.
echo Environment setup completed!
echo To activate the environment, run: venv\Scripts\activate.bat
echo To build executables, run: scripts\build_windows.bat
pause