"""Session cache manager for ServiceNow authentication."""

import json
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, Dict
from threading import Lock


class SessionCache:
    """Manages cached ServiceNow sessions with expiration."""

    def __init__(self, cache_path: Optional[str] = None, duration_hours: int = 8):
        if cache_path is None:
            project_root = Path(__file__).parent.parent
            cache_path = project_root / "cache" / "sessions.json"

        self.cache_path = Path(cache_path)
        self.duration_hours = duration_hours
        self._lock = Lock()

        # Ensure cache directory exists
        self.cache_path.parent.mkdir(parents=True, exist_ok=True)

        self._cache = self._load_cache()

    def _load_cache(self) -> Dict:
        """Load cache from disk."""
        if not self.cache_path.exists():
            return {}

        try:
            with open(self.cache_path, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return {}

    def _save_cache(self):
        """Save cache to disk."""
        try:
            with open(self.cache_path, 'w') as f:
                json.dump(self._cache, f, indent=2)
        except IOError as e:
            print(f"Warning: Failed to save session cache: {e}")

    def get_session(self, instance_name: str) -> Optional[Dict]:
        """Get cached session for instance if valid."""
        with self._lock:
            if instance_name not in self._cache:
                return None

            session_data = self._cache[instance_name]
            expires_at = datetime.fromisoformat(session_data['expires_at'])

            if datetime.now() >= expires_at:
                # Session expired
                del self._cache[instance_name]
                self._save_cache()
                return None

            return session_data['session']

    def save_session(self, instance_name: str, session: Dict):
        """Save session to cache with expiration."""
        with self._lock:
            expires_at = datetime.now() + timedelta(hours=self.duration_hours)

            self._cache[instance_name] = {
                'session': session,
                'expires_at': expires_at.isoformat(),
                'created_at': datetime.now().isoformat()
            }

            self._save_cache()

    def invalidate_session(self, instance_name: str):
        """Remove session from cache."""
        with self._lock:
            if instance_name in self._cache:
                del self._cache[instance_name]
                self._save_cache()

    def clear_all(self):
        """Clear all cached sessions."""
        with self._lock:
            self._cache = {}
            self._save_cache()

    def list_cached_sessions(self) -> Dict[str, Dict]:
        """List all cached sessions with their expiration times."""
        with self._lock:
            result = {}
            now = datetime.now()

            for instance_name, data in self._cache.items():
                expires_at = datetime.fromisoformat(data['expires_at'])
                result[instance_name] = {
                    'valid': now < expires_at,
                    'expires_at': data['expires_at'],
                    'created_at': data['created_at']
                }

            return result
