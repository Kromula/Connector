# Changelog

All notable changes to the Connector (ServiceNow MCP Server) project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned
- OAuth 2.0 authentication support
- Batch operations for bulk data processing
- Enhanced logging and debugging options
- Video tutorials and expanded documentation

## [1.0.0] - 2026-01-09

### Added
- Initial release of ServiceNow MCP Server
- Interactive MFA authentication with push notification support
- Session caching with configurable expiration (default 8 hours)
- Multi-instance support via YAML configuration
- 16 MCP tools for ServiceNow operations:
  - General table operations (get_records, get_record, create_record, update_record, delete_record)
  - Incident management (get_incidents, create_incident, update_incident)
  - UI Actions management (get_ui_actions, get_ui_action, create_ui_action, update_ui_action)
  - Schema operations (get_tables, get_table_schema)
  - Business Rules (get_business_rules, create_business_rule)
- CLI tool `sn-connect` for authentication and session management
- Comprehensive documentation (README, QUICKSTART, PROJECT_STRUCTURE)
- Helper scripts for Windows and Unix systems
- Example configuration files
- Issue templates for GitHub
- Contributing guidelines
- MIT License

### Features
- **Authentication**
  - Basic authentication with username/password
  - Interactive MFA approval flow
  - 5-minute timeout for MFA approval
  - Automatic session verification

- **Session Management**
  - JSON-based session caching
  - Thread-safe cache operations
  - Automatic expiration handling
  - Session validation before use

- **Configuration**
  - YAML-based instance configuration
  - Environment variable support for passwords
  - Configurable session duration
  - Multiple instance support

- **CLI Commands**
  - `sn-connect --instance <name>` - Authenticate to instance
  - `sn-connect --list` - List configured instances
  - `sn-connect --show-cache` - View cached sessions
  - `sn-connect --clear-cache` - Clear all sessions
  - `sn-connect --force` - Force re-authentication

### Documentation
- Complete README with setup instructions
- Quick start guide for new users
- Project structure documentation
- Example MCP configuration for Claude Desktop
- Issue templates for bug reports, feature requests, and questions
- Contributing guidelines
- Pull request template

### Security
- Credentials properly gitignored
- Session data stored locally
- Support for environment variable passwords
- No sensitive data in repository

## [0.1.0] - Development

### Development Phase
- Initial architecture and design
- Core authentication implementation
- MCP tool development
- Documentation creation

---

## Categories

### Added
For new features.

### Changed
For changes in existing functionality.

### Deprecated
For soon-to-be removed features.

### Removed
For now removed features.

### Fixed
For any bug fixes.

### Security
In case of vulnerabilities.
