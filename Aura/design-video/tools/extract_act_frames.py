#!/usr/bin/env python3
"""Extract review stills from Manim partial_movie_files.

After ``manim -ql scenes/sceneN_actM.py SceneNActM``, run this to get PNGs
for agent/human layout QA (see MANIM-STANDARDS.md checklist).

Usage (repo root):
  python Aura/design-video/tools/extract_act_frames.py --scene scene6_act1
  python Aura/design-video/tools/extract_act_frames.py --scene scene6_act1 --quality 2160p60
  python Aura/design-video/tools/extract_act_frames.py --scene scene6_act1 --pick last
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
MEDIA = REPO / "Aura" / "design-video" / "aura_manim" / "media" / "videos"
OUT_BASE = REPO / "Aura" / "design-video" / "vo" / "review_frames"


def scene_to_class(scene: str) -> str:
    """scene6_act1 → Scene6Act1"""
    parts = scene.replace("scene", "").split("_act")
    if len(parts) != 2:
        raise ValueError(f"Expected sceneN_actM, got {scene!r}")
    return f"Scene{parts[0]}Act{parts[1]}"


def find_partial_dir(scene: str, quality: str, class_name: str) -> Path:
    base = MEDIA / scene / quality / "partial_movie_files"
    if not base.exists():
        raise FileNotFoundError(f"No partial_movie_files at {base} — render with manim -ql first")
    direct = base / class_name
    if direct.is_dir():
        return direct
    subs = [p for p in base.iterdir() if p.is_dir()]
    if len(subs) == 1:
        return subs[0]
    if class_name in {p.name for p in subs}:
        return direct
    raise FileNotFoundError(
        f"Could not find partial dir for {class_name} under {base}. "
        f"Found: {[p.name for p in subs]}"
    )


def video_duration_seconds(path: Path) -> float:
    result = subprocess.run(
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
        capture_output=True,
        text=True,
        check=True,
    )
    return float(result.stdout.strip())


def extract_last_frame(video: Path, out_png: Path) -> None:
    out_png.parent.mkdir(parents=True, exist_ok=True)
    dur = video_duration_seconds(video)
    # EOF seek fails on sub-second Manim partials — use mid-frame for short clips.
    seek = max(0.0, dur * 0.5) if dur < 2.0 else max(0.0, dur - 0.1)
    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-loglevel",
            "error",
            "-ss",
            f"{seek:.3f}",
            "-i",
            str(video),
            "-frames:v",
            "1",
            "-update",
            "1",
            str(out_png),
        ],
        check=True,
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Extract layout review frames from Manim partials")
    parser.add_argument("--scene", required=True, help="e.g. scene6_act1")
    parser.add_argument("--quality", default="480p15", help="480p15 or 2160p60")
    parser.add_argument(
        "--pick",
        choices=("last", "all"),
        default="last",
        help="last frame per partial (default) or all partials",
    )
    parser.add_argument("--class-name", default=None, help="Override Scene class folder name")
    args = parser.parse_args()

    class_name = args.class_name or scene_to_class(args.scene)
    partial_dir = find_partial_dir(args.scene, args.quality, class_name)
    partials = sorted(partial_dir.glob("*.mp4"))
    if not partials:
        print(f"No partial MP4s in {partial_dir}", file=sys.stderr)
        sys.exit(1)

    out_dir = OUT_BASE / args.scene / args.quality
    out_dir.mkdir(parents=True, exist_ok=True)

    for i, mp4 in enumerate(partials):
        name = mp4.stem
        out_png = out_dir / f"{i:03d}_{name}.png"
        extract_last_frame(mp4, out_png)
        print(out_png.relative_to(REPO))

    print(f"\n{len(partials)} frame(s) → {out_dir.relative_to(REPO)}")
    print("Check against MANIM-STANDARDS.md § Frame checklist before user review.")


if __name__ == "__main__":
    main()
