# BDD Cucumber Playwright MCP - Python

A Behavior-Driven Development (BDD) testing framework using Cucumber (Behave), Playwright, and Model Context Protocol (MCP) integration for Python.

## Overview

This project provides a complete BDD testing framework for web automation with:
- **Behave**: BDD framework (Cucumber for Python)
- **Playwright**: Modern browser automation
- **MCP Integration**: Test orchestration, dynamic data fetching, and reporting

## Features

- Google Search automation with validation
- MCP integration for test orchestration
- Dynamic test data fetching from MCP
- Test result reporting to MCP
- Page Object Model (POM) pattern
- Screenshot capture on test failures
- Comprehensive logging

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

## Installation

1. **Clone or navigate to the project directory**

2. **Create a virtual environment (recommended)**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On Linux/Mac
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Install Playwright browsers**
   ```bash
   playwright install
   ```

## Project Structure

```
.
├── features/
│   ├── google_search.feature          # Gherkin feature file
│   ├── step_definitions/
│   │   └── google_search_steps.py     # Step definitions
│   └── support/
│       ├── hooks.py                    # Behave hooks
│       ├── world.py                    # Custom world/context
│       └── mcp_client.py              # MCP client integration
├── pages/
│   └── google_search_page.py          # Page Object Model
├── reports/                            # Test reports and screenshots
├── behave.ini                          # Behave configuration
├── requirements.txt                    # Python dependencies
└── README.md                           # This file
```

## Running Tests

### Standard Execution
```bash
behave
```

### Headed Mode (Visible Browser)
```bash
behave --define headed=true
```

### Debug Mode
```bash
behave --no-capture
```

### Generate Reports
```bash
behave --junit
```

Reports will be generated in the `reports/` directory.

## Configuration

Edit `behave.ini` to customize:
- Browser type (chromium, firefox, webkit)
- Headed/headless mode
- Base URL
- Log levels
- Report formats

## MCP Integration

The framework includes MCP integration for:
1. **Test Orchestration**: Coordinate test execution and manage test state
2. **Dynamic Data**: Fetch test data (keywords, validation criteria) from MCP server
3. **Reporting**: Send test results, screenshots, and logs to MCP

### MCP Client Usage

The MCP client is automatically initialized in hooks. To use it in step definitions:

```python
# Fetch dynamic data
mcp_data = await context.world.mcp_client.fetch_dynamic_data("search_keyword")

# Report test results
await context.world.mcp_client.report_test_result(
    "test_name",
    "passed",
    {"details": "..."}
)
```

## Test Scenarios

### Google Search for "AI"

The main test scenario:
- Navigates to Google
- Searches for "AI"
- Validates search results are displayed
- Validates page title contains "AI"

## Troubleshooting

### Playwright Browser Issues
If browsers are not installed:
```bash
playwright install chromium
```

### MCP Connection Issues
If MCP connection fails, tests will continue without MCP integration. Check logs for connection errors.

### Cookie Consent
The framework automatically handles Google's cookie consent dialog if present.

## Contributing

1. Follow the Page Object Model pattern for page interactions
2. Use descriptive Gherkin scenarios
3. Implement proper error handling and logging
4. Add screenshots on test failures

## License

MIT

