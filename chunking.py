from collections import defaultdict
from pathlib import Path

from langchain_text_splitters import RecursiveCharacterTextSplitter

CHUNK_SIZE = 800
OVERLAP = 400  

splitter = RecursiveCharacterTextSplitter(chunk_size=CHUNK_SIZE, chunk_overlap=OVERLAP)


def chunks_erstellen(dokumente):
    return splitter.split_documents(dokumente)


def chunks_anzeigen(chunks):
    chunks_pro_datei = defaultdict(list)
    for chunk in chunks:
        dateiname = Path(chunk.metadata["source"]).name
        chunks_pro_datei[dateiname].append(chunk)

    print()
    print(f"OVERLAP = {OVERLAP}  ->  {len(chunks_pro_datei)} Dateien, {len(chunks)} Chunks")

    for dateiname, datei_chunks in sorted(chunks_pro_datei.items()):
        print(f"\n{dateiname}: {len(datei_chunks)} Chunks")
        for nummer, chunk in enumerate(datei_chunks):
            laenge = len(chunk.page_content)
            balken = "=" * round(30 * laenge / CHUNK_SIZE)
            erste_zeile = chunk.page_content.split("\n")[0][:40]
            print(f"Chunk {nummer:2}: [{balken:<30}] {laenge:4} | {erste_zeile}")

    visum = chunks_pro_datei.get("visum.txt", [])
    visumarten = ["Geschäftsvisum", "Beschäftigungsvisum", "Familienbesuchsvisum",
                  "Offizielles Visum", "Studierendenvisum", "Touristenvisum",
                  "Transitvisum", "Sonstiges Visum"]
    ohne = [n for n, chunk in enumerate(visum)
            if not any(visumart in chunk.page_content for visumart in visumarten)]

    print()
    print(f"visum.txt: Chunks ohne Visumart im Text: {len(ohne)} von {len(visum)}")
    print("Das sind die Chunks:", ohne)


if __name__ == "__main__":
    from laden import dokumente

    chunks_anzeigen(chunks_erstellen(dokumente))