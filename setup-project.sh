#!/bin/bash
# Quick setup script to enable Connector in a project

echo ""
echo "========================================"
echo " ServiceNow Connector - Project Setup"
echo "========================================"
echo ""

if [ -z "$1" ]; then
    echo "Usage: ./setup-project.sh /path/to/your/project"
    echo ""
    echo "Example: ./setup-project.sh /mnt/e/Claude\ Dev/ux-analyser"
    echo ""
    exit 1
fi

PROJECT_DIR="$1"

if [ ! -d "$PROJECT_DIR" ]; then
    echo "[ERROR] Project directory does not exist: $PROJECT_DIR"
    exit 1
fi

echo "[INFO] Setting up Connector for: $PROJECT_DIR"
echo ""

# Create .claude directory if it doesn't exist
if [ ! -d "$PROJECT_DIR/.claude" ]; then
    echo "[INFO] Creating .claude directory..."
    mkdir -p "$PROJECT_DIR/.claude"
fi

# Copy settings template
echo "[INFO] Copying MCP settings..."
cp "E:/Claude Dev/servicenow-mcp/templates/claude-settings.json" "$PROJECT_DIR/.claude/settings.json"

if [ $? -eq 0 ]; then
    echo "[OK] Settings copied successfully!"
    echo ""
    echo "[INFO] ServiceNow Connector is now available in this project."
    echo ""
    echo "Available instances:"
    echo "  - My Instance"
    echo "  - Handtmann Test"
    echo ""
    echo "Try: \"Get the latest incidents from Handtmann Test\""
    echo ""
else
    echo "[ERROR] Failed to copy settings"
    exit 1
fi

exit 0
