# AGENTS.md — ai-agents-spec-driven-demo

This file provides context for AI agents, coding assistants, and human collaborators
working inside this repository.

---

## Purpose

This repo is a practical reference implementation of **spec-driven AI development**.
Every feature begins as a written spec. Every agent has a defined role. Every output
artifact is committed alongside the code that produced it.

The goal is not just to use AI tools — but to structure work so that AI agents can
participate meaningfully at every stage: planning, implementation, review, and documentation.

---

## Repository Layout

```
ai-agents-spec-driven-demo/
├── AGENTS.md                    ← this file
├── README.md                    ← project overview
├── opencode.json                ← opencode configuration
│
├── SPEC/                        ← all specs live here, written before code
│   ├── architecture.md
│   ├── constitution.md
│   ├── roadmap.md
│   ├── tech-stack.md
│   └── features/
│       ├── _template.md         ← canonical template for new feature specs
│       └── *.md                 ← one file per demo feature
│
├── .opencode/
│   ├── agents/                  ← agent definitions (context + role + constraints)
│   └── commands/                ← custom slash commands for this project
│
├── .agents/
│   └── skills/                  ← reusable skill definitions
│       ├── spec-writer/
│       └── output-validator/
│
└── demos/                       ← self-contained runnable demos
    ├── 01-spec-to-api/
    ├── 02-code-reviewer-agent/
    ├── 03-changelog-agent/
    ├── 04-rag-mini/
    └── 05-prompt-chain/
```

---

## Conventions

### Spec-first rule
No code is written without a corresponding `SPEC.md` in the same folder (for demos)
or a feature file under `SPEC/features/` (for project-level features). Specs are
written in plain language — no jargon, no implementation details unless necessary.

### Agent definitions (`.opencode/agents/`)
Each `.md` file in `.opencode/agents/` defines a named agent with:
- `role` — what the agent is responsible for
- `context` — what it knows about the project
- `constraints` — what it must not do
- `output format` — how it should structure its responses

### Custom commands (`.opencode/commands/`)
Each `.md` file in `.opencode/commands/` defines a slash command that can be
invoked inside OpenCode. Commands are parameterized and call agents or run workflows.

### Skills (`.agents/skills/`)
Skills are reusable capability definitions that can be loaded into any agent session.
Each skill has a `SKILL.md` describing its purpose, inputs, outputs, and usage examples.

### Demo structure
Each demo under `demos/` follows this layout:
```
demos/<name>/
├── SPEC.md          ← what this demo does and why
├── <script>.py      ← the implementation
├── [input files]    ← any static input data
└── output/          ← committed artifacts from a real run
```

Output artifacts are always committed. Reviewers do not need to run anything.

---

## Key Decisions

- **Python only** — all scripts use the standard `openai` Python SDK, no heavy frameworks
- **No vector databases** — the RAG demo uses in-memory cosine similarity for clarity
- **Structured outputs** — all agents use `response_format: json_object` or Pydantic models
  where applicable, to make outputs predictable and parseable
- **No `.env` committed** — API keys go in environment variables; `.env.example` documents them

---

## Environment Variables

| Variable | Used by |
|---|---|
| `OPENAI_API_KEY` | All demo scripts |

---

## Running a demo

```sh
cd demos/<demo-name>
pip install openai          # only dependency for most demos
export OPENAI_API_KEY=sk-...
python <script>.py
```

Output will be written to `output/` — but those files are already committed so
running is optional.
