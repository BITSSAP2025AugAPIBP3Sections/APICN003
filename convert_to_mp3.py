"""Convert Xbox Game Bar recordings to MP3 and copy to demo/.

Usage:
    python convert_to_mp3.py

Put all your .mp4 recordings from Videos\\Captures\\ into a folder,
or just run this script — it will look in Videos\\Captures\\ automatically
and ask you to map each file to vivo_0 through vivo_7.
"""
import os
import shutil
from pathlib import Path

from moviepy import VideoFileClip

CAPTURES_DIR = Path.home() / "Videos" / "Screen Recordings"
DEMO_DIR = Path("demo")

VIVO_MAP = {
    "0": "vivo_0.mp3 (free choice)",
    "1": "vivo_1.mp3 (Q-E01: slab rates new regime)",
    "2": "vivo_2.mp3 (Q-E02: 80C deduction)",
    "3": "vivo_3.mp3 (Q-E05: LTCG rate)",
    "4": "vivo_4.mp3 (Q-M01: salary tax computation)",
    "5": "vivo_5.mp3 (Q-M04: VDA taxation)",
    "6": "vivo_6.mp3 (Q-C01: Mr A full computation)",
    "7": "vivo_7.mp3 (Q-C03: residential status)",
}


def convert(src: Path, dest: Path) -> None:
    print(f"  Converting {src.name} -> {dest.name} ...")
    clip = VideoFileClip(str(src))
    clip.audio.write_audiofile(str(dest), fps=44100, logger=None)
    clip.close()
    print(f"  Saved: {dest}")


def main():
    DEMO_DIR.mkdir(exist_ok=True)

    # Find all mp4 files in Captures sorted by creation time
    videos = sorted(CAPTURES_DIR.glob("*.mp4"), key=lambda p: p.stat().st_mtime)

    if not videos:
        print(f"No .mp4 files found in {CAPTURES_DIR}")
        print("Move your Xbox Game Bar recordings there and run again.")
        return

    print(f"Found {len(videos)} recording(s) in {CAPTURES_DIR}:\n")
    for i, v in enumerate(videos):
        size_mb = v.stat().st_size / 1024 / 1024
        print(f"  [{i}] {v.name}  ({size_mb:.1f} MB)")

    print()
    print("Enter the index number for each vivo file (or press Enter to skip):\n")

    for key, label in VIVO_MAP.items():
        val = input(f"  Which recording is {label}? Enter index (0-{len(videos)-1}) or skip: ").strip()
        if not val:
            print(f"  Skipped {label}")
            continue
        try:
            idx = int(val)
            src = videos[idx]
            dest = DEMO_DIR / f"vivo_{key}.mp3"
            convert(src, dest)
        except (ValueError, IndexError):
            print(f"  Invalid index, skipping.")

    print("\nDone! Check the demo/ folder:")
    for f in sorted(DEMO_DIR.glob("vivo_*.mp3")):
        size_kb = f.stat().st_size / 1024
        print(f"  {f.name}  ({size_kb:.0f} KB)")


if __name__ == "__main__":
    main()
