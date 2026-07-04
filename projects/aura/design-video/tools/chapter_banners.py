#!/usr/bin/env python3
"""Generate 2s chapter title cards (2160p60) for VO chapter exports.

Requires: pip install pillow (included in Aura/design-video/.venv)

Usage (repo root):
  Aura/design-video/.venv/bin/python Aura/design-video/tools/chapter_banners.py --all
  Aura/design-video/.venv/bin/python Aura/design-video/tools/chapter_banners.py --chapter 2
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
import tempfile
from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    print("Install Pillow: Aura/design-video/.venv/bin/pip install pillow", file=sys.stderr)
    sys.exit(1)

TOOLS = Path(__file__).resolve().parent
REPO = TOOLS.parents[2]
DESIGN = REPO / "Aura" / "design-video"
VO_DIR = DESIGN / "vo"
BANNER_DIR = DESIGN / "aura_manim" / "media" / "banners"

BANNER_SEC = 2.0
WIDTH = 3840
HEIGHT = 2160
FPS = 60
BG = "#0a0a0f"
MUTED = "#98989d"
ACCENT = "#5ac8fa"
FONT = "/System/Library/Fonts/Supplemental/Arial.ttf"

YOUTUBE_CH_RE = re.compile(r"\*\*YouTube chapter:\*\*\s*\*([^*]+)\*")


def chapter_titles() -> dict[int, str]:
    titles: dict[int, str] = {}
    for path in sorted(VO_DIR.glob("scene*.md")):
        stem = path.stem
        if not stem[5:].isdigit():
            continue
        ch = int(stem[5:])
        text = path.read_text(encoding="utf-8")
        m = YOUTUBE_CH_RE.search(text)
        titles[ch] = m.group(1).strip() if m else f"Chapter {ch}"
    return titles


def _text_size(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.FreeTypeFont) -> tuple[int, int]:
    box = draw.textbbox((0, 0), text, font=font)
    return box[2] - box[0], box[3] - box[1]


def render_banner_png(chapter: int, png: Path, *, title: str | None = None) -> None:
    label = title or chapter_titles().get(chapter, f"Chapter {chapter}")
    img = Image.new("RGB", (WIDTH, HEIGHT), BG)
    draw = ImageDraw.Draw(img)
    font_sub = ImageFont.truetype(FONT, 72)
    font_main = ImageFont.truetype(FONT, 108)
    sub = f"Chapter {chapter}"
    w1, h1 = _text_size(draw, sub, font_sub)
    w2, h2 = _text_size(draw, label, font_main)
    gap = 28
    total_h = h1 + gap + h2
    y0 = (HEIGHT - total_h) // 2
    draw.text(((WIDTH - w1) // 2, y0), sub, font=font_sub, fill=MUTED)
    draw.text(((WIDTH - w2) // 2, y0 + h1 + gap), label, font=font_main, fill=ACCENT)
    png.parent.mkdir(parents=True, exist_ok=True)
    img.save(png)


def render_banner(chapter: int, dst: Path, *, title: str | None = None) -> Path:
    dst.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        png = Path(tmp) / "frame.png"
        render_banner_png(chapter, png, title=title)
        subprocess.run(
            [
                "ffmpeg",
                "-y",
                "-loop",
                "1",
                "-i",
                str(png),
                "-f",
                "lavfi",
                "-i",
                "anullsrc=r=48000:cl=mono",
                "-t",
                str(BANNER_SEC),
                "-r",
                str(FPS),
                "-c:v",
                "libx264",
                "-preset",
                "fast",
                "-crf",
                "18",
                "-pix_fmt",
                "yuv420p",
                "-c:a",
                "aac",
                "-b:a",
                "128k",
                "-shortest",
                "-movflags",
                "+faststart",
                str(dst),
            ],
            check=True,
            capture_output=True,
        )
    return dst


def banner_path(chapter: int, *, refresh: bool = False) -> Path:
    dst = BANNER_DIR / f"ch{chapter}_2160p60.mp4"
    if refresh or not dst.is_file():
        render_banner(chapter, dst)
    return dst


def prepend_banner(body: Path, chapter: int, out: Path, *, refresh_banner: bool = False) -> None:
    """Concat 2s title card + chapter body."""
    banner = banner_path(chapter, refresh=refresh_banner)
    with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False) as f:
        f.write(f"file '{banner}'\nfile '{body}'\n")
        list_path = Path(f.name)
    out.parent.mkdir(parents=True, exist_ok=True)
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
            "-c:v",
            "libx264",
            "-preset",
            "fast",
            "-crf",
            "18",
            "-pix_fmt",
            "yuv420p",
            "-c:a",
            "aac",
            "-b:a",
            "192k",
            "-movflags",
            "+faststart",
            str(out),
        ],
        check=True,
        capture_output=True,
    )
    list_path.unlink(missing_ok=True)


def main() -> None:
    parser = argparse.ArgumentParser(description="Render 2s chapter title banners")
    parser.add_argument("--chapter", type=int, default=None)
    parser.add_argument("--all", action="store_true")
    parser.add_argument("--refresh", action="store_true")
    args = parser.parse_args()

    chapters = list(chapter_titles().keys()) if args.all else ([args.chapter] if args.chapter is not None else [])
    if not chapters:
        parser.print_help()
        sys.exit(1)

    titles = chapter_titles()
    for ch in sorted(chapters):
        dst = banner_path(ch, refresh=args.refresh)
        print(f"ch{ch}: {dst.relative_to(REPO)} · “{titles.get(ch, '')}”")


if __name__ == "__main__":
    main()
