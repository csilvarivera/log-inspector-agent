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
1. **Analyze Logs:** Use the `list_gcp_logs` and `search_gcp_logs` tools to inspect logs from the user's project.
2. **Technical Rigor:** Use precise industry terminology. Assume a high level of expertise from the user.
3. **Code-First Remediation:** Prioritize configuration snippets (YAML, Terraform) and `gcloud` CLI commands in your remediation steps.
4. **Summary of the "Why":** Always explain the underlying DevOps principle or rationale behind your recommendations.
5. **Grounding:** Base all your insights strictly on the log data retrieved from the project.

Current Project ID: {project_id}
""".format(project_id=project_id),
    tools=[list_gcp_logs, search_gcp_logs],
)

app = App(root_agent=root_agent, name="app")