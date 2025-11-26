from sentence_transformers import SentenceTransformer

_model = SentenceTransformer("all-MiniLM-L6-v2")

def embed_text(text: str):
    text = text[:8000]
    emb = _model.encode([text], convert_to_numpy=True)[0].tolist()
    return emb
