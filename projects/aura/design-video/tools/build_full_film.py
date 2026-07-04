#!/usr/bin/env python3
"""Concat all chapter VO exports into one film (each chapter already has 2s banner).

Usage (repo root):
  python Aura/design-video/tools/mux_chapter_vo.py --all --banner
  python Aura/design-video/tools/build_full_film.py
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
sys.path.insert(0, str(TOOLS))
from video_catalog import probe_duration  # noqa: E402

REPO = TOOLS.parents[2]
DESIGN = REPO / "Aura" / "design-video"
OUTPUT = DESIGN / "output"


def chapter_vo_path(ch: int) -> Path | None:
    p = OUTPUT / f"scene{ch}_chapter{ch}_2160p60_vo.mp4"
    return p if p.is_file() else None


def main() -> None:
    parser = argparse.ArgumentParser(description="Concat chapter _vo MP4s → full film")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    paths: list[Path] = []
    for ch in range(10):
        p = chapter_vo_path(ch)
        if p:
            paths.append(p)

    if not paths:
        print("No sceneN_chapterN_2160p60_vo.mp4 files — run mux_chapter_vo.py --all --banner", file=sys.stderr)
        sys.exit(1)

    out = OUTPUT / "aura_design_video_2160p60_vo.mp4"
    if args.dry_run:
        print(f"Would concat {len(paths)} chapter(s) → {out.name}")
        for p in paths:
            print(f"  {p.name} ({probe_duration(p):.1f}s)")
        return

    list_path = OUTPUT / "full_film_concat.txt"
    list_path.write_text("\n".join(f"file '{p}'" for p in paths) + "\n")
    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-f",
            "concat",
            "-safe",
            "0",
            "-i",
            str(list_path),
            "-c",
            "copy",
            str(out),
        ],
        check=True,
        capture_output=True,
    )
    dur = probe_duration(out)
    print(f"{out.relative_to(REPO)} ({dur:.1f}s) · {len(paths)} chapters")


if __name__ == "__main__":
    main()
