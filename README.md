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

### 3. Set your credentials

All scripts use the standard `openai` Python SDK and read three environment variables:

| Variable | Required | Description |
|---|---|---|
| `OPENAI_API_KEY` | Yes | Your API key or auth token |
| `OPENAI_BASE_URL` | No | API endpoint — set this to use a non-OpenAI provider |
| `OPENAI_MODEL` | No | Model to use — defaults to `gpt-4o` (or `gpt-4o-mini` for lighter demos) |

---

#### Option A — GitHub Copilot (recommended)

If you have an active GitHub Copilot subscription you already have API access through
GitHub's OpenAI-compatible endpoint. No separate API key or payment needed.

Requirements: [GitHub CLI](https://cli.github.com) installed and authenticated (`gh auth login`).

```sh
export OPENAI_API_KEY=$(gh auth token)
export OPENAI_BASE_URL=https://api.githubcopilot.com
```

Available models depend on your Copilot plan:

| Model | Individual / Business | Enterprise |
|---|---|---|
| `gpt-4o`, `gpt-4o-mini`, `gpt-4.1` | Yes | Yes |
| `claude-sonnet-4.6`, `claude-haiku-4.5`, `claude-opus-4.7` | No | Yes |
| `gemini-3.5-flash`, `gemini-3.1-pro-preview` | No | Yes |

> Claude and Gemini models are listed in the API but can be gated behind Copilot Enterprise.
> If you have Individual or Business, use `gpt-4o` — it works out of the box.

Verify it works:
```sh
.venv/bin/python3 -c "
from openai import OpenAI
import os
r = OpenAI().chat.completions.create(
    model=os.environ.get('OPENAI_MODEL', 'gpt-4o'),
    messages=[{'role': 'user', 'content': 'Reply with just: OK'}]
)
print(r.choices[0].message.content)
"
```

Expected output: `OK`

---

#### Option B — OpenAI direct

```sh
export OPENAI_API_KEY=sk-...
# OPENAI_BASE_URL not needed — the SDK defaults to api.openai.com
```

Available models: `gpt-4o`, `gpt-4o-mini`, `gpt-4.1`, etc.

---

#### Option C — Anthropic (Claude) direct

The scripts use the `openai` SDK, which is **not** compatible with the Anthropic SDK directly.
However, Anthropic provides an OpenAI-compatible endpoint:

```sh
export OPENAI_API_KEY=sk-ant-...
export OPENAI_BASE_URL=https://api.anthropic.com/v1
export OPENAI_MODEL=claude-sonnet-4-5
```

> Note: not all features (e.g. `response_format: json_object`) are supported identically
> on the Anthropic direct endpoint. Option A (GitHub Copilot) is the most reliable way
> to use Claude with these scripts.

---

### 4. Run each demo

All commands run from the repo root. Output is written to each demo's `output/` folder
(gitignored — output belongs to you, not the repo).

**Demo 01 — Spec to API**
```sh
.venv/bin/python3 demos/01-spec-to-api/generate.py
# output → demos/01-spec-to-api/output/main.py
```
Reads `SPEC.md`, generates a complete FastAPI application. Validates syntax before writing.

What to expect:
- A Python file with Pydantic models, 5 route handlers, and a `uvicorn.run` entrypoint
- The script prints `Done. Written N lines to ...`

---

**Demo 02 — Code Reviewer Agent**
```sh
.venv/bin/python3 demos/02-code-reviewer-agent/agent.py
# output → demos/02-code-reviewer-agent/output/review.md
```
Reads `sample_diff.txt` (an intentionally flawed auth diff), returns a structured review.

What to expect:
- A Markdown file with a summary, a severity-tagged findings table, and a verdict
- The MD5 password hashing and unguarded `None` secret should both appear as `critical`
- Verdict: `request-changes`

---

**Demo 03 — Changelog Agent**
```sh
.venv/bin/python3 demos/03-changelog-agent/agent.py
# output → demos/03-changelog-agent/output/CHANGELOG.md
```
Reads `git_log.txt`, rewrites and groups commits into Keep a Changelog format.

What to expect:
- `Added`, `Changed`, `Fixed`, `Removed` sections
- No commit hashes in the output
- Noise commits (`wip`, `cleanup`, `fix typo`) discarded

---

**Demo 04 — RAG Mini Pipeline**
```sh
.venv/bin/python3 demos/04-rag-mini/pipeline.py
# output → demos/04-rag-mini/output/answers.md
```
Embeds `docs/` files, answers 3 questions using in-memory cosine similarity. No vector DB.

What to expect:
- Progress printed per question: `Processing: How is cosine similarity...`
- Each answer cites the source document and similarity score
- Embedding model is always `text-embedding-3-small` (via Copilot or OpenAI)

---

**Demo 05 — Prompt Chain**
```sh
.venv/bin/python3 demos/05-prompt-chain/chain.py
# output → demos/05-prompt-chain/output/result.md
```
Four-step chain: plan → draft → critique → refine. Each step feeds into the next.

What to expect:
- Four progress lines: `Step 1/4 — Planning...` through `Step 4/4 — Refining...`
- Output file with all four steps as sections
- Step 4 noticeably more complete than Step 2

---

### 5. Run all demos at once

```sh
export OPENAI_API_KEY=$(gh auth token)
export OPENAI_BASE_URL=https://api.githubcopilot.com
# OPENAI_MODEL defaults to gpt-4o — change if you have Copilot Enterprise

for script in \
  demos/01-spec-to-api/generate.py \
  demos/02-code-reviewer-agent/agent.py \
  demos/03-changelog-agent/agent.py \
  demos/04-rag-mini/pipeline.py \
  demos/05-prompt-chain/chain.py
do
  echo "\n--- Running $script ---"
  .venv/bin/python3 $script
done
```

---

## Two-layer architecture

This repo has two distinct layers that serve different purposes. Understanding this
distinction is the core idea the project demonstrates.

```
Layer 1 — Runtime demos        demos/*/
Layer 2 — AI dev infrastructure  AGENTS.md, SPEC/, .opencode/, .agents/
```

They are completely independent. Layer 2 never gets called by Layer 1.

---

### Layer 1 — Runtime demos (`demos/`)

These are the Python scripts you run. They call the LLM API at runtime and produce
output files. They have no dependency on anything in Layer 2.

---

### Layer 2 — AI development infrastructure

This layer is not code you execute. It is a set of structured documents that give
AI coding assistants (like [OpenCode](https://opencode.ai), GitHub Copilot Chat, or
Cursor) the context they need to work effectively inside this project. Think of it as
documentation written for AI tools instead of humans.

#### `AGENTS.md`

Read by AI assistants automatically when they open this repo. It tells the assistant:

- What this project is and how it is structured
- What conventions to follow (spec-first rule, output artifact pattern)
- What environment variables are needed and why
- How to run the demos
- What the coordinate system or domain-specific concepts are

Without `AGENTS.md`, an AI assistant has to guess all of this from the code. With it,
the assistant immediately has the full project context and gives better, more consistent
answers from the first message.

#### `SPEC/`

The specification layer. Written **before** any code. Contains:

| File | Purpose |
|---|---|
| `constitution.md` | The non-negotiable principles of this project — referenced when any decision is unclear |
| `architecture.md` | How the system is structured and why — layers, data flow, constraints |
| `roadmap.md` | What is done, in progress, and planned |
| `tech-stack.md` | What tools are used, what is intentionally excluded, and why |
| `features/_template.md` | The canonical template every feature spec must follow |
| `features/*.md` | One spec per demo — written before the script was created |

The `SPEC/` folder serves two audiences simultaneously:
1. **Humans** — establishes shared understanding before implementation starts
2. **AI assistants** — gives the assistant the intent and constraints behind the code,
   so it can reason about correctness rather than just syntax

When an AI assistant reads `SPEC/features/code-reviewer-agent.md` before editing
`demos/02-code-reviewer-agent/agent.py`, it knows what the script is supposed to do,
what it must not do, and what the acceptance criteria are. It cannot get that from the
code alone.

#### `.opencode/agents/`

Named agent definitions read by [OpenCode](https://opencode.ai) during a development
session. Each file defines a specific role the AI takes on when invoked:

| File | What it defines |
|---|---|
| `spec-writer.md` | Role, rules, and output format for writing feature specs |
| `code-reviewer.md` | Review rubric, severity levels, what NOT to comment on |
| `changelog.md` | How to group commits, what to discard, output format |

These are not called by the demo scripts. They are invoked when **you** ask the AI
assistant to perform that role during development — for example, asking it to write a
spec for a new feature, or review a diff before committing.

#### `.opencode/commands/`

Custom slash commands that extend the AI assistant's interface for this project.
Defined in Markdown, registered with OpenCode, invoked by typing them in chat:

| Command | What it does |
|---|---|
| `/new-feature <description>` | Activates `spec-writer` agent → scaffolds a new `SPEC/features/*.md` |
| `/review [file]` | Activates `code-reviewer` agent → reviews current diff, returns structured report |
| `/spec-check <demo>` | Activates `output-validator` skill → checks implementation against its spec |

Again — these are development-time tools. They are not wired into the Python scripts.

#### `.agents/skills/`

Reusable capability definitions that can be loaded into any AI agent session,
not just OpenCode. A skill is a portable description of *how to do something*:

| Skill | What it teaches the agent |
|---|---|
| `spec-writer` | Step-by-step process for turning plain English into a structured spec |
| `output-validator` | How to compare a committed artifact against its spec statically |

The difference between a skill and an agent definition: an **agent** has a role and
owns a task end-to-end. A **skill** is a reusable capability that any agent can load.
`spec-writer` the agent uses `spec-writer` the skill, but the skill can also be loaded
into a general-purpose assistant session without the full agent definition.

---

## How the two layers work together in practice

Here is the actual development workflow this repo was built with:

```
1. Open repo in OpenCode
   → AGENTS.md is read automatically → assistant has full project context

2. Type: /new-feature "an agent that reads a CSV and detects anomalies"
   → spec-writer agent activates
   → reads _template.md
   → produces SPEC/features/csv-anomaly-detector.md

3. Review and approve the spec (human step)

4. Ask: "implement this spec"
   → assistant reads the spec + AGENTS.md + tech-stack.md
   → writes demos/06-csv-anomaly-detector/agent.py

5. Type: /spec-check demos/06-csv-anomaly-detector
   → output-validator skill activates
   → compares implementation against spec acceptance criteria
   → returns a pass/fail checklist

6. Type: /review
   → code-reviewer agent activates
   → reviews the diff
   → returns structured findings before commit
```

The demo scripts in `demos/` are the **output** of this workflow — artifacts produced
by running it. The infrastructure in Layer 2 is what made building them structured
and repeatable.

---

## Philosophy

See [SPEC/constitution.md](SPEC/constitution.md) for the principles guiding this project.

The short version: specs exist so that both humans and AI agents have a shared, unambiguous
description of intent before implementation begins. Agents work best when given clear roles,
bounded context, and structured output requirements.
