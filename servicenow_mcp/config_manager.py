"""Configuration manager for ServiceNow instances."""

import os
import yaml
from pathlib import Path
from typing import Dict, Optional


class ConfigManager:
    """Manages ServiceNow instance configurations from YAML file."""

    def __init__(self, config_path: Optional[str] = None):
        if config_path is None:
            # Default to config/instances.yaml in project root
            project_root = Path(__file__).parent.parent
            config_path = project_root / "config" / "instances.yaml"

        self.config_path = Path(config_path)
        self.config = self._load_config()

    def _load_config(self) -> Dict:
        """Load configuration from YAML file."""
        if not self.config_path.exists():
            raise FileNotFoundError(
                f"Configuration file not found: {self.config_path}\n"
                f"Please copy config/instances.yaml.example to config/instances.yaml "
                f"and configure your ServiceNow instances."
            )

        with open(self.config_path, 'r') as f:
            return yaml.safe_load(f)

    def get_instance_config(self, instance_name: str) -> Dict:
        """Get configuration for a specific instance."""
        instances = self.config.get('instances', {})

        if instance_name not in instances:
            available = ', '.join(instances.keys())
            raise ValueError(
                f"Instance '{instance_name}' not found in configuration. "
                f"Available instances: {available}"
            )

        instance_config = instances[instance_name].copy()

        # Try to get password from environment variable if not in config
        if 'password' not in instance_config or not instance_config['password']:
            env_var = f"SERVICENOW_PASSWORD_{instance_name.upper().replace('-', '_')}"
            password = os.environ.get(env_var)
            if password:
                instance_config['password'] = password

        return instance_config

    def list_instances(self) -> list:
        """List all configured instance names."""
        return list(self.config.get('instances', {}).keys())

    def get_session_config(self) -> Dict:
        """Get session cache configuration."""
        return self.config.get('session', {
            'cache_duration_hours': 8,
            'cache_location': 'cache/sessions.json'
        })
