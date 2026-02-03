import pytest
from unittest.mock import MagicMock, patch
from app.logging_tools import list_gcp_logs

@patch("google.cloud.logging.Client")
def test_list_gcp_logs_success(mock_client_class):
    # Setup mock
    mock_client = mock_client_class.return_value
    mock_entry = MagicMock()
    mock_entry.payload = "Test log message"
    mock_entry.severity = "ERROR"
    mock_entry.timestamp = "2026-02-03T10:00:00Z"
    mock_entry.resource.type = "project"
    
    mock_client.list_entries.return_value = [mock_entry]
    
    # Call tool
    mock_tool_context = MagicMock()
    result = list_gcp_logs(project_id="test-project", severity="ERROR", limit=1, tool_context=mock_tool_context)
    
    # Assertions
    assert result["status"] == "success"
    assert len(result["logs"]) == 1
    assert result["logs"][0]["payload"] == "Test log message"
    assert result["logs"][0]["severity"] == "ERROR"
    assert result["logs"][0]["resource_type"] == "project"
    
    mock_client.list_entries.assert_called_once()

@patch("google.cloud.logging.Client")
def test_search_gcp_logs_success(mock_client_class):
    # Setup mock
    mock_client = mock_client_class.return_value
    mock_entry = MagicMock()
    mock_entry.payload = "Exception in thread main"
    mock_entry.severity = "ERROR"
    mock_entry.timestamp = "2026-02-03T11:00:00Z"
    mock_entry.resource.type = "cloud_run_revision"
    
    mock_client.list_entries.return_value = [mock_entry]
    
    # Call tool
    from app.logging_tools import search_gcp_logs
    mock_tool_context = MagicMock()
    result = search_gcp_logs(project_id="test-project", query="Exception", limit=5, tool_context=mock_tool_context)
    
    # Assertions
    assert result["status"] == "success"
    assert "Exception" in result["logs"][0]["payload"]
    assert result["logs"][0]["resource_type"] == "cloud_run_revision"
    
    # Verify filter
    args, kwargs = mock_client.list_entries.call_args
    assert '"Exception"' in kwargs["filter_"]

@patch("google.cloud.logging.Client")
def test_list_gcp_logs_with_protobuf_payload(mock_client_class):
    # Setup mock
    mock_client = mock_client_class.return_value
    mock_entry = MagicMock()
    
    # Mock a protobuf message
    from google.protobuf.any_pb2 import Any
    mock_payload = Any()
    mock_payload.type_url = "type.googleapis.com/google.protobuf.Empty"
    mock_payload.value = b""
    
    mock_entry.payload = mock_payload
    mock_entry.severity = "INFO"
    mock_entry.timestamp = "2026-02-03T12:00:00Z"
    mock_entry.log_name = "projects/test/logs/test"
    mock_entry.resource.type = "project"
    
    mock_client.list_entries.return_value = [mock_entry]
    
    # Call tool
    mock_tool_context = MagicMock()
    result = list_gcp_logs(project_id="test-project", severity="INFO", limit=1, tool_context=mock_tool_context)
    
    # Assertions
    assert result["status"] == "success"
    assert len(result["logs"]) == 1
    # Check that it's a dict and contains protobuf fields
    assert isinstance(result["logs"][0]["payload"], dict)
    assert "@type" in result["logs"][0]["payload"]
    assert result["logs"][0]["payload"]["@type"] == "type.googleapis.com/google.protobuf.Empty"

@patch("google.cloud.logging.Client")
def test_search_gcp_logs_with_complex_filters(mock_client_class):
    # Setup mock
    mock_client = mock_client_class.return_value
    mock_entry = MagicMock()
    mock_entry.payload = "Complex search result"
    mock_entry.severity = "WARNING"
    mock_entry.resource.type = "k8s_container"
    
    mock_client.list_entries.return_value = [mock_entry]
    
    # Call tool with multiple filters
    from app.logging_tools import search_gcp_logs
    result = search_gcp_logs(
        project_id="test-project",
        query="Specific Error",
        severity="WARNING",
        resource_type="k8s_container",
        hours=5
    )
    
    # Assertions
    assert result["status"] == "success"
    
    # Verify complex filter string
    args, kwargs = mock_client.list_entries.call_args
    filter_str = kwargs["filter_"]
    assert '"Specific Error"' in filter_str
    assert "severity=WARNING" in filter_str
    assert 'resource.type="k8s_container"' in filter_str
    assert "timestamp>=" in filter_str
