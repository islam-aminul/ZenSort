@echo off
REM Run ZenSort GUI with virtual environment

REM Change to script's parent directory
cd /d "%~dp0.."

REM Check if virtual environment exists
if not exist "venv\Scripts\activate.bat" (
    echo Virtual environment not found. Please run setup_env.bat first.
    pause
    exit /b 1
)

REM Activate virtual environment and run GUI
call venv\Scripts\activate.bat && python src\gui.py