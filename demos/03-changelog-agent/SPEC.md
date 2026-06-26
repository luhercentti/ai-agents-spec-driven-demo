# Demo: Changelog Agent

## What this demo does
Reads a raw git log (`git_log.txt`) and produces a clean, grouped CHANGELOG
in Keep a Changelog format using the OpenAI API.

The changelog is committed to `output/CHANGELOG.md`. You do not need to run
anything to see the result.

## How to run
```sh
pip install openai
export OPENAI_API_KEY=sk-...
python agent.py
# output/CHANGELOG.md will be written
```
