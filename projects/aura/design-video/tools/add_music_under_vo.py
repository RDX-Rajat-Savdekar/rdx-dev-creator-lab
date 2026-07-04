#!/usr/bin/env python3
"""Mix background music under VO on the design-video full film.

Documentary bed loops for the full runtime; optional accent track (e.g. hype)
plays at intro + outro only so dense narration stays readable.

Usage (repo root):
  python Aura/design-video/tools/add_music_under_vo.py
  python Aura/design-video/tools/add_music_under_vo.py --bed-volume 0.05 --accent-volume 0.04
  python Aura/design-video/tools/add_music_under_vo.py --no-accent

Defaults:
  input:  output/aura_design_video_2160p60_vo.mp4
  output: output/aura_design_video_2160p60_vo_music.mp4
  bed:    Aura/music/leberch-documentary-517370.mp3  @ 0.06
  accent: Aura/music/solarflex-hype-background-music-558271.mp3  @ 0.05 (intro/outro)
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
MUSIC = REPO / "Aura" / "music"
DEFAULT_IN = DESIGN / "output" / "aura_design_video_2160p60_vo.mp4"
DEFAULT_OUT = DESIGN / "output" / "aura_design_video_2160p60_vo_music.mp4"
DEFAULT_BED = MUSIC / "leberch-documentary-517370.mp3"
DEFAULT_ACCENT = MUSIC / "solarflex-hype-background-music-558271.mp3"


def loop_trim_fades(duration: float, volume: float, fade_in: float, fade_out: float) -> str:
    fade_out_start = max(0.0, duration - fade_out)
    return (
        f"aloop=loop=-1:size=2e+09,atrim=0:{duration},asetpts=PTS-STARTPTS,"
        f"volume={volume},"
        f"afade=t=in:st=0:d={fade_in},"
        f"afade=t=out:st={fade_out_start}:d={fade_out}"
    )


def accent_segment(length: float, volume: float, fade_in: float, fade_out: float) -> str:
    fade_out_start = max(0.0, length - fade_out)
    return (
        f"atrim=0:{length},asetpts=PTS-STARTPTS,"
        f"volume={volume},"
        f"afade=t=in:st=0:d={fade_in},"
        f"afade=t=out:st={fade_out_start}:d={fade_out}"
    )


def build_filter(
    duration: float,
    *,
    bed_volume: float,
    accent_volume: float,
    accent_intro: float,
    accent_outro: float,
    fade_in: float,
    fade_out: float,
    use_accent: bool,
) -> str:
    bed = loop_trim_fades(duration, bed_volume, fade_in, fade_out)
    parts = [f"[1:a]{bed}[bed]"]

    if use_accent:
        intro_len = min(accent_intro, duration * 0.5)
        outro_len = min(accent_outro, duration * 0.5)
        outro_delay_ms = int(max(0.0, duration - outro_len) * 1000)

        intro = accent_segment(intro_len, accent_volume, fade_in=1.0, fade_out=5.0)
        outro = accent_segment(outro_len, accent_volume, fade_in=2.0, fade_out=4.0)
        parts.extend(
            [
                f"[2:a]{intro}[intro]",
                f"[2:a]{outro}[outro]",
                f"[outro]adelay={outro_delay_ms}|{outro_delay_ms}[outro_d]",
                "[bed][intro]amix=inputs=2:duration=first:dropout_transition=0[bed_i]",
                "[bed_i][outro_d]amix=inputs=2:duration=first:dropout_transition=0[bg]",
            ]
        )
    else:
        parts.append("[bed]anull[bg]")

    parts.append("[0:a][bg]amix=inputs=2:duration=first:dropout_transition=2[aout]")
    return ";".join(parts)


def mix_under_vo(
    video: Path,
    bed: Path,
    output: Path,
    *,
    accent: Path | None,
    bed_volume: float,
    accent_volume: float,
    accent_intro: float,
    accent_outro: float,
    fade_in: float,
    fade_out: float,
) -> None:
    duration = probe_duration(video)
    use_accent = accent is not None
    filt = build_filter(
        duration,
        bed_volume=bed_volume,
        accent_volume=accent_volume,
        accent_intro=accent_intro,
        accent_outro=accent_outro,
        fade_in=fade_in,
        fade_out=fade_out,
        use_accent=use_accent,
    )
    cmd = [
        "ffmpeg",
        "-y",
        "-i",
        str(video),
        "-i",
        str(bed),
    ]
    if use_accent:
        cmd.extend(["-i", str(accent)])
    cmd.extend(
        [
            "-filter_complex",
            filt,
            "-map",
            "0:v",
            "-map",
            "[aout]",
            "-c:v",
            "copy",
            "-c:a",
            "aac",
            "-b:a",
            "192k",
            "-shortest",
            str(output),
        ]
    )
    print("→", " ".join(cmd))
    subprocess.run(cmd, check=True)


def main() -> None:
    parser = argparse.ArgumentParser(description="Mix music bed + optional accent under VO")
    parser.add_argument("--input", "-i", type=Path, default=DEFAULT_IN)
    parser.add_argument("--output", "-o", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--bed", type=Path, default=DEFAULT_BED, help="Looping documentary bed")
    parser.add_argument(
        "--accent",
        type=Path,
        default=DEFAULT_ACCENT,
        help="Intro/outro accent (e.g. hype). Pass --no-accent to skip.",
    )
    parser.add_argument("--no-accent", action="store_true")
    parser.add_argument(
        "--bed-volume",
        type=float,
        default=0.06,
        help="Documentary bed gain under VO (default 0.06)",
    )
    parser.add_argument(
        "--accent-volume",
        type=float,
        default=0.05,
        help="Accent gain at intro/outro (default 0.05)",
    )
    parser.add_argument("--accent-intro", type=float, default=35.0, help="Accent intro seconds")
    parser.add_argument("--accent-outro", type=float, default=35.0, help="Accent outro seconds")
    parser.add_argument("--fade-in", type=float, default=1.0)
    parser.add_argument("--fade-out", type=float, default=4.0)
    args = parser.parse_args()

    if not args.input.is_file():
        sys.exit(f"Missing video: {args.input}")
    if not args.bed.is_file():
        sys.exit(f"Missing bed track: {args.bed}")

    accent = None
    if not args.no_accent:
        if not args.accent.is_file():
            sys.exit(f"Missing accent track: {args.accent}")
        accent = args.accent

    args.output.parent.mkdir(parents=True, exist_ok=True)
    mix_under_vo(
        args.input,
        args.bed,
        args.output,
        accent=accent,
        bed_volume=args.bed_volume,
        accent_volume=args.accent_volume,
        accent_intro=args.accent_intro,
        accent_outro=args.accent_outro,
        fade_in=args.fade_in,
        fade_out=args.fade_out,
    )
    dur = probe_duration(args.output)
    print(f"\nDone: {args.output.relative_to(REPO)} ({dur:.1f}s)")
    if accent:
        print(f"  bed: {args.bed.name} @ {args.bed_volume}")
        print(f"  accent: {accent.name} @ {args.accent_volume} (intro {args.accent_intro}s, outro {args.accent_outro}s)")
    else:
        print(f"  bed: {args.bed.name} @ {args.bed_volume}")
    print("Tip: if music fights VO, retry with --bed-volume 0.04 --accent-volume 0.03")


if __name__ == "__main__":
    try:
        main()
    except subprocess.CalledProcessError as exc:
        sys.exit(exc.returncode)
