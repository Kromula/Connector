"""CLI tool for authenticating to ServiceNow instances."""

import argparse
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from servicenow_mcp.config_manager import ConfigManager
from servicenow_mcp.session_cache import SessionCache
from servicenow_mcp.auth.servicenow_auth import ServiceNowAuth, AuthenticationError


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description='Authenticate to a ServiceNow instance with MFA support'
    )
    parser.add_argument(
        '--instance',
        required=True,
        help='Instance name from config/instances.yaml'
    )
    parser.add_argument(
        '--force',
        action='store_true',
        help='Force re-authentication even if cached session exists'
    )
    parser.add_argument(
        '--list',
        action='store_true',
        help='List all configured instances'
    )
    parser.add_argument(
        '--show-cache',
        action='store_true',
        help='Show cached sessions status'
    )
    parser.add_argument(
        '--clear-cache',
        action='store_true',
        help='Clear all cached sessions'
    )

    args = parser.parse_args()

    try:
        # Initialize managers
        config_manager = ConfigManager()
        session_config = config_manager.get_session_config()
        session_cache = SessionCache(
            cache_path=session_config.get('cache_location'),
            duration_hours=session_config.get('cache_duration_hours', 8)
        )

        # Handle list instances
        if args.list:
            print("\n[LIST] Configured Instances:")
            for instance in config_manager.list_instances():
                print(f"       * {instance}")
            return 0

        # Handle show cache
        if args.show_cache:
            print("\n[CACHE] Cached Sessions:")
            cached = session_cache.list_cached_sessions()
            if not cached:
                print("        No cached sessions")
            else:
                for instance, info in cached.items():
                    status = "[VALID]" if info['valid'] else "[EXPIRED]"
                    print(f"        {instance}: {status}")
                    print(f"           Created: {info['created_at']}")
                    print(f"           Expires: {info['expires_at']}")
            return 0

        # Handle clear cache
        if args.clear_cache:
            session_cache.clear_all()
            print("[OK] All cached sessions cleared")
            return 0

        # Get instance configuration
        instance_name = args.instance
        instance_config = config_manager.get_instance_config(instance_name)

        # Check for password
        if 'password' not in instance_config or not instance_config['password']:
            print(f"\n[ERROR] Password not found for instance '{instance_name}'")
            print(f"        Set it in config/instances.yaml or environment variable:")
            print(f"        SERVICENOW_PASSWORD_{instance_name.upper().replace('-', '_')}")
            return 1

        # Check for cached session
        if not args.force:
            cached_session = session_cache.get_session(instance_name)
            if cached_session:
                print(f"\n[OK] Using cached session for '{instance_name}'")
                print(f"     Session valid until: {cached_session.get('expires_at', 'unknown')}")

                # Verify session is still valid
                auth = ServiceNowAuth(
                    instance_url=instance_config['url'],
                    username=instance_config['username'],
                    password=instance_config['password']
                )
                if auth.verify_session(cached_session):
                    print("     [OK] Session verified and active")
                    return 0
                else:
                    print("     [WARNING] Session validation failed, re-authenticating...")
                    session_cache.invalidate_session(instance_name)

        # Authenticate
        auth = ServiceNowAuth(
            instance_url=instance_config['url'],
            username=instance_config['username'],
            password=instance_config['password']
        )

        session_data = auth.authenticate(interactive=True)

        # Cache the session
        session_cache.save_session(instance_name, session_data)

        print(f"\n[OK] Authentication complete!")
        print(f"     Session cached for {session_config.get('cache_duration_hours', 8)} hours")
        print(f"\n     You can now use the ServiceNow MCP server with instance: {instance_name}")

        return 0

    except FileNotFoundError as e:
        print(f"\n[ERROR] Configuration Error:\n        {str(e)}")
        return 1
    except ValueError as e:
        print(f"\n[ERROR] {str(e)}")
        return 1
    except AuthenticationError as e:
        print(f"\n[ERROR] Authentication Failed:\n        {str(e)}")
        return 1
    except KeyboardInterrupt:
        print("\n\n[WARNING] Authentication cancelled by user")
        return 1
    except Exception as e:
        print(f"\n[ERROR] Unexpected error: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
