"""
Behave hooks for test setup and teardown.
"""
import logging
import os
from datetime import datetime
from behave import before_all, after_all, before_scenario, after_scenario, after_step
from playwright.sync_api import sync_playwright
from config.config_manager import ConfigManager

logger = logging.getLogger(__name__)


@before_all
def before_all_hook(context):
    """Initialize MCP client and install Playwright browsers."""
    logger.info("=" * 80)
    logger.info("Starting test suite...")
    logger.info("=" * 80)
    
    # Load configuration
    env = context.config.userdata.get('environment', 'dev')
    context.config_manager = ConfigManager(environment=env)
    logger.info(f"Environment: {context.config_manager.environment}")
    logger.info(f"Base URL: {context.config_manager.get_base_url()}")
    
    # Ensure reports and screenshots directories exist
    os.makedirs('reports', exist_ok=True)
    os.makedirs('reports/screenshots', exist_ok=True)
    
    # Initialize screenshot list for the test run
    context.screenshots = []
    
    # Install Playwright browsers if not already installed
    try:
        logger.info("Checking Playwright browser installation...")
        with sync_playwright() as p:
            # This will trigger browser installation if needed
            browser = p.chromium.launch(headless=True)
            browser.close()
        logger.info("Playwright browsers are ready")
    except Exception as error:
        logger.warning(f"Playwright browser check failed: {error}")
        logger.info("You may need to run: playwright install")


@after_all
def after_all_hook(context):
    """Disconnect MCP and generate reports."""
    logger.info("=" * 80)
    logger.info("Test suite completed.")
    logger.info("=" * 80)
    
    # Generate timestamped reports
    if hasattr(context, 'world') and context.world:
        # Generate HTML report
        if hasattr(context.world, 'report_generator'):
            test_results = []
            if context.world.mcp_client:
                test_results = context.world.mcp_client.get_test_results()
            
            if test_results:
                # Get screenshots from context
                screenshots = getattr(context, 'screenshots', [])
                html_report = context.world.report_generator.generate_html_report(
                    test_results, "Google Search Automation", screenshots
                )
                json_report = context.world.report_generator.generate_json_report(test_results)
                logger.info(f"Reports generated: {html_report}, {json_report}")
                if screenshots:
                    logger.info(f"Report includes {len(screenshots)} screenshots")
        
        # Generate summary report if MCP client was used
        if context.world.mcp_client:
            results = context.world.mcp_client.get_test_results()
            if results:
                logger.info(f"Total test results collected: {len(results)}")


@before_scenario
def before_scenario_hook(context, scenario):
    """Initialize browser context before each scenario."""
    logger.info(f"\n{'=' * 80}")
    logger.info(f"Scenario: {scenario.name}")
    logger.info(f"{'=' * 80}")
    
    # Initialize screenshot list for scenario
    if not hasattr(context, 'screenshots'):
        context.screenshots = []
    context.scenario_screenshots = []
    
    # Initialize custom world
    if not hasattr(context, 'world'):
        from features.support.world import CustomWorld
        context.world = CustomWorld(context)
    
    # Initialize browser
    import asyncio
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    
    loop.run_until_complete(context.world.init_browser())
    
    # Initialize MCP client
    loop.run_until_complete(context.world.init_mcp())
    
    # Start test orchestration via MCP
    if context.world.mcp_client:
        loop.run_until_complete(
            context.world.mcp_client.start_test_orchestration(scenario.name)
        )


@after_scenario
def after_scenario_hook(context, scenario):
    """Cleanup browser and capture screenshots on failure."""
    import asyncio
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    
    # Capture screenshot on failure
    if scenario.status == 'failed' and context.world.page:
        screenshot_path = f"reports/screenshot_{scenario.name.replace(' ', '_')}.png"
        try:
            loop.run_until_complete(
                context.world.page.screenshot(path=screenshot_path)
            )
            logger.info(f"Screenshot saved: {screenshot_path}")
            
            # Report failure to MCP
            if context.world.mcp_client:
                loop.run_until_complete(
                    context.world.mcp_client.report_test_result(
                        scenario.name,
                        "failed",
                        {"error": str(scenario.exception) if hasattr(scenario, 'exception') else "Unknown error"},
                        screenshot_path
                    )
                )
        except Exception as error:
            logger.error(f"Error capturing screenshot: {error}")
    elif scenario.status == 'passed' and context.world.mcp_client:
        # Report success to MCP
        loop.run_until_complete(
            context.world.mcp_client.report_test_result(
                scenario.name,
                "passed",
                {"duration": scenario.duration if hasattr(scenario, 'duration') else None}
            )
        )
    
    # Stop test orchestration
    if context.world.mcp_client:
        loop.run_until_complete(
            context.world.mcp_client.stop_test_orchestration(scenario.name)
        )
    
    # Cleanup browser
    loop.run_until_complete(context.world.cleanup())
    
    logger.info(f"Scenario {scenario.status}: {scenario.name}")
    
    # Store scenario screenshots in context
    if hasattr(context, 'scenario_screenshots'):
        context.screenshots.extend(context.scenario_screenshots)


@after_step
def after_step_hook(context, step):
    """Capture screenshot after each step, especially for navigation steps."""
    import asyncio
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    
    # Only capture screenshots if page is available and step passed
    if hasattr(context, 'world') and context.world and context.world.page:
        try:
            # Create screenshot filename based on step
            step_name = step.name.replace(' ', '_').replace('"', '').replace('/', '_')[:50]
            scenario_name = step.scenario.name.replace(' ', '_')[:30] if hasattr(step, 'scenario') else 'unknown'
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            
            screenshot_filename = f"screenshot_{scenario_name}_{step_name}_{timestamp}.png"
            screenshot_path = os.path.join('reports', 'screenshots', screenshot_filename)
            
            # Ensure directory exists
            os.makedirs(os.path.dirname(screenshot_path), exist_ok=True)
            
            # Take screenshot
            loop.run_until_complete(
                context.world.page.screenshot(path=screenshot_path, full_page=True)
            )
            
            # Store screenshot info
            screenshot_info = {
                'step': step.name,
                'step_type': step.keyword,
                'scenario': scenario_name,
                'path': screenshot_path,
                'timestamp': timestamp,
                'status': step.status if hasattr(step, 'status') else 'unknown'
            }
            
            if not hasattr(context, 'scenario_screenshots'):
                context.scenario_screenshots = []
            context.scenario_screenshots.append(screenshot_info)
            
            if not hasattr(context, 'screenshots'):
                context.screenshots = []
            context.screenshots.append(screenshot_info)
            
            logger.info(f"Screenshot captured for step: {step.name[:50]}")
            logger.debug(f"Screenshot saved: {screenshot_path}")
            
        except Exception as error:
            logger.warning(f"Could not capture screenshot for step: {error}")

