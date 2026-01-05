# Framework Enhancements Documentation

## Overview
The framework has been enhanced with improved structure, test data management, configuration management, and timestamped reporting.

## New Structure

```
.
├── config/
│   ├── __init__.py
│   └── config_manager.py          # Configuration management
├── test_data/
│   ├── test_data.json              # Test data (keywords, URLs, etc.)
│   └── environments/
│       ├── dev.json                # Development environment config
│       ├── staging.json            # Staging environment config
│       └── prod.json               # Production environment config
├── pages/
│   ├── base_page.py                # Base Page Object Model class
│   └── google_search_page.py      # Enhanced Google Search page
├── utils/
│   ├── __init__.py
│   ├── report_generator.py         # Timestamped report generation
│   └── test_data_loader.py         # Test data loader
└── features/
    └── support/
        ├── world.py                # Enhanced with config and test data
        └── hooks.py                # Enhanced with environment support
```

## Features

### 1. Test Data Management
- **Location**: `test_data/test_data.json`
- **Purpose**: Centralized test data storage
- **Usage**: Access via `context.world.test_data.get("key")`

**Example:**
```python
# Get search keyword
keyword = context.world.test_data.get_search_keyword("ai")

# Get validation criteria
criteria = context.world.test_data.get_validation_criteria()

# Get URL
url = context.world.test_data.get_url("google")
```

### 2. Configuration Management
- **Location**: `config/config_manager.py`
- **Purpose**: Environment-specific configuration
- **Environments**: dev, staging, prod
- **Usage**: Access via `context.world.config.get("key")`

**Set Environment:**
```bash
# Via behave.ini
[behave.userdata]
environment = dev

# Via environment variable
export TEST_ENV=staging
python -m behave

# Via command line
python -m behave --define environment=prod
```

**Example:**
```python
# Get base URL
base_url = context.world.config.get_base_url()

# Get browser type
browser = context.world.config.get_browser()

# Get timeout
timeout = context.world.config.get_timeout()

# Check if headless
is_headless = context.world.config.is_headless()
```

### 3. Enhanced Page Object Model
- **Base Class**: `pages/base_page.py`
- **Features**:
  - Common methods (navigate, click, fill, etc.)
  - Configuration integration
  - Timeout management
  - Screenshot support

**Usage:**
```python
from pages.base_page import BasePage

class MyPage(BasePage):
    def __init__(self, page, config=None):
        super().__init__(page, config)
    
    # Inherits: navigate, click, fill, get_text, etc.
```

### 4. Timestamped Reports
- **Location**: `utils/report_generator.py`
- **Features**:
  - HTML reports with timestamps
  - JSON reports with timestamps
  - Automatic timestamp in filenames
  - Test summary and statistics

**Report Files:**
- `test_report_YYYYMMDD_HHMMSS.html`
- `test_report_YYYYMMDD_HHMMSS.json`

**Usage:**
```python
# Automatic in hooks
# Reports are generated after all tests complete
```

### 5. Environment-Specific Settings
- **Location**: `test_data/environments/`
- **Files**: `dev.json`, `staging.json`, `prod.json`
- **Settings**:
  - Base URLs
  - API URLs
  - Timeouts
  - Browser settings
  - Viewport sizes
  - MCP configuration

## Usage Examples

### Running Tests with Different Environments

```bash
# Development (default)
python -m behave

# Staging
python -m behave --define environment=staging

# Production
python -m behave --define environment=prod
```

### Accessing Test Data in Steps

```python
@given('I search for "{keyword_name}"')
def step_search(context, keyword_name):
    # Get keyword from test data
    keyword = context.world.test_data.get_search_keyword(keyword_name)
    context.google_page.search(keyword)
```

### Accessing Configuration

```python
# In step definitions
base_url = context.world.config.get_base_url()
timeout = context.world.config.get_timeout()

# In page objects
class MyPage(BasePage):
    def __init__(self, page, config=None):
        super().__init__(page, config)
        self.timeout = self.config.get_timeout()
```

## Benefits

1. **Separation of Concerns**: Test data, configuration, and code are separated
2. **Environment Management**: Easy switching between environments
3. **Maintainability**: Centralized configuration and test data
4. **Traceability**: Timestamped reports for each test run
5. **Reusability**: Base page class for common operations
6. **Scalability**: Easy to add new pages, environments, and test data

## Migration Guide

### Old Code
```python
# Hard-coded values
url = "https://www.google.com"
keyword = "AI"
timeout = 30000
```

### New Code
```python
# From configuration
url = context.world.config.get_base_url()
keyword = context.world.test_data.get_search_keyword("ai")
timeout = context.world.config.get_timeout()
```

## Next Steps

1. Add more test data as needed
2. Create additional environment configurations
3. Extend base page class with more common methods
4. Add more utility functions
5. Enhance reporting with more details

