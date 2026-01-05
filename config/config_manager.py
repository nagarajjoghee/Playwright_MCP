"""
Configuration Manager for handling environment-specific settings.
"""
import json
import os
import logging
from typing import Dict, Any, Optional
from pathlib import Path

logger = logging.getLogger(__name__)


class ConfigManager:
    """Manages configuration and environment settings."""
    
    def __init__(self, environment: str = None):
        self.project_root = Path(__file__).parent.parent
        self.config_dir = self.project_root / "config"
        self.test_data_dir = self.project_root / "test_data"
        self.environments_dir = self.test_data_dir / "environments"
        
        # Determine environment from env variable or default to dev
        self.environment = environment or os.getenv("TEST_ENV", "dev")
        self.config: Dict[str, Any] = {}
        self.test_data: Dict[str, Any] = {}
        
        self._load_config()
        self._load_test_data()
    
    def _load_config(self):
        """Load environment-specific configuration."""
        try:
            env_file = self.environments_dir / f"{self.environment}.json"
            if env_file.exists():
                with open(env_file, 'r') as f:
                    self.config = json.load(f)
                logger.info(f"Loaded configuration for environment: {self.environment}")
            else:
                logger.warning(f"Config file not found: {env_file}, using defaults")
                self.config = self._get_default_config()
        except Exception as error:
            logger.error(f"Error loading config: {error}")
            self.config = self._get_default_config()
    
    def _load_test_data(self):
        """Load test data from JSON file."""
        try:
            test_data_file = self.test_data_dir / "test_data.json"
            if test_data_file.exists():
                with open(test_data_file, 'r') as f:
                    self.test_data = json.load(f)
                logger.info("Test data loaded successfully")
            else:
                logger.warning(f"Test data file not found: {test_data_file}")
                self.test_data = {}
        except Exception as error:
            logger.error(f"Error loading test data: {error}")
            self.test_data = {}
    
    def _get_default_config(self) -> Dict[str, Any]:
        """Get default configuration."""
        return {
            "environment": "dev",
            "base_url": "https://www.google.com",
            "timeout": 30000,
            "retry_count": 2,
            "headless": True,
            "browser": "chromium",
            "viewport": {"width": 1280, "height": 720},
            "mcp": {"enabled": True}
        }
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value by key (supports dot notation)."""
        keys = key.split('.')
        value = self.config
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
                if value is None:
                    return default
            else:
                return default
        return value if value is not None else default
    
    def get_test_data(self, key: str, default: Any = None) -> Any:
        """Get test data value by key (supports dot notation)."""
        keys = key.split('.')
        value = self.test_data
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
                if value is None:
                    return default
            else:
                return default
        return value if value is not None else default
    
    def get_base_url(self) -> str:
        """Get base URL for current environment."""
        return self.get("base_url", "https://www.google.com")
    
    def get_browser(self) -> str:
        """Get browser type."""
        return self.get("browser", "chromium")
    
    def is_headless(self) -> bool:
        """Check if headless mode is enabled."""
        return self.get("headless", True)
    
    def get_timeout(self) -> int:
        """Get timeout value."""
        return self.get("timeout", 30000)
    
    def get_viewport(self) -> Dict[str, int]:
        """Get viewport dimensions."""
        return self.get("viewport", {"width": 1280, "height": 720})
    
    def is_mcp_enabled(self) -> bool:
        """Check if MCP is enabled."""
        return self.get("mcp.enabled", True)

