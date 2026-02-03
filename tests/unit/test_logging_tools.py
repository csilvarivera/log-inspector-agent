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
    
    mock_client.list_entries.return_value = [mock_entry]
    
    # Call tool
    mock_tool_context = MagicMock()
    result = list_gcp_logs(project_id="test-project", severity="ERROR", limit=1, tool_context=mock_tool_context)
    
    # Assertions
    assert result["status"] == "success"
    assert len(result["logs"]) == 1
    assert result["logs"][0]["payload"] == "Test log message"
    assert result["logs"][0]["severity"] == "ERROR"
    
    mock_client.list_entries.assert_called_once()

@patch("google.cloud.logging.Client")
def test_search_gcp_logs_success(mock_client_class):
    # Setup mock
    mock_client = mock_client_class.return_value
    mock_entry = MagicMock()
    mock_entry.payload = "Exception in thread main"
    mock_entry.severity = "ERROR"
    mock_entry.timestamp = "2026-02-03T11:00:00Z"
    
    mock_client.list_entries.return_value = [mock_entry]
    
    # Call tool
    from app.logging_tools import search_gcp_logs
    mock_tool_context = MagicMock()
    result = search_gcp_logs(project_id="test-project", query="Exception", limit=5, tool_context=mock_tool_context)
    
    # Assertions
    assert result["status"] == "success"
    assert "Exception" in result["logs"][0]["payload"]
    
    # Verify filter
    args, kwargs = mock_client.list_entries.call_args
    assert 'textPayload:"Exception"' in kwargs["filter_"] or 'jsonPayload:"Exception"' in kwargs["filter_"] or '"Exception"' in kwargs["filter_"]
