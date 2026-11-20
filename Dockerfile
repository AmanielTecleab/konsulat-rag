FROM python:3.14-slim

ENV PYTHONUNBUFFERED=1 \
    PORT=7860 \
    QDRANT_MODE=local \
    QDRANT_PATH=/app/qdrant_storage

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

EXPOSE 7860

CMD ["python", "app.py"]
