import pytest
from unittest.mock import MagicMock, patch
from app.reporting_tools import generate_log_chart

@patch("app.reporting_tools.plt")
def test_generate_log_chart_success(mock_plt):
    summary_data = {"ERROR": 10, "WARNING": 5, "INFO": 20}
    
    # Mock savefig
    mock_plt.savefig = MagicMock()
    
    result = generate_log_chart(summary_data)
    
    assert result["status"] == "success"
    assert result["chart_path"].endswith(".png")
    
    # Verify plotting calls
    mock_plt.bar.assert_called_once()
    mock_plt.savefig.assert_called_once()
    mock_plt.close.assert_called_once()
