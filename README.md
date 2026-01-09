# ServiceNow MCP Server (Connector)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![GitHub issues](https://img.shields.io/github/issues/Kromula/Connector)](https://github.com/Kromula/Connector/issues)
[![GitHub stars](https://img.shields.io/github/stars/Kromula/Connector)](https://github.com/Kromula/Connector/stargazers)

A Model Context Protocol (MCP) server that provides authenticated access to ServiceNow instances with MFA support and session caching.

## Features

- **MFA Support**: Interactive MFA approval flow with mobile push notifications
- **Session Caching**: Persist authenticated sessions for hours (configurable)
- **Multi-Instance**: Support multiple ServiceNow customer instances via YAML configuration
- **Rich API Tools**: Comprehensive MCP tools for ServiceNow operations
- **Easy Authentication**: Simple CLI command to authenticate and cache sessions

## Installation

### From Source

```bash
cd servicenow-mcp
pip install -e .
```

### Using pip

```bash
pip install -r requirements.txt
```

## Configuration

### 1. Create Instance Configuration

Copy the example configuration and customize it:

```bash
cp config/instances.yaml.example config/instances.yaml
```

Edit `config/instances.yaml`:

```yaml
instances:
  customer1-dev:
    url: https://customer1dev.service-now.com
    username: admin
    # password: your_password  # Or use environment variable

  customer1-prod:
    url: https://customer1.service-now.com
    username: admin

session:
  cache_duration_hours: 8
  cache_location: cache/sessions.json
```

### 2. Set Passwords (Recommended via Environment Variables)

```bash
# Windows
set SERVICENOW_PASSWORD_CUSTOMER1_DEV=your_password_here

# Linux/Mac
export SERVICENOW_PASSWORD_CUSTOMER1_DEV=your_password_here
```

Or store passwords directly in `config/instances.yaml` (less secure).

## Usage

### Authenticate to a ServiceNow Instance

Use the `sn-connect` CLI tool to authenticate with MFA:

```bash
sn-connect --instance customer1-dev
```

The tool will:
1. Prompt for authentication
2. Wait for you to approve MFA on your mobile device
3. Cache the session for reuse (default: 8 hours)

#### CLI Options

```bash
# Force re-authentication (ignore cached session)
sn-connect --instance customer1-dev --force

# List all configured instances
sn-connect --instance any --list

# Show cached sessions status
sn-connect --instance any --show-cache

# Clear all cached sessions
sn-connect --instance any --clear-cache
```

### Run the MCP Server

After authenticating, start the MCP server:

```bash
servicenow-mcp
```

Or run directly with Python:

```bash
python -m servicenow_mcp.main
```

### Configure MCP Client (Claude Desktop)

Add to your Claude Desktop MCP configuration (`claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "servicenow": {
      "command": "python",
      "args": [
        "-m",
        "servicenow_mcp.main"
      ],
      "cwd": "E:/Claude Dev/servicenow-mcp"
    }
  }
}
```

## Available MCP Tools

### General Table Operations

- **get_records**: Query records from any table
- **get_record**: Get a single record by sys_id
- **create_record**: Create a new record
- **update_record**: Update an existing record
- **delete_record**: Delete a record

### Incident Management

- **get_incidents**: Get incident records with filters
- **create_incident**: Create a new incident
- **update_incident**: Update an incident (state, assignment, notes)

### UI Actions

- **get_ui_actions**: List UI Actions (optionally filtered by table)
- **get_ui_action**: Get a specific UI Action
- **create_ui_action**: Create a new UI Action
- **update_ui_action**: Update an existing UI Action

### Schema & Metadata

- **get_tables**: List available tables
- **get_table_schema**: Get field definitions for a table

### Business Rules

- **get_business_rules**: List Business Rules (optionally filtered by table)
- **create_business_rule**: Create a new Business Rule

## Example Usage in Claude

Once configured, you can use natural language with Claude:

```
"Show me all high-priority incidents in customer1-dev"

"Create an incident in customer1-prod with description 'Database connection timeout'"

"Get the schema for the incident table"

"List all UI Actions for the incident table"

"Create a UI Action that closes an incident on the incident form"
```

## Project Structure

```
servicenow-mcp/
├── config/
│   ├── instances.yaml.example    # Example configuration
│   └── instances.yaml             # Your configuration (gitignored)
├── cache/                         # Session cache (gitignored)
├── logs/                          # Application logs (gitignored)
├── servicenow_mcp/
│   ├── __init__.py
│   ├── main.py                    # MCP server entry point
│   ├── config_manager.py          # YAML configuration loader
│   ├── session_cache.py           # Session caching with expiration
│   ├── auth/
│   │   ├── __init__.py
│   │   └── servicenow_auth.py     # Authentication with MFA support
│   ├── mcp_server/
│   │   ├── __init__.py
│   │   └── server.py              # MCP server implementation
│   └── cli/
│       ├── __init__.py
│       └── sn_connect.py          # CLI authentication tool
├── requirements.txt
├── setup.py
├── pyproject.toml
└── README.md
```

## Session Management

Sessions are cached locally with the following behavior:

- **Duration**: 8 hours by default (configurable in `instances.yaml`)
- **Location**: `cache/sessions.json` (configurable)
- **Validation**: Sessions are verified before use
- **Expiration**: Automatically removed when expired

### Managing Sessions

```bash
# View cached sessions
sn-connect --instance any --show-cache

# Clear all sessions (forces re-authentication)
sn-connect --instance any --clear-cache

# Force re-authentication for specific instance
sn-connect --instance customer1-dev --force
```

## MFA Authentication Flow

When authenticating with MFA enabled:

1. CLI sends username/password to ServiceNow
2. ServiceNow sends push notification to your mobile device
3. CLI polls for approval (max 5 minutes)
4. You approve on your device
5. CLI receives session and caches it

The next time you authenticate (within session duration), the cached session is used automatically.

## Security Considerations

- Store passwords in environment variables, not in YAML files
- Keep `config/instances.yaml` and `cache/` gitignored
- Sessions are stored locally in `cache/sessions.json`
- Use appropriate file permissions on cache directory
- Sessions expire automatically after configured duration

## Troubleshooting

### "No valid session found"

Run authentication:
```bash
sn-connect --instance <instance-name>
```

### MFA timeout

Increase polling timeout in `servicenow_auth.py` or approve faster on your device.

### Connection errors

- Verify instance URL in `config/instances.yaml`
- Check network connectivity to ServiceNow
- Ensure credentials are correct

### Session validation fails

Clear cache and re-authenticate:
```bash
sn-connect --instance <instance-name> --clear-cache
sn-connect --instance <instance-name>
```

## Development

### Run Tests

```bash
pytest
```

### Code Formatting

```bash
black servicenow_mcp/
```

### Type Checking

```bash
mypy servicenow_mcp/
```

## Contributing

We welcome contributions! Please see our [Contributing Guidelines](.github/CONTRIBUTING.md) for details.

### How to Contribute

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Reporting Issues

Found a bug or have a feature request? Please create an issue:
- [Report a Bug](https://github.com/Kromula/Connector/issues/new?template=bug_report.md)
- [Request a Feature](https://github.com/Kromula/Connector/issues/new?template=feature_request.md)
- [Ask a Question](https://github.com/Kromula/Connector/issues/new?template=question.md)

## Repository

GitHub: [https://github.com/Kromula/Connector](https://github.com/Kromula/Connector)

## License

MIT License - see [LICENSE](LICENSE) file for details

## Acknowledgments

- Built with [Model Context Protocol](https://modelcontextprotocol.io/)
- Powered by [ServiceNow REST API](https://developer.servicenow.com/dev.do)
- Created with Claude Code

## Support

- Documentation: [README.md](README.md) | [QUICKSTART.md](QUICKSTART.md)
- Issues: [GitHub Issues](https://github.com/Kromula/Connector/issues)
- Security: [Security Policy](.github/SECURITY.md)
