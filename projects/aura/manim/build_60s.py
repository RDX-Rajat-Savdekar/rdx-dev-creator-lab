#!/usr/bin/env python3
"""Render Manim text cards and assemble Aura 60s rough cut.

Usage (from repo root):
  uv run python Aura/manim/build_60s.py
  uv run python Aura/manim/build_60s.py --skip-render   # reuse existing Manim exports
  uv run python Aura/manim/build_60s.py --quality h     # 1080p-quality Manim (-qh)

Add background music after assembly:
  .venv/bin/python Aura/manim/add_music.py --music Aura/music/your-track.mp3
  See Aura/music/README.md for track recommendations and licensing.
"""

from __future__ import annotations

import argparse
import glob
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
MANIM_DIR = Path(__file__).resolve().parent
MANIM_BIN = REPO / ".venv" / "bin" / "manim"
CARDS = MANIM_DIR / "aura_cards.py"
CLIPS = REPO / "Aura" / "clips"
MEDIA = MANIM_DIR / "media"
OUT = REPO / "Aura" / "output"
BUILD = OUT / "build"

FULL_CARDS = ["HookCard", "ProblemCard", "PipelineCard", "ProofCard", "CTACard"]
OVERLAYS = [
    "ProductLowerThird",
    "SpeechLowerThird",
    "SoundLowerThird",
    "LocaleLowerThird",
]


