from google.cloud import logging
from google.adk.tools import ToolContext

def list_gcp_logs(project_id: str, severity: str = None, limit: int = 10, tool_context: ToolContext = None) -> dict:
    """Lists recent logs from a Google Cloud project.

    Args:
        project_id: The GCP Project ID to fetch logs from.
        severity: Filter logs by severity (e.g., 'ERROR', 'WARNING', 'INFO').
        limit: The maximum number of log entries to return.

    Returns:
        A dictionary containing the status and the retrieved logs.
    """
    try:
        client = logging.Client(project=project_id)
        
        filter_str = ""
        if severity:
            filter_str = f"severity={severity}"
            
        entries = client.list_entries(filter_=filter_str, max_results=limit)
        
        logs = []
        for entry in entries:
            logs.append({
                "payload": entry.payload,
                "severity": entry.severity,
                "timestamp": str(entry.timestamp),
                "log_name": entry.log_name
            })
            
        return {
            "status": "success",
            "logs": logs
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }

def search_gcp_logs(project_id: str, query: str, limit: int = 10, tool_context: ToolContext = None) -> dict:
    """Searches logs in a Google Cloud project for a specific query.

    Args:
        project_id: The GCP Project ID to search logs in.
        query: The search term or expression (e.g., 'Exception', 'error').
        limit: The maximum number of log entries to return.

    Returns:
        A dictionary containing the status and the matching logs.
    """
    try:
        client = logging.Client(project=project_id)
        
        # Search across payloads
        filter_str = f'"{query}"'
            
        entries = client.list_entries(filter_=filter_str, max_results=limit)
        
        logs = []
        for entry in entries:
            logs.append({
                "payload": entry.payload,
                "severity": entry.severity,
                "timestamp": str(entry.timestamp),
                "log_name": entry.log_name
            })
            
        return {
            "status": "success",
            "logs": logs
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }