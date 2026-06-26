# Vector Embeddings

## What are vector embeddings?

A vector embedding is a numerical representation of a piece of text (or image, audio, etc.)
as a list of floating-point numbers — a point in a high-dimensional space. The key property
is that semantically similar items are placed close together in that space.

For example, the sentences "The dog ran across the park" and "A puppy sprinted through the
garden" would have embeddings that are geometrically close, even though they share no words.

## How are embeddings generated?

Embeddings are produced by a neural network trained on large amounts of text data. The network
learns to map inputs to vectors such that similar inputs produce similar vectors. Modern embedding
models like OpenAI's `text-embedding-3-small` produce vectors of 1536 dimensions.

The process: raw text → tokenization → transformer network → fixed-size vector output.

## Measuring similarity

The most common way to measure similarity between two embeddings is cosine similarity:

```
similarity = dot(A, B) / (||A|| * ||B||)
```

This produces a value between -1 and 1. Values close to 1 mean the texts are semantically
similar. Values close to 0 mean they are unrelated.

## Common use cases

- Semantic search: find documents relevant to a query without exact keyword matching
- Retrieval-augmented generation (RAG): retrieve relevant context before generating an answer
- Clustering: group similar documents together without predefined categories
- Recommendation: find items similar to one a user has already engaged with
