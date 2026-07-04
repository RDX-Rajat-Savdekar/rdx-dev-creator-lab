#!/usr/bin/env python3
"""Mux cleaned VO onto chapter video — no Resolve required.

Per act: trim or freeze-extend video to match processed WAV length, mux audio.
Concat acts → output/sceneN_chapterN_2160p60_vo.mp4

Usage (repo root):
  python Aura/design-video/tools/mux_chapter_vo.py --chapter 0 --dry-run
  python Aura/design-video/tools/mux_chapter_vo.py --chapter 0 --banner
  python Aura/design-video/tools/mux_chapter_vo.py --all --banner
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tempfile
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
sys.path.insert(0, str(TOOLS))
from chapter_banners import prepend_banner  # noqa: E402
from video_catalog import find_act_mp4, probe_duration  # noqa: E402
from vo_video_fit import fit_video_vo_hold  # noqa: E402

REPO = TOOLS.parents[2]
DESIGN = REPO / "Aura" / "design-video"
VO_DIR = DESIGN / "vo"
CLIPS = VO_DIR / "vo_clips.json"
PROCESSED = DESIGN / "aura_manim" / "media" / "audio" / "processed"
OUTPUT = DESIGN / "output"
MEDIA = DESIGN / "aura_manim" / "media" / "videos"
QUALITY = "2160p60"


def load_clip(chapter: int, act: int) -> dict | None:
    if not CLIPS.is_file():
        return None
    for c in json.loads(CLIPS.read_text(encoding="utf-8")):
        if c["chapter"] == chapter and c["act"] == act:
            return c
    return None


def target_duration(entry: dict, wav: Path) -> float:
    """Match full cleaned WAV — hold frame fills any gap vs speech."""
    return probe_duration(wav) or float(entry.get("clean_sec") or 0)


def fit_video_to_duration(
    src: Path,
    dst: Path,
    target: float,
    scene_py: Path | None,
    *,
    dry_run: bool,
) -> None:
    base = probe_duration(src) or 0
    if dry_run:
        from vo_video_fit import parse_content_end

        end = parse_content_end(scene_py, base)
        mode = "extend hold" if target > end + 0.04 else "trim"
        print(f"    video {base:.2f}s → {target:.2f}s · content_end {end:.2f}s ({mode})")
        return
    fit_video_vo_hold(src, dst, target, scene_py, dry_run=False)


def mux_av(video: Path, audio: Path, dst: Path, *, dry_run: bool) -> None:
    if dry_run:
        return
    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-i",
            str(video),
            "-i",
            str(audio),
            "-map",
            "0:v:0",
            "-map",
            "1:a:0",
            "-c:v",
            "copy",
            "-c:a",
            "aac",
            "-b:a",
            "192k",
            "-shortest",
            str(dst),
        ],
        check=True,
        capture_output=True,
    )


def list_acts(chapter: int) -> list[int]:
    acts: list[int] = []
    for act in range(1, 13):
        if find_act_mp4(chapter, act, QUALITY):
            acts.append(act)
        elif act == 1:
            break
    return acts


def mux_chapter(chapter: int, *, dry_run: bool, work_dir: Path | None = None, banner: bool = False) -> Path | None:
    acts = list_acts(chapter)
    if not acts:
        print(f"ch{chapter}: no 4K acts", file=sys.stderr)
        return None

    tmp_ctx = tempfile.TemporaryDirectory() if work_dir is None else None
    base = work_dir or Path(tmp_ctx.name)  # type: ignore[union-attr]

    pieces: list[Path] = []
    print(f"Chapter {chapter} — {len(acts)} act(s)")

    for act in acts:
        src = find_act_mp4(chapter, act, QUALITY)
        wav = PROCESSED / f"ch{chapter}_act{act}.wav"
        entry = load_clip(chapter, act) or {}
        scene_py = DESIGN / "aura_manim" / "scenes" / f"scene{chapter}_act{act}.py"
        if not src or not wav.is_file():
            print(f"  act{act}: missing video or {wav.name}", file=sys.stderr)
            sys.exit(1)
        target = target_duration(entry, wav)
        print(f"  act{act}: {wav.name} target={target:.2f}s (video base {probe_duration(src):.2f}s)")

        vid_fit = base / f"ch{chapter}_act{act}_fit.mp4"
        out = base / f"ch{chapter}_act{act}_mux.mp4"
        fit_video_to_duration(src, vid_fit, target, scene_py, dry_run=dry_run)
        if not dry_run:
            mux_av(vid_fit, wav, out, dry_run=False)
        pieces.append(out if not dry_run else src)

    if dry_run:
        out_path = OUTPUT / f"scene{chapter}_chapter{chapter}_2160p60_vo.mp4"
        if banner:
            print(f"  + 2s chapter banner")
        print(f"  → would write {out_path}")
        return out_path

    list_path = base / "concat.txt"
    list_path.write_text("\n".join(f"file '{p}'" for p in pieces) + "\n")
    OUTPUT.mkdir(parents=True, exist_ok=True)
    body_path = base / f"scene{chapter}_body.mp4"
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
            str(body_path),
        ],
        check=True,
        capture_output=True,
    )
    out_path = OUTPUT / f"scene{chapter}_chapter{chapter}_2160p60_vo.mp4"
    if banner:
        print(f"  + 2s banner: Chapter {chapter}")
        prepend_banner(body_path, chapter, out_path)
    else:
        body_path.replace(out_path)
    dur = probe_duration(out_path)
    print(f"  → {out_path.relative_to(REPO)} ({dur:.1f}s)")
    if tmp_ctx:
        tmp_ctx.cleanup()
    return out_path


def main() -> None:
    parser = argparse.ArgumentParser(description="Mux VO onto chapter video (ffmpeg)")
    parser.add_argument("--chapter", type=int, default=None)
    parser.add_argument("--all", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument(
        "--banner",
        action="store_true",
        help="Prepend 2s chapter title card (YouTube chapter name from vo/sceneN.md)",
    )
    args = parser.parse_args()

    if not CLIPS.is_file():
        print(f"Run process_vo_audio.py first → {CLIPS}", file=sys.stderr)
        sys.exit(1)

    if args.all:
        chapters = [ch for ch in range(10) if list_acts(ch)]
    elif args.chapter is not None:
        chapters = [args.chapter]
    else:
        parser.print_help()
        sys.exit(1)

    for ch in chapters:
        mux_chapter(ch, dry_run=args.dry_run, banner=args.banner)


if __name__ == "__main__":
    main()
