---
title: Smart Summarizer
emoji: 📝
colorFrom: blue
colorTo: green
sdk: docker
python_version: "3.13"
app_file: app.py
pinned: false
---

# Smart Summarizer

An AI-powered text summarizer with a FastAPI streaming backend and Gradio UI. Built as Project 1 of a Gen AI learning roadmap.

## Features

- FastAPI backend with `/summarize` endpoint
- Streaming responses via SSE (Server-Sent Events) — text appears token by token
- Gradio UI connected to the FastAPI backend
- Powered by Groq API (LLaMA 3.1)
- Dockerized with supervisord managing both processes

## Stack

- `fastapi` — async backend
- `groq` — LLM API (LLaMA 3.1 8B)
- `gradio` — UI
- `uvicorn` — ASGI server
- `supervisord` — process manager inside Docker
- `uv` — dependency management

## Project Structure

```
smart-summarizer/
├── main.py              # FastAPI backend with streaming endpoint
├── app.py               # Gradio UI
├── Dockerfile           # Docker build config
├── supervisord.conf     # Runs FastAPI + Gradio as two processes
├── requirements.txt     # Generated via uv export
└── .env                 # GROQ_API_KEY (not committed)
```

## Running Locally

**Without Docker:**

```bash
# Terminal 1 — start FastAPI
uv run uvicorn main:app --reload

# Terminal 2 — start Gradio UI
uv run app.py
```

Open `http://localhost:7860`

**With Docker:**

```bash
docker build -t smart-summarizer .
docker run -p 7860:7860 -e GROQ_API_KEY=your_key_here smart-summarizer
```

Open `http://localhost:7860`

## Environment Variables

| Variable | Description |
|----------|-------------|
| `GROQ_API_KEY` | Your Groq API key |

## API

### POST `/summarize`

**Request:**
```json
{ "text": "Your text to summarize..." }
```

**Response:** SSE stream — each event contains a text chunk.
```
data: Here
data:  is
data:  the summary...
```
