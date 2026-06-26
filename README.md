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

## Running the demos locally

Output artifacts are pre-committed — you can read every `output/` file without running
anything. If you want to re-run a demo and regenerate the output, follow these steps.

### 1. Clone the repo

```sh
git clone git@github.com:luhercentti/ai-agents-spec-driven-demo.git
cd ai-agents-spec-driven-demo
```

### 2. Create a virtual environment and install dependencies

```sh
python3 -m venv .venv
.venv/bin/pip install openai numpy
```

### 3. Set your API credentials

The scripts use the `openai` Python SDK. They read two environment variables:

| Variable | Value |
|---|---|
| `OPENAI_API_KEY` | Your API key |
| `OPENAI_BASE_URL` | The API endpoint (optional — defaults to OpenAI) |

**Option A — OpenAI API key:**
```sh
export OPENAI_API_KEY=sk-...
```

**Option B — GitHub Copilot (no separate API key needed):**

If you have the GitHub CLI (`gh`) installed and are logged in, your Copilot subscription
already gives you access to the same models via a compatible endpoint:

```sh
export OPENAI_API_KEY=$(gh auth token)
export OPENAI_BASE_URL=https://api.githubcopilot.com
```

Verify it works:
```sh
.venv/bin/python3 -c "
from openai import OpenAI
r = OpenAI().chat.completions.create(model='gpt-4o', messages=[{'role':'user','content':'say OK'}])
print(r.choices[0].message.content)
"
```

### 4. Run each demo

All commands are run from the repo root. Output is written to each demo's `output/` folder.

**Demo 01 — Spec to API**
```sh
.venv/bin/python3 demos/01-spec-to-api/generate.py
# output: demos/01-spec-to-api/output/main.py
```
Reads `SPEC.md`, generates a complete FastAPI application. Validates the output is
syntactically correct Python before writing it.

**Demo 02 — Code Reviewer Agent**
```sh
.venv/bin/python3 demos/02-code-reviewer-agent/agent.py
# output: demos/02-code-reviewer-agent/output/review.md
```
Reads `sample_diff.txt` (an intentionally flawed auth diff), returns a structured
review with severity-tagged findings and a verdict.

**Demo 03 — Changelog Agent**
```sh
.venv/bin/python3 demos/03-changelog-agent/agent.py
# output: demos/03-changelog-agent/output/CHANGELOG.md
```
Reads `git_log.txt`, rewrites and groups commits into Keep a Changelog format.
Noise commits (`wip`, `cleanup`, `fix typo`) are discarded automatically.

**Demo 04 — RAG Mini Pipeline**
```sh
.venv/bin/python3 demos/04-rag-mini/pipeline.py
# output: demos/04-rag-mini/output/answers.md
```
Embeds the two docs in `docs/`, answers three questions using cosine similarity
retrieval. No vector database — all similarity computed in memory with numpy.

**Demo 05 — Prompt Chain**
```sh
.venv/bin/python3 demos/05-prompt-chain/chain.py
# output: demos/05-prompt-chain/output/result.md
```
Runs a four-step chain (plan → draft → critique → refine) and prints progress
to stdout as each step completes. The output file contains all four steps.

### 5. What to look for in the output

| Demo | What to verify |
|---|---|
| 01 | All 5 endpoints from the spec exist in `output/main.py`; file is valid Python |
| 02 | MD5 password hashing and unguarded `None` secret are both flagged as `critical` |
| 03 | No commit hashes in output; noise commits excluded; grouped into sections |
| 04 | Each answer cites a source file and similarity score |
| 05 | Step 4 (Refined) is materially different from Step 2 (Draft) |
