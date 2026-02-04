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

from google.adk.agents import Agent
from google.adk.apps import App
from google.adk.models import Gemini
from google.adk.tools import load_artifacts

from google.genai import types


import os
import google.auth

from app.logging_tools import list_gcp_logs, search_gcp_logs
from app.reporting_tools import generate_log_summary, generate_log_chart, debug_artifact_save

_, project_id = google.auth.default()

root_agent = Agent(
    name="root_agent",
    model=Gemini(
        model="gemini-3-flash-preview"
    ),
    instruction="""You are a Professional & Expert Log Inspector Agent for Google Cloud. 
Your primary goal is to analyze Google Cloud logs to identify errors, anomalies, and provide actionable remediation steps aligned with Google Cloud best practices.

Key Responsibilities:
                                                             
1. **Log Analysis**: Retrieve logs using `list_gcp_logs` and `search_gcp_logs`.
2. **Mandatory Visualization**: You MUST call `generate_log_summary` and then `generate_log_chart` for every single analysis report. THE USER NEEDS TO SEE THE CHART.Call the `load_artifacts` tool to load the artifact.
3. **Artifact Test**: If the user asks for a 'debug artifact test', call `debug_artifact_save` with any text.
4. **Readable Logs**: Format details in markdown tables + blockquotes for readability.
5. **Insights**: Assume high expertise; provide deep technical root cause analysis and remediation.

Current Project ID: {project_id}
""".format(project_id=project_id),
    tools=[list_gcp_logs, search_gcp_logs, generate_log_summary, generate_log_chart, debug_artifact_save, load_artifacts],
)

app = App(root_agent=root_agent, name="app")
