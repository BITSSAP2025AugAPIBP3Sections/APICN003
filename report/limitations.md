# Limitations — APICN003

## Known Weaknesses

**Context Window**: Fixed chunk size (900 chars) may split complex calculations or tables mid-content, breaking continuity for multi-step tax computations.

**No Reranking**: Direct top-k retrieval without reranking can surface tangentially relevant chunks. A cross-encoder reranking stage would improve precision.

**Single-Turn Context**: Multi-turn conversations append full history to each LLM call, but retrieval doesn't use conversation context—follow-up questions like "what about the old regime?" may retrieve poorly without the original question's context.

**Embedding Model**: all-MiniLM-L6-v2 is fast but trained on general text, not legal/tax documents. Domain-specific fine-tuning or a larger model (e.g., BGE-large) would improve accuracy.

**Year Ambiguity**: Retrieval doesn't weight recent budgets higher. Queries about "current rates" may mix FY 2022-23 and FY 2024-25 chunks equally; temporal scoping is manual.

**STT Accuracy**: Press-to-talk recording captures background noise. Voice Activity Detection (VAD) would clip silence and improve transcription quality.

**TTS Latency**: Sentence-chunked streaming helps but pyttsx3 is synchronous—each chunk blocks until playback finishes. Async TTS (Piper with streaming) would reduce perceived latency further.

**No Guardrails**: System prompt instructs "answer only from context" but no post-processing verifies citation accuracy or detects hallucinations.

**Scalability**: FAISS IndexFlatIP is exhaustive search (O(n))—works for ~2000 chunks but would need HNSW/IVF indexing at 100k+ scale.

Word count: ~230
