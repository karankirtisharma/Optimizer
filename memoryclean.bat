@echo off
title 🧠 RAM Cleaner - Standby Memory Cleanup
color 0A

echo ========================================
echo         MEMORY CLEANUP TOOL
echo ========================================

:: Check if EmptyStandbyList.exe exists
set TOOL=EmptyStandbyList.exe

if exist "%~dp0%TOOL%" (
    echo [+] Running %TOOL% to free standby RAM...
    "%~dp0%TOOL%" standbylist
    echo [✓] Standby memory cleaned successfully.
) else (
    echo [!] %TOOL% not found in this folder.
    echo Download it from:
    echo https://wj32.org/wp/software/empty-standby-list/
)

echo.
pause
