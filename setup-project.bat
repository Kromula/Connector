@echo off
REM Quick setup script to enable Connector in a project

echo.
echo ========================================
echo  ServiceNow Connector - Project Setup
echo ========================================
echo.

if "%1"=="" (
    echo Usage: setup-project.bat "C:\path\to\your\project"
    echo.
    echo Example: setup-project.bat "E:\Claude Dev\ux-analyser"
    echo.
    exit /b 1
)

set PROJECT_DIR=%~1

if not exist "%PROJECT_DIR%" (
    echo [ERROR] Project directory does not exist: %PROJECT_DIR%
    exit /b 1
)

echo [INFO] Setting up Connector for: %PROJECT_DIR%
echo.

REM Create .claude directory if it doesn't exist
if not exist "%PROJECT_DIR%\.claude" (
    echo [INFO] Creating .claude directory...
    mkdir "%PROJECT_DIR%\.claude"
)

REM Copy settings template
echo [INFO] Copying MCP settings...
copy /Y "E:\Claude Dev\servicenow-mcp\templates\claude-settings.json" "%PROJECT_DIR%\.claude\settings.json" >nul

if %ERRORLEVEL% EQU 0 (
    echo [OK] Settings copied successfully!
    echo.
    echo [INFO] ServiceNow Connector is now available in this project.
    echo.
    echo Available instances:
    echo   - My Instance
    echo   - Handtmann Test
    echo.
    echo Try: "Get the latest incidents from Handtmann Test"
    echo.
) else (
    echo [ERROR] Failed to copy settings
    exit /b 1
)

exit /b 0
