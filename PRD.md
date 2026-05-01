# Product Requirements Document — LoopForge

**Version:** 0.1  
**Status:** Active Development  
**Author:** [Your name / handle]  
**Last updated:** May 2026

---

## 1. Problem Statement

### 1.1 Context

Modern AI coding assistants (Claude Code, Cursor, Aider) are powerful but stateless between steps. A developer running a real-world refactoring task must manually:

1. Trigger code generation
2. Run tests
3. Read failures
4. Prompt the model to fix them
5. Repeat — sometimes 5–10 iterations

Each intervention breaks flow. For complex tasks (auth refactors, API migrations, schema changes), this manual loop takes hours that should take minutes.

For professionals operating across domains — e.g., a developer who is also a practicing attorney — the overhead compounds. Legal drafting requires the same structured iteration: draft → review → revise → cross-reference. No tool today handles both in a unified agentic session.

### 1.2 Current Pain Points

| Pain Point | Impact |
|---|---|
| Manual test-fix loops | ~40% of agentic session time is human-in-the-loop waiting |
| Context loss between sessions | Long tasks must be restarted; expensive token re-ingestion |
| No cross-domain agent | Code and documentation require completely separate workflows |
| Token cost ceilings | Complex tasks hit rate/cost limits mid-execution |

---

## 2. Goals

### 2.1 Primary Goals

- **G1:** Fully automate the code → test → fix → verify loop without human intervention
- **G2:** Enable a single agentic session to produce both implementation code and its accompanying documentation
- **G3:** Evaluate MiMo V2.5 Pro as a cost-effective backbone for long-context agentic tasks

### 2.2 Non-Goals (v0.1)

- Not a general-purpose AI assistant or chat interface
- Not a replacement for Cursor or Claude Code (integrates with them)
- Not a SaaS product (personal tooling first)

---

## 3. User Stories

**As a developer running a refactor:**  
I want the agent to read my codebase, implement the change, run tests, fix failures, and confirm success — without me watching the terminal.

**As a developer shipping a feature:**  
I want the agent to write the code *and* generate the PR description, usage documentation, and a changelog entry in the same session.

**As an attorney reviewing technical contracts:**  
I want the agent to analyze code described in an agreement, produce a structured technical summary, and flag ambiguous implementation clauses.

---

## 4. Architecture

### 4.1 Agent Roles

| Agent | Responsibility |
|---|---|
| **Coordinator** | Receives task, decomposes into subtasks, routes to specialists |
| **Code Agent** | Implements code changes, runs lint/test, self-corrects |
| **Document Agent** | Generates specs, usage docs, legal-technical summaries |
| **Synthesis Agent** | Merges outputs from parallel agents into final deliverable |

### 4.2 Code Agent — Closed Loop

```
Input: task description + codebase path
  │
  ▼
[Read context] → parse existing code, identify relevant files
  │
  ▼
[Plan] → outline changes required (structured reasoning step)
  │
  ▼
[Implement] → generate diffs / new files
  │
  ▼
[Validate] → run linter + test suite
  │
  ├─ PASS → output result, hand off to Document Agent
  │
  └─ FAIL → analyze error, generate targeted fix → [Implement] (max 8 iterations)
               └─ if still failing after limit → surface to user with diagnosis
```

### 4.3 Multi-Agent Flow

```
Coordinator receives task
    │
    ├── Route: Code subtasks → Code Agent (parallel)
    ├── Route: Doc subtasks → Document Agent (parallel)
    │
    └── Synthesis Agent merges outputs when both complete
```

### 4.4 Model Configuration

```yaml
# config/models.yaml
coordinator: claude-sonnet-4  # High reasoning, low volume
code_agent: mimo-v2.5-pro     # High volume, long context (evaluation target)
document_agent: mimo-v2.5-pro # High volume, structured output
synthesis: claude-sonnet-4    # Final quality pass
```

---

## 5. Technical Requirements

### 5.1 Functional Requirements

| ID | Requirement | Priority |
|---|---|---|
| F1 | Agent reads entire codebase into context before acting | P0 |
| F2 | Lint and test suite execute automatically after each implementation step | P0 |
| F3 | On test failure, agent parses stderr and generates targeted fix (not full rewrite) | P0 |
| F4 | Max iteration limit configurable (default: 8) | P1 |
| F5 | Document agent receives code output as input context | P0 |
| F6 | Coordinator supports parallel agent execution | P1 |
| F7 | Session state persists to disk (resume interrupted runs) | P1 |
| F8 | Model backend swappable via config (Claude, MiMo, others) | P0 |

### 5.2 Non-Functional Requirements

| ID | Requirement |
|---|---|
| NF1 | Target: <2 min for single-file refactor end-to-end |
| NF2 | Support context windows up to 1M tokens |
| NF3 | Structured logging for all agent decisions (benchmark data collection) |
| NF4 | Config-driven — no hardcoded model names or paths |

---

## 6. Benchmark Plan

Primary evaluation: **MiMo V2.5 Pro vs Claude Sonnet** on agentic coding tasks.

### 6.1 Test Cases

| Test | Description | Metric |
|---|---|---|
| Auth refactor | Refactor JWT auth module, all tests pass | Iterations to success, tokens used |
| API migration | Migrate REST endpoints to new schema | Error rate, self-correction accuracy |
| Long-context doc | Generate spec from 80k-token codebase | Coherence score (manual review) |
| Cross-domain | Code + legal summary in one session | Output quality, session token cost |

### 6.2 Success Criteria

- MiMo matches Claude on test-pass rate within ±5%
- MiMo costs ≤60% of Claude equivalent for same task
- No degradation in self-correction accuracy over 5+ iteration loops

---

## 7. Roadmap

### v0.1 — Foundation (current)
- [x] Single-agent code loop (read → implement → test → fix)
- [x] Lint/test integration
- [ ] Document agent (in progress)

### v0.2 — Multi-agent
- [ ] Coordinator routing logic
- [ ] Parallel agent execution
- [ ] Synthesis step

### v0.3 — Benchmark & Evaluate
- [ ] MiMo V2.5 Pro integration via platform.xiaomimimo.com API
- [ ] Benchmark suite
- [ ] Results published to `/benchmarks`

### v1.0 — Stable
- [ ] Full pipeline end-to-end tested
- [ ] Config-driven model selection
- [ ] Documentation complete

---

## 8. Open Questions

- How to handle partial test suite failures (some pass, some fail) — fix all or fix incrementally?
- What is the right iteration limit before surfacing to user?
- For the Document Agent, how much code context should be passed — full output or summary?

---

*This document is the source of truth for LoopForge development. Updated as decisions are made.*
