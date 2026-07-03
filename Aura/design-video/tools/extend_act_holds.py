#!/usr/bin/env python3
"""Freeze-frame hold extension — simulates extra scene.wait() without re-rendering Manim.

Manim's scene.wait() holds whatever is on screen. This tool appends cloned last-frame
holds to finished act MP4s via ffmpeg tpad — fast VO pacing iteration.

Usage (repo root):
  python Aura/design-video/tools/extend_act_holds.py --show
  python Aura/design-video/tools/extend_act_holds.py --init
  python Aura/design-video/tools/extend_act_holds.py --apply
  python Aura/design-video/tools/extend_act_holds.py --chapter 1 --extra 3.0
  python Aura/design-video/tools/extend_act_holds.py --apply --concat

Config: vo/hold_extensions.json
  { "acts": { "1:3": 2.5 }, "notes": { "1:3": "VO ran long on rejection beat" } }

Keys are "chapter:act". Values are EXTRA seconds after the Manim clip ends.
Output: aura_manim/media/videos/sceneN_actM/2160p60/SceneNActM_vo.mp4
Concat: output/sceneN_chapterN_2160p60_vo.mp4 (when --concat)
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
DESIGN = REPO / "Aura" / "design-video"
MEDIA = DESIGN / "aura_manim" / "media" / "videos"
OUTPUT = DESIGN / "output"
CONFIG = DESIGN / "vo" / "hold_extensions.json"
QUALITY = "2160p60"


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


def find_act_mp4(chapter: int, act: int) -> Path | None:
    folder = MEDIA / f"scene{chapter}_act{act}" / QUALITY
    p = folder / f"Scene{chapter}Act{act}.mp4"
    return p if p.is_file() else None


def list_acts(chapter: int, max_acts: int = 12) -> list[int]:
    acts: list[int] = []
    for act in range(1, max_acts + 1):
        if find_act_mp4(chapter, act):
            acts.append(act)
        elif act == 1:
            break
    return acts


def extend_mp4(src: Path, dst: Path, extra_sec: float) -> None:
    if extra_sec <= 0:
        if dst != src:
            dst.write_bytes(src.read_bytes())
        return
    dst.parent.mkdir(parents=True, exist_ok=True)
    # tpad stop_mode=clone: hold last frame for extra_sec
    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-i",
            str(src),
            "-vf",
            f"tpad=stop_mode=clone:stop_duration={extra_sec:.3f}",
            "-c:v",
            "libx264",
            "-preset",
            "fast",
            "-crf",
            "18",
            "-pix_fmt",
            "yuv420p",
            "-movflags",
            "+faststart",
            str(dst),
        ],
        check=True,
        capture_output=True,
    )


def load_config() -> dict:
    if not CONFIG.is_file():
        return {"acts": {}, "notes": {}}
    return json.loads(CONFIG.read_text(encoding="utf-8"))


def save_config(data: dict) -> None:
    CONFIG.parent.mkdir(parents=True, exist_ok=True)
    CONFIG.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def act_key(chapter: int, act: int) -> str:
    return f"{chapter}:{act}"


def show_table() -> None:
    cfg = load_config()
    extras = cfg.get("acts", {})
    notes = cfg.get("notes", {})
    print(f"Act holds (extra end-frame seconds) · config: {CONFIG.relative_to(REPO)}\n")
    print(f"{'Ch':<4} {'Act':<4} {'Base':>7} {'Extra':>7} {'Total':>7}  Note")
    print("-" * 72)
    for ch in range(10):
        acts = list_acts(ch)
        if not acts:
            continue
        for act in acts:
            src = find_act_mp4(ch, act)
            assert src
            base = probe_duration(src)
            extra = float(extras.get(act_key(ch, act), 0.0))
            total = base + extra
            note = notes.get(act_key(ch, act), "")
            print(f"{ch:<4} {act:<4} {base:6.1f}s {extra:6.1f}s {total:6.1f}s  {note}")


def init_config() -> None:
    data = load_config()
    acts_map = data.setdefault("acts", {})
    notes = data.setdefault("notes", {})
    for ch in range(10):
        for act in list_acts(ch):
            k = act_key(ch, act)
            acts_map.setdefault(k, 0.0)
            notes.setdefault(k, "")
    data["_help"] = (
        "extra_sec per act = seconds to freeze LAST frame after Manim render. "
        "Same visual as scene.wait() at end of act. Edit values, then --apply."
    )
    save_config(data)
    print(f"Initialized {CONFIG}")
    show_table()


def apply_holds(chapter: int | None, concat: bool) -> None:
    cfg = load_config()
    extras = cfg.get("acts", {})
    chapters = [chapter] if chapter is not None else [ch for ch in range(10) if list_acts(ch)]

    for ch in chapters:
        for act in list_acts(ch):
            src = find_act_mp4(ch, act)
            if not src:
                continue
            extra = float(extras.get(act_key(ch, act), 0.0))
            dst = src.parent / f"Scene{ch}Act{act}_vo.mp4"
            if extra <= 0 and dst.is_file():
                dst.unlink()
                print(f"ch{ch} act{act}: removed _vo (extra=0)")
                continue
            if extra <= 0:
                continue
            base = probe_duration(src)
            print(f"ch{ch} act{act}: {base:.1f}s + {extra:.1f}s hold → {dst.name}")
            extend_mp4(src, dst, extra)

        if concat:
            build_chapter_concat(ch, use_vo=True)


def build_chapter_concat(chapter: int, *, use_vo: bool) -> None:
    acts = list_acts(chapter)
    if not acts:
        return
    lines: list[str] = []
    for act in acts:
        folder = MEDIA / f"scene{chapter}_act{act}" / QUALITY
        vo = folder / f"Scene{chapter}Act{act}_vo.mp4"
        base = folder / f"Scene{chapter}Act{act}.mp4"
        pick = vo if use_vo and vo.is_file() else base
        if not pick.is_file():
            print(f"Missing {pick}", file=sys.stderr)
            sys.exit(1)
        lines.append(f"file '{pick}'")
    OUTPUT.mkdir(parents=True, exist_ok=True)
    suffix = "_vo" if use_vo else ""
    list_path = OUTPUT / f"scene{chapter}_concat{suffix}.txt"
    out_path = OUTPUT / f"scene{chapter}_chapter{chapter}_2160p60{suffix}.mp4"
    list_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
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
            str(out_path),
        ],
        check=True,
        capture_output=True,
    )
    dur = probe_duration(out_path)
    print(f"Concat ch{chapter}: {out_path.name} ({dur:.1f}s)")


def set_chapter_extra(chapter: int, extra: float, act: int | None) -> None:
    cfg = load_config()
    acts_map = cfg.setdefault("acts", {})
    targets = [act] if act else list_acts(chapter)
    for a in targets:
        acts_map[act_key(chapter, a)] = round(extra, 2)
    save_config(cfg)
    print(f"Set ch{chapter} extra={extra:g}s on act(s) {targets}")


def main() -> None:
    parser = argparse.ArgumentParser(description="ffmpeg freeze-frame VO holds")
    parser.add_argument("--show", action="store_true", help="Print act durations + config")
    parser.add_argument("--init", action="store_true", help="Create vo/hold_extensions.json template")
    parser.add_argument("--apply", action="store_true", help="Apply holds from config")
    parser.add_argument("--concat", action="store_true", help="With --apply, rebuild chapter concat")
    parser.add_argument("--chapter", type=int, default=None)
    parser.add_argument("--act", type=int, default=None)
    parser.add_argument("--extra", type=float, default=None, help="Set extra hold for chapter/act")
    parser.add_argument("--concat-only", action="store_true", help="Rebuild concat from _vo files")
    args = parser.parse_args()

    if args.show:
        show_table()
        return
    if args.init:
        init_config()
        return
    if args.extra is not None:
        if args.chapter is None:
            print("--extra requires --chapter", file=sys.stderr)
            sys.exit(1)
        set_chapter_extra(args.chapter, args.extra, args.act)
        return
    if args.apply:
        apply_holds(args.chapter, args.concat)
        return
    if args.concat_only:
        chs = [args.chapter] if args.chapter is not None else [c for c in range(10) if list_acts(c)]
        for ch in chs:
            build_chapter_concat(ch, use_vo=True)
        return

    parser.print_help()


if __name__ == "__main__":
    main()
