from typing import List
from backend import config
import os

def get_embeddings(texts: List[str], model: str = "text-embedding-3-small") -> List[List[float]]:
    """Return list of embedding vectors for given texts using OpenAI API."""
    if not config.OPENAI_API_KEY:
        raise RuntimeError("OPENAI_API_KEY not configured")
    # OpenAI SDK (>=1.0)
    from openai import OpenAI
    client = OpenAI(api_key=config.OPENAI_API_KEY)
    resp = client.embeddings.create(model=model, input=texts)
    return [d.embedding for d in resp.data]
