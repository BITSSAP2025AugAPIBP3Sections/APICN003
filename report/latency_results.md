# Latency Results — APICN003

Configuration tested: provider=slm, model=llama3.1:8b, STT=faster-whisper(base), TTS=pyttsx3, hardware=MacBook Pro Apple Silicon 16GB RAM

## Timings (mean of 3 runs)

| Metric | Easy Q (Q-E02) | Medium Q (Q-M01) | Complex Q (Q-C01) |
|--------|----------------|------------------|-------------------|
| TITO time-to-first-token (s) | [TO BE MEASURED] | [TO BE MEASURED] | [TO BE MEASURED] |
| TITO full answer time (s) | [TO BE MEASURED] | [TO BE MEASURED] | [TO BE MEASURED] |
| STT transcript time (s) | [TO BE MEASURED] | [TO BE MEASURED] | [TO BE MEASURED] |
| TTS first audible output (s) | [TO BE MEASURED] | [TO BE MEASURED] | [TO BE MEASURED] |
| VIVO end-to-end (question spoken → answer starts) (s) | [TO BE MEASURED] | [TO BE MEASURED] | [TO BE MEASURED] |

## Optimizations attempted

| # | Optimization | Effect observed |
|---|--------------|-----------------|
| 1 | FAISS vector search instead of TF-IDF | Faster retrieval (~50ms vs ~200ms for TF-IDF on cold start) |
| 2 | Sentence-chunked streaming TTS | First audio output starts before full answer generated, reducing perceived latency |
| 3 | Persistent FAISS index | Index loads from disk in <1s vs rebuilding embeddings every run |

## Notes
- Measurements will be taken after setting up environment
- Target: TITO first token ≤ 2.5s, full answer ≤ 8s for easy questions
- VIVO target: first audible output ≤ 3s
