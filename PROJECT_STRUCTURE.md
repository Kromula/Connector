# ServiceNow MCP Server - Project Structure

## Complete File Tree

```
servicenow-mcp/
│
├── config/
│   ├── instances.yaml.example      # Example ServiceNow instance configuration
│   └── instances.yaml              # Your actual configuration (create from example)
│
├── cache/                          # Session cache storage (auto-generated)
│   └── sessions.json               # Cached authentication sessions
│
├── logs/                           # Application logs (auto-generated)
│
├── servicenow_mcp/                 # Main Python package
│   ├── __init__.py                 # Package initialization
│   ├── main.py                     # MCP server entry point
│   ├── config_manager.py           # YAML configuration loader
│   ├── session_cache.py            # Session caching with expiration
│   │
│   ├── auth/                       # Authentication module
│   │   ├── __init__.py
│   │   └── servicenow_auth.py      # ServiceNow auth with MFA support
│   │
│   ├── mcp_server/                 # MCP server implementation
│   │   ├── __init__.py
│   │   └── server.py               # MCP server with all tools
│   │
│   └── cli/                        # Command-line tools
│       ├── __init__.py
│       └── sn_connect.py           # Authentication CLI tool
│
├── .gitignore                      # Git ignore rules
├── .env.example                    # Environment variables template
├── LICENSE                         # MIT License
├── README.md                       # Full documentation
├── QUICKSTART.md                   # Quick start guide
├── requirements.txt                # Python dependencies
├── setup.py                        # Package setup script
├── pyproject.toml                  # Modern Python project config
├── mcp_config_example.json         # Claude Desktop MCP config example
│
├── authenticate.bat                # Windows authentication script
├── authenticate.sh                 # Linux/Mac authentication script
├── run_server.bat                  # Windows server launcher
└── run_server.sh                   # Linux/Mac server launcher
```

## Key Components

### Core Modules

1. **config_manager.py** (89 lines)
   - Loads YAML configuration
   - Manages multiple instance configs
   - Supports environment variable passwords

2. **session_cache.py** (97 lines)
   - Thread-safe session storage
   - Automatic expiration handling
   - JSON-based persistence

3. **auth/servicenow_auth.py** (157 lines)
   - Basic authentication
   - Interactive MFA flow with polling
   - Session verification
   - 5-minute timeout for MFA approval

4. **mcp_server/server.py** (539 lines)
   - 16 MCP tools for ServiceNow operations
   - Automatic session management
   - Comprehensive error handling
   - Full CRUD operations for tables

5. **cli/sn_connect.py** (138 lines)
   - Interactive authentication
   - Session management commands
   - Instance listing and status

### MCP Tools Provided

#### General Operations (5 tools)
- get_records
- get_record
- create_record
- update_record
- delete_record

#### Incident Management (3 tools)
- get_incidents
- create_incident
- update_incident

#### UI Actions (4 tools)
- get_ui_actions
- get_ui_action
- create_ui_action
- update_ui_action

#### Schema & Metadata (2 tools)
- get_tables
- get_table_schema

#### Business Rules (2 tools)
- get_business_rules
- create_business_rule

## Configuration Files

### instances.yaml Structure
```yaml
instances:
  <instance-name>:
    url: https://<instance>.service-now.com
    username: <username>
    password: <optional-password>

session:
  cache_duration_hours: 8
  cache_location: cache/sessions.json
```

### Environment Variables
```
SERVICENOW_PASSWORD_<INSTANCE_NAME_UPPER>
```

## Entry Points

### CLI Commands (after installation)
- `sn-connect` - Authenticate to instances
- `servicenow-mcp` - Run MCP server

### Python Module Commands
- `python -m servicenow_mcp.main` - Run MCP server
- `python -m servicenow_mcp.cli.sn_connect` - Authentication CLI

### Helper Scripts
- `authenticate.bat` / `authenticate.sh` - Quick authentication
- `run_server.bat` / `run_server.sh` - Quick server start

## Data Flow

```
User Request
    ↓
MCP Tool Call
    ↓
Session Cache Check
    ↓
[Valid?] → Yes → Use Cached Session
    ↓ No
Authenticate with MFA
    ↓
Cache New Session
    ↓
ServiceNow API Call
    ↓
Return Result
```

## Authentication Flow

```
1. sn-connect --instance customer1-dev
2. Load instance config from YAML
3. Check for cached session
4. [Expired/Missing] → Authenticate
5. Send credentials to ServiceNow
6. [MFA Required] → Wait for mobile approval
7. Poll every 5 seconds (max 5 minutes)
8. Receive session cookies
9. Cache session (8 hours default)
10. Ready for MCP operations
```

## Session Cache Structure

```json
{
  "customer1-dev": {
    "session": {
      "cookies": {...},
      "auth": ["username", "password"],
      "instance_url": "https://...",
      "authenticated_at": "2026-01-09T10:00:00"
    },
    "expires_at": "2026-01-09T18:00:00",
    "created_at": "2026-01-09T10:00:00"
  }
}
```

## Security Features

- Passwords via environment variables (recommended)
- Session expiration (configurable)
- Automatic session validation
- Local-only session storage
- Gitignored sensitive files
- Thread-safe cache operations

## Installation Steps

1. `pip install -r requirements.txt`
2. `cp config/instances.yaml.example config/instances.yaml`
3. Edit `config/instances.yaml`
4. Set environment variables for passwords
5. `sn-connect --instance <name>`
6. Configure Claude Desktop MCP
7. Restart Claude Desktop

## Dependencies

- **requests** - HTTP client for ServiceNow API
- **PyYAML** - YAML configuration parsing
- **mcp** - Model Context Protocol SDK
- **pytest** (dev) - Testing framework
- **black** (dev) - Code formatting
- **mypy** (dev) - Type checking

## Lines of Code

- Python code: ~1,020 lines
- Documentation: ~500 lines
- Configuration: ~150 lines
- **Total: ~1,670 lines**
