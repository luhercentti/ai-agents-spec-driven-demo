# ai-agents-spec-driven-demo

A reference implementation of **spec-driven AI development** — a workflow where
every feature starts as a written specification, and AI agents participate at each
stage of the development process.

This repo demonstrates five concrete patterns for working with LLMs in production:
spec-to-code generation, autonomous code review, changelog automation, retrieval-augmented
generation, and structured prompt chaining.

---

## Structure

```
SPEC/               ← project-wide specs (architecture, constitution, roadmap, tech-stack)
SPEC/features/      ← one spec file per demo feature, written before implementation
.opencode/agents/   ← named agent definitions with roles, context, and constraints
.opencode/commands/ ← custom slash commands that invoke agents or run workflows
.agents/skills/     ← reusable skill definitions loadable into any agent session
demos/              ← self-contained Python demos with committed output artifacts
```

---

## Demos

| # | Demo | Pattern demonstrated |
|---|---|---|
| [01](demos/01-spec-to-api/) | Spec to API | Read a spec → generate a working FastAPI app |
| [02](demos/02-code-reviewer-agent/) | Code Reviewer Agent | Read a diff → produce a structured, actionable review |
| [03](demos/03-changelog-agent/) | Changelog Agent | Read git log → write a human-readable CHANGELOG |
| [04](demos/04-rag-mini/) | RAG Mini Pipeline | Embed local docs → retrieve → answer questions |
| [05](demos/05-prompt-chain/) | Prompt Chain | Multi-step chain: plan → draft → critique → refine |

Each demo has:
- A `SPEC.md` written before any code
- A clean Python script (~60–100 lines)
- An `output/` folder with committed artifacts from a real run

---

## Agent Infrastructure

### `.opencode/agents/`

Named agents that understand this project's context and constraints:

- `spec-writer.md` — turns plain-English requirements into structured feature specs
- `code-reviewer.md` — reviews diffs and produces structured, prioritized feedback
- `changelog.md` — reads git history and produces clean, grouped changelogs

### `.opencode/commands/`

Custom slash commands for use inside OpenCode:

- `/new-feature` — scaffolds a new feature spec from a prompt
- `/review` — runs the code-reviewer agent on the current diff
- `/spec-check` — validates that implementation matches its spec

### `.agents/skills/`

Reusable skills that can be loaded into any agent session:

- `spec-writer` — structured spec writing from natural language input
- `output-validator` — compares output artifacts against their source spec

---

## Philosophy

See [SPEC/constitution.md](SPEC/constitution.md) for the principles guiding this project.

The short version: specs exist so that both humans and AI agents have a shared, unambiguous
description of intent before implementation begins. Agents are not magic — they work best
when given clear roles, bounded context, and structured output requirements.

---

## Requirements

- Python 3.11+
- `openai` Python SDK (`pip install openai`)
- `OPENAI_API_KEY` environment variable

Output artifacts are pre-committed, so **no API key is needed to explore the results**.
