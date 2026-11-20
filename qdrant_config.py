import os

from dotenv import load_dotenv
from qdrant_client import QdrantClient


def qdrant_client_erstellen() -> QdrantClient:
    load_dotenv()
    modus = os.getenv("QDRANT_MODE", "local").strip().lower()

    if modus == "local":
        pfad = os.getenv("QDRANT_PATH", "qdrant_storage")
        return QdrantClient(path=pfad)

    if modus == "server":
        return QdrantClient(
            url=os.getenv("QDRANT_URL", "http://localhost:6333"),
            api_key=os.getenv("QDRANT_API_KEY") or None,
        )

    raise ValueError("QDRANT_MODE muss 'local' oder 'server' sein.")