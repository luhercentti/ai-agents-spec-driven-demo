# Demo: RAG Mini Pipeline

## What this demo does
Embeds a small set of local Markdown documents and answers questions using
retrieval-augmented generation — with no external vector database.

The full Q&A run is committed to `output/answers.md`. You do not need to run
anything to see the result.

## How it works
1. Reads all `.md` files from `docs/`
2. Chunks each document by paragraph
3. Embeds each chunk using `text-embedding-3-small`
4. For each question: embeds the question, finds the most similar chunk via
   cosine similarity (numpy), passes chunk + question to `gpt-4o-mini`
5. Writes all answers with source citations to `output/answers.md`

## How to run
```sh
pip install openai numpy
export OPENAI_API_KEY=sk-...
python pipeline.py
# output/answers.md will be written
```
