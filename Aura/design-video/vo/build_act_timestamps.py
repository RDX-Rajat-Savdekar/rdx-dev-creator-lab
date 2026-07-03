#!/usr/bin/env python3
"""Print act timeline table from 2160p60 per-act Manim renders.

Usage (repo root):
  python Aura/design-video/vo/build_act_timestamps.py --chapter 0
  python Aura/design-video/vo/build_act_timestamps.py --chapter 0 --markdown
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
MEDIA = REPO / "Aura" / "design-video" / "aura_manim" / "media" / "videos"


def probe_duration(path: Path) -> float:
    out = subprocess.check_output(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "csv=p=0",
            str(path),
        ],
        text=True,
    ).strip()
    return float(out)


def fmt_ts(seconds: float) -> str:
    m = int(seconds // 60)
    s = seconds % 60
    return f"{m}:{s:04.1f}" if m else f"0:{s:04.1f}"


def find_act_mp4(chapter: int, act: int) -> Path | None:
    # Chapter 0 uses scene0_actN / Scene0ActN naming.
    folder = MEDIA / f"scene{chapter}_act{act}" / "2160p60"
    candidate = folder / f"Scene{chapter}Act{act}.mp4"
    if candidate.exists():
        return candidate
    # Fallback: Scene0Act1 style for chapter 0 only
    if chapter == 0:
        alt = folder / f"Scene0Act{act}.mp4"
        if alt.exists():
            return alt
    return None


def collect(chapter: int, max_acts: int = 12) -> list[tuple[int, float, Path]]:
    rows: list[tuple[int, float, Path]] = []
    for act in range(1, max_acts + 1):
        path = find_act_mp4(chapter, act)
        if path is None:
            if act == 1:
                print(f"No renders under {MEDIA}/scene{chapter}_act1/2160p60/", file=sys.stderr)
                sys.exit(1)
            break
        rows.append((act, probe_duration(path), path))
    return rows


def main() -> None:
    parser = argparse.ArgumentParser(description="Act timestamps from 2160p60 renders")
    parser.add_argument("--chapter", type=int, required=True, help="Chapter number (e.g. 0)")
    parser.add_argument("--markdown", action="store_true", help="Markdown table for vo/sceneN.md")
    args = parser.parse_args()

    rows = collect(args.chapter)
    t = 0.0
    lines: list[str] = []

    if args.markdown:
        lines.append("| Act | Start | End | Dur | Render |")
        lines.append("|-----|-------|-----|-----|--------|")

    for act, dur, path in rows:
        start, end = t, t + dur
        rel = path.relative_to(REPO)
        if args.markdown:
            lines.append(
                f"| {act} | {fmt_ts(start)} | {fmt_ts(end)} | {dur:.1f}s | `{rel}` |"
            )
        else:
            lines.append(
                f"act{act}: {fmt_ts(start)} → {fmt_ts(end)}  ({dur:.1f}s)  {rel}"
            )
        t = end

    lines.append("")
    lines.append(f"total: {fmt_ts(t)}  ({t:.1f}s)")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
