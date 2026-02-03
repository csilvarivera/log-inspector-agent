from collections import Counter
from google.adk.tools import ToolContext

def generate_log_summary(logs: list[dict], tool_context: ToolContext = None) -> dict:
    """Generates a statistical summary of logs by severity.

    Args:
        logs: A list of log entries (dictionaries). Each entry should have a 'severity' key.

    Returns:
        A dictionary containing the status and the summary counts.
    """
    try:
        if not logs:
            return {
                "status": "success",
                "summary": {},
                "total_logs": 0
            }

        severities = [log.get("severity", "UNKNOWN") for log in logs]
        counts = dict(Counter(severities))
        
        return {
            "status": "success",
            "summary": counts,
            "total_logs": len(logs)
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }

try:
    import matplotlib.pyplot as plt
except ImportError:
    plt = None

import tempfile
import os

def generate_log_chart(summary_data: dict, tool_context: ToolContext = None) -> dict:
    """Generates a bar chart from log summary data.

    Args:
        summary_data: A dictionary where keys are categories (e.g., severity) and values are counts.

    Returns:
        A dictionary containing the status and the path to the generated chart image.
    """
    if plt is None:
        return {
            "status": "error",
            "message": "matplotlib is not installed."
        }

    try:
        categories = list(summary_data.keys())
        counts = list(summary_data.values())

        plt.figure(figsize=(10, 6))
        plt.bar(categories, counts, color='skyblue')
        plt.xlabel('Severity')
        plt.ylabel('Count')
        plt.title('Log Severity Distribution')
        plt.xticks(rotation=45)
        plt.tight_layout()

        # Create a temporary file
        fd, path = tempfile.mkstemp(suffix=".png")
        os.close(fd)

        plt.savefig(path)
        plt.close()

        return {
            "status": "success",
            "chart_path": path
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }
