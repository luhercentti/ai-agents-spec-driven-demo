"""
Demo 04 — RAG Mini Pipeline
Embeds local Markdown docs, retrieves relevant chunks, answers questions.
No external vector database — cosine similarity computed in memory with numpy.
Output is written to output/answers.md.
"""

import sys
import os
from pathlib import Path

import numpy as np
from openai import OpenAI

DOCS_DIR = Path(__file__).parent / "docs"
OUTPUT_PATH = Path(__file__).parent / "output" / "answers.md"
SIMILARITY_THRESHOLD = 0.3
CHAT_MODEL = os.environ.get("OPENAI_MODEL", "gpt-4o-mini")
EMBED_MODEL = "text-embedding-3-small"

QUESTIONS = [
    "How is cosine similarity calculated between two embeddings?",
    "What are the three stages of a RAG pipeline?",
    "What chunking strategy does this demo use and why?",
]


def load_chunks() -> list[dict]:
    """Read all .md files and split into paragraph-level chunks."""
    chunks = []
    for path in sorted(DOCS_DIR.glob("*.md")):
        text = path.read_text().strip()
        paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
        for para in paragraphs:
            chunks.append({"text": para, "source": path.name})
    if not chunks:
        print(f"Error: no .md files found in {DOCS_DIR}", file=sys.stderr)
        sys.exit(1)
    return chunks


def embed_texts(client: OpenAI, texts: list[str]) -> np.ndarray:
    """Embed a list of strings using text-embedding-3-small."""
    response = client.embeddings.create(
        model=EMBED_MODEL,
        input=texts,
    )
    vectors = [item.embedding for item in response.data]
    return np.array(vectors, dtype=np.float32)


def cosine_similarity(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    """Compute cosine similarity between vector a and each row of matrix b."""
    a_norm = a / (np.linalg.norm(a) + 1e-10)
    b_norms = b / (np.linalg.norm(b, axis=1, keepdims=True) + 1e-10)
    return b_norms @ a_norm


def answer_question(client: OpenAI, question: str, context: str, source: str) -> str:
    """Answer a question using only the provided context chunk."""
    system = (
        "You are a precise assistant. Answer the question using ONLY the provided context. "
        "If the context does not contain enough information to answer, say: "
        "'The provided context does not contain enough information to answer this question.'"
    )
    user = f"Context:\n{context}\n\nQuestion: {question}"
    response = client.chat.completions.create(
        model=CHAT_MODEL,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
    )
    return response.choices[0].message.content.strip()


def main() -> None:
    client = OpenAI()
    print("Loading and chunking documents...")
    chunks = load_chunks()
    chunk_texts = [c["text"] for c in chunks]

    print(f"Embedding {len(chunks)} chunks (embed model: {EMBED_MODEL}, chat model: {CHAT_MODEL})...")
    chunk_embeddings = embed_texts(client, chunk_texts)

    results = []
    for question in QUESTIONS:
        print(f"Processing: {question[:60]}...")
        q_embedding = embed_texts(client, [question])[0]
        similarities = cosine_similarity(q_embedding, chunk_embeddings)
        best_idx = int(np.argmax(similarities))
        best_score = float(similarities[best_idx])

        if best_score < SIMILARITY_THRESHOLD:
            answer = "No sufficiently relevant context found in the knowledge base."
            source = "n/a"
        else:
            best_chunk = chunks[best_idx]
            answer = answer_question(client, question, best_chunk["text"], best_chunk["source"])
            source = best_chunk["source"]

        results.append({
            "question": question,
            "answer": answer,
            "source": source,
            "score": best_score,
        })

    lines = ["# RAG Mini — Q&A Results\n"]
    for r in results:
        lines.append(f"## Q: {r['question']}\n")
        lines.append(f"{r['answer']}\n")
        lines.append(f"*Source: `{r['source']}` (similarity: {r['score']:.3f})*\n")

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text("\n".join(lines))
    print(f"Done. Answers written to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
