"""
Step definitions for Google Search feature.
"""
import logging
import asyncio
from behave import given, when, then, step
from pages.google_search_page import GoogleSearchPage

logger = logging.getLogger(__name__)


def run_async(coro):
    """Helper to run async functions in sync context."""
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    return loop.run_until_complete(coro)


@given('I navigate to Google')
def step_navigate_to_google(context):
    """Navigate to Google homepage."""
    try:
        # Ensure world is initialized
        if not hasattr(context, 'world') or context.world is None:
            from features.support.world import CustomWorld
            import asyncio
            context.world = CustomWorld(context)
            try:
                loop = asyncio.get_event_loop()
            except RuntimeError:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
            loop.run_until_complete(context.world.init_browser())
            loop.run_until_complete(context.world.init_mcp())
        
        google_page = GoogleSearchPage(context.world.page)
        run_async(google_page.navigate(context.world.base_url))
        context.google_page = google_page
        logger.info("Successfully navigated to Google")
    except Exception as error:
        logger.error(f"Error navigating to Google: {error}")
        raise


@when('I search for "{keyword}"')
def step_search_for_keyword(context, keyword):
    """Perform a search with the given keyword."""
    try:
        # Optionally fetch keyword from MCP for dynamic data
        if context.world.mcp_client and context.world.mcp_client.is_connected():
            mcp_data = run_async(
                context.world.mcp_client.fetch_dynamic_data("search_keyword")
            )
            if mcp_data.get("keyword"):
                keyword = mcp_data["keyword"]
                logger.info(f"Using keyword from MCP: {keyword}")
        
        # Perform search
        if not hasattr(context, 'google_page'):
            context.google_page = GoogleSearchPage(context.world.page)
        
        run_async(context.google_page.search(keyword))
        context.search_keyword = keyword
        logger.info(f"Search completed for keyword: {keyword}")
    except Exception as error:
        logger.error(f"Error performing search: {error}")
        raise


@then('I should see search results displayed')
def step_verify_search_results_displayed(context):
    """Verify that search results are displayed."""
    try:
        if not hasattr(context, 'google_page'):
            context.google_page = GoogleSearchPage(context.world.page)
        
        results_displayed = run_async(
            context.google_page.are_search_results_displayed()
        )
        
        # Report to MCP
        if context.world.mcp_client:
            run_async(
                context.world.mcp_client.report_test_result(
                    "verify_search_results",
                    "passed" if results_displayed else "failed",
                    {
                        "results_displayed": results_displayed,
                        "keyword": getattr(context, 'search_keyword', 'unknown')
                    }
                )
            )
        
        assert results_displayed, "Search results are not displayed"
        logger.info("Search results verification passed")
    except AssertionError as error:
        logger.error(f"Assertion failed: {error}")
        raise
    except Exception as error:
        logger.error(f"Error verifying search results: {error}")
        raise


@step('the page title should contain "{expected_text}"')
def step_verify_page_title_contains(context, expected_text):
    """Verify that the page title contains the expected text."""
    try:
        if not hasattr(context, 'google_page'):
            context.google_page = GoogleSearchPage(context.world.page)
        
        page_title = run_async(context.google_page.get_page_title())
        
        # Optionally fetch validation criteria from MCP
        if context.world.mcp_client and context.world.mcp_client.is_connected():
            validation_data = run_async(
                context.world.mcp_client.fetch_dynamic_data("validation_criteria")
            )
            if validation_data.get("title_contains"):
                expected_text = validation_data["title_contains"]
                logger.info(f"Using validation criteria from MCP: {expected_text}")
        
        title_contains_text = expected_text.lower() in page_title.lower()
        
        # Report to MCP
        if context.world.mcp_client:
            run_async(
                context.world.mcp_client.report_test_result(
                    "verify_page_title",
                    "passed" if title_contains_text else "failed",
                    {
                        "page_title": page_title,
                        "expected_text": expected_text,
                        "contains": title_contains_text
                    }
                )
            )
        
        assert title_contains_text, (
            f"Page title '{page_title}' does not contain '{expected_text}'"
        )
        logger.info(f"Page title verification passed: '{expected_text}' found in '{page_title}'")
    except AssertionError as error:
        logger.error(f"Assertion failed: {error}")
        raise
    except Exception as error:
        logger.error(f"Error verifying page title: {error}")
        raise

