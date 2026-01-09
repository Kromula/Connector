# ServiceNow Connector - Project Setup Script (PowerShell)
# Usage: .\setup-project.ps1 "C:\path\to\your\project"

param(
    [Parameter(Mandatory=$true)]
    [string]$ProjectDir
)

Write-Host ""
Write-Host "========================================"
Write-Host " ServiceNow Connector - Project Setup"
Write-Host "========================================"
Write-Host ""

# Get script directory
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$TemplateFile = Join-Path $ScriptDir "templates\claude-settings.json"

# Validate project directory
if (-not (Test-Path $ProjectDir)) {
    Write-Host "[ERROR] Project directory does not exist: $ProjectDir" -ForegroundColor Red
    exit 1
}

Write-Host "[INFO] Setting up Connector for: $ProjectDir" -ForegroundColor Cyan
Write-Host ""

# Create .claude directory if it doesn't exist
$ClaudeDir = Join-Path $ProjectDir ".claude"
if (-not (Test-Path $ClaudeDir)) {
    Write-Host "[INFO] Creating .claude directory..." -ForegroundColor Yellow
    New-Item -ItemType Directory -Path $ClaudeDir -Force | Out-Null
}

# Copy settings template
$DestFile = Join-Path $ClaudeDir "settings.json"
Write-Host "[INFO] Copying MCP settings..." -ForegroundColor Yellow

try {
    Copy-Item -Path $TemplateFile -Destination $DestFile -Force

    Write-Host "[OK] Settings copied successfully!" -ForegroundColor Green
    Write-Host ""
    Write-Host "[INFO] ServiceNow Connector is now available in this project." -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Available instances:" -ForegroundColor White
    Write-Host "  - My Instance" -ForegroundColor White
    Write-Host "  - Handtmann Test" -ForegroundColor White
    Write-Host ""
    Write-Host "Try: ""Get the latest incidents from Handtmann Test""" -ForegroundColor Gray
    Write-Host ""

} catch {
    Write-Host "[ERROR] Failed to copy settings: $_" -ForegroundColor Red
    Write-Host "[ERROR] Template file: $TemplateFile" -ForegroundColor Red
    Write-Host "[ERROR] Destination: $DestFile" -ForegroundColor Red
    exit 1
}

exit 0
