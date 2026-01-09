@echo off
REM Windows batch script for ServiceNow authentication

if "%1"=="" (
    echo Usage: authenticate.bat instance-name
    echo Example: authenticate.bat customer1-dev
    echo.
    echo Available commands:
    echo   authenticate.bat --list         List configured instances
    echo   authenticate.bat --show-cache   Show cached sessions
    echo   authenticate.bat --clear-cache  Clear all cached sessions
    exit /b 1
)

python -m servicenow_mcp.cli.sn_connect --instance %1 %2 %3 %4
