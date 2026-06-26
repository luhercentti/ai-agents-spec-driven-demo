# Tech Stack

## Runtime

| Tool | Version | Role |
|---|---|---|
| Python | 3.11+ | All demo scripts |
| openai SDK | latest | LLM API calls in all demos |
| numpy | latest | Cosine similarity in RAG demo only |

No other runtime dependencies. No frameworks. No ORMs. No async runtimes.

---

## AI / LLM

| Tool | Why chosen |
|---|---|
| OpenAI API (`gpt-4o`) | Best structured output support; JSON mode is reliable |
| `response_format: json_object` | Forces deterministic output schema from agents |
| Pydantic (where used) | Validates and types structured LLM responses |

`gpt-4o-mini` is used in demos where cost matters and task complexity is low
(e.g., changelog generation). `gpt-4o` is used where reasoning quality matters
(e.g., code review, spec generation).

---

## Developer Tooling

| Tool | Role |
|---|---|
| OpenCode | AI-assisted development, custom agents and commands |
| `.opencode/agents/` | Named agent definitions with context and constraints |
| `.opencode/commands/` | Slash commands for common development workflows |
| `.agents/skills/` | Reusable skill modules for agent sessions |

---

## Not Used (and why)

| Tool | Why excluded |
|---|---|
| LangChain | Abstraction hides the patterns this project aims to demonstrate |
| LlamaIndex | Same reason; RAG demo uses raw cosine similarity instead |
| FastAPI (runtime) | Demo 01 *generates* a FastAPI app — it doesn't run one |
| Docker | No services to containerize; all demos are single-file scripts |
| pytest | Demos are output-only; no unit tests needed for generation scripts |

---

## File Formats

- Specs: Markdown (`.md`)
- Agent definitions: Markdown (`.md`) — parsed by OpenCode
- Demo scripts: Python (`.py`)
- Output artifacts: Markdown or Python depending on demo
- Configuration: JSON (`opencode.json`)
