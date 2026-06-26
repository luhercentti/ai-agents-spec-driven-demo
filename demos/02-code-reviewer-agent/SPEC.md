# Demo: Code Reviewer Agent

## What this demo does
Reads a unified diff (`sample_diff.txt`) and produces a structured, prioritized
code review using the OpenAI API.

The review is committed to `output/review.md`. You do not need to run anything
to see the result.

## How to run
```sh
pip install openai
export OPENAI_API_KEY=sk-...
python agent.py
# output/review.md will be written
```
