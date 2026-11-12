# Architecture — APICN003

## Overview

APICN003 implements a RAG-based Income Tax chatbot supporting all four interaction modes (TITO/TIVO/VITO/VIVO) with semantic vector search replacing the baseline TF-IDF approach.

## Core Components

**Ingestion Pipeline** (`src/rag/ingest.py`): Extracts text from Income Tax PDFs using PyMuPDF, chunks documents with configurable size (900 chars) and overlap (150 chars), and stores chunks with metadata (document name, page number) in JSON format.

**Semantic Retriever** (`src/rag/retriever.py`): Uses sentence-transformers (all-MiniLM-L6-v2) to encode chunks into 384-dimensional embeddings. FAISS IndexFlatIP provides fast cosine similarity search over normalized vectors. On first run, builds and persists the index; subsequent runs load from disk for instant startup.

**LLM Provider Switch** (`src/rag/llm.py`): Unified interface supporting five providers via environment variables: local SLM (Ollama), Groq, OpenAI, Anthropic, OpenRouter. All providers use OpenAI-compatible APIs except Anthropic (native Messages API). System prompt constrains answers to retrieved context and enforces source citation.

**Speech-to-Text** (`src/speech/stt.py`): Defaults to faster-whisper (base model) running locally with press-to-talk recording. Cloud fallback to Groq/OpenAI Whisper API via environment variable.

**Text-to-Speech** (`src/speech/tts.py`): Defaults to pyttsx3 for local synthesis. Sentence-chunked streaming reduces latency by speaking the first two sentences while generating the rest.

## Mode Pipelines

- **TITO**: question → retriever.search(top_k=5) → build context → llm.chat → display answer + sources
- **TIVO**: TITO pipeline + tts.speak (sentence-chunked)
- **VITO**: stt.record_to_wav → stt.transcribe → TITO pipeline
- **VIVO**: VITO → TIVO (full voice loop)

## Key Improvements Over Baseline

1. **Semantic search**: FAISS + sentence-transformers replaces TF-IDF, capturing meaning beyond keyword matching
2. **Fast retrieval**: Normalized vectors + inner product = efficient cosine similarity at scale
3. **Persistent index**: Pre-built FAISS index loads in <1s vs rebuilding TF-IDF postings every run
4. **Streaming TTS**: Sentence-chunked playback starts speaking while generation continues

## Data Flow

```
PDFs → ingest → chunks.json + FAISS index
Query → encode → FAISS search → top-k chunks → format context → LLM → answer
Voice: microphone → WAV → faster-whisper → text query (then same as above)
Voice out: answer text → sentence chunker → pyttsx3 streaming
```

## Trade-offs

- **Vector embeddings**: Slower ingestion (~2min for full corpus) but far better retrieval quality
- **Model size**: all-MiniLM-L6-v2 is lightweight (80MB) but still outperforms TF-IDF
- **Local-first**: Faster-whisper and pyttsx3 run offline; cloud providers available via .env

Word count: ~380
