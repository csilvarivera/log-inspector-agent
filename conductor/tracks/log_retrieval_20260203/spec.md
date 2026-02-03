# Specification: log_retrieval_20260203

## Overview
This track focuses on implementing the core capability for the Log Inspector Agent to interact with Google Cloud Logging. The goal is to provide a set of tools that allow the agent to fetch, filter, and analyze logs from a user-specified Google Cloud project.

## Functional Requirements
- **Project Context:** The tool must be able to target a specific Google Cloud Project ID.
- **Log Retrieval:** 
    - Fetch log entries based on a time range (default to last hour).
    - Filter by log severity (e.g., ERROR, WARNING, INFO).
    - Limit the number of results to prevent overwhelming the agent's context window.
- **Log Searching:**
    - Search for specific keywords or regex patterns within log messages.
- **Error Handling:**
    - Handle common GCP errors such as "Permission Denied" or "Project Not Found" with user-friendly messages.

## Technical Requirements
- **Library:** Use the official `google-cloud-logging` Python client library.
- **ADK Integration:** Implement as `FunctionTool` objects to be registered with the `LlmAgent`.
- **Security:** Rely on Application Default Credentials (ADC) for authentication.
- **Performance:** Ensure efficient log querying to maintain agent responsiveness.

## Acceptance Criteria
- Agent can successfully list recent ERROR logs from a specified GCP project.
- Agent can search for a specific string (e.g., "exception") in logs and return the matching entries.
- Tools are fully tested with unit tests (mocking GCP responses).
- >80% code coverage for the new tool implementation.
