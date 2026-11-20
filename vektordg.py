import uuid

from langchain_core.documents import Document
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, PointStruct, VectorParams

from chunking import chunks_erstellen
from embedding import erstelle_embeddings
from qdrant_config import qdrant_client_erstellen

VECTOR_SIZE = 1536
QDRANT_COLLECTION = "konsulat"
UPSERT_BATCH_SIZE = 64


def speichere_vektoren(
    chunks: list[Document],
    embeddings: list[list[float]],
    client: QdrantClient,
    collection_name: str = QDRANT_COLLECTION,
) -> None:
    if len(chunks) != len(embeddings):
        raise ValueError("Anzahl der Chunks und Embeddings muss übereinstimmen.")
    if not chunks:
        print("Keine Chunks zum Speichern vorhanden.")
        return

    if not client.collection_exists(collection_name):
        client.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(size=VECTOR_SIZE, distance=Distance.COSINE),
        )
    else:
        config = client.get_collection(collection_name).config.params.vectors
        if getattr(config, "size", None) != VECTOR_SIZE:
            raise ValueError(
                f"Collection '{collection_name}' muss unbenannte Vektoren mit "
                f"{VECTOR_SIZE} Dimensionen verwenden."
            )

    datei_indizes: dict[str, int] = {}
    punkte = []
    for chunk, embedding in zip(chunks, embeddings):
        if len(embedding) != VECTOR_SIZE:
            raise ValueError(
                f"Embedding hat {len(embedding)} statt {VECTOR_SIZE} Dimensionen."
            )

        quelle = str(chunk.metadata.get("source", "unbekannt"))
        chunk_index = datei_indizes.get(quelle, 0)
        datei_indizes[quelle] = chunk_index + 1
        punkt_id = str(uuid.uuid5(uuid.NAMESPACE_URL, f"{quelle}:{chunk_index}"))

        punkte.append(
            PointStruct(
                id=punkt_id,
                vector=embedding,
                payload={
                    "text": chunk.page_content,
                    "source": quelle,
                    "chunk_index": chunk_index,
                    "quelle": str(chunk.metadata.get("quelle", "")),
                    "kategorie": str(chunk.metadata.get("kategorie", "")),
                },
            )
        )

    for start in range(0, len(punkte), UPSERT_BATCH_SIZE):
        client.upsert(
            collection_name=collection_name,
            points=punkte[start:start + UPSERT_BATCH_SIZE],
            wait=True,
        )

    print(f"{len(punkte)} Vektoren in Qdrant-Collection '{collection_name}' gespeichert.")


def main() -> None:
    from laden import dokumente

    chunks = chunks_erstellen(dokumente)
    if not chunks:
        raise RuntimeError("Es wurden keine Text-Chunks zum Indexieren gefunden.")

    client = qdrant_client_erstellen()
    try:
        client.get_collections()
    except Exception as error:
        raise SystemExit(
            "Qdrant ist nicht erreichbar. Starte zuerst den lokalen Qdrant-Server "
            "oder prüfe QDRANT_URL in der .env-Datei."
        ) from error

    embeddings = erstelle_embeddings([chunk.page_content for chunk in chunks])
    speichere_vektoren(chunks, embeddings, client)


if __name__ == "__main__":
    main()