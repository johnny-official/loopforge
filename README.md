# LoopForge

> Agentic workflow engine for closed-loop software development and cross-domain document automation

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Status: Active Development](https://img.shields.io/badge/Status-Active%20Development-green.svg)]()
[![Models: Claude | MiMo](https://img.shields.io/badge/Models-Claude%20%7C%20MiMo-blue.svg)]()

---

## Overview

**LoopForge** is a personal agentic pipeline that automates the full software development cycle — from reading existing codebases through refactoring, testing, self-correction, and documentation — without manual intervention between steps.

Built and used daily by a practicing attorney and software developer, LoopForge bridges two high-context domains: production-grade code engineering and structured legal/technical document generation.

---

## The Problem

Long agentic AI sessions — multi-step code generation → test → debug → refactor loops — consume tokens aggressively and hit cost ceilings before completing complex tasks. Switching between software and legal work compounds this: every context switch is expensive in both time and tokens.

Existing tools solve either coding *or* document automation. LoopForge connects both in a single continuous agent session.

---

## Architecture

```
┌─────────────────────────────────────────────────┐
│                  Coordinator Agent               │
│         (Task decomposition & routing)           │
└────────────┬───────────────────┬─────────────────┘
             │                   │
             ▼                   ▼
┌────────────────────┐  ┌────────────────────────┐
│   Code Agent       │  │   Document Agent        │
│                    │  │                         │
│ • Read codebase    │  │ • Generate tech specs   │
│ • Plan refactor    │  │ • Draft usage docs      │
│ • Implement        │  │ • Legal-technical briefs│
│ • Run lint/tests   │  │ • Structured summaries  │
│ • Self-correct     │  │                         │
└────────────┬───────┘  └──────────┬──────────────┘
             │                     │
             └──────────┬──────────┘
                        ▼
             ┌─────────────────────┐
             │   Synthesis Agent   │
             │  (Merge & finalize) │
             └─────────────────────┘
```

### Core Loop (Code Agent)

```
Read Context → Plan → Implement → Lint/Test → Self-Correct → ✓ Done
                 ↑___________________________|  (on failure)
```

The agent runs this loop autonomously. Failures trigger targeted self-correction, not a full restart.

---

## Key Features

- **Closed-loop execution** — lint, test, and self-correction run unattended
- **Cross-domain sessions** — code and documentation generated in the same context window
- **Multi-agent coordination** — coordinator routes subtasks to specialized agents in parallel
- **Model-agnostic backbone** — currently running on Claude via Claude Code; benchmarking MiMo V2.5 Pro as a cost-effective alternative for long-context reasoning tasks
- **Long-context optimized** — designed for sessions requiring 500K–1M token context windows

---

## Tech Stack

| Layer | Tool |
|---|---|
| Primary IDE | Cursor |
| Agentic CLI | Claude Code |
| Backbone Models | Claude Sonnet (primary), MiMo V2.5 Pro (evaluation) |
| Languages | Python, TypeScript |
| Test runners | pytest, vitest |
| Linting | ruff, eslint |

---

## Usage

> ⚠️ This repo is under active development. Core loop is functional; multi-agent coordinator is in progress.

### Prerequisites

```bash
# Claude Code
npm install -g @anthropic-ai/claude-code

# Python dependencies
pip install -r requirements.txt
```

### Run the code agent loop

```bash
python loopforge/agent.py --mode code --target ./src --task "refactor auth module"
```

### Run full pipeline (code + docs)

```bash
python loopforge/agent.py --mode full --target ./src --task "add rate limiting" --doc-output ./docs
```

---

## Benchmark Goals

One primary goal of this project is evaluating **MiMo V2.5 Pro** as a drop-in replacement for Claude in long agentic sessions — specifically:

- Multi-step reasoning over large codebases (>100k tokens of context)
- Self-correction accuracy over 5+ iteration loops
- Cross-domain coherence (does code context carry correctly into doc generation?)
- Token efficiency: cost per completed task vs. Claude baseline

Results will be published in [`/benchmarks`](./benchmarks).

---

## Project Status

| Component | Status |
|---|---|
| Single-agent code loop | ✅ Working |
| Lint/test self-correction | ✅ Working |
| Document generation agent | 🔄 In progress |
| Multi-agent coordinator | 🔄 In progress |
| MiMo V2.5 Pro integration | 📋 Planned |
| Benchmark suite | 📋 Planned |

---

## Author

Software engineer, IT professional, and practicing attorney. Building tools at the intersection of legal work and software automation.

---

## License

MIT
