"""
Behave hooks for test setup and teardown.
"""
import logging
import os
from datetime import datetime
from behave import before_all, after_all, before_scenario, after_scenario
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
    
    # Ensure reports directory exists
    os.makedirs('reports', exist_ok=True)
    
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
                html_report = context.world.report_generator.generate_html_report(
                    test_results, "Google Search Automation"
                )
                json_report = context.world.report_generator.generate_json_report(test_results)
                logger.info(f"Reports generated: {html_report}, {json_report}")
        
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

