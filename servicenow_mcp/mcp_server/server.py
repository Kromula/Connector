"""ServiceNow MCP Server implementation."""

import json
import logging
from typing import Any, Dict, Optional
from mcp.server import Server
from mcp.types import Tool, TextContent
import requests

from ..config_manager import ConfigManager
from ..session_cache import SessionCache
from ..auth.servicenow_auth import ServiceNowAuth, AuthenticationError


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ServiceNowMCPServer:
    """MCP Server for ServiceNow API operations."""

    def __init__(self):
        self.app = Server("servicenow-mcp")
        self.config_manager = ConfigManager()

        session_config = self.config_manager.get_session_config()
        self.session_cache = SessionCache(
            cache_path=session_config.get('cache_location'),
            duration_hours=session_config.get('cache_duration_hours', 8)
        )

        # Register tools
        self._register_tools()

    def _register_tools(self):
        """Register all ServiceNow MCP tools."""

        @self.app.list_tools()
        async def list_tools() -> list[Tool]:
            """List available ServiceNow tools."""
            return [
                Tool(
                    name="get_records",
                    description="Get records from any ServiceNow table",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "instance": {
                                "type": "string",
                                "description": "ServiceNow instance name from config"
                            },
                            "table": {
                                "type": "string",
                                "description": "Table name (e.g., incident, sys_user, cmdb_ci)"
                            },
                            "query": {
                                "type": "string",
                                "description": "Encoded query string (e.g., 'active=true^priority=1')"
                            },
                            "limit": {
                                "type": "number",
                                "description": "Maximum number of records to return",
                                "default": 10
                            }
                        },
                        "required": ["instance", "table"]
                    }
                ),
                Tool(
                    name="get_record",
                    description="Get a single record by sys_id",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "instance": {
                                "type": "string",
                                "description": "ServiceNow instance name"
                            },
                            "table": {
                                "type": "string",
                                "description": "Table name"
                            },
                            "sys_id": {
                                "type": "string",
                                "description": "Sys ID of the record"
                            }
                        },
                        "required": ["instance", "table", "sys_id"]
                    }
                ),
                Tool(
                    name="create_record",
                    description="Create a new record in any ServiceNow table",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "instance": {
                                "type": "string",
                                "description": "ServiceNow instance name"
                            },
                            "table": {
                                "type": "string",
                                "description": "Table name"
                            },
                            "data": {
                                "type": "object",
                                "description": "Record data as key-value pairs"
                            }
                        },
                        "required": ["instance", "table", "data"]
                    }
                ),
                Tool(
                    name="update_record",
                    description="Update an existing record",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "instance": {
                                "type": "string",
                                "description": "ServiceNow instance name"
                            },
                            "table": {
                                "type": "string",
                                "description": "Table name"
                            },
                            "sys_id": {
                                "type": "string",
                                "description": "Sys ID of the record to update"
                            },
                            "data": {
                                "type": "object",
                                "description": "Fields to update as key-value pairs"
                            }
                        },
                        "required": ["instance", "table", "sys_id", "data"]
                    }
                ),
                Tool(
                    name="delete_record",
                    description="Delete a record from ServiceNow",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "instance": {
                                "type": "string",
                                "description": "ServiceNow instance name"
                            },
                            "table": {
                                "type": "string",
                                "description": "Table name"
                            },
                            "sys_id": {
                                "type": "string",
                                "description": "Sys ID of the record to delete"
                            }
                        },
                        "required": ["instance", "table", "sys_id"]
                    }
                ),
                Tool(
                    name="get_incidents",
                    description="Get incident records with optional filters",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "instance": {
                                "type": "string",
                                "description": "ServiceNow instance name"
                            },
                            "query": {
                                "type": "string",
                                "description": "Encoded query (e.g., 'active=true^state=1')"
                            },
                            "limit": {
                                "type": "number",
                                "description": "Maximum number of incidents",
                                "default": 10
                            }
                        },
                        "required": ["instance"]
                    }
                ),
                Tool(
                    name="create_incident",
                    description="Create a new incident",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "instance": {
                                "type": "string",
                                "description": "ServiceNow instance name"
                            },
                            "short_description": {
                                "type": "string",
                                "description": "Brief description of the incident"
                            },
                            "description": {
                                "type": "string",
                                "description": "Detailed description"
                            },
                            "urgency": {
                                "type": "string",
                                "description": "Urgency level (1=High, 2=Medium, 3=Low)",
                                "enum": ["1", "2", "3"]
                            },
                            "impact": {
                                "type": "string",
                                "description": "Impact level (1=High, 2=Medium, 3=Low)",
                                "enum": ["1", "2", "3"]
                            },
                            "assignment_group": {
                                "type": "string",
                                "description": "Assignment group sys_id or name"
                            }
                        },
                        "required": ["instance", "short_description"]
                    }
                ),
                Tool(
                    name="update_incident",
                    description="Update an existing incident",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "instance": {
                                "type": "string",
                                "description": "ServiceNow instance name"
                            },
                            "sys_id": {
                                "type": "string",
                                "description": "Incident sys_id"
                            },
                            "state": {
                                "type": "string",
                                "description": "State (1=New, 2=In Progress, 6=Resolved, 7=Closed)"
                            },
                            "assigned_to": {
                                "type": "string",
                                "description": "Assigned to user sys_id"
                            },
                            "assignment_group": {
                                "type": "string",
                                "description": "Assignment group"
                            },
                            "work_notes": {
                                "type": "string",
                                "description": "Work notes to add"
                            },
                            "close_notes": {
                                "type": "string",
                                "description": "Closure notes"
                            }
                        },
                        "required": ["instance", "sys_id"]
                    }
                ),
                Tool(
                    name="get_ui_actions",
                    description="Get UI Actions from ServiceNow, optionally filtered by table",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "instance": {
                                "type": "string",
                                "description": "ServiceNow instance name"
                            },
                            "table": {
                                "type": "string",
                                "description": "Filter by table name (e.g., incident, change_request)"
                            },
                            "limit": {
                                "type": "number",
                                "description": "Maximum number of UI Actions to return",
                                "default": 50
                            }
                        },
                        "required": ["instance"]
                    }
                ),
                Tool(
                    name="get_ui_action",
                    description="Get a specific UI Action by sys_id",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "instance": {
                                "type": "string",
                                "description": "ServiceNow instance name"
                            },
                            "sys_id": {
                                "type": "string",
                                "description": "Sys ID of the UI Action"
                            }
                        },
                        "required": ["instance", "sys_id"]
                    }
                ),
                Tool(
                    name="create_ui_action",
                    description="Create a new UI Action in ServiceNow",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "instance": {"type": "string", "description": "ServiceNow instance name"},
                            "name": {"type": "string", "description": "Name of the UI Action"},
                            "table": {"type": "string", "description": "Table the UI Action applies to"},
                            "action_name": {"type": "string", "description": "Action name (used in scripting)"},
                            "script": {"type": "string", "description": "Server-side script to execute"},
                            "client_script_v2": {"type": "string", "description": "Client-side script (onClick)"},
                            "condition": {"type": "string", "description": "Condition script for when to show the action"},
                            "hint": {"type": "string", "description": "Tooltip/hint text"},
                            "order": {"type": "number", "description": "Display order", "default": 100},
                            "active": {"type": "boolean", "description": "Whether the UI Action is active", "default": True},
                            "form_button": {"type": "boolean", "description": "Show as form button", "default": False},
                            "form_link": {"type": "boolean", "description": "Show as form link", "default": False},
                            "form_context_menu": {"type": "boolean", "description": "Show in form context menu", "default": False},
                            "list_button": {"type": "boolean", "description": "Show as list button", "default": False},
                            "list_link": {"type": "boolean", "description": "Show as list link", "default": False},
                            "list_context_menu": {"type": "boolean", "description": "Show in list context menu", "default": False}
                        },
                        "required": ["instance", "name", "table"]
                    }
                ),
                Tool(
                    name="update_ui_action",
                    description="Update an existing UI Action",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "instance": {
                                "type": "string",
                                "description": "ServiceNow instance name"
                            },
                            "sys_id": {
                                "type": "string",
                                "description": "Sys ID of the UI Action to update"
                            },
                            "data": {
                                "type": "object",
                                "description": "Fields to update (name, script, condition, etc.)"
                            }
                        },
                        "required": ["instance", "sys_id", "data"]
                    }
                ),
                Tool(
                    name="get_tables",
                    description="List available tables in ServiceNow",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "instance": {
                                "type": "string",
                                "description": "ServiceNow instance name"
                            },
                            "limit": {
                                "type": "number",
                                "description": "Maximum number of tables to return",
                                "default": 100
                            }
                        },
                        "required": ["instance"]
                    }
                ),
                Tool(
                    name="get_table_schema",
                    description="Get schema information for a specific table",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "instance": {
                                "type": "string",
                                "description": "ServiceNow instance name"
                            },
                            "table": {
                                "type": "string",
                                "description": "Table name"
                            }
                        },
                        "required": ["instance", "table"]
                    }
                ),
                Tool(
                    name="get_business_rules",
                    description="Get Business Rules, optionally filtered by table",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "instance": {
                                "type": "string",
                                "description": "ServiceNow instance name"
                            },
                            "table": {
                                "type": "string",
                                "description": "Filter by table name"
                            },
                            "limit": {
                                "type": "number",
                                "description": "Maximum number to return",
                                "default": 50
                            }
                        },
                        "required": ["instance"]
                    }
                ),
                Tool(
                    name="create_business_rule",
                    description="Create a new Business Rule",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "instance": {"type": "string", "description": "ServiceNow instance name"},
                            "name": {"type": "string", "description": "Name of the Business Rule"},
                            "collection": {"type": "string", "description": "Table name"},
                            "script": {"type": "string", "description": "Script to execute"},
                            "when": {
                                "type": "string",
                                "description": "When to run (before, after, async, display)",
                                "enum": ["before", "after", "async", "display"]
                            },
                            "active": {"type": "boolean", "description": "Whether active", "default": True}
                        },
                        "required": ["instance", "name", "collection", "script"]
                    }
                )
            ]

        @self.app.call_tool()
        async def call_tool(name: str, arguments: Any) -> list[TextContent]:
            """Handle tool calls."""
            try:
                result = await self._handle_tool_call(name, arguments)
                return [TextContent(type="text", text=json.dumps(result, indent=2))]
            except Exception as e:
                logger.error(f"Tool call error: {str(e)}")
                return [TextContent(type="text", text=f"Error: {str(e)}")]

    def _get_authenticated_session(self, instance_name: str) -> requests.Session:
        """Get or create an authenticated session for an instance."""
        # Try to get cached session
        cached_session = self.session_cache.get_session(instance_name)

        if cached_session:
            # Get instance config for creating session
            instance_config = self.config_manager.get_instance_config(instance_name)
            auth = ServiceNowAuth(
                instance_url=instance_config['url'],
                username=instance_config['username'],
                password=instance_config.get('password', '')
            )

            # Verify session is still valid
            if auth.verify_session(cached_session):
                return auth.create_authenticated_session(cached_session)
            else:
                # Session invalid, clear it
                self.session_cache.invalidate_session(instance_name)

        # No valid cached session
        raise AuthenticationError(
            f"No valid session found for instance '{instance_name}'. "
            f"Please run: sn-connect --instance {instance_name}"
        )

    async def _handle_tool_call(self, name: str, arguments: Dict[str, Any]) -> Dict:
        """Handle individual tool calls."""
        instance_name = arguments.get('instance')
        if not instance_name:
            raise ValueError("Instance name is required")

        # Get authenticated session
        session = self._get_authenticated_session(instance_name)
        instance_config = self.config_manager.get_instance_config(instance_name)
        base_url = instance_config['url']

        # Route to appropriate handler
        if name == "get_records":
            return self._get_records(session, base_url, arguments)
        elif name == "get_record":
            return self._get_record(session, base_url, arguments)
        elif name == "create_record":
            return self._create_record(session, base_url, arguments)
        elif name == "update_record":
            return self._update_record(session, base_url, arguments)
        elif name == "delete_record":
            return self._delete_record(session, base_url, arguments)
        elif name == "get_incidents":
            return self._get_incidents(session, base_url, arguments)
        elif name == "create_incident":
            return self._create_incident(session, base_url, arguments)
        elif name == "update_incident":
            return self._update_incident(session, base_url, arguments)
        elif name == "get_ui_actions":
            return self._get_ui_actions(session, base_url, arguments)
        elif name == "get_ui_action":
            return self._get_ui_action(session, base_url, arguments)
        elif name == "create_ui_action":
            return self._create_ui_action(session, base_url, arguments)
        elif name == "update_ui_action":
            return self._update_ui_action(session, base_url, arguments)
        elif name == "get_tables":
            return self._get_tables(session, base_url, arguments)
        elif name == "get_table_schema":
            return self._get_table_schema(session, base_url, arguments)
        elif name == "get_business_rules":
            return self._get_business_rules(session, base_url, arguments)
        elif name == "create_business_rule":
            return self._create_business_rule(session, base_url, arguments)
        else:
            raise ValueError(f"Unknown tool: {name}")

    def _get_records(self, session: requests.Session, base_url: str, args: Dict) -> Dict:
        """Get records from a table."""
        table = args['table']
        url = f"{base_url}/api/now/table/{table}"

        params = {'sysparm_limit': args.get('limit', 10)}
        if args.get('query'):
            params['sysparm_query'] = args['query']

        response = session.get(url, params=params)
        response.raise_for_status()
        return response.json()

    def _get_record(self, session: requests.Session, base_url: str, args: Dict) -> Dict:
        """Get a single record by sys_id."""
        table = args['table']
        sys_id = args['sys_id']
        url = f"{base_url}/api/now/table/{table}/{sys_id}"

        response = session.get(url)
        response.raise_for_status()
        return response.json()

    def _create_record(self, session: requests.Session, base_url: str, args: Dict) -> Dict:
        """Create a new record."""
        table = args['table']
        data = args['data']
        url = f"{base_url}/api/now/table/{table}"

        response = session.post(url, json=data)
        response.raise_for_status()
        return response.json()

    def _update_record(self, session: requests.Session, base_url: str, args: Dict) -> Dict:
        """Update an existing record."""
        table = args['table']
        sys_id = args['sys_id']
        data = args['data']
        url = f"{base_url}/api/now/table/{table}/{sys_id}"

        response = session.put(url, json=data)
        response.raise_for_status()
        return response.json()

    def _delete_record(self, session: requests.Session, base_url: str, args: Dict) -> Dict:
        """Delete a record."""
        table = args['table']
        sys_id = args['sys_id']
        url = f"{base_url}/api/now/table/{table}/{sys_id}"

        response = session.delete(url)
        response.raise_for_status()
        return {"success": True, "message": "Record deleted"}

    def _get_incidents(self, session: requests.Session, base_url: str, args: Dict) -> Dict:
        """Get incidents."""
        args['table'] = 'incident'
        return self._get_records(session, base_url, args)

    def _create_incident(self, session: requests.Session, base_url: str, args: Dict) -> Dict:
        """Create an incident."""
        data = {k: v for k, v in args.items() if k != 'instance'}
        args_copy = {'table': 'incident', 'data': data}
        return self._create_record(session, base_url, args_copy)

    def _update_incident(self, session: requests.Session, base_url: str, args: Dict) -> Dict:
        """Update an incident."""
        sys_id = args.pop('sys_id')
        data = {k: v for k, v in args.items() if k != 'instance'}
        args_copy = {'table': 'incident', 'sys_id': sys_id, 'data': data}
        return self._update_record(session, base_url, args_copy)

    def _get_ui_actions(self, session: requests.Session, base_url: str, args: Dict) -> Dict:
        """Get UI Actions."""
        url = f"{base_url}/api/now/table/sys_ui_action"
        params = {'sysparm_limit': args.get('limit', 50)}
        if args.get('table'):
            params['sysparm_query'] = f"table={args['table']}"

        response = session.get(url, params=params)
        response.raise_for_status()
        return response.json()

    def _get_ui_action(self, session: requests.Session, base_url: str, args: Dict) -> Dict:
        """Get a specific UI Action."""
        sys_id = args['sys_id']
        url = f"{base_url}/api/now/table/sys_ui_action/{sys_id}"

        response = session.get(url)
        response.raise_for_status()
        return response.json()

    def _create_ui_action(self, session: requests.Session, base_url: str, args: Dict) -> Dict:
        """Create a UI Action."""
        data = {k: v for k, v in args.items() if k != 'instance'}
        url = f"{base_url}/api/now/table/sys_ui_action"

        response = session.post(url, json=data)
        response.raise_for_status()
        return response.json()

    def _update_ui_action(self, session: requests.Session, base_url: str, args: Dict) -> Dict:
        """Update a UI Action."""
        sys_id = args['sys_id']
        data = args['data']
        url = f"{base_url}/api/now/table/sys_ui_action/{sys_id}"

        response = session.put(url, json=data)
        response.raise_for_status()
        return response.json()

    def _get_tables(self, session: requests.Session, base_url: str, args: Dict) -> Dict:
        """Get list of tables."""
        url = f"{base_url}/api/now/table/sys_db_object"
        params = {
            'sysparm_limit': args.get('limit', 100),
            'sysparm_fields': 'name,label,super_class'
        }

        response = session.get(url, params=params)
        response.raise_for_status()
        return response.json()

    def _get_table_schema(self, session: requests.Session, base_url: str, args: Dict) -> Dict:
        """Get table schema."""
        table = args['table']
        url = f"{base_url}/api/now/table/sys_dictionary"
        params = {
            'sysparm_query': f"name={table}",
            'sysparm_fields': 'element,column_label,internal_type,mandatory,max_length,reference'
        }

        response = session.get(url, params=params)
        response.raise_for_status()
        return response.json()

    def _get_business_rules(self, session: requests.Session, base_url: str, args: Dict) -> Dict:
        """Get Business Rules."""
        url = f"{base_url}/api/now/table/sys_script"
        params = {'sysparm_limit': args.get('limit', 50)}
        if args.get('table'):
            params['sysparm_query'] = f"collection={args['table']}"

        response = session.get(url, params=params)
        response.raise_for_status()
        return response.json()

    def _create_business_rule(self, session: requests.Session, base_url: str, args: Dict) -> Dict:
        """Create a Business Rule."""
        data = {k: v for k, v in args.items() if k != 'instance'}
        url = f"{base_url}/api/now/table/sys_script"

        response = session.post(url, json=data)
        response.raise_for_status()
        return response.json()

    async def run(self):
        """Run the MCP server."""
        from mcp.server.stdio import stdio_server

        async with stdio_server() as (read_stream, write_stream):
            await self.app.run(
                read_stream,
                write_stream,
                self.app.create_initialization_options()
            )
