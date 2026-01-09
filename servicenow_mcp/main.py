"""Main entry point for ServiceNow MCP Server."""

import asyncio
import sys
from .mcp_server.server import ServiceNowMCPServer


def main():
    """Run the ServiceNow MCP Server."""
    server = ServiceNowMCPServer()
    asyncio.run(server.run())


if __name__ == "__main__":
    main()
