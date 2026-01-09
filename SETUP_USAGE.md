# Setup Script Usage Guide

Quick guide for using the setup scripts to add Connector to your projects.

## Available Scripts

We provide three setup scripts:
- `setup-project.ps1` - PowerShell (Recommended for Windows)
- `setup-project.bat` - Windows Batch
- `setup-project.sh` - Bash/Linux/Mac

## Usage

### Method 1: PowerShell (Recommended)

**From Windows PowerShell or PowerShell 7:**
```powershell
cd "E:\Claude Dev\servicenow-mcp"
.\setup-project.ps1 "E:\path\to\your\project"
```

**Example:**
```powershell
.\setup-project.ps1 "E:\Claude Dev\MyProject"
```

### Method 2: Windows Batch File

**From Windows Command Prompt (cmd.exe):**
```cmd
cd "E:\Claude Dev\servicenow-mcp"
setup-project.bat "E:\path\to\your\project"
```

**Important:** Do NOT run .bat files from Git Bash - use cmd.exe or PowerShell

### Method 3: Bash Script

**From Git Bash, WSL, Linux, or Mac:**
```bash
cd "E:/Claude Dev/servicenow-mcp"
./setup-project.sh "/path/to/your/project"
```

## Manual Setup (Alternative)

If scripts don't work, manually create the configuration:

1. Navigate to your project
2. Create `.claude` directory
3. Copy the template:

```bash
mkdir -p "your-project/.claude"
cp "E:/Claude Dev/servicenow-mcp/templates/claude-settings.json" "your-project/.claude/settings.json"
```

## What Gets Created

The setup script creates:
```
your-project/
└── .claude/
    └── settings.json
```

**Content of settings.json:**
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

## Verification

After setup, verify the configuration:

1. Check the file exists:
   ```bash
   cat "your-project/.claude/settings.json"
   ```

2. Start Claude Code in your project:
   ```bash
   cd your-project
   claude-code
   ```

3. Test ServiceNow access:
   ```
   "Get the latest 3 incidents from Handtmann Test"
   ```

## When NOT to Use

Don't use the Connector MCP setup if your project:
- Has its own direct ServiceNow connection (e.g., via .env files)
- Already has a different MCP configuration
- Uses a different ServiceNow authentication method

In these cases, the project should use its own connection method.

## Troubleshooting

### Script doesn't run
- **PowerShell**: Run `Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned`
- **Batch**: Make sure you're in cmd.exe, not Git Bash
- **Bash**: Make script executable: `chmod +x setup-project.sh`

### "Path not found" error
- Verify the project path exists
- Use absolute paths
- Quote paths with spaces

### Settings not taking effect
- Restart your Claude Code session
- Verify `.claude/settings.json` exists
- Check JSON syntax is valid

## Support

For issues:
- GitHub: https://github.com/Kromula/Connector/issues
- Documentation: See GLOBAL_SETUP.md for comprehensive guide
