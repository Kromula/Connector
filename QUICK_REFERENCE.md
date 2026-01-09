# Quick Reference Card

## 🎯 Setup New Project (3 Steps)

```bash
# 1. Go to your project
cd "E:/Claude Dev/YourProject"

# 2. Copy the template
mkdir .claude
copy "E:\Claude Dev\servicenow-mcp\templates\claude-settings.json" ".claude\settings.json"

# 3. Restart Claude Code
```

**Done!** ServiceNow is now available in your project.

---

## 🔑 Authentication Commands

```bash
# Authenticate to an instance
python -m servicenow_mcp.cli.sn_connect --instance "Handtmann Test"

# Check sessions
python -m servicenow_mcp.cli.sn_connect --instance any --show-cache

# List instances
python -m servicenow_mcp.cli.sn_connect --instance any --list
```

---

## 📝 What's in settings.json

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

---

## 🌐 Available Instances

- `My Instance` - empdoconnor.service-now.com
- `Handtmann Test` - handtmanntest.service-now.com

---

## 🧪 Test It

In Claude Code, ask:
```
"Get the latest 3 incidents from Handtmann Test"
"Show me the sys_user table schema"
"List all UI Actions for the incident table"
```

---

## ❓ Not Working?

**Check 1:** Does the file exist?
```bash
cat .claude/settings.json
```

**Check 2:** Is session valid?
```bash
python -m servicenow_mcp.cli.sn_connect --instance any --show-cache
```

**Check 3:** Restart Claude Code completely

---

## 📂 File Structure

```
Your Project/
└── .claude/
    └── settings.json  ← Only file needed!
```

---

## 🔄 When Session Expires

Re-authenticate (every 8 hours):
```bash
python -m servicenow_mcp.cli.sn_connect --instance "Handtmann Test"
```

---

## 📚 Full Docs

- Simple Guide: `SIMPLE_SETUP_GUIDE.md`
- Visual Diagram: `SETUP_DIAGRAM.txt`
- Complete Guide: `GLOBAL_SETUP.md`
- GitHub: https://github.com/Kromula/Connector
