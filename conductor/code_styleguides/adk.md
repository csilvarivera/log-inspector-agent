# Google Agent Development Kit (ADK) Style Guide

This document outlines best practices and style rules for building agents using the Google Agent Development Kit (ADK).

## 1. Core Principles
- **Modularity**: Break down complex problems into smaller, manageable agents and tools.
- **Composability**: Combine simple agents and tools to build sophisticated systems.
- **Observability**: Ensure detailed event logging and tracing are utilized to understand agent behavior.
- **Extensibility**: Design tools and agents to be easily integrated with external services.

## 2. Tool Definitions
Defining tools correctly is critical for LLM performance.
- **Function Signature**: Use type hints for all parameters. `def my_tool(param: Type, tool_context: ToolContext) -> dict:`.
- **Naming**: Use descriptive verb-noun names (e.g., `calculate_tax`, `fetch_logs`).
- **Docstrings (Critical)**: Explain the purpose, when to use it, and detail all arguments.
    - Avoid mentioning `tool_context` in the docstring as it confuses the LLM.
    - Describe the structure of the returned `dict`.
- **Return Type**: Must always return a `dict` (JSON-serializable). Include a `status` key.
- **No Defaults**: Do not use default values for parameters in tool functions.

## 3. Agent Configuration
- **Instruction Crafting**: 
    - Be specific and concise.
    - Define a clear persona and role.
    - Explicitly constrain behavior and tool usage.
    - Define expected output formats.
- **Structured Output**: Use `output_schema` with Pydantic models for reliable JSON responses. 
    - *Note: Using `output_schema` disables tool calling for that agent.*
- **Model Selection**: Prefer modern Gemini families (e.g., `gemini-2.5-flash`, `gemini-3-flash-preview`).

## 4. Context & State Management
- **Shared State**: Use `session.state` to pass intermediate results between agents.
- **ToolContext**: Use `tool_context` for interacting with the ADK runtime (state, artifacts, actions).
- **Prefixes**:
    - `user:` for persistent user data across sessions.
    - `app:` for application-wide persistent data.
    - `temp:` for ephemeral data valid only during the current invocation.

## 5. Multi-Agent Patterns
- **Delegation**: Use `transfer_to_agent` for dynamic control handovers.
- **Agent-as-a-Tool**: Use `AgentTool` when a parent agent needs a specific output from a sub-agent without losing control.
- **Sequential/Parallel/Loop**: Use standard ADK workflow agents for deterministic orchestration.

## 6. Testing & Evaluation
- **Programmatic Testing**: Use a script to call `runner.run_async` for quick validation.
- **Adk Eval**: Create `.evalset.json` files for systematic performance assessment.
- **Safety**: Implement guardrails in tools and use model/tool callbacks for safety checks.

## 7. Common Pitfalls to Avoid
- **Infinite Loops**: Always set `max_iterations` in `LoopAgent` and `max_llm_calls` in `RunConfig`.
- **Large State**: Avoid storing unnecessary data in `session.state` to keep context windows small.
- **Mutable Defaults**: Never use mutable objects as default arguments in tools or callbacks.