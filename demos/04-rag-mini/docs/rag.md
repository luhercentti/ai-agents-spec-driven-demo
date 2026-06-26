# Retrieval-Augmented Generation (RAG)

## What is RAG?

Retrieval-Augmented Generation is a technique for improving LLM responses by providing
relevant external context at inference time. Instead of relying solely on the model's
training data, RAG retrieves the most relevant documents from a knowledge base and
includes them in the prompt.

The result: answers that are grounded in specific, verifiable source material rather than
the model's general (and potentially outdated or hallucinated) knowledge.

## The RAG pipeline

A typical RAG pipeline has three stages:

**1. Indexing (offline)**
Documents are chunked into passages, each passage is converted to an embedding vector,
and all vectors are stored in a vector database or in-memory structure.

**2. Retrieval (at query time)**
The user's question is converted to an embedding. The system finds the most similar
document chunks using cosine similarity or approximate nearest neighbor search.

**3. Generation**
The retrieved chunks are included in the LLM prompt as context. The model is instructed
to answer using only the provided context, reducing hallucinations.

## Chunking strategies

How you split documents significantly affects retrieval quality:

- **Fixed-size chunks**: split every N tokens. Simple, but may cut mid-sentence.
- **Paragraph chunks**: split on double newlines. Preserves semantic units.
- **Sentence chunks**: split on sentence boundaries. High granularity but more vectors.
- **Sliding window**: overlapping chunks to avoid missing context at boundaries.

This demo uses paragraph chunking (double newline split) for simplicity.

## When RAG is not enough

RAG improves factual grounding but does not solve all LLM problems:
- If the relevant document is not in the knowledge base, RAG cannot help.
- If the chunk size is too large, irrelevant text dilutes the context.
- If the embedding model is poor, retrieval quality suffers regardless of the generator.
