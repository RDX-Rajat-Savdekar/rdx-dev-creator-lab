#!/usr/bin/env python3
"""Adjust ``scene.wait()`` timings in sceneN_act*.py for VO pacing.

Visual-first workflow: ship Manim with default holds (~5.5s), read VO over
concat, then bulk-add or trim waits without hand-editing every act.

Usage (repo root):
  python Aura/design-video/tools/adjust_waits.py --chapter 4 --show
  python Aura/design-video/tools/adjust_waits.py --chapter 4 --add 2.0
  python Aura/design-video/tools/adjust_waits.py --chapter 6 --act 2 --set 8.0
  python Aura/design-video/tools/adjust_waits.py --chapter 4 --add 2.0 --dry-run

Only edits ``scene{N}_act{M}.py`` (not ``sceneN_full``). By default only
``scene.wait(...)`` with duration >= ``--min-hold`` (1.5s).
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
SCENES = REPO / "Aura" / "design-video" / "aura_manim" / "scenes"

WAIT_RE = re.compile(r"scene\.wait\(\s*([0-9]+(?:\.[0-9]+)?)\s*\)")


def act_files(chapter: int, act: int | None) -> list[Path]:
    files = sorted(SCENES.glob(f"scene{chapter}_act*.py"))
    if act is not None:
        files = [p for p in files if p.stem == f"scene{chapter}_act{act}"]
    return files


def list_waits(source: str, min_hold: float) -> list[float]:
    return [float(m.group(1)) for m in WAIT_RE.finditer(source) if float(m.group(1)) >= min_hold]


def show_chapter(chapter: int, min_hold: float) -> None:
    print(f"Chapter {chapter} — scene.wait() (>= {min_hold}s)\n")
    print(f"{'Act':<6} {'File':<22} {'Waits'}")
    print("-" * 50)
    for path in act_files(chapter, None):
        act = path.stem.split("_act")[-1]
        waits = list_waits(path.read_text(), min_hold)
        vals = ", ".join(f"{v:g}s" for v in waits) or "(none)"
        print(f"{act:<6} {path.name:<22} {vals}")


def apply_edit(
    source: str,
    *,
    add: float | None,
    set_val: float | None,
    min_hold: float,
) -> tuple[str, int]:
    changes = 0

    def repl(m: re.Match[str]) -> str:
        nonlocal changes
        val = float(m.group(1))
        if val < min_hold:
            return m.group(0)
        if set_val is not None:
            new_val = set_val
        elif add is not None:
            new_val = round(val + add, 2)
        else:
            return m.group(0)
        changes += 1
        return f"scene.wait({new_val:g})"

    return WAIT_RE.sub(repl, source), changes


def main() -> None:
    parser = argparse.ArgumentParser(description="Adjust scene.wait() VO holds per chapter")
    parser.add_argument("--chapter", type=int, required=True)
    parser.add_argument("--act", type=int, default=None)
    parser.add_argument("--show", action="store_true")
    parser.add_argument("--add", type=float, default=None)
    parser.add_argument("--set", type=float, dest="set_val", default=None)
    parser.add_argument("--min-hold", type=float, default=1.5)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    if args.show:
        show_chapter(args.chapter, args.min_hold)
        return

    if args.add is None and args.set_val is None:
        print("Specify --show, --add N, or --set N", file=sys.stderr)
        sys.exit(1)

    files = act_files(args.chapter, args.act)
    if not files:
        print(f"No act files for chapter {args.chapter}", file=sys.stderr)
        sys.exit(1)

    total = 0
    for path in files:
        source = path.read_text()
        new_source, n = apply_edit(
            source, add=args.add, set_val=args.set_val, min_hold=args.min_hold
        )
        if n:
            action = f"set→{args.set_val:g}" if args.set_val is not None else f"add {args.add:+.1f}"
            print(f"{path.name}: {n} wait(s) {action}")
            if not args.dry_run:
                path.write_text(new_source)
            total += n

    if total == 0:
        print("No matching scene.wait() calls found")
    elif args.dry_run:
        print(f"\nDry run — {total} change(s), no files written")
    else:
        ch = args.chapter
        print(f"\nUpdated {total} wait(s). Re-render acts, then re-concat chapter {ch}.")


if __name__ == "__main__":
    main()
