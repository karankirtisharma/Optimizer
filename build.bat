@echo off
:: Build script for Ruddibaba Optimizer
:: This script builds the executable and creates an installer

setlocal enabledelayedexpansion

:: Check if Python is installed
where python >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Python is not installed or not in PATH.
    echo Please install Python 3.7 or later from https://www.python.org/downloads/
    pause
    exit /b 1
)

:: Create a virtual environment if it doesn't exist
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
    if %ERRORLEVEL% NEQ 0 (
        echo Failed to create virtual environment.
        pause
        exit /b 1
    )
)

:: Activate the virtual environment
call "venv\Scripts\activate.bat"
if %ERRORLEVEL% NEQ 0 (
    echo Failed to activate virtual environment.
    pause
    exit /b 1
)

:: Install build dependencies
echo Installing build dependencies...
pip install -r requirements.txt
pip install pyinstaller nsis

:: Run the build script
echo Starting build process...
python scripts/build.py

:: Check if build was successful
if %ERRORLEVEL% NEQ 0 (
    echo Build failed with error code %ERRORLEVEL%
    pause
    exit /b %ERRORLEVEL%
)

echo.
echo Build completed successfully!
echo.
echo The following files were created:
echo   - Executable: dist\RuddibabaOptimizer.exe
echo   - Installer:  build\RuddibabaOptimizer_Setup_0.1.0.exe
echo.
pause
