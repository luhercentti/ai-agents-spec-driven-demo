# Demo: Prompt Chain

## What this demo does
Implements a four-step prompt chain — plan, draft, critique, refine — to produce
a higher-quality explanation than a single-shot prompt would.

The full chain output (all four steps) is committed to `output/result.md`.
You do not need to run anything to see the result.

## The task
Write a technical explanation of how vector embeddings work for a software engineer
who has not worked with ML before.

## The chain
1. **Plan** — produce a structured outline of key points to cover
2. **Draft** — write a full explanation based on the outline
3. **Critique** — structured feedback: clarity, accuracy, gaps
4. **Refine** — revised final version incorporating the critique

## How to run
```sh
pip install openai
export OPENAI_API_KEY=sk-...
python chain.py
# output/result.md will be written
```
