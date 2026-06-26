# Feature Spec: RAG Mini Pipeline

## Status
done

## Summary
Embed a small set of local Markdown documents and answer questions using retrieval-augmented generation,
with no external vector database.

## Problem
RAG is often demonstrated with heavyweight infrastructure (Pinecone, Weaviate, FAISS).
This demo shows the core mechanics — embed, retrieve, generate — in a single readable
Python script using only numpy for cosine similarity.

## Inputs
- A `docs/` folder containing two or more `.md` files (the knowledge base)
- A hardcoded list of three questions defined in the script

## Outputs
- A Markdown file (`output/answers.md`) containing each question followed by its answer,
  with a citation showing which document was retrieved

## Behavior
1. Script reads all `.md` files from `docs/`
2. Chunks each document by paragraph (double newline split)
3. Embeds each chunk using OpenAI `text-embedding-3-small`
4. For each question:
   a. Embeds the question
   b. Computes cosine similarity against all chunk embeddings
   c. Retrieves the top-1 most similar chunk
   d. Passes the chunk + question to `gpt-4o-mini` with a strict grounding instruction:
      "Answer only from the provided context. If the context does not contain the answer, say so."
   e. Appends the question, answer, and source filename to the output
5. Writes the full Q&A to `output/answers.md`

## Constraints
- Must not answer from model training data — answers must be grounded in retrieved context
- Must cite the source document for every answer
- Must handle the case where no relevant chunk is found (similarity below 0.3 threshold)
- No external vector database — cosine similarity is computed in memory with numpy

## Acceptance Criteria
- [ ] `output/answers.md` contains all three questions with answers
- [ ] Each answer includes a citation (source filename)
- [ ] At least one answer correctly uses information from a specific doc
- [ ] The script runs end-to-end without external services beyond the OpenAI API

## Open Questions
- None
