"""
Screenshot Manager for organizing and managing test screenshots.
"""
import os
import logging
from pathlib import Path
from typing import List, Dict, Any
from datetime import datetime

logger = logging.getLogger(__name__)


class ScreenshotManager:
    """Manages screenshots for test steps."""
    
    def __init__(self, screenshots_dir: str = "reports/screenshots"):
        self.project_root = Path(__file__).parent.parent
        self.screenshots_dir = self.project_root / screenshots_dir
        self.screenshots_dir.mkdir(parents=True, exist_ok=True)
        self.screenshots: List[Dict[str, Any]] = []
    
    def add_screenshot(self, step_name: str, step_type: str, scenario_name: str, 
                      screenshot_path: str, status: str = "passed"):
        """Add screenshot information."""
        screenshot_info = {
            'step': step_name,
            'step_type': step_type,
            'scenario': scenario_name,
            'path': screenshot_path,
            'relative_path': str(Path(screenshot_path).relative_to(self.project_root)),
            'timestamp': datetime.now().isoformat(),
            'status': status
        }
        self.screenshots.append(screenshot_info)
        return screenshot_info
    
    def get_screenshots_for_scenario(self, scenario_name: str) -> List[Dict[str, Any]]:
        """Get all screenshots for a specific scenario."""
        return [s for s in self.screenshots if s.get('scenario') == scenario_name]
    
    def get_screenshots_for_step(self, step_name: str) -> List[Dict[str, Any]]:
        """Get all screenshots for a specific step."""
        return [s for s in self.screenshots if step_name in s.get('step', '')]
    
    def get_all_screenshots(self) -> List[Dict[str, Any]]:
        """Get all screenshots."""
        return self.screenshots
    
    def generate_screenshot_html(self, screenshots: List[Dict[str, Any]] = None) -> str:
        """Generate HTML for displaying screenshots."""
        if screenshots is None:
            screenshots = self.screenshots
        
        if not screenshots:
            return "<p>No screenshots available.</p>"
        
        html = "<div class='screenshots-container'>"
        for screenshot in screenshots:
            relative_path = screenshot.get('relative_path', screenshot.get('path', ''))
            step_name = screenshot.get('step', 'Unknown Step')
            step_type = screenshot.get('step_type', '')
            status = screenshot.get('status', 'unknown')
            
            html += f"""
            <div class='screenshot-item {status}'>
                <h4>{step_type} {step_name}</h4>
                <img src='{relative_path}' alt='{step_name}' class='screenshot-image' />
                <p class='screenshot-info'>Status: {status.upper()} | Time: {screenshot.get('timestamp', '')}</p>
            </div>
            """
        html += "</div>"
        return html

