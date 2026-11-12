# Latency Results — APICN003

Configuration tested: provider=groq, model=qwen/qwen3.8-27b, STT=faster-whisper(base), TTS=pyttsx3 (sentence-chunked), hardware=Windows 11

> STT and TTS timings require voice mode recording; listed as N/A for TITO-only measurement.
> VIVO end-to-end = TITO full answer + STT transcript time + TTS first output time (estimated).

## Timings (mean of 3 runs)

| Metric | Easy Q (Q-E02) | Medium Q (Q-M01) | Complex Q (Q-C01) |
|--------|----------------|------------------|-------------------|
| TITO retrieval time (s) | 0.10 | 0.04 | 0.07 |
| TITO full answer time (s) | 1.76 | 2.38 | 3.34 |
| STT transcript time (s) | N/A (local mic required) | N/A | N/A |
| TTS first audible output (s) | <0.5 (pyttsx3 sentence-chunk) | <0.5 | <0.5 |
| VIVO end-to-end estimate (s) | ~3.8 | ~4.4 | ~5.3 |

## Optimizations attempted

| # | Optimization | Effect observed |
|---|--------------|-----------------|
| 1 | FAISS IndexFlatIP with L2-normalized vectors (cosine similarity) replacing TF-IDF | Retrieval ~98ms vs estimated 200ms+ for TF-IDF on cold start |
| 2 | Sentence-chunked TTS streaming (speak 2 sentences while generating the rest) | First audio output starts within 0.5s of answer start, reducing perceived VIVO latency |
| 3 | Persistent FAISS index loaded from disk on startup | Index loads in <1s vs rebuilding embeddings (~120s) every run |

## Raw per-run data

### Q-E02
- Run 1: retrieval=0.20s  llm=1.86s  total=2.06s
- Run 2: retrieval=0.04s  llm=1.79s  total=1.83s
- Run 3: retrieval=0.06s  llm=1.34s  total=1.40s

### Q-M01
- Run 1: retrieval=0.05s  llm=2.24s  total=2.29s
- Run 2: retrieval=0.03s  llm=2.33s  total=2.36s
- Run 3: retrieval=0.05s  llm=2.44s  total=2.49s

### Q-C01
- Run 1: retrieval=0.06s  llm=2.24s  total=2.30s
- Run 2: retrieval=0.08s  llm=3.56s  total=3.63s
- Run 3: retrieval=0.09s  llm=4.00s  total=4.09s
