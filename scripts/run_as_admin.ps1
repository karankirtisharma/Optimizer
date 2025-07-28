<#
.SYNOPSIS
    Runs Ruddibaba Optimizer with administrator privileges
.DESCRIPTION
    This script launches the Ruddibaba Optimizer with administrator privileges,
    which is required for certain optimization tasks.
.EXAMPLE
    .\run_as_admin.ps1 --level safe
.NOTES
    File Name      : run_as_admin.ps1
    Prerequisite   : PowerShell 5.1 or later
#>

param(
    [ValidateSet('safe', 'optional', 'hardcore')]
    [string]$Level = 'safe',
    
    [switch]$NoBackup,
    
    [switch]$Force
)

# Check if running as administrator
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)

if (-not $isAdmin) {
    # Relaunch as administrator
    $arguments = "-NoProfile -ExecutionPolicy Bypass -File `"$($MyInvocation.MyCommand.Definition)`" -Level $Level"
    if ($NoBackup) { $arguments += " -NoBackup" }
    if ($Force) { $arguments += " -Force" }
    
    Start-Process powershell -Verb RunAs -ArgumentList $arguments
    exit
}

# Get the script directory
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
$projectRoot = Split-Path -Parent $scriptDir

# Activate virtual environment if it exists
$venvPath = Join-Path $projectRoot "venv"
if (Test-Path $venvPath) {
    & "$venvPath\Scripts\Activate.ps1"
}

# Build the command
$command = "ruddibaba-optimizer optimize run --level $Level"
if ($NoBackup) { $command += " --no-backup" }
if ($Force) { $command += " --force" }

# Run the optimizer
Write-Host "Running Ruddibaba Optimizer with $Level optimizations..." -ForegroundColor Cyan
Invoke-Expression $command

# Keep the window open if not running in a pipeline
if ($Host.Name -eq 'ConsoleHost') {
    Write-Host "`nPress any key to continue..." -NoNewline
    $null = $Host.UI.RawUI.ReadKey('NoEcho,IncludeKeyDown')
}
