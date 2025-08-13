import os
import numpy as np
import faiss
from typing import List, Tuple
from backend import config

def _index(dim: int) -> faiss.IndexFlatIP:
    """Use cosine similarity via inner product after L2-normalization."""
    if os.path.exists(config.FAISS_INDEX_PATH):
        idx = faiss.read_index(config.FAISS_INDEX_PATH)
        if idx.d != dim:
            # rebuild if dims differ
            idx = faiss.IndexFlatIP(dim)
    else:
        idx = faiss.IndexFlatIP(dim)
    return idx

def _save(idx):
    os.makedirs(os.path.dirname(config.FAISS_INDEX_PATH), exist_ok=True)
    faiss.write_index(idx, config.FAISS_INDEX_PATH)

def _l2_normalize(x: np.ndarray) -> np.ndarray:
    norms = np.linalg.norm(x, axis=1, keepdims=True) + 1e-12
    return x / norms

def add_vectors(vectors: List[List[float]], ids: List[int]) -> None:
    arr = np.array(vectors, dtype="float32")
    arr = _l2_normalize(arr)
    idx = _index(arr.shape[1])
    if idx.ntotal == 0:
        idx.add_with_ids(arr, np.array(ids, dtype="int64"))
    else:
        idx.add_with_ids(arr, np.array(ids, dtype="int64"))
    _save(idx)

def search(vector: List[float], k: int = 5) -> Tuple[List[int], List[float]]:
    arr = np.array([vector], dtype="float32")
    arr = _l2_normalize(arr)
    idx = _index(arr.shape[1])
    D, I = idx.search(arr, k)
    return I[0].tolist(), D[0].tolist()
