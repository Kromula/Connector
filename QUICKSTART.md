# Quick Start Guide

## 1. Install Dependencies

```bash
pip install -r requirements.txt
```

## 2. Configure Your Instances

```bash
# Copy the example configuration
cp config/instances.yaml.example config/instances.yaml

# Edit config/instances.yaml with your ServiceNow instances
# Add your instance URLs and usernames
```

## 3. Set Passwords (Environment Variables Recommended)

### Windows
```cmd
set SERVICENOW_PASSWORD_CUSTOMER1_DEV=your_password_here
set SERVICENOW_PASSWORD_CUSTOMER1_PROD=your_password_here
```

### Linux/Mac
```bash
export SERVICENOW_PASSWORD_CUSTOMER1_DEV=your_password_here
export SERVICENOW_PASSWORD_CUSTOMER1_PROD=your_password_here
```

## 4. Authenticate to an Instance

```bash
python -m servicenow_mcp.cli.sn_connect --instance customer1-dev
```

Follow the prompts:
- Enter your credentials (if not in config)
- Approve the MFA push notification on your mobile device
- Wait for confirmation

## 5. Verify Cached Session

```bash
python -m servicenow_mcp.cli.sn_connect --instance customer1-dev --show-cache
```

## 6. Configure Claude Desktop

Add this to your Claude Desktop MCP configuration file:

**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
**Mac**: `~/Library/Application Support/Claude/claude_desktop_config.json`
**Linux**: `~/.config/Claude/claude_desktop_config.json`

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

## 7. Restart Claude Desktop

Restart Claude Desktop to load the MCP server.

## 8. Test in Claude

Ask Claude:
```
"List all configured ServiceNow instances"
"Show me the incident table schema"
"Get the first 5 incidents from customer1-dev"
```

## Common Commands

### Authentication Management
```bash
# List instances
python -m servicenow_mcp.cli.sn_connect --instance any --list

# Show cached sessions
python -m servicenow_mcp.cli.sn_connect --instance any --show-cache

# Force re-authentication
python -m servicenow_mcp.cli.sn_connect --instance customer1-dev --force

# Clear all sessions
python -m servicenow_mcp.cli.sn_connect --instance any --clear-cache
```

### Running the Server Manually
```bash
# Run MCP server directly
python -m servicenow_mcp.main

# Or use the installed command (after pip install -e .)
servicenow-mcp
```

## Troubleshooting

### MFA Not Working
- Ensure you approve the notification within 5 minutes
- Check that MFA is properly configured on your ServiceNow instance
- Verify network connectivity

### Session Expired
```bash
# Just re-authenticate
python -m servicenow_mcp.cli.sn_connect --instance customer1-dev
```

### Password Issues
- Set via environment variables (recommended)
- Or add to config/instances.yaml under each instance
- Variable format: `SERVICENOW_PASSWORD_<INSTANCE_NAME_UPPERCASE>`

### Connection Errors
- Verify instance URL in config/instances.yaml
- Check network/firewall settings
- Test URL in browser first

## Next Steps

1. Explore available MCP tools in the README
2. Try different ServiceNow API operations
3. Configure additional instances
4. Set up session duration to your preference
