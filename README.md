# Log Inspector Agent

This agent inspects logs from Google Cloud Logging and provides insights, error analysis, and visualizations based on the log data. It is designed to help developers identify root causes and remediation steps for issues in their Google Cloud environments.

## Project Structure

```
log-inspector-agent/
├── app/                  # Core agent code
│   ├── agent.py          # Main agent logic and tool definitions
│   ├── logging_tools.py  # GCP Logging interaction tools
│   ├── reporting_tools.py # Summary and chart generation tools
│   └── agent_engine_app.py # Agent Engine application wrapper
├── .cloudbuild/          # CI/CD pipeline configurations
├── deployment/           # Infrastructure and deployment scripts
├── tests/                # Unit and integration tests
├── .env.example          # Template for environment variables
└── pyproject.toml        # Project dependencies and metadata
```

## Requirements

Ensure the following are installed on your system:

- **Python 3.10+**
- **uv**: Python package manager for dependency management.
- **Google Cloud SDK**: For authentication and accessing GCP services.
- **make**: For running development commands.

## Getting Started

### 1. Environment Configuration

Copy the example environment file and fill in your project details:

```bash
cp .env.example .env
```

Required variables:
- `GOOGLE_CLOUD_PROJECT`: Your Google Cloud Project ID.
- `GOOGLE_CLOUD_LOCATION`: The location for GCP services (e.g., global).
- `GOOGLE_GENAI_USE_VERTEXAI`: Set to True to use Vertex AI for the Gemini model.

### 2. Installation

Install the project dependencies using uv:

```bash
make install
```

Key dependencies handled by this project include:
- `google-adk`: The framework for building the agent.
- `google-cloud-logging`: For fetching logs from GCP.
- `matplotlib`: Used for generating log severity distribution charts.
- `pandas`: Used for data manipulation during log summarization.

### 3. Running Locally

Launch the local development playground:

```bash
make playground
```

This will start the ADK web interface where you can interact with the agent.

## Key Features

- **GCP Log Retrieval**: Tools to list and search logs using advanced filters and time ranges.
- **Severity Extraction Fallback**: Automatic extraction of severity levels from log payloads when official labels are missing.
- **Visual Analytics**: Generation of severity distribution charts with clear labels.
- **Formatted Insights**: Balanced log display using tables for metadata and blockquotes for full messages.

## Sample Queries

You can ask the agent questions like:

- "Show me the last 5 errors in the ReasoningEngine logs from the last hour."
- "Search for 'timeout' in my Cloud Run logs and show me a severity distribution chart."
- "Analyze logs for project [PROJECT_ID] and tell me if there are any critical issues."
- "What is the distribution of log severities for my GKE cluster in the last 24 hours?"

## Deployment

To deploy the agent to Google Cloud Agent Engine:

```bash
gcloud config set project [YOUR-PROJECT-ID]
make deploy
```

Refer to the deployment directory for more detailed infrastructure setup instructions.
