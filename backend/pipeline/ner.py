from typing import List, Tuple

# spaCy optional lazy load to speed up cold start
_nlp = None

def _ensure_nlp():
    global _nlp
    if _nlp is None:
        import spacy
        try:
            _nlp = spacy.load("en_core_web_sm")
        except OSError:
            # model not present
            _nlp = spacy.blank("en")
            _nlp.add_pipe("ner")

def extract_entities(text: str) -> List[Tuple[str, str]]:
    """Return [(label, text), ...]"""
    _ensure_nlp()
    doc = _nlp(text)
    return [(ent.label_, ent.text) for ent in doc.ents]
