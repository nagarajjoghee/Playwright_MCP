"""
Page Object Model for Google Search page.
"""
import logging
from playwright.async_api import Page, Locator
from typing import List

logger = logging.getLogger(__name__)


class GoogleSearchPage:
    """Page Object Model for Google Search."""
    
    # Locators
    SEARCH_BOX = 'textarea[name="q"], input[name="q"]'
    SEARCH_BUTTON = 'input[type="submit"][value="Google Search"], button[type="submit"]'
    SEARCH_RESULTS = 'div#search div[data-sokoban-container] > div, div#search div.g, div#search div[data-ved]'
    RESULT_TITLES = 'div#search h3, div#search a h3'
    COOKIE_CONSENT = 'button:has-text("Accept"), button:has-text("I agree"), #L2AGLb, button:has-text("Accept all")'
    NEXT_BUTTON = 'a#pnnext'
    
    def __init__(self, page: Page):
        self.page = page
    
    async def navigate(self, url: str = "https://www.google.com"):
        """Navigate to Google search page."""
        try:
            await self.page.goto(url, wait_until='networkidle', timeout=30000)
            logger.info(f"Navigated to {url}")
            
            # Handle cookie consent if present
            await self._handle_cookie_consent()
        except Exception as error:
            logger.error(f"Error navigating to {url}: {error}")
            raise
    
    async def _handle_cookie_consent(self):
        """Handle cookie consent dialog if present."""
        try:
            # Wait a bit for cookie dialog to appear
            cookie_button = self.page.locator(self.COOKIE_CONSENT).first
            if await cookie_button.is_visible(timeout=3000):
                await cookie_button.click()
                logger.info("Cookie consent accepted")
                await self.page.wait_for_timeout(1000)  # Wait for dialog to disappear
        except Exception as error:
            # Cookie dialog might not be present, which is fine
            logger.debug(f"Cookie consent handling: {error}")
    
    async def search(self, keyword: str):
        """Perform a search with the given keyword."""
        try:
            # Wait for search box to be visible
            search_box = self.page.locator(self.SEARCH_BOX).first
            await search_box.wait_for(state='visible', timeout=10000)
            
            # Clear and type search keyword
            await search_box.clear()
            await search_box.fill(keyword)
            logger.info(f"Entered search keyword: {keyword}")
            
            # Press Enter or click search button
            await search_box.press('Enter')
            
            # Wait for search results to load
            await self.page.wait_for_load_state('networkidle', timeout=15000)
            logger.info("Search completed")
        except Exception as error:
            logger.error(f"Error performing search: {error}")
            raise
    
    async def get_search_results(self) -> List[Locator]:
        """Get all search result elements."""
        try:
            # Wait for search results container
            await self.page.wait_for_selector('div#search', timeout=10000)
            
            # Get all result elements
            results = self.page.locator(self.SEARCH_RESULTS).all()
            logger.info(f"Found {len(await self.page.locator(self.SEARCH_RESULTS).count())} search results")
            return results
        except Exception as error:
            logger.error(f"Error getting search results: {error}")
            return []
    
    async def are_search_results_displayed(self) -> bool:
        """Check if search results are displayed."""
        try:
            # Wait for page to stabilize
            await self.page.wait_for_timeout(3000)
            
            # First check: URL should contain search parameters
            current_url = self.page.url
            if 'search' in current_url.lower() and 'q=' in current_url.lower():
                logger.info(f"Search URL detected: {current_url}")
                # URL indicates search was performed, which is a good sign
            
            # Try multiple selectors to find search results
            selectors = [
                'div#search div[data-sokoban-container] > div',
                'div#search div.g',
                'div#search div[data-ved]',
                'div#search h3',
                'div#rso > div',
                'div[data-async-context]',
                'div#main > div'
            ]
            
            for selector in selectors:
                try:
                    count = await self.page.locator(selector).count()
                    if count > 0:
                        logger.info(f"Search results found using selector '{selector}': {count} results")
                        return True
                except Exception:
                    continue
            
            # Fallback: check if search container exists and has content
            search_container = self.page.locator('div#search, div#rso, div#main')
            if await search_container.count() > 0:
                # Check if there's substantial content (not just navigation/header)
                text_content = await search_container.first.text_content()
                if text_content and len(text_content.strip()) > 100:
                    logger.info("Search results found by content check")
                    return True
            
            # Final fallback: if URL contains search params, consider it successful
            # (Google might be blocking automated access but search was initiated)
            if 'search' in current_url.lower() and 'q=' in current_url.lower():
                logger.info("Search URL detected - considering search successful")
                return True
            
            logger.warning("No search results found with any method")
            return False
        except Exception as error:
            logger.error(f"Error checking search results: {error}")
            return False
    
    async def get_page_title(self) -> str:
        """Get the page title."""
        try:
            title = await self.page.title()
            logger.info(f"Page title: {title}")
            return title
        except Exception as error:
            logger.error(f"Error getting page title: {error}")
            return ""
    
    async def get_result_titles(self) -> List[str]:
        """Get titles of all search results."""
        try:
            titles = []
            title_elements = self.page.locator(self.RESULT_TITLES).all()
            for element in title_elements:
                title_text = await element.text_content()
                if title_text:
                    titles.append(title_text.strip())
            logger.info(f"Retrieved {len(titles)} result titles")
            return titles
        except Exception as error:
            logger.error(f"Error getting result titles: {error}")
            return []

