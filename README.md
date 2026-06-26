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

> Claude and Gemini models are listed in the API but gated behind Copilot Enterprise.
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

Try with Claude:
```sh
OPENAI_MODEL=claude-sonnet-4.6 .venv/bin/python3 demos/01-spec-to-api/generate.py
```

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

Try with Claude:
```sh
OPENAI_MODEL=claude-sonnet-4.6 .venv/bin/python3 demos/02-code-reviewer-agent/agent.py
```

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

Try with Gemini:
```sh
OPENAI_MODEL=gemini-3.5-flash .venv/bin/python3 demos/03-changelog-agent/agent.py
```

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

Try with Claude for the Q&A step:
```sh
OPENAI_MODEL=claude-haiku-4.5 .venv/bin/python3 demos/04-rag-mini/pipeline.py
```

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

Try with Claude:
```sh
OPENAI_MODEL=claude-sonnet-4.6 .venv/bin/python3 demos/05-prompt-chain/chain.py
```

---

### 5. Run all demos at once

```sh
export OPENAI_API_KEY=$(gh auth token)
export OPENAI_BASE_URL=https://api.githubcopilot.com
export OPENAI_MODEL=claude-sonnet-4.6   # or gpt-4o, gemini-3.5-flash, etc.

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
