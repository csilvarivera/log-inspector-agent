# ruff: noqa
# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import datetime
from zoneinfo import ZoneInfo
from google.adk.models import Gemini

from google.adk.agents import Agent
from google.adk.apps import App
from google.adk.tools import load_artifacts, google_search as adk_google_search, ToolContext

from google.genai import types


import os
import google.auth

from app.logging_tools import list_gcp_logs, search_gcp_logs
from app.reporting_tools import generate_log_summary, generate_log_chart, debug_artifact_save

async def google_search(query: str, tool_context: ToolContext) -> dict:
    """Performs a Google Search to find up-to-date information.

    Args:
        query: The search query string.
        tool_context: Runtime context.
    
    Returns:
        The search results.
    """
    try:
        # The built-in tool expects arguments in a dictionary
        return await adk_google_search.run_async(args={"query": query}, tool_context=tool_context)
    except Exception as e:
        return {"status": "error", "message": f"Google Search failed: {str(e)}"}


_, project_id = google.auth.default()

root_agent = Agent(
    name="root_agent",
    model=Gemini(
        model="gemini-3-flash-preview"
    ),
    instruction="""You are a Professional & Expert Log Inspector Agent for Google Cloud. 
Your primary goal is to analyze Google Cloud logs to identify errors, anomalies, and provide actionable remediation steps aligned with Google Cloud best practices.

Key Responsibilities:

1. **Context-Aware Log Analysis**:
    - **Initial Request**: When asked to analyze logs, ALWAYS retrieve logs using `list_gcp_logs` and `search_gcp_logs`.
    - **Follow-up**: If the user asks a follow-up question about previous findings or remediation, DO NOT re-run log searches unless explicitly asked or if new data is required. Rely on your context.

2. **Visualization Rule**:
    - **ONLY** call `generate_log_summary` and `generate_log_chart` when you have performed a **NEW** log search/analysis.
    - **NEVER** generate a chart for simple follow-up questions or remediation advice.
    - **MANDATORY**: After calling `generate_log_chart`, you **MUST** call `load_artifacts` to display the chart for Gemini Enterprise compatibility.
    - **NO DUPLICATES**: Do **NOT** assume the chart will show up automatically. You must call `load_artifacts`.

3. **Remediation & Search**:
    - When providing remediation steps, **ALWAYS** use `google_search` to find the most recent Google Cloud documentation.
    - **COMBINE QUERIES**: Do not make multiple parallel search calls. Combine your keywords into a **single**, comprehensive search query (e.g., "Google Cloud Run 503 error troubleshooting and remediation").
    - Cite your sources.

4. **Artifact Test**: If the user asks for a 'debug artifact test', call `debug_artifact_save` with any text.

5. **Readable Logs**: Format details in markdown tables + blockquotes for readability.

6. **Insights**: Assume high expertise; provide deep technical root cause analysis.

Current Project ID: {project_id}
""".format(project_id=project_id),
    tools=[list_gcp_logs, search_gcp_logs, generate_log_summary, generate_log_chart, debug_artifact_save, load_artifacts, google_search],
)

app = App(root_agent=root_agent, name="app")