def run(cmd: list[str], *, check: bool = True, cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    print("→", " ".join(cmd))
    return subprocess.run(cmd, check=check, text=True, cwd=cwd or REPO)


def render_manim(scene: str, *, quality: str, transparent: bool) -> None:
    q = {"l": "-ql", "m": "-qm", "h": "-qh"}[quality]
    cmd = [
        str(MANIM_BIN),
        q,
        "-r",
        "1280,720",
        "--frame_rate",
        "60",
        "--media_dir",
        str(MEDIA),
    ]
    if transparent:
        cmd.append("-t")
    cmd.extend([str(CARDS.name), scene])
    run(cmd, cwd=MANIM_DIR)


def find_render(scene: str, *, transparent: bool) -> Path:
    """Locate latest Manim export for a scene."""
    sub = "videos" if not transparent else "videos"
    pattern = str(MEDIA / sub / "aura_cards" / quality_dir_glob(scene) / f"{scene}.*")
    # Manim CE puts files in media/videos/aura_cards/<quality>/SceneName.ext
    roots = list(MEDIA.glob(f"videos/aura_cards/*/{scene}.*"))
    if not roots:
        roots = list(MEDIA.glob(f"**/{scene}.mp4")) + list(MEDIA.glob(f"**/{scene}.mov"))
    if not roots:
        raise FileNotFoundError(f"No render found for {scene} under {MEDIA}")
    return max(roots, key=lambda p: p.stat().st_mtime)


def quality_dir_glob(scene: str) -> str:
    return "*"


def ffmpeg_trim(src: Path, start: float, duration: float, dst: Path) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    run(
        [
            "ffmpeg",
            "-y",
            "-ss",
            str(start),
            "-i",
            str(src),
            "-t",
            str(duration),
            "-an",
            "-c:v",
            "libx264",
            "-crf",
            "18",
            "-preset",
            "fast",
            "-r",
            "60",
            "-pix_fmt",
            "yuv420p",
            str(dst),
        ]
    )


def ffmpeg_overlay(base: Path, overlay: Path, dst: Path) -> None:
    """Composite transparent overlay (mov/webm) or opaque mp4 on demo clip."""
    dst.parent.mkdir(parents=True, exist_ok=True)
    ext = overlay.suffix.lower()
    if ext in {".mov", ".webm"}:
        filt = "[1:v]scale=1280:720,format=yuva420p[ov];[0:v][ov]overlay=0:0:format=auto,format=yuv420p"
    else:
        filt = "[1:v]scale=1280:720,format=yuva420p,colorchannelmixer=aa=0.95[ov];[0:v][ov]overlay=0:0,format=yuv420p"
    run(
        [
            "ffmpeg",
            "-y",
            "-i",
            str(base),
            "-i",
            str(overlay),
            "-filter_complex",
            filt,
            "-an",
            "-c:v",
            "libx264",
            "-crf",
            "18",
            "-preset",
            "fast",
            "-r",
            "60",
            "-shortest",
            str(dst),
        ]
    )


def ffmpeg_concat(segments: list[Path], dst: Path) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    list_file = BUILD / "concat.txt"
    lines = [f"file '{p.resolve()}'" for p in segments]
    list_file.write_text("\n".join(lines) + "\n")
    run(
        [
            "ffmpeg",
            "-y",
            "-f",
            "concat",
            "-safe",
            "0",
            "-i",
            str(list_file),
            "-c:v",
            "libx264",
            "-crf",
            "18",
            "-preset",
            "fast",
            "-pix_fmt",
            "yuv420p",
            "-movflags",
            "+faststart",
            str(dst),
        ]
    )


def normalize_card(src: Path, dst: Path, duration: float) -> None:
    """Re-time full-screen Manim card to exact segment length."""
    dst.parent.mkdir(parents=True, exist_ok=True)
    run(
        [
            "ffmpeg",
            "-y",
            "-i",
            str(src),
            "-t",
            str(duration),
            "-an",
            "-vf",
            "scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2:color=0x0a0a0f,fps=60",
            "-c:v",
            "libx264",
            "-crf",
            "18",
            "-preset",
            "fast",
            "-pix_fmt",
            "yuv420p",
            str(dst),
        ]
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Build Aura 60s with Manim text + demo clips")
    parser.add_argument("--skip-render", action="store_true", help="Reuse existing Manim media/")
    parser.add_argument("--quality", choices=["l", "m", "h"], default="l", help="Manim quality flag")
    args = parser.parse_args()

    BUILD.mkdir(parents=True, exist_ok=True)
    OUT.mkdir(parents=True, exist_ok=True)

    if not args.skip_render:
        print("\n=== Rendering Manim full-screen cards ===")
        for scene in FULL_CARDS:
            render_manim(scene, quality=args.quality, transparent=False)
        print("\n=== Rendering Manim lower-thirds (transparent) ===")
        for scene in OVERLAYS:
            render_manim(scene, quality=args.quality, transparent=True)

    print("\n=== Locating Manim exports ===")
    renders = {s: find_render(s, transparent=False) for s in FULL_CARDS}
    overlays = {s: find_render(s, transparent=True) for s in OVERLAYS}
    for name, path in {**renders, **overlays}.items():
        print(f"  {name}: {path.relative_to(REPO)}")

    print("\n=== Trimming demo clips ===")
    d1 = CLIPS / "D1_live-en-captions.mp4"
    d2 = CLIPS / "D2_second-speaker.mp4"
    d3 = CLIPS / "D3_whisper-detected.mp4"
    d4 = CLIPS / "D4_siren-emergency-vehicle.mp4"
    d5 = CLIPS / "D5_clapping.mp4"
    d6 = CLIPS / "D6_japanese-locale.mp4"

    ffmpeg_trim(d1, 0, 3, BUILD / "d1_product_raw.mp4")
    ffmpeg_trim(d1, 3, 7, BUILD / "d1_speech_raw.mp4")
    ffmpeg_trim(d2, 0, 3, BUILD / "d2_speech_raw.mp4")
    ffmpeg_trim(d3, 0, 3, BUILD / "d3_sound_raw.mp4")
    ffmpeg_trim(d4, 0, 5, BUILD / "d4_sound_raw.mp4")
    ffmpeg_trim(d5, 0, 4, BUILD / "d5_sound_raw.mp4")
    ffmpeg_trim(d6, 0, 10, BUILD / "d6_locale_raw.mp4")

    print("\n=== Compositing lower-thirds onto demo clips ===")
    ffmpeg_overlay(BUILD / "d1_product_raw.mp4", overlays["ProductLowerThird"], BUILD / "seg_product.mp4")
    ffmpeg_concat(
        [BUILD / "d1_speech_raw.mp4", BUILD / "d2_speech_raw.mp4"],
        BUILD / "speech_combined.mp4",
    )
    ffmpeg_overlay(BUILD / "speech_combined.mp4", overlays["SpeechLowerThird"], BUILD / "seg_speech.mp4")
    ffmpeg_concat(
        [BUILD / "d3_sound_raw.mp4", BUILD / "d4_sound_raw.mp4", BUILD / "d5_sound_raw.mp4"],
        BUILD / "sound_combined.mp4",
    )
    ffmpeg_overlay(BUILD / "sound_combined.mp4", overlays["SoundLowerThird"], BUILD / "seg_sound.mp4")
    ffmpeg_overlay(BUILD / "d6_locale_raw.mp4", overlays["LocaleLowerThird"], BUILD / "seg_locale.mp4")

    print("\n=== Normalizing Manim cards to beat durations ===")
    normalize_card(renders["HookCard"], BUILD / "seg_hook.mp4", 3.0)
    normalize_card(renders["ProblemCard"], BUILD / "seg_problem.mp4", 4.0)
    normalize_card(renders["PipelineCard"], BUILD / "seg_pipeline.mp4", 4.0)
    normalize_card(renders["ProofCard"], BUILD / "seg_proof.mp4", 6.0)
    normalize_card(renders["CTACard"], BUILD / "seg_cta.mp4", 6.0)

    timeline = [
        BUILD / "seg_hook.mp4",
        BUILD / "seg_problem.mp4",
        BUILD / "seg_product.mp4",
        BUILD / "seg_speech.mp4",
        BUILD / "seg_sound.mp4",
        BUILD / "seg_pipeline.mp4",
        BUILD / "seg_locale.mp4",
        BUILD / "seg_proof.mp4",
        BUILD / "seg_cta.mp4",
    ]

    print("\n=== Final concat ===")
    final = OUT / "aura-60s-rough-assembly.mp4"
    ffmpeg_concat(timeline, final)

    total = sum(
        float(
            subprocess.check_output(
                [
                    "ffprobe",
                    "-v",
                    "error",
                    "-show_entries",
                    "format=duration",
                    "-of",
                    "default=noprint_wrappers=1:nokey=1",
                    str(p),
                ],
                text=True,
            ).strip()
        )
        for p in timeline
    )
    print(f"\nDone: {final.relative_to(REPO)}")
    print(f"Duration: {total:.1f}s (target ~58s)")
    print("\nManim text: full cards + lower-thirds. Muted. Tweak aura_cards.py and re-run to iterate.")


if __name__ == "__main__":
    try:
        main()
    except subprocess.CalledProcessError as exc:
        sys.exit(exc.returncode)
