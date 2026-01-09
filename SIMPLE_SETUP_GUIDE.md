# Simple Setup Guide - Using Connector in Your Projects

## Quick Answer

To use Connector in a project with Claude Code, you need **one file** in your project:

```
your-project/
└── .claude/
    └── settings.json
```

That's it! This file tells Claude Code where to find the Connector server.

---

## Step-by-Step Setup for ANY Project

### Step 1: Open Your Project Directory

```bash
cd "E:\Claude Dev\YourProjectName"
```

### Step 2: Create the .claude Directory

**Windows (PowerShell or cmd):**
```cmd
mkdir .claude
```

**Git Bash/Linux/Mac:**
```bash
mkdir -p .claude
```

### Step 3: Create settings.json File

Create a file at `.claude/settings.json` with this exact content:

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

**That's literally all you need!**

### Step 4: Restart Claude Code

If Claude Code is already running in your project:
1. Exit Claude Code
2. Navigate to your project directory
3. Start Claude Code again

### Step 5: Test It

In Claude Code, try:
```
"Get the latest 3 incidents from Handtmann Test"
```

---

## What This File Does

The `settings.json` file tells Claude Code:
- **"servicenow"**: The name of this MCP server
- **"command": "python"**: How to run the server
- **"args": ["-m", "servicenow_mcp.main"]**: What to run (the Connector module)
- **"cwd": "E:/Claude Dev/servicenow-mcp"**: Where the Connector code lives

---

## Copy-Paste Method (Easiest)

**From any project directory:**

### Windows PowerShell:
```powershell
# Create directory
New-Item -ItemType Directory -Force -Path ".claude"

# Copy template
Copy-Item "E:\Claude Dev\servicenow-mcp\templates\claude-settings.json" ".claude\settings.json"
```

### Windows Command Prompt (cmd):
```cmd
mkdir .claude
copy "E:\Claude Dev\servicenow-mcp\templates\claude-settings.json" ".claude\settings.json"
```

### Git Bash/Linux/Mac:
```bash
mkdir -p .claude
cp "E:/Claude Dev/servicenow-mcp/templates/claude-settings.json" ".claude/settings.json"
```

---

## Using the Automated Script

### Windows PowerShell (Recommended):
```powershell
cd "E:\Claude Dev\servicenow-mcp"
.\setup-project.ps1 "E:\Claude Dev\YourProjectName"
```

### Windows cmd.exe:
```cmd
cd "E:\Claude Dev\servicenow-mcp"
setup-project.bat "E:\Claude Dev\YourProjectName"
```

---

## Verifying Setup

### 1. Check the file exists:
```bash
cat .claude/settings.json
```

You should see the JSON content.

### 2. Check it's valid JSON:
Copy the content and paste it into https://jsonlint.com/

### 3. Start Claude Code:
```bash
cd "E:\Claude Dev\YourProjectName"
claude-code
```

### 4. Test ServiceNow access:
```
"List all configured ServiceNow instances"
"Get 3 incidents from My Instance"
```

---

## Common Issues & Solutions

### Issue: "No tools available" or "Can't connect to ServiceNow"

**Solution:** The `.claude/settings.json` file is missing or incorrect.

**Check:**
```bash
# Does the file exist?
ls .claude/settings.json

# Is it valid JSON?
cat .claude/settings.json
```

### Issue: "Module not found" error

**Solution:** The Connector package isn't installed globally.

**Fix:**
```bash
cd "E:/Claude Dev/servicenow-mcp"
pip install --user -e .
```

### Issue: "No valid session found"

**Solution:** You need to authenticate to the instance first.

**Fix:**
```bash
python -m servicenow_mcp.cli.sn_connect --instance "Handtmann Test"
```

### Issue: Settings file exists but tools don't work

**Solution:** Restart Claude Code completely.

1. Exit Claude Code
2. Wait 5 seconds
3. Start Claude Code again from your project directory

---

## What About Claude Desktop?

Claude Desktop is different - it has **one global config** for ALL conversations.

**Location:**
- Windows: `%APPDATA%\Claude\claude_desktop_config.json`
- Mac: `~/Library/Application Support/Claude/claude_desktop_config.json`

