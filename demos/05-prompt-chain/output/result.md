# Prompt Chain Output

**Task:** Write a technical explanation of how vector embeddings work for a software engineer who has not worked with ML before.

---

## Step 1 — Outline

- **What is a vector embedding?**
  - A numerical representation of data (text, image, etc.) as a list of floating-point numbers
  - Think of it as coordinates in a high-dimensional space

- **Why do we need them?**
  - Computers can't do math on words — numbers are required for computation
  - Embeddings encode *meaning*, not just identity (unlike integer IDs)

- **How are they generated?**
  - A neural network is trained to map inputs to fixed-size vectors
  - Similar inputs are pushed close together; dissimilar inputs are pushed apart
  - The network learns this through exposure to large amounts of data

- **What does "similar" mean geometrically?**
  - Cosine similarity: measures the angle between two vectors
  - Dot product normalized by magnitude — gives a value between -1 and 1
  - Close to 1 = semantically similar; close to 0 = unrelated

- **Dimensions**
  - Modern models produce vectors with hundreds or thousands of dimensions
  - Each dimension loosely corresponds to some latent feature (not human-interpretable)

- **Practical uses for software engineers**
  - Semantic search (find docs by meaning, not keywords)
  - RAG: retrieve context before generating an LLM answer
  - Clustering, deduplication, recommendation

- **Key properties to remember**
  - Same model must be used for both documents and queries
  - Distance in embedding space reflects semantic distance
  - Embeddings are static snapshots — they don't update as meaning shifts

---

## Step 2 — Draft

If you've worked with databases, you know that a string like `"the user canceled their subscription"` is just an opaque sequence of characters to a computer. You can check if it equals another string, but you can't do any meaningful math on it. You can't ask "how close is this to `'the customer ended their plan'`?"

Vector embeddings solve this. A vector embedding converts text (or any data) into a list of numbers — a *vector* — in a way that preserves semantic meaning. Two sentences that mean roughly the same thing will have embeddings that are numerically close to each other. Two sentences that are unrelated will have embeddings that are far apart.

**The basic idea**

Imagine a 2D map where every sentence in the English language has a coordinate. Sentences about weather cluster in one area. Sentences about databases cluster in another. Sentences about cooking are somewhere else entirely. A vector embedding is exactly this — just in hundreds or thousands of dimensions instead of two.

**How they're created**

Embeddings come from neural networks trained on large amounts of text. During training, the network learns to place similar texts near each other in vector space. You don't train these yourself — you call an API (like OpenAI's `text-embedding-3-small`) and get a vector back.

The output is a list of floating-point numbers, typically 768 to 3072 values long. You don't interpret individual values. The vector is meaningful as a whole, not dimension-by-dimension.

**Measuring similarity**

The standard way to compare two embeddings is *cosine similarity*:

```
similarity = dot(A, B) / (||A|| × ||B||)
```

This gives a value between -1 and 1. In practice, with text embeddings, you'll mostly see values between 0 and 1. A score of 0.9 means highly similar; a score of 0.1 means effectively unrelated.

**What you actually do with them**

The most common use case you'll encounter as a software engineer is *semantic search*: embed your documents once (offline), embed the user's query at runtime, find the documents with the highest cosine similarity. This is how RAG (Retrieval-Augmented Generation) systems work — retrieve relevant context, then pass it to an LLM.

**One rule that trips people up**

You must always use the same embedding model for both your documents and your queries. Embeddings from different models live in different vector spaces and cannot be compared. If you re-embed your documents with a new model, you must re-embed everything — there's no way to migrate.

---

## Step 3 — Critique

**Clarity:** The 2D map analogy is helpful but introduced before establishing what a vector is — readers without math backgrounds may not connect "list of numbers" to "coordinate." The cosine similarity formula appears without context for readers who don't know what a dot product is.

**Accuracy:** The statement "A score of 0.9 means highly similar; a score of 0.1 means effectively unrelated" is a reasonable heuristic but presented as a universal rule. Thresholds vary significantly by model and use case. Calling this out more carefully would improve precision.

**Gaps:**
- No mention of what happens with non-text data (images, code) — the outline promised this
- The training process is described very vaguely ("learns to place similar texts near each other") without any intuition for *how* (e.g., contrastive learning, next-sentence prediction)
- The "static snapshots" property mentioned in the outline is missing from the draft
- No mention of chunking — which is directly relevant when engineers embed real documents

---

## Step 4 — Refined

If you've worked with databases, you know that the string `"the user canceled their subscription"` is just an opaque blob to a computer. You can check if it equals another string, but you can't do meaningful math on it. You can't ask: *how close is this to `"the customer ended their plan"`?*

Vector embeddings solve this. An embedding converts text into a **list of floating-point numbers** — a vector — in a way that preserves semantic meaning. Two sentences with similar meaning end up as numerically similar vectors. Two unrelated sentences end up far apart.

**What a vector is**

A vector is just an ordered list of numbers: `[0.23, -0.81, 0.04, ...]`. If you have two numbers, you can plot them as a point in 2D space. With three numbers, it's 3D space. Embedding vectors have hundreds or thousands of dimensions — too many to visualize, but the geometry works exactly the same way. *Distance in that space reflects semantic distance.*

**How embeddings are created**

Embedding models are neural networks trained on large amounts of text. During training, the network is shown pairs of sentences and learns to assign coordinates such that similar sentences end up close together and dissimilar ones end up far apart. The specific technique varies — some models use contrastive learning (explicitly pushing similar pairs together and dissimilar pairs apart); others use self-supervised tasks like predicting missing words.

You don't train these models yourself. You call an API — for example, OpenAI's `text-embedding-3-small` — pass in a string, and receive a vector (typically 1536 floats). You treat it as a black box.

**Measuring similarity**

The standard similarity metric is **cosine similarity**:

```
similarity = dot(A, B) / (||A|| × ||B||)
```

If the dot product and norms feel unfamiliar: this formula measures the *angle* between two vectors. A small angle (vectors pointing in roughly the same direction) gives a score near 1. A large angle gives a score near 0. Two completely perpendicular vectors give exactly 0.

Similarity scores are not universal thresholds — a "good" score depends on your model and task. In practice, you calibrate by looking at real examples from your data.

**What you do with embeddings**

The most common use case for software engineers is **semantic search**: embed your documents once (offline), store the vectors, embed a query at runtime, and retrieve the documents with the highest cosine similarity. No keywords required.

This is also the foundation of **RAG (Retrieval-Augmented Generation)**: retrieve the most relevant document chunks, include them in the LLM prompt as context, and let the model answer from that grounded source rather than from general training knowledge.

One practical note: real documents are usually too long to embed in one piece. You split them into chunks (by paragraph, sentence, or fixed token count) and embed each chunk separately. Retrieval happens at the chunk level.

**Two properties to keep in mind**

First, embeddings are **static**. Once you embed a document, its vector doesn't change if the world changes — only if the text changes. They are snapshots of meaning at the time of embedding.

Second, you must **always use the same model** for documents and queries. Embeddings from different models exist in incompatible vector spaces. If you switch models, you must re-embed everything from scratch.
