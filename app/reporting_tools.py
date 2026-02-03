from collections import Counter
import io
from google.adk.tools import ToolContext
from google.genai import types

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

        severities = [log.get("severity") or "UNKNOWN" for log in logs]
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
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
except ImportError:
    plt = None

import tempfile
import os

async def generate_log_chart(summary_data: dict, tool_context: ToolContext = None) -> dict:
    """Generates a bar chart from log summary data and saves it as an artifact.

    Args:
        summary_data: A dictionary where keys are categories (e.g., severity) and values are counts.
                     Can also be the full result dictionary from generate_log_summary.

    Returns:
        A dictionary containing the status, the name of the generated chart artifact,
        and a suggested markdown snippet for display.
    """
    if plt is None:
        return {
            "status": "error",
            "message": "matplotlib is not installed."
        }

    try:
        import time
        with open("execution_debug.log", "a") as f:
            f.write(f"[{time.ctime()}] generate_log_chart called with {len(summary_data)} categories\n")

        # Robustly handle nested summary data if the agent passes the whole tool result
        if "summary" in summary_data and isinstance(summary_data["summary"], dict):
            summary_data = summary_data["summary"]

        if not summary_data:
            return {
                "status": "error",
                "message": "summary_data is empty or invalid."
            }

        categories = list(summary_data.keys())
        counts = list(summary_data.values())

        plt.figure(figsize=(10, 6))
        bars = plt.bar(categories, counts, color='skyblue')
        plt.xlabel('Severity')
        plt.ylabel('Count')
        plt.title('Log Severity Distribution')
        plt.xticks(rotation=45)
        
        # Add values at the top of the bars
        plt.bar_label(bars, padding=3)
        
        plt.tight_layout()

        # Save to BytesIO buffer instead of temp file
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        image_bytes = buf.read()
        plt.close()

        # Save as ADK artifact
        # Using a timestamp to avoid UI caching if the same session is reused
        import time
        artifact_filename = f"log_chart_{int(time.time())}.png"

        if tool_context:
            artifact = types.Part.from_bytes(data=image_bytes, mime_type="image/png")
            try:
                await tool_context.save_artifact(filename=artifact_filename, artifact=artifact)
            except Exception as e:
                 return {
                    "status": "error",
                    "message": f"Failed to save artifact: {str(e)}"
                }
        else:
            return {
                "status": "error",
                "message": "Internal Error: ToolContext is missing. Artifact cannot be saved."
            }

        return {
            "status": "success",
            "artifact_name": artifact_filename,
            "markdown": f"![Log Severity Distribution]({artifact_filename})"
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Chart generation failed: {str(e)}"
        }

async def debug_artifact_save(text: str, tool_context: ToolContext = None) -> dict:
    """A debug tool to verify that artifacts are being saved correctly.
    It saves a simple text file as an artifact and logs execution to a local file.

    Args:
        text: Any text to save in the artifact.
    """
    import time
    with open("execution_debug.log", "a") as f:
        f.write(f"[{time.ctime()}] debug_artifact_save called with text: {text}\n")

    if not tool_context:
        return {"status": "error", "message": "ToolContext missing"}
    
    filename = "debug_test.txt"
    artifact = types.Part.from_bytes(data=text.encode("utf-8"), mime_type="text/plain")
    try:
        await tool_context.save_artifact(filename=filename, artifact=artifact)
        return {"status": "success", "artifact_name": filename}
    except Exception as e:
        return {"status": "error", "message": f"Failed to save debug artifact: {str(e)}"}
