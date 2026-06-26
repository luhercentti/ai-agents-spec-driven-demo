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
demos/              ← self-contained Python demos — you run these locally
```

---

## Demos

| # | Demo | Pattern |
|---|---|---|
| [01](demos/01-spec-to-api/) | Spec to API | Read a spec → generate a working FastAPI app |
| [02](demos/02-code-reviewer-agent/) | Code Reviewer Agent | Read a diff → produce a structured, actionable review |
| [03](demos/03-changelog-agent/) | Changelog Agent | Read git log → write a human-readable CHANGELOG |
| [04](demos/04-rag-mini/) | RAG Mini Pipeline | Embed local docs → retrieve → answer questions |
| [05](demos/05-prompt-chain/) | Prompt Chain | Multi-step chain: plan → draft → critique → refine |

Each demo has a `SPEC.md` written before any code and a clean Python script (~60–100 lines).
**Output is generated locally by you — nothing is pre-committed.**

---

## Running the demos locally

### 1. Clone the repo

```sh
git clone git@github.com:luhercentti/ai-agents-spec-driven-demo.git
cd ai-agents-spec-driven-demo
```

### 2. Create a virtual environment

```sh
python3 -m venv .venv
.venv/bin/pip install openai numpy
```

> Python 3.11 or higher required.

### 3. Set your API credentials

The scripts use the standard `openai` Python SDK. They read two environment variables:

```sh
OPENAI_API_KEY   # required — your API key or token
OPENAI_BASE_URL  # optional — defaults to OpenAI; set this to use another provider
```

Pick one of the three options below depending on what you have access to:

---

**Option A — OpenAI**

Sign up at https://platform.openai.com, create an API key, then:

```sh
export OPENAI_API_KEY=sk-...
```

Models used: `gpt-4o`, `gpt-4o-mini`, `text-embedding-3-small`

---

**Option B — GitHub Copilot**

If you have an active GitHub Copilot subscription, you already have access to the
same models through GitHub's API — no separate payment needed.

Requirements: [GitHub CLI](https://cli.github.com) installed and logged in (`gh auth login`).

```sh
export OPENAI_API_KEY=$(gh auth token)
export OPENAI_BASE_URL=https://api.githubcopilot.com
```

Verify your setup:
```sh
.venv/bin/python3 -c "
from openai import OpenAI
r = OpenAI().chat.completions.create(
    model='gpt-4o',
    messages=[{'role': 'user', 'content': 'Reply with just: OK'}]
)
print(r.choices[0].message.content)
"
```

Expected output: `OK`

---

**Option C — Anthropic (Claude)**

Sign up at https://console.anthropic.com, create an API key, then install the SDK:

```sh
pip install anthropic
export ANTHROPIC_API_KEY=sk-ant-...
```

> Note: the demo scripts use the OpenAI SDK. To use Claude you would need to swap
> the client in each script to `anthropic.Anthropic()` and adjust the API call format.
> Options A and B work out of the box with no code changes.

---

### 4. Run each demo

All commands run from the repo root. Output is written to each demo's `output/` folder
(which is gitignored — it belongs to you, not the repo).

**Demo 01 — Spec to API**
```sh
.venv/bin/python3 demos/01-spec-to-api/generate.py
```
Reads `demos/01-spec-to-api/SPEC.md`, calls the LLM, and writes a complete FastAPI
application to `demos/01-spec-to-api/output/main.py`.

What to expect:
- A single Python file with Pydantic models, route handlers, and a `uvicorn.run` entrypoint
- Exactly the 5 endpoints described in the spec — no more, no less
- Valid Python syntax (the script validates this before writing)

---

**Demo 02 — Code Reviewer Agent**
```sh
.venv/bin/python3 demos/02-code-reviewer-agent/agent.py
```
Reads `demos/02-code-reviewer-agent/sample_diff.txt` (an intentionally flawed auth diff)
and writes a structured review to `demos/02-code-reviewer-agent/output/review.md`.

What to expect:
- A Markdown report with a summary, a findings table, and a verdict
- The MD5 password hashing and the unguarded `None` secret should both appear as `critical`
- Verdict will be `request-changes`

---

**Demo 03 — Changelog Agent**
```sh
.venv/bin/python3 demos/03-changelog-agent/agent.py
```
Reads `demos/03-changelog-agent/git_log.txt` and writes a formatted changelog to
`demos/03-changelog-agent/output/CHANGELOG.md`.

What to expect:
- Keep a Changelog format with `Added`, `Changed`, `Fixed`, `Removed` sections
- No commit hashes anywhere in the output
- Noise commits (`wip`, `cleanup`, `fix typo`) discarded or merged

---

**Demo 04 — RAG Mini Pipeline**
```sh
.venv/bin/python3 demos/04-rag-mini/pipeline.py
```
Embeds the Markdown files in `demos/04-rag-mini/docs/`, answers three hardcoded questions
using cosine similarity retrieval, and writes results to `demos/04-rag-mini/output/answers.md`.

What to expect:
- Progress printed to stdout as each question is processed
- Each answer cites which source document was retrieved and its similarity score
- Answers grounded in the docs, not in general model knowledge

---

**Demo 05 — Prompt Chain**
```sh
.venv/bin/python3 demos/05-prompt-chain/chain.py
```
Runs a four-step chain (plan → draft → critique → refine) and writes all four steps
to `demos/05-prompt-chain/output/result.md`.

What to expect:
- Four progress lines printed to stdout: `Step 1/4`, `Step 2/4`, `Step 3/4`, `Step 4/4`
- Output file contains all four steps with clear section headers
- Step 4 (Refined) is noticeably more complete than Step 2 (Draft)

---

## Agent Infrastructure

### `.opencode/agents/`

Named agents used during development with [OpenCode](https://opencode.ai):

- `spec-writer.md` — turns plain-English requirements into structured feature specs
- `code-reviewer.md` — reviews diffs and produces structured, prioritized feedback
- `changelog.md` — reads git history and produces clean, grouped changelogs

### `.opencode/commands/`

Custom slash commands for use inside OpenCode:

- `/new-feature` — scaffolds a new feature spec from a prompt
- `/review` — runs the code-reviewer agent on the current diff
- `/spec-check` — validates that implementation matches its spec

### `.agents/skills/`

Reusable skills loadable into any agent session:

- `spec-writer` — structured spec writing from natural language input
- `output-validator` — compares output artifacts against their source spec

---

## Philosophy

See [SPEC/constitution.md](SPEC/constitution.md) for the principles guiding this project.

The short version: specs exist so that both humans and AI agents have a shared, unambiguous
description of intent before implementation begins. Agents work best when given clear roles,
bounded context, and structured output requirements.
