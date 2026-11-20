# Hugging Face Docker Space veröffentlichen

## Voraussetzungen

1. Lege auf Hugging Face ein neues Space mit SDK **Docker** an.
2. Verbinde dein lokales Git-Repository mit dem Hugging-Face-Repository.
3. Das echte OpenRouter/OpenAI-Secret darf niemals in Git gespeichert werden.

## Secret

Lege im Hugging-Face-Space unter **Settings -> Variables and secrets** folgende Variable an:

- Name: `OPENAI_API_KEY`
- Secret: dein OpenRouter- oder OpenAI-Schlüssel

Optional:

- `OPENAI_CHAT_MODEL=gpt-4.1-mini`
- `OPENAI_EMBEDDING_MODEL=text-embedding-3-small`

## Hochladen

```powershell
cd C:\Users\a_tec\OneDrive\Desktop\konsulat-rag
git init
git remote add space https://huggingface.co/spaces/DEIN-NAME/konsulat-rag
git add Dockerfile app.py chunking.py embedding.py laden.py llm_config.py qdrant_config.py rag.py vektordg.py requirements.txt data README.md
git add -f qdrant_storage
git commit -m "Deploy Konsulat-RAG"
git push -u space main
```

Hugging Face nutzt den Docker-SDK-Mode und erkennt den Port über `app_port: 7860`.
