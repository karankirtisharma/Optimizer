@echo off
:: Ruddibaba Optimizer Setup
:: This script helps install and set up the Ruddibaba Optimizer

setlocal enabledelayedexpansion

:: Check if running as administrator
net session >nul 2>&1
if %ERRORLEVEL% == 0 (
    set "ADMIN=1"
) else (
    set "ADMIN=0"
    echo This script requires administrator privileges to install properly.
    echo Please right-click and select "Run as administrator"
    pause
    exit /b 1
)

echo ===============================================
echo    Ruddibaba Optimizer Setup
echo ===============================================
echo.

:: Check if Python is installed
where python >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Python is not installed or not in PATH.
    echo Please install Python 3.7 or later from https://www.python.org/downloads/
    pause
    exit /b 1
)

:: Check Python version
python -c "import sys; exit(0 if sys.version_info >= (3, 7) else 1)" >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Python 3.7 or later is required.
    echo Please install Python 3.7 or later from https://www.python.org/downloads/
    pause
    exit /b 1
)

:: Get the script directory
set "SCRIPT_DIR=%~dp0"
set "PROJECT_ROOT=%SCRIPT_DIR%.."

:: Create a virtual environment
echo Creating virtual environment...
python -m venv "%PROJECT_ROOT%\venv"
if %ERRORLEVEL% NEQ 0 (
    echo Failed to create virtual environment.
    pause
    exit /b 1
)

:: Activate the virtual environment
call "%PROJECT_ROOT%\venv\Scripts\activate.bat"
if %ERRORLEVEL% NEQ 0 (
    echo Failed to activate virtual environment.
    pause
    exit /b 1
)

:: Install dependencies
echo Installing dependencies...
pip install --upgrade pip
pip install -r "%PROJECT_ROOT%\requirements.txt"
pip install "%PROJECT_ROOT%"
if %ERRORLEVEL% NEQ 0 (
    echo Failed to install dependencies.
    pause
    exit /b 1
)

:: Create shortcuts
echo Creating shortcuts...
set "DESKTOP=%USERPROFILE%\Desktop"
set "START_MENU=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Ruddibaba Optimizer"

:: Create Start Menu folder
if not exist "%START_MENU%" (
    mkdir "%START_MENU%"
)

:: Create desktop shortcuts
powershell -Command "
    $WshShell = New-Object -comObject WScript.Shell;
    
    # CLI Shortcuts
    $Shortcut = $WshShell.CreateShortcut('%DESKTOP%\Ruddibaba Optimizer.lnk');
    $Shortcut.TargetPath = 'cmd.exe';
    $Shortcut.Arguments = '/k ""%PROJECT_ROOT%\venv\Scripts\activate.bat" && ruddibaba-optimizer"';
    $Shortcut.WorkingDirectory = '%PROJECT_ROOT%';
    $Shortcut.IconLocation = '%%SystemRoot%%\System32\SHELL32.dll,21';
    $Shortcut.Save();
    
    $Shortcut = $WshShell.CreateShortcut('%DESKTOP%\Ruddibaba Optimizer (Admin).lnk');
    $Shortcut.TargetPath = 'powershell.exe';
    $Shortcut.Arguments = '-NoProfile -ExecutionPolicy Bypass -Command "Start-Process powershell -Verb RunAs -ArgumentList ''-NoProfile -ExecutionPolicy Bypass -Command """"""cd ''\""""%PROJECT_ROOT%\"""; & .\venv\Scripts\Activate.ps1; ruddibaba-optimizer""""""';
    $Shortcut.WorkingDirectory = '%PROJECT_ROOT%';
    $Shortcut.IconLocation = '%%SystemRoot%%\System32\SHELL32.dll,21';
    $Shortcut.Save();
    
    # GUI Shortcuts
    $guiLauncher = '%PROJECT_ROOT%\scripts\gui_launcher.py';
    $guiIcon = '%%SystemRoot%%\System32\SHELL32.dll,21';
    
    # Desktop GUI Shortcut
    $Shortcut = $WshShell.CreateShortcut('%DESKTOP%\Ruddibaba Optimizer GUI.lnk');
    $Shortcut.TargetPath = 'pythonw.exe';
    $Shortcut.Arguments = '""%guiLauncher""';
    $Shortcut.WorkingDirectory = '%PROJECT_ROOT%';
    $Shortcut.IconLocation = $guiIcon;
    $Shortcut.Save();
    
    # Start Menu GUI Shortcut
    $Shortcut = $WshShell.CreateShortcut('%START_MENU%\Ruddibaba Optimizer GUI.lnk');
    $Shortcut.TargetPath = 'pythonw.exe';
    $Shortcut.Arguments = '""%guiLauncher""';
    $Shortcut.WorkingDirectory = '%PROJECT_ROOT%';
    $Shortcut.IconLocation = $guiIcon;
    $Shortcut.Save();
    
    # CLI Start Menu Shortcuts
    $Shortcut = $WshShell.CreateShortcut('%START_MENU%\Ruddibaba Optimizer.lnk');
    $Shortcut.TargetPath = 'cmd.exe';
    $Shortcut.Arguments = '/k ""%PROJECT_ROOT%\venv\Scripts\activate.bat" && ruddibaba-optimizer"';
    $Shortcut.WorkingDirectory = '%PROJECT_ROOT%';
    $Shortcut.IconLocation = '%%SystemRoot%%\System32\SHELL32.dll,21';
    $Shortcut.Save();
    
    $Shortcut = $WshShell.CreateShortcut('%START_MENU%\Ruddibaba Optimizer (Admin).lnk');
    $Shortcut.TargetPath = 'powershell.exe';
    $Shortcut.Arguments = '-NoProfile -ExecutionPolicy Bypass -Command "Start-Process powershell -Verb RunAs -ArgumentList ''-NoProfile -ExecutionPolicy Bypass -Command """"""cd ''\""""%PROJECT_ROOT%\"""; & .\venv\Scripts\Activate.ps1; ruddibaba-optimizer""""""';
    $Shortcut.WorkingDirectory = '%PROJECT_ROOT%';
    $Shortcut.IconLocation = '%%SystemRoot%%\System32\SHELL32.dll,21';
    $Shortcut.Save();
"

echo.
echo ===============================================
echo    Installation Complete!
echo ===============================================
echo.
echo Ruddibaba Optimizer has been successfully installed.
echo.
echo Shortcuts have been created on your desktop and in the Start Menu.
echo.
echo To run the optimizer:
echo 1. Double-click 'Ruddibaba Optimizer' for normal mode
echo 2. Right-click 'Ruddibaba Optimizer (Admin)' and select 'Run as administrator' for full access
echo.
pause
