from openai import OpenAI

from llm_config import modellname_ermitteln, openai_client_erstellen

EMBEDDING_MODEL = "text-embedding-3-small"
EMBEDDING_BATCH_SIZE = 64


def erstelle_embeddings(
    texte: list[str],
    batch_size: int = EMBEDDING_BATCH_SIZE,
    client: OpenAI | None = None,
) -> list[list[float]]:
    if batch_size < 1:
        raise ValueError("batch_size muss mindestens 1 sein.")
    if any(not text.strip() for text in texte):
        raise ValueError("Leere Texte können nicht eingebettet werden.")
    if not texte:
        return []

    if client is None:
        client = openai_client_erstellen()

    model = modellname_ermitteln("OPENAI_EMBEDDING_MODEL", EMBEDDING_MODEL)
    embeddings = []

    for start in range(0, len(texte), batch_size):
        batch = texte[start:start + batch_size]
        response = client.embeddings.create(model=model, input=batch)
        ergebnisse = sorted(response.data, key=lambda item: item.index)
        if len(ergebnisse) != len(batch):
            raise RuntimeError("OpenAI hat nicht für jeden Text ein Embedding geliefert.")
        embeddings.extend(item.embedding for item in ergebnisse)

    return embeddings