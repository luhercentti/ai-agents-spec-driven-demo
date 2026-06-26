# Architecture

## Overview

This project is a collection of self-contained Python demos, each implementing a
distinct AI agent pattern. There is no shared runtime, no shared database, and no
service mesh. Each demo is independently executable.

The project also includes a meta-layer of agent infrastructure (`.opencode/`, `.agents/`)
that defines how AI tools interact with the project itself during development.

---

## Layers

### 1. Demo Layer (`demos/`)

Five standalone Python scripts, each solving a specific problem using the OpenAI API.
Each demo:
- Has its own `SPEC.md`
- Has its own input data (committed)
- Has its own `output/` folder with committed artifacts
- Has no dependencies on other demos

### 2. Spec Layer (`SPEC/`)

Project-wide documentation written before any code:
- `constitution.md` — immutable principles
- `architecture.md` — this file; describes structural decisions
- `roadmap.md` — what is done, what is in progress, what is planned
- `tech-stack.md` — what tools are used and why
- `features/` — one spec per demo, written in the feature template format

### 3. Agent Infrastructure Layer (`.opencode/`, `.agents/`)

Definitions that make AI tooling aware of this project:
- `.opencode/agents/` — named agents with roles and constraints
- `.opencode/commands/` — slash commands that invoke workflows
- `.agents/skills/` — reusable capability modules for agent sessions

---

## Data Flow (per demo)

```
Input data (committed file or SPEC.md)
  └─→ Python script
        └─→ OpenAI API call (with structured prompt)
              └─→ parsed response
                    └─→ written to output/ (committed artifact)
```

No demo writes to external services. No demo reads from a database. The only
external dependency is the OpenAI API, which is accessed via the `openai` Python SDK.

---

## Dependency Strategy

Each demo has one runtime dependency: `openai`. The RAG demo additionally uses
`numpy` for cosine similarity. No LangChain, no LlamaIndex, no vector databases.

Keeping dependencies minimal makes the code readable and the patterns visible.

---

## Agent Interaction Model

Agents in `.opencode/agents/` are used during development, not at runtime.
They assist with writing specs, reviewing code, and generating changelogs.
They do not run as part of any demo's execution path.

---

## Key Constraints

- All output artifacts are committed to the repository
- No `.env` files are committed; environment variables are documented in `.env.example`
- No agent modifies specs or architectural decisions autonomously
- All inter-component communication is via files, not function calls or sockets
