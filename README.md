# APICN003 — RAG VoiceBot

Advanced RAG-based Income Tax chatbot with FAISS vector search, streaming TTS, and optimized latency for all four modes (TITO/TIVO/VITO/VIVO).

## How to run

1. `python -m venv .venv` → activate
2. `pip install -r requirements.txt`
3. `cp .env.example .env` → set `LLM_PROVIDER` (+ model/key). For SLM: `ollama pull llama3.1:8b` then `ollama serve`.
4. Copy the corpus PDFs from the assignment repo's `data/` folder into `data/` (e.g. if you cloned the assignment repo: `cp ../../data/*.pdf data/`; otherwise download them) — PDFs are git-ignored, only `src/rag/ingest.py` builds the index.
5. `python src/rag/ingest.py` → builds `index/chunks.json`.
6. `python src/app.py --question "What is the 80C limit?"` (one-shot) or `python src/app.py --mode tito` (chat loop). TITO requires nothing beyond the LLM; voice modes additionally need `pip install faster-whisper sounddevice soundfile` and a microphone.

## Modes

- **TITO** `--mode tito` — chat loop with sources.
- **TIVO** `--mode tivo` — same + pyttsx3/piper speaks the answer.
- **VITO** `--mode vito` — press-Enter press-Enter recording → faster-whisper → RAG → text.
- **VIVO** `--mode vivo` — both of the above chained.

## Team
| Member | Email |
|--------|-------|
| Bhoomika Rajashekhar | 2023sl70027 |
| Swetha S Sankar | 2023sl70029 |

## Hardware used

- MacBook Pro (Darwin 27.0.0)
- CPU: Apple Silicon
- RAM: 16GB
- FAISS vector search + OpenAI-compatible endpoint
