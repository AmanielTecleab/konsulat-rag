from langchain_community.document_loaders import DirectoryLoader, TextLoader

loader = DirectoryLoader(
    "data",
    glob="*.txt",
    loader_cls=TextLoader,
    loader_kwargs={"encoding": "utf-8"},
)

dokumente = loader.load()

for d in dokumente:
    zeilen = d.page_content.split("\n")

    kopf = {}
    i = 0
    while i < len(zeilen) and zeilen[i].startswith(("QUELLE:", "KATEGORIE:")):
        schluessel, wert = zeilen[i].split(":", 1)
        kopf[schluessel.strip().lower()] = wert.strip()
        i += 1

    d.metadata.update(kopf)
    d.page_content = "\n".join(zeilen[i:]).strip()

if __name__ == "__main__":
    for d in dokumente:
        erste_zeile = d.page_content.split("\n")[0]
        print(d.metadata["source"], "|", d.metadata.get("quelle"), "|",
              d.metadata.get("kategorie"), "|", erste_zeile)