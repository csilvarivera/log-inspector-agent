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
