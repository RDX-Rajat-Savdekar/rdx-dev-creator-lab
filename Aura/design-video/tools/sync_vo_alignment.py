#!/usr/bin/env python3
"""Apply transcript-based VO alignment → hold_extensions.json + wait suggestions.

Reads vo/vo_clips.json (run process_vo_audio.py --transcribe first).
Uses speech_end + tail pad as required act length — avoids Resolve for extend path.

Usage (repo root):
  python Aura/design-video/tools/sync_vo_alignment.py --show
  python Aura/design-video/tools/sync_vo_alignment.py --write-holds
  python Aura/design-video/tools/sync_vo_alignment.py --write-waits --dry-run
  python Aura/design-video/tools/sync_vo_alignment.py --apply-holds --concat --chapter 0
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
sys.path.insert(0, str(TOOLS))

REPO = TOOLS.parents[2]
DESIGN = REPO / "Aura" / "design-video"
VO_DIR = DESIGN / "vo"
CLIPS = VO_DIR / "vo_clips.json"
HOLDS = VO_DIR / "hold_extensions.json"
WAITS = VO_DIR / "wait_adjustments.json"
PAD = 1.0


def load_clips() -> list[dict]:
    if not CLIPS.is_file():
        print(f"Missing {CLIPS} — run process_vo_audio.py --transcribe", file=sys.stderr)
        sys.exit(1)
    return json.loads(CLIPS.read_text(encoding="utf-8"))


def required_video_sec(entry: dict) -> float:
    """Speech must finish + tail pad when audio starts at act t=0."""
    tx = entry.get("transcript") or {}
    segs = tx.get("segments") or []
    if segs:
        return round(float(segs[-1]["end"]) + PAD, 2)
    return float(entry.get("clean_sec") or 0)


def align_entry(entry: dict) -> dict:
    video = float(entry.get("video_sec") or 0)
    clean = float(entry.get("clean_sec") or 0)
    req = required_video_sec(entry)
    delta = round(req - video, 2)
    current_wait = entry.get("current_wait")
    suggested_wait = None
    hold_extra = 0.0
    if delta < -0.3 and current_wait is not None:
        suggested_wait = round(max(1.5, float(current_wait) + delta), 1)
        action = f"trim video ~{-delta:.1f}s (or wait→{suggested_wait:g}s)"
    elif delta > 0.3:
        hold_extra = delta
        action = f"extend video ~{delta:.1f}s"
    else:
        action = "ok"
    speech_sec = entry.get("speech_sec")
    return {
        **entry,
        "required_video_sec": req,
        "delta_align": delta,
        "hold_extra": hold_extra,
        "suggested_wait": suggested_wait,
        "action": action,
        "speech_sec": speech_sec,
    }


def show_table(rows: list[dict]) -> None:
    print(f"{'Ch':<3} {'Act':<3} {'Speech':>7} {'ReqVid':>7} {'Video':>7} {'Δ':>7}  Action")
    print("-" * 72)
    for r in rows:
        sp = f"{r['speech_sec']:.1f}s" if r.get("speech_sec") else "—"
        print(
            f"{r['chapter']:<3} {r['act']:<3} {sp:>7} "
            f"{r['required_video_sec']:6.1f}s {r['video_sec']:6.1f}s "
            f"{r['delta_align']:+6.1f}s  {r['action']}"
        )


def write_holds(rows: list[dict]) -> None:
    data = {"acts": {}, "notes": {}}
    if HOLDS.is_file():
        data = json.loads(HOLDS.read_text(encoding="utf-8"))
    acts = data.setdefault("acts", {})
    notes = data.setdefault("notes", {})
    for r in rows:
        k = r["key"]
        extra = float(r.get("hold_extra") or 0)
        acts[k] = extra if extra > 0.05 else 0.0
        if extra > 0.05:
            notes[k] = f"auto: speech+pad needs +{extra:.1f}s vs video"
        elif k in notes and notes[k].startswith("auto:"):
            notes[k] = ""
    data["_help"] = (
        "extra_sec per act = seconds to freeze LAST frame after Manim render. "
        "Generated from Whisper speech_end + tail pad. Run extend_act_holds.py --apply."
    )
    HOLDS.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    n = sum(1 for r in rows if (r.get("hold_extra") or 0) > 0.05)
    print(f"Wrote {HOLDS.relative_to(REPO)} ({n} act(s) need extend)")


def write_waits(rows: list[dict], dry_run: bool) -> None:
    items = [
        {
            "chapter": r["chapter"],
            "act": r["act"],
            "key": r["key"],
            "current_wait": r.get("current_wait"),
            "suggested_wait": r.get("suggested_wait"),
            "delta_align": r.get("delta_align"),
        }
        for r in rows
        if r.get("suggested_wait") is not None
    ]
    WAITS.write_text(json.dumps({"acts": items}, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {WAITS.relative_to(REPO)} ({len(items)} trim candidates)")
    if dry_run:
        for it in items[:8]:
            print(f"  ch{it['chapter']} act{it['act']}: {it['current_wait']}→{it['suggested_wait']}")
        if len(items) > 8:
            print(f"  … +{len(items) - 8} more")
        return
    for it in items:
        cmd = [
            sys.executable,
            str(TOOLS / "adjust_waits.py"),
            "--chapter",
            str(it["chapter"]),
            "--act",
            str(it["act"]),
            "--set",
            str(it["suggested_wait"]),
        ]
        subprocess.run(cmd, check=True)
    print(f"Updated {len(items)} act file(s). Re-render 4K acts + re-concat.")


def apply_holds(chapter: int | None, concat: bool) -> None:
    cmd = [sys.executable, str(TOOLS / "extend_act_holds.py"), "--apply"]
    if chapter is not None:
        cmd.extend(["--chapter", str(chapter)])
    if concat:
        cmd.append("--concat")
    subprocess.run(cmd, check=True)


def main() -> None:
    parser = argparse.ArgumentParser(description="Transcript-based VO alignment config")
    parser.add_argument("--show", action="store_true")
    parser.add_argument("--write-holds", action="store_true")
    parser.add_argument("--write-waits", action="store_true")
    parser.add_argument("--apply-holds", action="store_true")
    parser.add_argument("--concat", action="store_true")
    parser.add_argument("--chapter", type=int, default=None)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    clips = load_clips()
    if args.chapter is not None:
        clips = [c for c in clips if c["chapter"] == args.chapter]
    rows = [align_entry(c) for c in clips]

    missing_tx = sum(1 for c in clips if not (c.get("transcript") or {}).get("segments"))
    if missing_tx:
        print(f"Warning: {missing_tx} clip(s) lack transcript — using clean_sec fallback", file=sys.stderr)

    if args.show or not any([args.write_holds, args.write_waits, args.apply_holds]):
        show_table(rows)
        ok = sum(1 for r in rows if abs(r["delta_align"]) <= 0.3)
        ext = sum(1 for r in rows if r["delta_align"] > 0.3)
        trim = sum(1 for r in rows if r["delta_align"] < -0.3)
        print(f"\n{len(rows)} acts · ok={ok} extend={ext} trim={trim}")
        return

    if args.write_holds:
        write_holds(rows)
    if args.write_waits:
        write_waits(rows, args.dry_run)
    if args.apply_holds:
        apply_holds(args.chapter, args.concat)


if __name__ == "__main__":
    main()
