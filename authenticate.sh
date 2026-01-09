#!/bin/bash
# Linux/Mac shell script for ServiceNow authentication

if [ -z "$1" ]; then
    echo "Usage: ./authenticate.sh instance-name"
    echo "Example: ./authenticate.sh customer1-dev"
    echo ""
    echo "Available commands:"
    echo "  ./authenticate.sh --list         List configured instances"
    echo "  ./authenticate.sh --show-cache   Show cached sessions"
    echo "  ./authenticate.sh --clear-cache  Clear all cached sessions"
    exit 1
fi

python -m servicenow_mcp.cli.sn_connect --instance "$@"
