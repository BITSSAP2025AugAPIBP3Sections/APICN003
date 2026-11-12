import os
import re
import subprocess

from dotenv import load_dotenv

load_dotenv()


def _speak_pyttsx3(text: str) -> None:
    import pyttsx3

    engine = pyttsx3.init()
    voice = os.getenv("TTS_VOICE")
    if voice:
        engine.setProperty("voice", voice)
    rate = int(os.getenv("TTS_RATE", 185))
    engine.setProperty("rate", rate)
    engine.say(text)
    engine.runAndWait()


def _speak_piper(text: str) -> None:
    """Stream to the piper CLI: piper --model <TTS_VOICE.wav> --output_file - | aplay."""
    proc = subprocess.Popen(
        ["piper", "--model", os.getenv("TTS_VOICE", "")],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
    )
    proc.communicate(text.encode())
    subprocess.run(
        # aplay on linux, ffplay as fallback
        ["aplay", "-"],
        input=proc.stdout,
        check=False,
    )


def _speak_edge(text: str) -> None:
    import asyncio
    import tempfile

    async def run():
        path = tempfile.mktemp(suffix=".mp3")
        await edge_tts.Communicate(text, os.getenv("TTS_VOICE", "en-IN-NeerjaNeural")).save(path)
        return path

    import edge_tts
    path = asyncio.run(run())
    # Play with pygame for blocking, in-process playback (no external player window)
    try:
        import pygame
        pygame.mixer.init()
        pygame.mixer.music.load(path)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
        pygame.mixer.quit()
    except ImportError:
        # Fallback: open with default Windows media player, then wait estimated duration
        import mutagen.mp3
        try:
            duration = mutagen.mp3.MP3(path).info.length
        except Exception:
            duration = len(text) / 15  # rough estimate: ~15 chars/sec
        subprocess.Popen(["start", "", path], shell=True)
        import time
        time.sleep(duration + 0.5)


_SENTENCE = re.compile(r"[^.!?]+\.[^.!?]*\.")


def _clean_for_speech(text: str) -> str:
    """Strip markdown formatting so TTS doesn't read symbols aloud."""
    import re
    text = re.sub(r"\*{1,3}([^*]+)\*{1,3}", r"\1", text)   # **bold** / *italic*
    text = re.sub(r"`{1,3}[^`]*`{1,3}", "", text)           # `code`
    text = re.sub(r"#{1,6}\s*", "", text)                    # ## headings
    text = re.sub(r"^\s*[-*+]\s+", "", text, flags=re.MULTILINE)  # bullet points
    text = re.sub(r"^\s*\d+\.\s+", "", text, flags=re.MULTILINE)  # numbered lists
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)    # [link](url)
    text = re.sub(r"₹", "rupees ", text)                     # ₹ symbol
    text = re.sub(r"\|[|\s\-:]+\|", "", text)                # table separators
    text = re.sub(r"\|", " ", text)                          # table pipes
    text = re.sub(r"\n{2,}", ". ", text)                     # paragraph breaks
    text = re.sub(r"\s{2,}", " ", text)                      # extra spaces
    return text.strip()


def speak(text: str, sentence_chunked: bool = True) -> None:
    """Speak the answer. Split long text into sentence pairs so TTS starts early."""
    text = _clean_for_speech(text)
    provider = os.getenv("TTS_PROVIDER", "pyttsx3")
    fn = {"pyttsx3": _speak_pyttsx3, "piper": _speak_piper, "edge": _speak_edge}[provider]
    if not sentence_chunked or len(text) < 200:
        fn(text)
        return
    parts = _SENTENCE.findall(text)
    tail = text[len("".join(parts)) :]
    parts = [p.strip() for p in parts if p.strip()]
    for i in range(0, len(parts), 2):
        fn(" ".join(parts[i : i + 2]) + (" " + tail if i + 2 >= len(parts) else ""))
