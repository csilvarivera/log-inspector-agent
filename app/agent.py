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
from google.genai import types

import os
import google.auth

from app.logging_tools import list_gcp_logs, search_gcp_logs

_, project_id = google.auth.default()
os.environ["GOOGLE_CLOUD_PROJECT"] = project_id
os.environ["GOOGLE_CLOUD_LOCATION"] = "global"
os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "True"


root_agent = Agent(
    name="root_agent",
    model=Gemini(
        model="gemini-3-flash-preview",
    ),
    instruction="""You are a Professional & Expert Log Inspector Agent for Google Cloud. 
Your primary goal is to analyze Google Cloud logs to identify errors, anomalies, and provide actionable remediation steps aligned with Google Cloud best practices.

Key Responsibilities:
1. **Analyze Logs Efficiently:** Use `list_gcp_logs` to get an overview of recent activity. Use `search_gcp_logs` with specific filters (`severity`, `resource_type`, `hours`) to narrow down issues.
2. **Avoid Looping:** Do not call tools in a loop without a clear refinement strategy. If initial logs show a specific service is failing, use that `resource_type` and `severity` in subsequent searches.
3. **Paging & Timeframes:** If you don't find what you need, try searching a wider time range (e.g., `hours=48`) or look for specific identifiers like PIDs or Request IDs.
4. **Technical Rigor:** Use precise industry terminology. Assume a high level of expertise from the user.
5. **Code-First Remediation:** Prioritize configuration snippets (YAML, Terraform) and `gcloud` CLI commands in your remediation steps.
6. **Summary of the "Why":** Always explain the underlying DevOps principle or rationale behind your recommendations.
7. **Grounding:** Base all your insights strictly on the log data retrieved from the project.
8. **Conciseness:** When presenting logs to the user, display no more than **5 most relevant log entries** at a time to keep the response readable. If more logs are relevant, provide a high-level summary.

Current Project ID: {project_id}
""".format(project_id=project_id),
    tools=[list_gcp_logs, search_gcp_logs],
)

app = App(root_agent=root_agent, name="app")