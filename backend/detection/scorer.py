from typing import Dict, Tuple, List
from backend.pipeline.embeddings import get_embeddings
from backend.pipeline.faiss_store import add_vectors, search

# Demo "typology" phrases you can expand
TYPOLOGIES = {
    1: "structuring transactions to avoid reporting thresholds",
    2: "suspicious wire transfer to high-risk jurisdiction",
    3: "use of cash-intensive business to launder funds",
}

# Build typology vectors once (id space starts at 1)
_typology_vectors: List[List[float]] = []

def ensure_typologies_indexed():
    global _typology_vectors
    if not _typology_vectors:
        texts = list(TYPOLOGIES.values())
        _typology_vectors = get_embeddings(texts)
        add_vectors(_typology_vectors, list(TYPOLOGIES.keys()))

def semantic_score(text: str) -> Tuple[int, float, str]:
    """Return (best_typology_id, score, phrase) for a description text."""
    ensure_typologies_indexed()
    vec = get_embeddings([text])[0]
    ids, scores = search(vec, k=1)
    best_id = ids[0] if ids else -1
    score = float(scores[0]) if scores else 0.0
    phrase = TYPOLOGIES.get(best_id, "")
    return best_id, score, phrase
