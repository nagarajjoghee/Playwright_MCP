"""
Custom World class for Behave context management.
"""
import logging
from playwright.async_api import async_playwright, Browser, BrowserContext, Page
from features.support.mcp_client import MCPClient
from config.config_manager import ConfigManager
from utils.test_data_loader import TestDataLoader
from utils.report_generator import ReportGenerator

logger = logging.getLogger(__name__)


class CustomWorld:
    """Custom world class extending behave's context."""
    
    def __init__(self, context):
        self.context = context
        
        # Initialize configuration and test data
        env = context.config.userdata.get('environment', 'dev')
        self.config = ConfigManager(environment=env)
        self.test_data = TestDataLoader()
        self.report_generator = ReportGenerator()
        
        self.browser: Browser = None
        self.browser_context: BrowserContext = None
        self.page: Page = None
        self.playwright = None
        self.mcp_client: MCPClient = None
        
        # Configuration from config manager (with fallback to behave.ini)
        self.headed = not self.config.is_headless() or context.config.userdata.getbool('headed', False)
        self.browser_type = self.config.get_browser()
        self.base_url = self.config.get_base_url()
    
    async def init_browser(self):
        """Initialize Playwright browser."""
        try:
            self.playwright = await async_playwright().start()
            
            browser_map = {
                'chromium': self.playwright.chromium,
                'firefox': self.playwright.firefox,
                'webkit': self.playwright.webkit
            }
            
            browser_launcher = browser_map.get(self.browser_type, self.playwright.chromium)
            
            self.browser = await browser_launcher.launch(
                headless=not self.headed,
                args=['--no-sandbox', '--disable-dev-shm-usage'] if not self.headed else []
            )
            
            viewport = self.config.get_viewport()
            self.browser_context = await self.browser.new_context(
                viewport=viewport,
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            )
            
            self.page = await self.browser_context.new_page()
            logger.info(f"Browser initialized: {self.browser_type} (headed={self.headed})")
        except Exception as error:
            logger.error(f"Error initializing browser: {error}")
            raise
    
    async def init_mcp(self):
        """Initialize MCP client."""
        try:
            self.mcp_client = MCPClient()
            await self.mcp_client.connect()
            logger.info("MCP client initialized")
        except Exception as error:
            logger.error(f"Error initializing MCP client: {error}")
            # Continue without MCP if initialization fails
            self.mcp_client = None
    
    async def cleanup(self):
        """Cleanup browser and MCP connections."""
        try:
            if self.page:
                await self.page.close()
            if self.browser_context:
                await self.browser_context.close()
            if self.browser:
                await self.browser.close()
            if self.playwright:
                await self.playwright.stop()
            logger.info("Browser cleanup completed")
        except Exception as error:
            logger.error(f"Error during browser cleanup: {error}")
        
        try:
            if self.mcp_client:
                await self.mcp_client.disconnect()
                logger.info("MCP client cleanup completed")
        except Exception as error:
            logger.error(f"Error during MCP cleanup: {error}")

