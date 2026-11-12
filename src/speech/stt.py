import os
import queue
import tempfile
import threading
import time

from dotenv import load_dotenv

load_dotenv()

_ever_initialized = False


def record_to_wav(seconds: float | None = None) -> str | None:
    """Press-Enter-to-start, press-Enter-to-stop recording (or fixed `seconds`)."""
    try:
        import sounddevice as sd
        import soundfile as sf
    except ImportError:
        print("Voice modes need: pip install sounddevice soundfile faster-whisper")
        return None
    sr = 16_000
    audio_q: queue.Queue = queue.Queue()

    def callback(indata, frames, t, status):
        audio_q.put(indata.copy())

    def wait_stop():
        input("  REC> press Enter to stop...")
        nonlocal running
        running = False

    running = True
    print("  REC> press Enter to start speaking...")
    with sd.InputStream(samplerate=sr, channels=1, dtype="int16", callback=callback):
        input()
        stopper = threading.Thread(target=wait_stop)
        stopper.start()
        if seconds:
            time.sleep(seconds)
            running = False
        frames = []
        while running:
            frames.append(audio_q.get())
    path = tempfile.mktemp(suffix=".wav")
    sf.write(path, np_stack(frames), sr)
    return path


def np_stack(frames):
    import numpy as np

    return np.concatenate(frames, axis=0) if frames else np.zeros((0, 1), dtype="int16")


def transcribe(wav_path: str | None) -> str | None:
    if wav_path is None:
        return None

    provider = os.getenv("STT_PROVIDER", "groq")

    # Cloud STT via Groq or OpenAI Whisper API
    if provider in ("groq", "openai"):
        import requests

        url = (
            "https://api.groq.com/openai/v1/audio/transcriptions"
            if provider == "groq"
            else "https://api.openai.com/v1/audio/transcriptions"
        )
        model = "whisper-large-v3-turbo" if provider == "groq" else "whisper-1"
        api_key = os.getenv("GROQ_API_KEY" if provider == "groq" else "OPENAI_API_KEY", "")
        t0 = time.time()
        resp = requests.post(
            url,
            headers={"Authorization": f"Bearer {api_key}"},
            files={"file": ("audio.wav", open(wav_path, "rb"), "audio/wav")},
            data={"model": model},
            timeout=60,
        )
        resp.raise_for_status()
        text = resp.json()["text"]
        print(f"  [stt groq {time.time()-t0:.1f}s] {text}")
        return text

    # Local faster-whisper fallback
    try:
        from faster_whisper import WhisperModel
        global _ever_initialized
        t0 = time.time()
        model = WhisperModel(os.getenv("STT_MODEL", "base"), device="auto", compute_type="auto")
        first = "" if _ever_initialized else f" (load {time.time()-t0:.1f}s)"
        _ever_initialized = True
        segments, _info = model.transcribe(wav_path)
        text = " ".join(s.text for s in segments)
        print(f"  [stt local{first}] {text}")
        return text
    except Exception as e:
        print(f"  [stt local failed: {e}] — falling back to groq")
        os.environ["STT_PROVIDER"] = "groq"
        return transcribe(wav_path)
