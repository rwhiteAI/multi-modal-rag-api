# Multimodal RAG API

A Flask API that ingests audio, image, and video files and answers questions about them using a local LLM. No cloud dependencies — everything runs on your machine.

## Stack

- Flask, ChromaDB, Ollama (Llama3), Whisper, EasyOCR, Moondream, OpenCV

## Prerequisites

- Python 3.11+
- [Ollama](https://ollama.com) installed and running
- [ffmpeg](https://ffmpeg.org) installed

```bash
ollama pull llama3
ollama pull moondream
```

## Setup

```bash
git clone https://github.com/rwhiteAI/multimodal-rag-api
cd multimodal-rag-api
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

## Endpoints

**POST /ingest** — Upload a file (`multipart/form-data`, key: `file`)
Supports `.mp3`, `.wav`, `.jpg`, `.png`, `.mp4`, `.mov`

**POST /query** — Ask a question (`application/json`)
```json
{
    "question": "what was discussed?",
    "media_type": "audio"
}
```
`media_type` is optional. Omit it to search all collections.

## Limitations

- Video processing is slow on CPU
- No text chunking yet — long content stored as one chunk
- No reranking

## Planned Improvements

- Text chunking for better retrieval accuracy
- Reranking with Flashrank
- PDF and document ingestion
- Async video processing