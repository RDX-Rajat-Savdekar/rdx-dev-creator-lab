#!/usr/bin/env python3
"""Mix background music under the Aura 60s assembly (no VO — keep music subtle).

Usage:
  .venv/bin/python Aura/manim/add_music.py --music Aura/music/your-track.mp3
  .venv/bin/python Aura/manim/add_music.py --music ~/Downloads/ambient.mp3 --volume 0.10

Input default:  Aura/output/aura-60s-rough-assembly.mp4
Output default: Aura/output/aura-60s-with-music.mp4
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
DEFAULT_IN = REPO / "Aura" / "output" / "aura-60s-rough-assembly.mp4"
DEFAULT_OUT = REPO / "Aura" / "output" / "aura-60s-with-music.mp4"


def probe_duration(path: Path) -> float:
    out = subprocess.check_output(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "default=noprint_wrappers=1:nokey=1",
            str(path),
        ],
        text=True,
    )
    return float(out.strip())


def mix_music(
    video: Path,
    music: Path,
    output: Path,
    *,
    volume: float,
    fade_in: float,
    fade_out: float,
) -> None:
    duration = probe_duration(video)
    fade_out_start = max(0.0, duration - fade_out)
    # Loop/trim music to video length; gentle fades so it doesn't feel abrupt.
    filt = (
        f"[1:a]aloop=loop=-1:size=2e+09,atrim=0:{duration},"
        f"volume={volume},"
        f"afade=t=in:st=0:d={fade_in},"
        f"afade=t=out:st={fade_out_start}:d={fade_out}[bg]"
    )
    cmd = [
        "ffmpeg",
        "-y",
        "-i",
        str(video),
        "-i",
        str(music),
        "-filter_complex",
        filt,
        "-map",
        "0:v",
        "-map",
        "[bg]",
        "-c:v",
        "copy",
        "-c:a",
        "aac",
        "-b:a",
        "192k",
        "-shortest",
        str(output),
    ]
    print("→", " ".join(cmd))
    subprocess.run(cmd, check=True)


def main() -> None:
    parser = argparse.ArgumentParser(description="Add background music to Aura 60s")
    parser.add_argument("--music", "-m", type=Path, required=True, help="Path to MP3/WAV/M4A")
    parser.add_argument("--input", "-i", type=Path, default=DEFAULT_IN, help="Muted assembly MP4")
    parser.add_argument("--output", "-o", type=Path, default=DEFAULT_OUT, help="Output MP4")
    parser.add_argument(
        "--volume",
        "-v",
        type=float,
        default=0.11,
        help="Music gain 0–1 (default 0.11 ≈ -19 dB — subtle under text)",
    )
    parser.add_argument("--fade-in", type=float, default=0.8, help="Fade-in seconds")
    parser.add_argument("--fade-out", type=float, default=4.0, help="Fade-out seconds at end")
    args = parser.parse_args()

    if not args.input.is_file():
        sys.exit(f"Missing video: {args.input}\nRun build_60s.py first.")
    if not args.music.is_file():
        sys.exit(f"Missing music file: {args.music}")

    args.output.parent.mkdir(parents=True, exist_ok=True)
    mix_music(
        args.input,
        args.music,
        args.output,
        volume=args.volume,
        fade_in=args.fade_in,
        fade_out=args.fade_out,
    )
    dur = probe_duration(args.output)
    print(f"\nDone: {args.output.relative_to(REPO)} ({dur:.1f}s)")
    print("Tip: if music feels loud, retry with --volume 0.08")


if __name__ == "__main__":
    try:
        main()
    except subprocess.CalledProcessError as exc:
        sys.exit(exc.returncode)
