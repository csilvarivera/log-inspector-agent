# Agent Starter Pack Development Guide

This guide covers operational principles for projects generated or enhanced using the Agent Starter Pack.

## 1. Code Preservation & Isolation
- **Surgical Precision**: Alter only the code segments directly targeted by a request.
- **Strict Preservation**: Ensure all surrounding code, configuration values, comments, and formatting remain identical.
- **No Unintended Mutations**: Do not change parameters like `model` or `version` unless explicitly requested.

## 2. Project Workflow
- **Standard Lifecycle**: `create` → `test` → `setup-cicd` → push to deploy.
- **Dependency Management**: Always use `uv` for Python dependency management. Run `make install` to ensure environment consistency.

## 3. Testing Protocols
- **Programmatic Validation**: Create a `run_agent.py` script to call the agent logic directly. Avoid relying solely on interactive playgrounds for automated tasks.
- **Local Testing**: Use `make playground` for manual human-in-the-loop verification only.
- **Continuous Integration**: Ensure tests pass in the local environment before pushing to staging or production.

## 4. Deployment & Infrastructure
- **Infrastructure as Code**: All GCP resources are managed via Terraform in the `deployment/` directory. Update Terraform configs before manual GCP changes.
- **CI/CD Triggers**: 
    - PRs trigger checks and tests.
    - Merges to `main` deploy to staging.
    - Production deployment requires manual approval.

## 5. Monitoring & Observability
- **Traces**: OpenTelemetry traces are exported to Cloud Trace.
- **Logs**: Prompt-response logging is handled via GCS and BigQuery. Metadata-only logging is enabled by default in deployed environments for privacy.
- **Custom Tracing**: Use the custom tracer in `app/app_utils/telemetry.py` for large payloads.
