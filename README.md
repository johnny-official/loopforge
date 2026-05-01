# LoopForge

> Agentic workflow engine for closed-loop software development and cross-domain document automation

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Status: Active Development](https://img.shields.io/badge/Status-Active%20Development-green.svg)]()
[![Models: Claude | MiMo](https://img.shields.io/badge/Models-Claude%20%7C%20MiMo-blue.svg)]()

## Overview

**LoopForge** is a personal agentic pipeline that automates the full software development cycle, from reading an existing codebase to refactoring, testing, self-correction, and documentation. The goal is to reduce manual handoffs between planning, coding, validation, and writing specs.

Built and used daily by a practicing attorney and software developer, LoopForge connects two high-context workflows: production-grade software engineering and structured legal or technical document generation.

## The Problem

Long agentic AI sessions consume tokens quickly, especially when a task requires several rounds of code generation, testing, debugging, and refactoring. Switching between software work and legal or technical writing makes this worse because every context switch costs time and tokens.

Existing tools usually focus on either coding or document automation. LoopForge connects both in a single continuous agent session.

## Architecture

LoopForge is organized around specialized agents with clear responsibilities.

<table>
  <tr><th>Agent</th><th>Role</th><th>Responsibilities</th></tr>
  <tr>
    <td>Coordinator Agent</td>
    <td>Workflow routing</td>
    <td>Breaks down tasks, assigns work, and coordinates outputs across agents.</td>
  </tr>
  <tr>
    <td>Code Agent</td>
    <td>Implementation loop</td>
    <td>Reads the codebase, plans changes, implements code, runs linting and tests, and self-corrects failures.</td>
  </tr>
  <tr>
    <td>Document Agent</td>
    <td>Documentation generation</td>
    <td>Creates technical specs, usage docs, legal-technical briefs, and structured summaries.</td>
  </tr>
  <tr>
    <td>Synthesis Agent</td>
    <td>Final assembly</td>
    <td>Merges outputs and prepares the final deliverable.</td>
  </tr>
</table>

### Core Loop

1. Read the relevant project context.
2. Plan the required code changes.
3. Implement the update.
4. Run linting and tests.
5. Analyze any failures.
6. Apply targeted fixes.
7. Verify the final result.

The agent runs this loop autonomously. Failures trigger targeted self-correction rather than a full restart.

## Key Features

- **Closed-loop execution:** linting, testing, and self-correction run as one workflow
- **Cross-domain sessions:** code and documentation are generated from the same project context
- **Multi-agent coordination:** a coordinator routes subtasks to specialized agents
- **Model-agnostic backbone:** currently running on Claude via Claude Code, with MiMo V2.5 Pro planned for long-context benchmarking
- **Long-context optimized:** designed for sessions requiring 500K to 1M token context windows

## Tech Stack

<table>
  <tr><th>Layer</th><th>Tool</th></tr>
  <tr><td>Primary IDE</td><td>Cursor</td></tr>
  <tr><td>Agentic CLI</td><td>Claude Code</td></tr>
  <tr><td>Backbone Models</td><td>Claude Sonnet primary, MiMo V2.5 Pro evaluation</td></tr>
  <tr><td>Languages</td><td>Python, TypeScript</td></tr>
  <tr><td>Test runners</td><td>pytest, vitest</td></tr>
  <tr><td>Linting</td><td>ruff, eslint</td></tr>
</table>

## Usage

> This repo is under active development. The core loop is functional and the multi-agent coordinator is in progress.

### Prerequisites

```bash
npm install -g @anthropic-ai/claude-code
pip install -r requirements.txt
```

### Run the code agent loop

```bash
python loopforge/agent.py -mode code -target ./src -task "refactor auth module"
```

### Run full pipeline with docs

```bash
python loopforge/agent.py -mode full -target ./src -task "add rate limiting" -doc-output ./docs
```

## Benchmark Goals

One primary goal of this project is evaluating **MiMo V2.5 Pro** as a drop-in replacement for Claude in long agentic sessions, specifically:

- Multi-step reasoning over large codebases with more than 100k tokens of context
- Self-correction accuracy over 5 or more iteration loops
- Cross-domain coherence between code context and document generation
- Token efficiency measured as cost per completed task compared with a Claude baseline

Results will be published in [`/benchmarks`](./benchmarks).

## Project Status

<table>
  <tr><th>Component</th><th>Status</th></tr>
  <tr><td>Single-agent code loop</td><td>Working</td></tr>
  <tr><td>Lint and test self-correction</td><td>Working</td></tr>
  <tr><td>Document generation agent</td><td>In progress</td></tr>
  <tr><td>Multi-agent coordinator</td><td>In progress</td></tr>
  <tr><td>MiMo V2.5 Pro integration</td><td>Planned</td></tr>
  <tr><td>Benchmark suite</td><td>Planned</td></tr>
</table>

## Author

Software engineer, IT professional, and practicing attorney. Building tools at the intersection of legal work and software automation.

## License

MIT
