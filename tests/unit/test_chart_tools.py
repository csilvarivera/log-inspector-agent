import pytest
from unittest.mock import MagicMock, patch
from app.reporting_tools import generate_log_chart

@pytest.mark.asyncio
@patch("app.reporting_tools.plt")
@patch("builtins.open", new_callable=MagicMock)
@patch("os.remove")
async def test_generate_log_chart_success(mock_remove, mock_open, mock_plt):
    summary_data = {"ERROR": 10, "WARNING": 5, "INFO": 20}
    
    # Mock savefig
    mock_plt.savefig = MagicMock()
    
    from unittest.mock import AsyncMock
    # Mock ToolContext
    mock_tool_context = MagicMock()
    mock_tool_context.save_artifact = AsyncMock(return_value="v1")
    
    # Mock open and read
    mock_file = MagicMock()
    mock_file.read.return_value = b"fake_image_bytes"
    mock_open.return_value.__enter__.return_value = mock_file

    result = await generate_log_chart(summary_data, tool_context=mock_tool_context)
    
    assert result["status"] == "success", f"Error message: {result.get('message')}"
    assert result["artifact_name"] == "log_severity_chart.png"
    
    # Verify plotting calls
    mock_plt.bar.assert_called_once()
    mock_plt.savefig.assert_called_once()
    mock_plt.close.assert_called_once()
    
    # Verify artifact save
    mock_tool_context.save_artifact.assert_called_once()
    assert mock_remove.called
