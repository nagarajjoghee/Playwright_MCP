"""
Test Data Loader for managing test data.
"""
import json
import logging
from pathlib import Path
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)


class TestDataLoader:
    """Loads and manages test data from JSON files."""
    
    def __init__(self, test_data_dir: str = "test_data"):
        self.project_root = Path(__file__).parent.parent
        self.test_data_dir = self.project_root / test_data_dir
        self.test_data: Dict[str, Any] = {}
        self._load_test_data()
    
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
    
    def get(self, key: str, default: Any = None) -> Any:
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
    
    def get_search_keyword(self, keyword_name: str = "ai") -> str:
        """Get search keyword from test data."""
        return self.get(f"search_keywords.{keyword_name}", keyword_name)
    
    def get_validation_criteria(self) -> Dict[str, Any]:
        """Get validation criteria from test data."""
        return self.get("validation_criteria", {})
    
    def get_url(self, url_name: str = "google") -> str:
        """Get URL from test data."""
        return self.get(f"urls.{url_name}", "")
    
    def get_timeout(self, timeout_type: str = "page_load") -> int:
        """Get timeout value from test data."""
        return self.get(f"timeouts.{timeout_type}", 30000)