**Content:** Same JSON structure as above

**Benefit:** All conversations in Claude Desktop can use ServiceNow

---

## Example: Setting Up 3 Different Projects

Let's say you have three projects that need ServiceNow:

### Project 1: Data Loader
```bash
cd "E:/Claude Dev/Data Loader"
mkdir .claude
copy "E:\Claude Dev\servicenow-mcp\templates\claude-settings.json" ".claude\settings.json"
```

### Project 2: Golf Stats Tracker
```bash
cd "E:/Claude Dev/Golf Stats Tracker"
mkdir .claude
copy "E:\Claude Dev\servicenow-mcp\templates\claude-settings.json" ".claude\settings.json"
```

### Project 3: Resolver
```bash
cd "E:/Claude Dev/Resolver"
mkdir .claude
copy "E:\Claude Dev\servicenow-mcp\templates\claude-settings.json" ".claude\settings.json"
```

**Same file, same content, works everywhere!**

---

## Key Concepts

### 1. One Connector Installation
- Installed once: `E:/Claude Dev/servicenow-mcp`
- Used by all projects
- Update once, all projects benefit

### 2. Per-Project Configuration
- Each project has `.claude/settings.json`
- All point to the same Connector installation
- Easy to set up, copy the template

### 3. Shared Sessions
- Authenticate once with `sn-connect`
- Sessions cached for 8 hours
- All projects use the same cached sessions

### 4. Available Instances
- My Instance (empdoconnor.service-now.com)
- Handtmann Test (handtmanntest.service-now.com)
- Add more in `config/instances.yaml`

---

## Quick Command Reference

### Authenticate to instance:
```bash
python -m servicenow_mcp.cli.sn_connect --instance "Handtmann Test"
```

### Check cached sessions:
```bash
python -m servicenow_mcp.cli.sn_connect --instance any --show-cache
```

### List configured instances:
```bash
python -m servicenow_mcp.cli.sn_connect --instance any --list
```

### Setup new project:
```bash
mkdir -p "your-project/.claude"
cp "E:/Claude Dev/servicenow-mcp/templates/claude-settings.json" "your-project/.claude/settings.json"
```

---

## Visual Guide

```
E:/Claude Dev/
├── servicenow-mcp/          ← Connector lives here (ONE installation)
│   ├── config/
│   │   └── instances.yaml   ← Your instances defined here
│   ├── cache/
│   │   └── sessions.json    ← Cached sessions here
│   └── templates/
│       └── claude-settings.json  ← Template to copy
│
├── Data Loader/
│   └── .claude/
│       └── settings.json    ← Points to servicenow-mcp ↑
│
├── Golf Stats Tracker/
│   └── .claude/
│       └── settings.json    ← Points to servicenow-mcp ↑
│
└── Resolver/
    └── .claude/
        └── settings.json    ← Points to servicenow-mcp ↑
```

---

## The Absolute Simplest Method

If nothing else works, do this manually:

1. **Go to your project folder**
2. **Create a folder called `.claude`**
3. **Inside `.claude`, create a file called `settings.json`**
4. **Paste this:**

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

5. **Save the file**
6. **Restart Claude Code**

**Done!**

---

## Still Not Working?

1. **Verify Connector is installed:**
   ```bash
   python -m servicenow_mcp.cli.sn_connect --instance any --list
   ```
   Should show: My Instance, Handtmann Test

2. **Verify sessions are cached:**
   ```bash
   python -m servicenow_mcp.cli.sn_connect --instance any --show-cache
   ```
   Should show valid sessions

3. **Check the settings file:**
   ```bash
   cat .claude/settings.json
   ```
   Should show the JSON above

4. **Test from command line:**
   ```bash
   cd "E:/Claude Dev/servicenow-mcp"
   python -m servicenow_mcp.main
   ```
   Should start the server (Ctrl+C to stop)

---

## Need Help?

- Full docs: `E:/Claude Dev/servicenow-mcp/README.md`
- Global setup: `E:/Claude Dev/servicenow-mcp/GLOBAL_SETUP.md`
- GitHub: https://github.com/Kromula/Connector/issues
