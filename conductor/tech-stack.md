# Tech Stack

## Core Technologies
- **Language:** [Python](https://www.python.org/) (>=3.10, <3.14)
- **Agent Framework:** [Google ADK](https://github.com/google/adk-python) (Agent Development Kit)
- **Cloud Platform:** [Google Cloud Platform (GCP)](https://cloud.google.com/)

## Data & Intelligence
- **Log Source:** [Google Cloud Logging](https://cloud.google.com/logging)
- **Log Retrieval:** 
    - **Method:** Google Cloud Logging API
    - **Library:** `google-cloud-logging` Python client
    - **Integration:** Can be exposed as a tool to the agent (e.g., via `FunctionTool` in ADK or an MCP server if using Model Context Protocol).
- **AI Models:** Gemini family (via Google ADK)

## Infrastructure & Deployment
- **Runtime:** [Vertex AI Agent Engine](https://cloud.google.com/vertex-ai/docs/agents/overview)
- **IaC:** [Terraform](https://www.terraform.io/)
- **CI/CD:** [Google Cloud Build](https://cloud.google.com/build)

## Development Tools
- **Package Manager:** [uv](https://docs.astral.sh/uv/)
- **Linter:** [Ruff](https://docs.astral.sh/ruff/)
- **Type Checker:** [ty](https://docs.astral.sh/ty/) (Astral's type checker)
- **Spelling:** [codespell](https://github.com/codespell-project/codespell)
- **Testing:** [pytest](https://docs.pytest.org/), [locust](https://locust.io/) (load testing)