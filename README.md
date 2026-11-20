---
title: Konsulat RAG
emoji: "🏛️"
colorFrom: green
colorTo: blue
sdk: docker
app_port: 7860
pinned: false
license: mit
---

# Konsulat-RAG: Embeddings und Qdrant

Die Chunks werden mit OpenAIs `text-embedding-3-small` eingebettet und in der Qdrant-Collection `konsulat` gespeichert. Jeder Punkt enthält den Text, den Quelldateinamen, den Chunk-Index sowie Quelle und Kategorie.

## Einrichtung unter Windows

1. Abhängigkeiten installieren:

   ```powershell
   & "C:\Users\a_tec\AppData\Local\Programs\Python\Python314\python.exe" -m pip install -r requirements.txt
   ```

2. Im Projektordner eine `.env`-Datei mit `OPENAI_API_KEY` anlegen. Ein Schlüssel mit dem OpenRouter-Präfix `sk-or-` wird automatisch über OpenRouter verwendet; OpenRouter-Modell-IDs werden passend ergänzt.

3. Qdrant verwendet standardmäßig den eingebetteten lokalen Modus. Die Datenbank wird persistent im Ordner `qdrant_storage` abgelegt; Docker oder ein separater Server sind dafür nicht erforderlich.

4. Vom Projektordner aus indexieren:

   ```powershell
   & "C:\Users\a_tec\AppData\Local\Programs\Python\Python314\python.exe" .\vektordg.py
   ```

5. Gradio-Frageoberfläche starten:

   ```powershell
   & "C:\Users\a_tec\AppData\Local\Programs\Python\Python314\python.exe" .\app.py
   ```

   Die Oberfläche öffnet sich unter `http://127.0.0.1:7860`. Während sie läuft, den lokalen Qdrant-Speicher nicht in einem zweiten Programm wie `rag.py` oder `vektordg.py` öffnen.

6. Alternativ Fragen im Terminal stellen:

   ```powershell
   & "C:\Users\a_tec\AppData\Local\Programs\Python\Python314\python.exe" .\rag.py
   ```

   Eine einzelne Frage geht auch direkt:

   ```powershell
   & "C:\Users\a_tec\AppData\Local\Programs\Python\Python314\python.exe" .\rag.py "Welche Unterlagen brauche ich für einen Reisepass?"
   ```

Der Dialog wird mit `ende` oder `Strg+C` beendet. Die Antwort verwendet nur die abgerufenen Textstellen und gibt die Quelldateien dazu aus. Für einen separaten Qdrant-Server `QDRANT_MODE=server`, `QDRANT_URL` und bei Bedarf `QDRANT_API_KEY` in `.env` setzen. Das Chat-Modell kann über `OPENAI_CHAT_MODEL` geändert werden. Die Vektordimension beträgt 1536; eine bestehende Collection gleichen Namens mit anderer Vektorkonfiguration wird nicht überschrieben.

## GitHub Codespaces testen

1. Repository auf GitHub erstellen und pushen.
2. Auf GitHub auf **Code** → **Codespaces** → **Create codespace** klicken.
3. Nach der Installation ausführen:

```bash
python app.py
```

4. Den automatisch geöffneten Port `7860` unter **Ports** auf **Public** oder **Private** setzen.

Lege den OpenRouter- oder OpenAI-Schlüssel im Codespace-Terminal als Umgebung fest:

```bash
export OPENAI_API_KEY="DEIN_SCHLUESSEL"
```

Den echten Schlüssel nicht in Git, README oder `.env`-Beispieldateien schreiben.