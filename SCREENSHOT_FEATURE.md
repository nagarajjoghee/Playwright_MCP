# Screenshot Feature Documentation

## Overview
The framework now automatically captures screenshots for each page navigation and test step, attaching them to the feature file steps and including them in the HTML reports.

## Features

### 1. Automatic Screenshot Capture
- **Navigation Screenshots**: Captured automatically when navigating to any page
- **Step Screenshots**: Captured after each test step execution
- **Full Page Screenshots**: Captures the entire page, not just the viewport

### 2. Screenshot Storage
- **Location**: `reports/screenshots/`
- **Naming Convention**:
  - Navigation: `navigation_<domain>_<timestamp>.png`
  - Steps: `screenshot_<scenario>_<step>_<timestamp>.png`

### 3. Integration with Reports
- Screenshots are automatically included in HTML test reports
- Each step shows its associated screenshot
- Screenshots are linked to their respective test steps

## How It Works

### Navigation Screenshots
When you navigate to a page using the `navigate()` method in any page object:
```python
await page.navigate("https://www.google.com")
# Automatically captures: navigation_www_google_com_20260104_234958.png
```

### Step Screenshots
After each step in your feature file, a screenshot is automatically captured:
```gherkin
Given I navigate to Google
# Screenshot: screenshot_Search_for_AI_keyword_I_navigate_to_Google_20260104_234958.png

When I search for "AI"
# Screenshot: screenshot_Search_for_AI_keyword_I_search_for_AI_20260104_234959.png
```

## Screenshot Information Stored

Each screenshot includes:
- **Step Name**: The Gherkin step text
- **Step Type**: Given, When, Then, And, But
- **Scenario Name**: The scenario it belongs to
- **Timestamp**: When the screenshot was taken
- **Status**: Passed, Failed, or Skipped
- **Path**: File system path to the screenshot

## Viewing Screenshots

### In HTML Reports
1. Run your tests: `python -m behave`
2. Open the HTML report: `reports/test_report.html`
3. Screenshots are displayed under each test step

### Direct Access
- Navigate to: `reports/screenshots/`
- Screenshots are organized by timestamp
- Each screenshot filename includes the step/scenario name

## Configuration

### Disable Navigation Screenshots
In your page object:
```python
await page.navigate(url, take_screenshot=False)
```

### Screenshot Directory
Default: `reports/screenshots/`
Can be configured in `utils/screenshot_manager.py`

## Example Output

```
reports/screenshots/
├── navigation_www_google_com_20260104_234958.png
├── screenshot_Search_for_AI_keyword_I_navigate_to_Google_20260104_234958.png
├── screenshot_Search_for_AI_keyword_I_search_for_AI_20260104_234959.png
├── screenshot_Search_for_AI_keyword_I_should_see_search_results_20260104_235000.png
└── screenshot_Search_for_AI_keyword_the_page_title_should_contain_AI_20260104_235001.png
```

## Benefits

1. **Visual Verification**: See exactly what the browser displayed at each step
2. **Debugging**: Easily identify where tests fail by viewing screenshots
3. **Documentation**: Screenshots serve as visual documentation of test execution
4. **Reporting**: Enhanced HTML reports with embedded screenshots
5. **Traceability**: Each step has a corresponding screenshot with timestamp

## Technical Details

### Hooks Used
- `@after_step`: Captures screenshot after each step
- `@before_scenario`: Initializes screenshot tracking
- `@after_scenario`: Consolidates screenshots for reporting

### Page Object Integration
- `BasePage.navigate()`: Automatically captures navigation screenshots
- All page objects inherit this functionality

### Report Integration
- `ReportGenerator`: Includes screenshots in HTML reports
- Screenshots are embedded as images in the report
- Each test result shows associated screenshots

## Best Practices

1. **Review Screenshots**: Check screenshots after test runs to verify expected behavior
2. **Clean Up**: Periodically clean old screenshots to save disk space
3. **Version Control**: Consider adding screenshots to `.gitignore` if they're large
4. **CI/CD**: Screenshots are useful for debugging failures in CI/CD pipelines

