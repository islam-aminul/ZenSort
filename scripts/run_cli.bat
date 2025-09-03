@echo off
REM Run ZenSort CLI with virtual environment

REM Change to script's parent directory
cd /d "%~dp0.."

REM Check if virtual environment exists
if not exist "venv\Scripts\activate.bat" (
    echo Virtual environment not found. Please run setup_env.bat first.
    pause
    exit /b 1
)

REM Check if arguments provided
if "%~1"=="" (
    echo Usage: run_cli.bat "source_directory" "destination_directory" [options]
    echo Example: run_cli.bat "C:\Photos" "D:\Organized" --quiet
    pause
    exit /b 1
)

if "%~2"=="" (
    echo Usage: run_cli.bat "source_directory" "destination_directory" [options]
    echo Example: run_cli.bat "C:\Photos" "D:\Organized" --quiet
    pause
    exit /b 1
)

REM Activate virtual environment and run CLI with all arguments
call venv\Scripts\activate.bat && python src\cli.py %*