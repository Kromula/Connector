# Global Setup Guide - Using Connector Across All Projects

This guide explains how to use the Connector (ServiceNow MCP Server) as a global tool available to all your Claude projects.

## Installation Complete ✓

The Connector has been installed as a global Python package. You can now use it from anywhere on your system.

## Method 1: Using with Claude Desktop (Recommended for Desktop App)

### Step 1: Locate Claude Desktop Config
The Claude Desktop configuration file is located at:
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
- **Mac**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Linux**: `~/.config/Claude/claude_desktop_config.json`

### Step 2: Add MCP Server Configuration

Create or edit the `claude_desktop_config.json` file:

```json
{
  "mcpServers": {
    "servicenow": {
      "command": "python",
      "args": ["-m", "servicenow_mcp.main"],
      "cwd": "E:/Claude Dev/servicenow-mcp"
    }
  }
}
```

### Step 3: Restart Claude Desktop

After saving the config file, restart Claude Desktop completely. The ServiceNow tools will then be available in **all conversations**.

### Step 4: Test It

In any Claude Desktop conversation, try:
- "Get the latest 3 incidents from My Instance"
- "List tables in Handtmann Test"

---

## Method 2: Using with Claude Code CLI (For Your Projects)

### Option A: Global MCP Settings (Recommended)

The Claude Code CLI uses MCP servers configured in your project's `.claude/settings.json` file. However, you can reference the global Connector installation.

**For your ux-analyser project:**

1. Navigate to your project:
   ```bash
   cd "path/to/your/ux-analyser"
   ```

2. Create or edit `.claude/settings.json`:
   ```json
   {
     "mcp": {
       "servers": {
         "servicenow": {
           "command": "python",
           "args": ["-m", "servicenow_mcp.main"],
           "cwd": "E:/Claude Dev/servicenow-mcp"
         }
       }
     }
   }
   ```

3. Start Claude Code in that project:
   ```bash
   claude-code
   ```

### Option B: Use Python Module Directly

Since Connector is now installed globally, you can also import and use it in any Python project:

```python
from servicenow_mcp.config_manager import ConfigManager
from servicenow_mcp.session_cache import SessionCache
from servicenow_mcp.auth import ServiceNowAuth

# Use the connector in your code
config = ConfigManager()
instances = config.list_instances()
```

### Option C: Create a Global Settings Template

Create a template file that you can copy to new projects:

**File: `E:/Claude Dev/servicenow-mcp/templates/claude-settings.json`**
```json
{
  "mcp": {
    "servers": {
      "servicenow": {
        "command": "python",
        "args": ["-m", "servicenow_mcp.main"],
        "cwd": "E:/Claude Dev/servicenow-mcp"
      }
    }
  }
}
```

**To use in a new project:**
```bash
cd your-new-project
mkdir -p .claude
cp "E:/Claude Dev/servicenow-mcp/templates/claude-settings.json" .claude/settings.json
```

---

## Method 3: Command Line Tools (Available Globally)

Since Connector is installed, you can use the CLI tools from anywhere:

```bash
# Authenticate from any directory
python -m servicenow_mcp.cli.sn_connect --instance "My Instance"

# Or if PATH is configured:
sn-connect --instance "Handtmann Test"

# List instances
python -m servicenow_mcp.cli.sn_connect --instance any --list

# Show cache
python -m servicenow_mcp.cli.sn_connect --instance any --show-cache
```

---

## Method 4: Using MCP Hooks (Advanced)

Create a global MCP hook that all projects can use:

### Step 1: Create Global Hook Script

**File: `E:/Claude Dev/servicenow-mcp/hooks/servicenow-hook.sh`** (for Git Bash/WSL)
```bash
#!/bin/bash
# ServiceNow MCP Hook - Auto-start on project open

# Check if ServiceNow is needed in this project
if [ -f ".servicenow-enabled" ]; then
  echo "Starting ServiceNow MCP Server..."
  python -m servicenow_mcp.main &
fi
```

**File: `E:/Claude Dev/servicenow-mcp/hooks/servicenow-hook.bat`** (for Windows)
```batch
@echo off
REM ServiceNow MCP Hook - Auto-start on project open

if exist ".servicenow-enabled" (
  echo Starting ServiceNow MCP Server...
  start /B python -m servicenow_mcp.main
)
```

### Step 2: Enable in Projects

In any project that needs ServiceNow access:
```bash
cd your-project
touch .servicenow-enabled  # Creates marker file
```

---

## Troubleshooting

### "Module not found" error
The package might not be in your Python path. Use the full path:
```bash
python -m servicenow_mcp.main
```

### MCP Server not showing in Claude Desktop
1. Verify the config file location
2. Check JSON syntax (use a JSON validator)
3. Restart Claude Desktop completely
4. Check Claude Desktop logs for errors

### Can't find the tools in Claude Code
1. Ensure `.claude/settings.json` exists in your project root
2. Verify the `cwd` path points to the Connector directory
3. Restart the Claude Code session

### PATH Warning
If you see PATH warnings, add this to your system PATH:
```
C:\Users\vecto\AppData\Roaming\Python\Python311\Scripts
```

---

## Quick Reference

### For Each New Project

**Option 1 - Copy settings:**
```bash
mkdir -p .claude
cp "E:/Claude Dev/servicenow-mcp/templates/claude-settings.json" .claude/settings.json
```

**Option 2 - Create settings manually:**
Create `.claude/settings.json` with:
```json
{
  "mcp": {
    "servers": {
      "servicenow": {
        "command": "python",
        "args": ["-m", "servicenow_mcp.main"],
        "cwd": "E:/Claude Dev/servicenow-mcp"
      }
    }
  }
}
```

### Available Instances
- `My Instance` - https://empdoconnor.service-now.com
- `Handtmann Test` - https://handtmanntest.service-now.com

### Session Management
```bash
# Check sessions
python -m servicenow_mcp.cli.sn_connect --instance any --show-cache

# Re-authenticate
python -m servicenow_mcp.cli.sn_connect --instance "Handtmann Test"
```

---

## Best Practices

1. **Keep sessions fresh**: Re-authenticate daily or when sessions expire
2. **One config, all projects**: Reference the same Connector installation
3. **Don't duplicate**: Keep config in one place (E:/Claude Dev/servicenow-mcp)
4. **Git ignore**: Always add `.claude/settings.json` to your project's `.gitignore`
5. **Update centrally**: Update Connector once, all projects benefit

---

## Support

- Issues: https://github.com/Kromula/Connector/issues
- Docs: See README.md in E:/Claude Dev/servicenow-mcp
