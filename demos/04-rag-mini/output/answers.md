# RAG Mini — Q&A Results

## Q: How is cosine similarity calculated between two embeddings?

Cosine similarity between two embeddings A and B is calculated using the formula:

```
similarity = dot(A, B) / (||A|| * ||B||)
```

This produces a value between -1 and 1. Values close to 1 indicate that the two texts are
semantically similar, while values close to 0 indicate they are unrelated.

*Source: `embeddings.md` (similarity: 0.871)*

## Q: What are the three stages of a RAG pipeline?

A typical RAG pipeline has three stages:

1. **Indexing (offline):** Documents are chunked into passages, each passage is converted to an embedding vector, and all vectors are stored in a vector database or in-memory structure.

2. **Retrieval (at query time):** The user's question is converted to an embedding. The system finds the most similar document chunks using cosine similarity or approximate nearest neighbor search.

3. **Generation:** The retrieved chunks are included in the LLM prompt as context. The model is instructed to answer using only the provided context, reducing hallucinations.

*Source: `rag.md` (similarity: 0.849)*

## Q: What chunking strategy does this demo use and why?

This demo uses paragraph chunking — splitting documents on double newlines. The reason given is simplicity: paragraph chunks preserve semantic units (unlike fixed-size chunks, which may cut mid-sentence) while avoiding the higher vector count of sentence-level chunking.

*Source: `rag.md` (similarity: 0.812)*
