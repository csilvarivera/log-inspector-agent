from google.cloud import logging
from google.adk.tools import ToolContext
from google.protobuf.json_format import MessageToDict
from google.protobuf.message import Message
import datetime

def sanitize_payload(payload):
    """Sanitizes the log payload for serialization.
    
    If the payload is a Protobuf message, it converts it to a dictionary.
    """
    if isinstance(payload, Message):
        return MessageToDict(payload)
    return payload

def build_filter_str(query: str = None, severity: str = None, log_name: str = None, resource_type: str = None, hours: int = None) -> str:
    """Helper to build a GCP logging filter string."""
    filters = []
    if query:
        filters.append(f'"{query}"')
    if severity:
        filters.append(f"severity={severity}")
    if log_name:
        filters.append(f'logName="{log_name}"')
    if resource_type:
        filters.append(f'resource.type="{resource_type}"')
    if hours:
        timestamp = (datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(hours=hours)).isoformat()
        filters.append(f'timestamp>="{timestamp}"')
    
    return " AND ".join(filters)

def list_gcp_logs(project_id: str, severity: str = None, resource_type: str = None, hours: int = 24, limit: int = 20, tool_context: ToolContext = None) -> dict:
    """Lists recent logs from a Google Cloud project with filtering options.

    Args:
        project_id: The GCP Project ID to fetch logs from.
        severity: Filter logs by severity (e.g., 'ERROR', 'WARNING', 'INFO').
        resource_type: Filter by GCP resource type (e.g., 'cloud_run_revision', 'k8s_container', 'gae_app').
        hours: How many hours back to look for logs. Defaults to 24.
        limit: The maximum number of log entries to return. Defaults to 20.

    Returns:
        A dictionary containing the status and the retrieved logs.
    """
    try:
        client = logging.Client(project=project_id)
        
        filter_str = build_filter_str(severity=severity, resource_type=resource_type, hours=hours)
            
        entries = client.list_entries(filter_=filter_str, max_results=limit)
        
        logs = []
        for entry in entries:
            logs.append({
                "payload": sanitize_payload(entry.payload),
                "severity": entry.severity,
                "timestamp": str(entry.timestamp),
                "log_name": entry.log_name,
                "resource_type": entry.resource.type if entry.resource else None
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

def search_gcp_logs(project_id: str, query: str, severity: str = None, resource_type: str = None, log_name: str = None, hours: int = 24, limit: int = 20, tool_context: ToolContext = None) -> dict:
    """Searches logs in a Google Cloud project with specific filters.

    Args:
        project_id: The GCP Project ID to search logs in.
        query: The search term or expression (e.g., 'Exception', 'error', 'request_id').
        severity: Filter by severity (e.g., 'ERROR', 'WARNING').
        resource_type: Filter by GCP resource type (service).
        log_name: Filter by a specific log name.
        hours: How many hours back to search. Defaults to 24.
        limit: The maximum number of log entries to return. Defaults to 20.

    Returns:
        A dictionary containing the status and the matching logs.
    """
    try:
        client = logging.Client(project=project_id)
        
        filter_str = build_filter_str(query=query, severity=severity, resource_type=resource_type, log_name=log_name, hours=hours)
            
        entries = client.list_entries(filter_=filter_str, max_results=limit)
        
        logs = []
        for entry in entries:
            logs.append({
                "payload": sanitize_payload(entry.payload),
                "severity": entry.severity,
                "timestamp": str(entry.timestamp),
                "log_name": entry.log_name,
                "resource_type": entry.resource.type if entry.resource else None
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