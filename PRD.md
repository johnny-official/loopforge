# Product Requirements Document: LoopForge

**Version:** 0.1  
**Status:** Active Development  
**Author:** [Your name / handle]  
**Last updated:** May 2026

## 1. Problem Statement

### 1.1 Context

Modern AI coding assistants such as Claude Code, Cursor, and Aider are powerful, but real-world development still requires a lot of manual coordination between steps. A developer running a serious refactor usually has to:

1. Trigger code generation
2. Run tests
3. Read failures
4. Prompt the model to fix them
5. Repeat the process, sometimes 5 to 10 times

Each manual intervention breaks flow. For complex tasks such as auth refactors, API migrations, and schema changes, this loop can take hours even when most of the work is repetitive.

For professionals operating across domains, such as a developer who is also a practicing attorney, the overhead compounds. Legal and technical drafting require the same structured process: draft, review, revise, and cross-reference. LoopForge is designed to support both workflows in one agentic session.

### 1.2 Current Pain Points

<table>
  <tr><th>Pain Point</th><th>Impact</th></tr>
  <tr><td>Manual test and fix loops</td><td>Large portions of agentic sessions are spent waiting for human intervention</td></tr>
  <tr><td>Context loss between sessions</td><td>Long tasks often require expensive context re-ingestion</td></tr>
  <tr><td>No cross-domain agent</td><td>Code and documentation are handled through separate workflows</td></tr>
  <tr><td>Token cost ceilings</td><td>Complex tasks can hit rate or cost limits before completion</td></tr>
</table>

## 2. Goals

### 2.1 Primary Goals

- **G1:** Automate the code, test, fix, and verify loop with minimal manual intervention
- **G2:** Enable one agentic session to produce both implementation code and supporting documentation
- **G3:** Evaluate MiMo V2.5 Pro as a cost-effective model backbone for long-context agentic tasks

### 2.2 Non-Goals for v0.1

- Not a general-purpose AI assistant or chat interface
- Not a replacement for Cursor or Claude Code
- Not a SaaS product at this stage

## 3. User Stories

**As a developer running a refactor:**  
I want the agent to read my codebase, implement the change, run tests, fix failures, and confirm success without me watching the terminal.

**As a developer shipping a feature:**  
I want the agent to write the code and generate the PR description, usage documentation, and changelog notes in the same session.

**As an attorney reviewing technical contracts:**  
I want the agent to analyze code described in an agreement, produce a structured technical summary, and flag ambiguous implementation clauses.

## 4. Architecture

### 4.1 Agent Roles

<table>
  <tr><th>Agent</th><th>Responsibility</th></tr>
  <tr><td>Coordinator</td><td>Receives the task, decomposes it into subtasks, and routes work to specialists</td></tr>
  <tr><td>Code Agent</td><td>Implements code changes, runs linting and tests, then self-corrects failures</td></tr>
  <tr><td>Document Agent</td><td>Generates specs, usage docs, and legal-technical summaries</td></tr>
  <tr><td>Synthesis Agent</td><td>Merges outputs from parallel agents into a final deliverable</td></tr>
</table>

### 4.2 Code Agent Closed Loop

```text
Input: task description and codebase path

Read context
Plan changes
Implement code
Validate with linting and tests
If validation passes, hand off to the Document Agent
If validation fails, analyze the error and apply a targeted fix
If the iteration limit is reached, surface the diagnosis to the user
```

### 4.3 Multi-Agent Flow

```text
Coordinator receives task
Coordinator routes code work to Code Agent
Coordinator routes documentation work to Document Agent
Synthesis Agent merges outputs after both complete
```

### 4.4 Model Configuration

```yaml
coordinator: claude-sonnet-4
code_agent: mimo-v2.5-pro
document_agent: mimo-v2.5-pro
synthesis: claude-sonnet-4
```

## 5. Technical Requirements

### 5.1 Functional Requirements

<table>
  <tr><th>ID</th><th>Requirement</th><th>Priority</th></tr>
  <tr><td>F1</td><td>Agent reads the relevant codebase context before acting</td><td>P0</td></tr>
  <tr><td>F2</td><td>Linting and tests run automatically after implementation steps</td><td>P0</td></tr>
  <tr><td>F3</td><td>On test failure, the agent parses stderr and generates a targeted fix</td><td>P0</td></tr>
  <tr><td>F4</td><td>Max iteration limit is configurable</td><td>P1</td></tr>
  <tr><td>F5</td><td>Document Agent receives finalized code output as input context</td><td>P0</td></tr>
  <tr><td>F6</td><td>Coordinator supports parallel agent execution</td><td>P1</td></tr>
  <tr><td>F7</td><td>Session state can persist to disk for interrupted runs</td><td>P1</td></tr>
  <tr><td>F8</td><td>Model backend is swappable through config</td><td>P0</td></tr>
</table>

### 5.2 Non-Functional Requirements

<table>
  <tr><th>ID</th><th>Requirement</th></tr>
  <tr><td>NF1</td><td>Target under 2 minutes for a single-file refactor</td></tr>
  <tr><td>NF2</td><td>Support context windows up to 1M tokens</td></tr>
  <tr><td>NF3</td><td>Structured logging for all agent decisions and benchmark data</td></tr>
  <tr><td>NF4</td><td>Config-driven model and path selection</td></tr>
</table>

## 6. Benchmark Plan

Primary evaluation: **MiMo V2.5 Pro vs Claude Sonnet** on agentic coding tasks.

### 6.1 Test Cases

<table>
  <tr><th>Test</th><th>Description</th><th>Metric</th></tr>
  <tr><td>Auth refactor</td><td>Refactor JWT auth module with all tests passing</td><td>Iterations to success and tokens used</td></tr>
  <tr><td>API migration</td><td>Migrate REST endpoints to a new schema</td><td>Error rate and self-correction accuracy</td></tr>
  <tr><td>Long-context doc</td><td>Generate a spec from an 80k-token codebase</td><td>Coherence score through manual review</td></tr>
  <tr><td>Cross-domain</td><td>Produce code and a legal summary in one session</td><td>Output quality and session token cost</td></tr>
</table>

### 6.2 Success Criteria

- MiMo matches Claude on test-pass rate within plus or minus 5 percent
- MiMo costs 60 percent or less of the Claude equivalent for the same task
- Self-correction accuracy stays stable over 5 or more iteration loops

## 7. Roadmap

### v0.1 Foundation

- [x] Single-agent code loop
- [x] Lint and test integration
- [ ] Document agent in progress

### v0.2 Multi-agent

- [ ] Coordinator routing logic
- [ ] Parallel agent execution
- [ ] Synthesis step

### v0.3 Benchmark and Evaluate

- [ ] MiMo V2.5 Pro integration via platform.xiaomimimo.com API
- [ ] Benchmark suite
- [ ] Results published to `/benchmarks`

### v1.0 Stable

- [ ] Full pipeline tested end to end
- [ ] Config-driven model selection
- [ ] Documentation complete

## 8. Open Questions

- Should partial test suite failures be fixed all at once or incrementally?
- What is the right iteration limit before surfacing a task to the user?
- How much code context should be passed to the Document Agent?

*This document is the source of truth for LoopForge development. Updated as decisions are made.*
