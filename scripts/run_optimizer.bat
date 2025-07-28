@echo off
:: Ruddibaba Optimizer Launcher
:: This script helps run the optimizer with the correct settings

setlocal enabledelayedexpansion

:: Default values
set LEVEL=safe
set BACKUP=--backup
set FORCE=

:: Parse command line arguments
:parse_args
if "%~1"=="" goto :args_parsed

if /i "%~1"=="--level" (
    set "LEVEL=%~2"
    shift
) else if /i "%~1"=="-l" (
    set "LEVEL=%~2"
    shift
) else if /i "%~1"=="--no-backup" (
    set "BACKUP=--no-backup"
) else if /i "%~1"=="--force" (
    set "FORCE=--force"
) else if /i "%~1"=="-f" (
    set "FORCE=--force"
) else (
    echo Unknown option: %~1
    goto :show_help
)

shift
goto :parse_args

:args_parsed

:: Check if Python is installed
where python >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Python is not installed or not in PATH.
    echo Please install Python 3.7 or later from https://www.python.org/downloads/
    pause
    exit /b 1
)

:: Get the script directory
set "SCRIPT_DIR=%~dp0"
set "PROJECT_ROOT=%SCRIPT_DIR%.."

:: Activate virtual environment if it exists
if exist "%PROJECT_ROOT%\venv\Scripts\activate.bat" (
    call "%PROJECT_ROOT%\venv\Scripts\activate.bat"
)

:: Build the command
set "COMMAND=python -m ruddibaba_optimizer.cli optimize run --level %LEVEL% %BACKUP% %FORCE%"

echo Running Ruddibaba Optimizer with %LEVEL% optimizations...

:: Run the command
%COMMAND%

:: Keep the window open if not running from command line
if "%cmdcmdline:"=%" == "%COMSPEC%" (
    echo.
    pause
)

exit /b 0

:show_help
echo Ruddibaba Optimizer Launcher
echo.
echo Usage: run_optimizer.bat [options]
echo.
echo Options:
echo   -l, --level LEVEL    Set optimization level: safe, optional, hardcore (default: safe)
echo   --no-backup          Skip creating a backup before making changes
echo   -f, --force          Run without confirmation
echo   -h, --help           Show this help message

exit /b 1
