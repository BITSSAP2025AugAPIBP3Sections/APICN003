# Submission — APICN003

- Team ID: APICN003
- Members: Bhoomika Rajashekhar (2023sl70027), Prathvi S (2023sl70028)
- App entry point: `python src/app.py`
- Default provider: SLM (Ollama + llama3.1:8b)
- STT engine: Groq Whisper API (whisper-large-v3-turbo) with faster-whisper local fallback
- TTS engine: edge-tts (Microsoft Neural Voice en-IN-NeerjaNeural) with sentence-chunked streaming

## External data used
- None beyond the assignment corpus

## AI coding assistant disclosure
- Claude Code used for: upgrading TF-IDF to FAISS vector search, implementing sentence-transformers embeddings, project structure setup, code documentation, and test results formatting

## One-line claim to fame
- Semantic vector search with FAISS + sentence-transformers for superior retrieval accuracy over baseline TF-IDF
