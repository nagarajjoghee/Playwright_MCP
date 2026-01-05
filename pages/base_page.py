"""
Base Page Object Model class.
"""
import logging
from typing import Optional
from playwright.async_api import Page, Locator, TimeoutError as PlaywrightTimeoutError
from config.config_manager import ConfigManager

logger = logging.getLogger(__name__)


class BasePage:
    """Base class for all page objects."""
    
    def __init__(self, page: Page, config: Optional[ConfigManager] = None):
        self.page = page
        self.config = config or ConfigManager()
        self.timeout = self.config.get_timeout()
        self.base_url = self.config.get_base_url()
    
    async def navigate(self, url: str = None, wait_until: str = "networkidle", take_screenshot: bool = True):
        """Navigate to a URL and optionally take a screenshot."""
        target_url = url or self.base_url
        try:
            await self.page.goto(target_url, wait_until=wait_until, timeout=self.timeout)
            logger.info(f"Navigated to {target_url}")
            
            # Take screenshot after navigation if enabled
            if take_screenshot:
                try:
                    from datetime import datetime
                    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                    # Extract domain name for filename
                    domain = target_url.replace('https://', '').replace('http://', '').split('/')[0].replace('.', '_')
                    screenshot_path = f"reports/screenshots/navigation_{domain}_{timestamp}.png"
                    await self.page.screenshot(path=screenshot_path, full_page=True)
                    logger.info(f"Navigation screenshot saved: {screenshot_path}")
                except Exception as screenshot_error:
                    logger.warning(f"Could not capture navigation screenshot: {screenshot_error}")
        except Exception as error:
            logger.error(f"Error navigating to {target_url}: {error}")
            raise
    
    async def wait_for_element(self, selector: str, timeout: int = None) -> Locator:
        """Wait for element to be visible."""
        timeout = timeout or self.timeout
        try:
            element = self.page.locator(selector).first
            await element.wait_for(state='visible', timeout=timeout)
            return element
        except PlaywrightTimeoutError:
            logger.error(f"Element not found: {selector}")
            raise
    
    async def click(self, selector: str, timeout: int = None):
        """Click an element."""
        element = await self.wait_for_element(selector, timeout)
        await element.click()
        logger.debug(f"Clicked element: {selector}")
    
    async def fill(self, selector: str, text: str, timeout: int = None):
        """Fill an input field."""
        element = await self.wait_for_element(selector, timeout)
        await element.clear()
        await element.fill(text)
        logger.debug(f"Filled element {selector} with: {text}")
    
    async def get_text(self, selector: str, timeout: int = None) -> str:
        """Get text content of an element."""
        element = await self.wait_for_element(selector, timeout)
        text = await element.text_content()
        return text.strip() if text else ""
    
    async def is_visible(self, selector: str, timeout: int = None) -> bool:
        """Check if element is visible."""
        try:
            element = self.page.locator(selector).first
            await element.wait_for(state='visible', timeout=timeout or 5000)
            return True
        except:
            return False
    
    async def get_title(self) -> str:
        """Get page title."""
        return await self.page.title()
    
    async def get_url(self) -> str:
        """Get current page URL."""
        return self.page.url
    
    async def take_screenshot(self, filename: str = None, full_page: bool = False):
        """Take a screenshot."""
        if not filename:
            from datetime import datetime
            filename = f"screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        
        await self.page.screenshot(path=filename, full_page=full_page)
        logger.info(f"Screenshot saved: {filename}")
        return filename
    
    async def wait_for_load_state(self, state: str = "networkidle", timeout: int = None):
        """Wait for page load state."""
        timeout = timeout or self.timeout
        await self.page.wait_for_load_state(state, timeout=timeout)

