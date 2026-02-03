import pytest
from app.reporting_tools import generate_log_summary

def test_generate_log_summary_success():
    logs = [
        {"severity": "ERROR", "timestamp": "2026-02-03T10:00:00Z"},
        {"severity": "ERROR", "timestamp": "2026-02-03T10:01:00Z"},
        {"severity": "WARNING", "timestamp": "2026-02-03T10:02:00Z"},
        {"severity": "INFO", "timestamp": "2026-02-03T10:03:00Z"},
    ]
    
    result = generate_log_summary(logs)
    
    assert result["status"] == "success"
    assert result["summary"]["ERROR"] == 2
    assert result["summary"]["WARNING"] == 1
    assert result["summary"]["INFO"] == 1
    assert result["total_logs"] == 4
