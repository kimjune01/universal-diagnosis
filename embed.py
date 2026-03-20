"""Embed pipe descriptions and trauma descriptions for semantic matching."""

import sqlite3
import struct
from pathlib import Path

from sentence_transformers import SentenceTransformer

DB_PATH = Path(__file__).parent / "diagnosis.db"
MODEL_NAME = "all-MiniLM-L6-v2"


def serialize(vec: list[float]) -> bytes:
    return struct.pack(f"{len(vec)}f", *vec)


def deserialize(blob: bytes) -> list[float]:
    n = len(blob) // 4
    return list(struct.unpack(f"{n}f", blob))


def cosine_sim(a: list[float], b: list[float]) -> float:
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = sum(x * x for x in a) ** 0.5
    norm_b = sum(x * x for x in b) ** 0.5
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)


def embed_pipes():
    """Embed all pipe descriptions that don't have embeddings yet."""
    db = sqlite3.connect(DB_PATH)
    rows = db.execute(
        "SELECT p.id, p.description FROM pipe p "
        "LEFT JOIN pipe_embedding pe ON pe.pipe_id = p.id "
        "WHERE pe.pipe_id IS NULL"
    ).fetchall()

    if not rows:
        print("No unembedded pipes.")
        return

    model = SentenceTransformer(MODEL_NAME)
    texts = [r[1] for r in rows]
    vecs = model.encode(texts)

    for (pipe_id, _), vec in zip(rows, vecs):
        db.execute(
            "INSERT INTO pipe_embedding (pipe_id, embedding, model) VALUES (?, ?, ?)",
            (pipe_id, serialize(vec.tolist()), MODEL_NAME),
        )

    db.commit()
    print(f"Embedded {len(rows)} pipes.")
    db.close()


def embed_traumas():
    """Embed all trauma descriptions that don't have embeddings yet."""
    db = sqlite3.connect(DB_PATH)
    rows = db.execute(
        "SELECT t.id, t.description FROM trauma t "
        "LEFT JOIN trauma_embedding te ON te.trauma_id = t.id "
        "WHERE te.trauma_id IS NULL"
    ).fetchall()

    if not rows:
        print("No unembedded traumas.")
        return

    model = SentenceTransformer(MODEL_NAME)
    texts = [r[1] for r in rows]
    vecs = model.encode(texts)

    for (trauma_id, _), vec in zip(rows, vecs):
        db.execute(
            "INSERT INTO trauma_embedding (trauma_id, embedding, model) VALUES (?, ?, ?)",
            (trauma_id, serialize(vec.tolist()), MODEL_NAME),
        )

    db.commit()
    print(f"Embedded {len(rows)} traumas.")
    db.close()


def find_similar_traumas(description: str, threshold: float = 0.6) -> list[dict]:
    """Find traumas similar to a description. Used for recurrence probes."""
    db = sqlite3.connect(DB_PATH)
    model = SentenceTransformer(MODEL_NAME)
    query_vec = model.encode(description).tolist()

    rows = db.execute(
        "SELECT t.id, t.description, t.date, t.category, t.company_id, te.embedding "
        "FROM trauma t JOIN trauma_embedding te ON te.trauma_id = t.id"
    ).fetchall()

    results = []
    for trauma_id, desc, date, category, company_id, blob in rows:
        stored_vec = deserialize(blob)
        sim = cosine_sim(query_vec, stored_vec)
        if sim >= threshold:
            results.append({
                "trauma_id": trauma_id,
                "description": desc,
                "date": date,
                "category": category,
                "company_id": company_id,
                "similarity": round(sim, 4),
            })

    results.sort(key=lambda x: x["similarity"], reverse=True)
    db.close()
    return results


if __name__ == "__main__":
    embed_pipes()
    embed_traumas()
