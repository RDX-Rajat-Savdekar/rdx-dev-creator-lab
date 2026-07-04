"""Export PNG frames from a rendered intro MP4."""

from __future__ import annotations

import argparse
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "output"


def main() -> None:
    parser = argparse.ArgumentParser(description="Extract intro frames for visual QA")
    parser.add_argument(
        "--video",
        type=Path,
        default=OUTPUT / "channel_intro_1080p60.mp4",
        help="Input MP4",
    )
    parser.add_argument(
        "--times",
        nargs="+",
        default=["3.5", "6.0", "8.5", "9.5"],
        help="Timestamps in seconds, or 'logo' for last frame",
    )
    args = parser.parse_args()

    if not args.video.is_file():
        raise SystemExit(f"Missing video: {args.video}")

    frames = OUTPUT / "frames"
    frames.mkdir(parents=True, exist_ok=True)

    for t in args.times:
        if t == "logo":
            out = frames / "frame_logo.png"
            cmd = [
                "ffmpeg",
                "-y",
                "-sseof",
                "-0.5",
                "-i",
                str(args.video),
                "-vframes",
                "1",
                str(out),
            ]
        else:
            out = frames / f"frame_{t}s.png"
            cmd = [
                "ffmpeg",
                "-y",
                "-ss",
                t,
                "-i",
                str(args.video),
                "-vframes",
                "1",
                str(out),
            ]
        subprocess.run(cmd, check=True, capture_output=True)
        print(out.relative_to(ROOT))


if __name__ == "__main__":
    main()
