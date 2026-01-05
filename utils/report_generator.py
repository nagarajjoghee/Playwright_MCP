"""
Report Generator with timestamp support.
"""
import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List
import logging

logger = logging.getLogger(__name__)


class ReportGenerator:
    """Generates test reports with timestamps."""
    
    def __init__(self, reports_dir: str = "reports"):
        self.project_root = Path(__file__).parent.parent
        self.reports_dir = self.project_root / reports_dir
        self.reports_dir.mkdir(exist_ok=True)
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.test_results: List[Dict[str, Any]] = []
    
    def get_timestamped_filename(self, base_name: str, extension: str = "html") -> str:
        """Generate filename with timestamp."""
        return f"{base_name}_{self.timestamp}.{extension}"
    
    def generate_html_report(self, test_results: List[Dict[str, Any]], 
                            feature_name: str = "Test Report",
                            screenshots: List[Dict[str, Any]] = None) -> str:
        """Generate HTML report with timestamp."""
        filename = self.get_timestamped_filename("test_report", "html")
        filepath = self.reports_dir / filename
        
        html_content = self._create_html_content(test_results, feature_name)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        logger.info(f"HTML report generated: {filepath}")
        return str(filepath)
    
    def generate_json_report(self, test_results: List[Dict[str, Any]]) -> str:
        """Generate JSON report with timestamp."""
        filename = self.get_timestamped_filename("test_report", "json")
        filepath = self.reports_dir / filename
        
        report_data = {
            "timestamp": self.timestamp,
            "generated_at": datetime.now().isoformat(),
            "test_results": test_results,
            "summary": self._calculate_summary(test_results)
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, indent=2)
        
        logger.info(f"JSON report generated: {filepath}")
        return str(filepath)
    
    def _calculate_summary(self, test_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate test summary."""
        total = len(test_results)
        passed = sum(1 for r in test_results if r.get("status") == "passed")
        failed = sum(1 for r in test_results if r.get("status") == "failed")
        skipped = sum(1 for r in test_results if r.get("status") == "skipped")
        
        return {
            "total": total,
            "passed": passed,
            "failed": failed,
            "skipped": skipped,
            "pass_rate": round((passed / total * 100) if total > 0 else 0, 2)
        }
    
    def _create_html_content(self, test_results: List[Dict[str, Any]], 
                            feature_name: str) -> str:
        """Create HTML content for report."""
        summary = self._calculate_summary(test_results)
        
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Test Report - {self.timestamp}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            min-height: 100vh;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 10px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
            overflow: hidden;
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }}
        .header h1 {{ font-size: 2.5em; margin-bottom: 10px; }}
        .header p {{ font-size: 1.1em; opacity: 0.9; }}
        .timestamp {{
            background: rgba(255,255,255,0.2);
            padding: 10px 20px;
            border-radius: 5px;
            display: inline-block;
            margin-top: 10px;
        }}
        .summary {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            padding: 30px;
            background: #f8f9fa;
        }}
        .stat-card {{
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            text-align: center;
        }}
        .stat-card h3 {{
            color: #667eea;
            margin-bottom: 10px;
            font-size: 0.9em;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}
        .stat-card .number {{
            font-size: 2.5em;
            font-weight: bold;
            color: #333;
        }}
        .stat-card.passed .number {{ color: #28a745; }}
        .stat-card.failed .number {{ color: #dc3545; }}
        .stat-card.skipped .number {{ color: #ffc107; }}
        .content {{ padding: 30px; }}
        .test-result {{
            border: 1px solid #e0e0e0;
            border-radius: 8px;
            padding: 20px;
            margin-bottom: 20px;
        }}
        .test-result.passed {{ border-left: 4px solid #28a745; }}
        .test-result.failed {{ border-left: 4px solid #dc3545; }}
        .test-result.skipped {{ border-left: 4px solid #ffc107; }}
        .footer {{
            background: #f8f9fa;
            padding: 20px;
            text-align: center;
            color: #666;
            border-top: 1px solid #e0e0e0;
        }}
        .step-screenshots {{
            margin-top: 20px;
            padding: 15px;
            background: #f8f9fa;
            border-radius: 5px;
        }}
        .screenshot-item {{
            margin: 15px 0;
            padding: 10px;
            background: white;
            border-radius: 5px;
            border: 1px solid #e0e0e0;
        }}
        .screenshot-image {{
            max-width: 100%;
            height: auto;
            border: 1px solid #ddd;
            border-radius: 5px;
            margin-top: 10px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🧪 Test Report</h1>
            <p>{feature_name}</p>
            <div class="timestamp">Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</div>
        </div>
        
        <div class="summary">
            <div class="stat-card">
                <h3>Total Tests</h3>
                <div class="number">{summary['total']}</div>
            </div>
            <div class="stat-card passed">
                <h3>Passed</h3>
                <div class="number">{summary['passed']}</div>
            </div>
            <div class="stat-card failed">
                <h3>Failed</h3>
                <div class="number">{summary['failed']}</div>
            </div>
            <div class="stat-card skipped">
                <h3>Skipped</h3>
                <div class="number">{summary['skipped']}</div>
            </div>
            <div class="stat-card">
                <h3>Pass Rate</h3>
                <div class="number">{summary['pass_rate']}%</div>
            </div>
        </div>

        <div class="content">
            <h2>Test Results</h2>
            {self._generate_test_results_html(test_results, screenshots)}
        </div>

        <div class="footer">
            <p>Report generated on: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
            <p>Timestamp: {self.timestamp}</p>
        </div>
    </div>
</body>
</html>"""
        return html
    
    def _generate_test_results_html(self, test_results: List[Dict[str, Any]], 
                                    screenshots: List[Dict[str, Any]] = None) -> str:
        """Generate HTML for test results with screenshots."""
        html = ""
        for result in test_results:
            status = result.get("status", "unknown")
            name = result.get("name", "Unknown Test")
            duration = result.get("duration", 0)
            details = result.get("details", {})
            
            # Find related screenshots
            step_screenshots = []
            if screenshots:
                step_screenshots = [s for s in screenshots if name.lower() in s.get('step', '').lower() or 
                                  s.get('scenario', '').lower() in name.lower()]
            
            html += f"""
            <div class="test-result {status}">
                <h3>{name}</h3>
                <p><strong>Status:</strong> {status.upper()}</p>
                <p><strong>Duration:</strong> {duration}s</p>
                <pre>{json.dumps(details, indent=2)}</pre>
            """
            
            # Add screenshots if available
            if step_screenshots:
                html += "<div class='step-screenshots'><h4>Screenshots:</h4>"
                for screenshot in step_screenshots:
                    relative_path = screenshot.get('relative_path', screenshot.get('path', ''))
                    step_name = screenshot.get('step', 'Step')
                    html += f"""
                    <div class='screenshot-item'>
                        <p><strong>{step_name}</strong></p>
                        <img src='{relative_path}' alt='{step_name}' class='screenshot-image' />
                    </div>
                    """
                html += "</div>"
            
            html += "</div>"
        return html

