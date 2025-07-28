@echo off
:: Ruddibaba Optimizer Uninstaller
:: This script helps uninstall the Ruddibaba Optimizer

setlocal enabledelayedexpansion

:: Check if running as administrator
net session >nul 2>&1
if %ERRORLEVEL% == 0 (
    set "ADMIN=1"
) else (
    set "ADMIN=0"
    echo This script requires administrator privileges to uninstall properly.
    echo Please right-click and select "Run as administrator"
    pause
    exit /b 1
)

echo ===============================================
echo    Ruddibaba Optimizer Uninstaller
echo ===============================================
echo.
echo This will remove Ruddibaba Optimizer and its data.
echo.

set /p CONFIRM="Are you sure you want to continue? (y/N): "
if /i not "%CONFIRM%"=="y" (
    echo Uninstall cancelled.
    pause
    exit /b 0
)

echo.
echo Starting uninstallation...

:: Get the script directory
set "SCRIPT_DIR=%~dp0"
set "PROJECT_ROOT=%SCRIPT_DIR%.."
set "APP_DATA=%LOCALAPPDATA%\RuddibabaOptimizer"

:: Remove application data
echo Removing application data...
if exist "%APP_DATA%" (
    rmdir /s /q "%APP_DATA%"
)

:: Remove shortcuts
echo Removing shortcuts...
set "DESKTOP=%USERPROFILE%\Desktop"
set "START_MENU=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Ruddibaba Optimizer"

del /q "%DESKTOP%\Ruddibaba Optimizer.lnk" 2>nul
del /q "%DESKTOP%\Ruddibaba Optimizer (Admin).lnk" 2>nul

if exist "%START_MENU%" (
    rmdir /s /q "%START_MENU%"
)

:: Unregister from pip if installed
where ruddibaba-optimizer >nul 2>&1
if %ERRORLEVEL% == 0 (
    echo Uninstalling Python package...
    pip uninstall -y ruddibaba-optimizer
)

echo.
echo Uninstallation complete!
echo.
echo Note: The following items were not removed:
echo   - Python and its packages (if installed globally)
echo   - Virtual environments (if created manually)
echo   - Custom configuration files (if any)
echo.
pause
