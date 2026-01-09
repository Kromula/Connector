"""ServiceNow authentication client with MFA support."""

import time
import requests
from typing import Dict, Optional
from datetime import datetime


class ServiceNowAuth:
    """Handles ServiceNow authentication including MFA."""

    def __init__(self, instance_url: str, username: str, password: str):
        self.instance_url = instance_url.rstrip('/')
        self.username = username
        self.password = password
        self.session = None

    def authenticate(self, interactive: bool = True) -> Dict:
        """
        Authenticate to ServiceNow with MFA support.

        Args:
            interactive: If True, prompts user to approve MFA on their device

        Returns:
            Dict containing session cookies and metadata
        """
        print(f"\n[AUTH] Authenticating to {self.instance_url}...")
        print(f"       User: {self.username}")

        # Create session
        session = requests.Session()

        # Try basic authentication first
        try:
            # Use basic auth headers for initial authentication
            session.auth = (self.username, self.password)

            # Test authentication with a simple API call
            test_url = f"{self.instance_url}/api/now/table/sys_user"
            params = {
                'sysparm_limit': 1,
                'sysparm_fields': 'sys_id,user_name'
            }

            response = session.get(test_url, params=params, timeout=30)

            # Check if we got a valid response
            if response.status_code == 200:
                print("[OK] Authentication successful (no MFA required)")
                return self._create_session_data(session)

            # Check for MFA required (401 with specific header or response)
            elif response.status_code == 401:
                if interactive and self._check_mfa_required(response):
                    print("\n[WARNING] MFA Required")
                    return self._handle_mfa_authentication(session)
                else:
                    raise AuthenticationError(
                        f"Authentication failed: {response.status_code} - {response.text}"
                    )

            else:
                raise AuthenticationError(
                    f"Unexpected response: {response.status_code} - {response.text}"
                )

        except requests.exceptions.RequestException as e:
            raise AuthenticationError(f"Connection error: {str(e)}")

    def _check_mfa_required(self, response: requests.Response) -> bool:
        """Check if MFA is required based on response."""
        # ServiceNow may indicate MFA in various ways
        # Check for MFA-related headers or response content
        mfa_headers = ['X-Is-Logged-In', 'X-UserToken']
        return any(header in response.headers for header in mfa_headers)

    def _handle_mfa_authentication(self, session: requests.Session) -> Dict:
        """Handle interactive MFA authentication."""
        print("\n[MFA] MFA Authentication Required")
        print("      Please approve the login request on your mobile device...")
        print("      (This usually appears as a push notification)")

        # Poll for MFA approval
        max_attempts = 60  # 5 minutes with 5-second intervals
        attempt = 0

        test_url = f"{self.instance_url}/api/now/table/sys_user"
        params = {'sysparm_limit': 1, 'sysparm_fields': 'sys_id,user_name'}

        while attempt < max_attempts:
            attempt += 1
            time.sleep(5)

            try:
                # Try the API call again
                response = session.get(test_url, params=params, timeout=30)

                if response.status_code == 200:
                    print("\n[OK] MFA approved! Authentication successful")
                    return self._create_session_data(session)

                elif response.status_code != 401:
                    # Some other error occurred
                    raise AuthenticationError(
                        f"Unexpected response during MFA: {response.status_code}"
                    )

                # Still waiting for MFA approval
                if attempt % 6 == 0:  # Every 30 seconds
                    print(f"      Still waiting... ({attempt * 5}s elapsed)")

            except requests.exceptions.RequestException as e:
                if attempt >= max_attempts:
                    raise AuthenticationError(f"MFA polling failed: {str(e)}")
                continue

        raise AuthenticationError(
            "MFA approval timeout. Please try again and approve within 5 minutes."
        )

    def _create_session_data(self, session: requests.Session) -> Dict:
        """Create session data dictionary from authenticated session."""
        cookies = session.cookies.get_dict()

        return {
            'cookies': cookies,
            'auth': (self.username, self.password),  # Store for session reuse
            'instance_url': self.instance_url,
            'authenticated_at': datetime.now().isoformat()
        }

    def create_authenticated_session(self, session_data: Dict) -> requests.Session:
        """Create a requests.Session from cached session data."""
        session = requests.Session()

        # Restore cookies
        for name, value in session_data['cookies'].items():
            session.cookies.set(name, value)

        # Restore basic auth
        if 'auth' in session_data:
            session.auth = tuple(session_data['auth'])

        return session

    def verify_session(self, session_data: Dict) -> bool:
        """Verify that a cached session is still valid."""
        try:
            session = self.create_authenticated_session(session_data)

            test_url = f"{self.instance_url}/api/now/table/sys_user"
            params = {'sysparm_limit': 1, 'sysparm_fields': 'sys_id'}

            response = session.get(test_url, params=params, timeout=10)
            return response.status_code == 200

        except:
            return False


class AuthenticationError(Exception):
    """Raised when authentication fails."""
    pass
