#!/usr/bin/env python3
"""Build full teleprompter exports from vo/sceneN.md files.

Usage (repo root):
  python Aura/design-video/tools/build_teleprompter.py
  python Aura/design-video/tools/build_teleprompter.py --wpm 140
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from parse_vo_docs import (  # noqa: E402
    export_teleprompter_md,
    export_teleprompter_txt,
    parse_all_vo_docs,
    summarize_chapters,
)

REPO = Path(__file__).resolve().parents[3]
VO_DIR = REPO / "Aura" / "design-video" / "vo"


def main() -> None:
    parser = argparse.ArgumentParser(description="Build teleprompter from vo/sceneN.md")
    parser.add_argument("--wpm", type=float, default=140.0)
    args = parser.parse_args()

    lines = parse_all_vo_docs(wpm=args.wpm)
    if not lines:
        print("No VO lines found in vo/sceneN.md", file=sys.stderr)
        sys.exit(1)

    VO_DIR.mkdir(parents=True, exist_ok=True)
    (VO_DIR / "teleprompter.txt").write_text(
        export_teleprompter_txt(lines), encoding="utf-8"
    )
    (VO_DIR / "TELEPROMPTER.md").write_text(
        export_teleprompter_md(lines, wpm=args.wpm), encoding="utf-8"
    )
    payload = {
        "wpm": args.wpm,
        "lines": [ln.to_dict() for ln in lines],
        "chapters": summarize_chapters(lines),
        "total_words": sum(ln.word_count for ln in lines),
        "total_seconds": round(sum(ln.target_seconds for ln in lines), 1),
    }
    (VO_DIR / "teleprompter.json").write_text(
        json.dumps(payload, indent=2), encoding="utf-8"
    )

    print(f"Wrote {len(lines)} act lines @ {args.wpm:g} wpm")
    print(f"  {VO_DIR / 'teleprompter.txt'}")
    print(f"  {VO_DIR / 'TELEPROMPTER.md'}")
    print(f"  {VO_DIR / 'teleprompter.json'}")
    print(f"Total: ~{payload['total_words']} words · ~{payload['total_seconds']}s VO")


if __name__ == "__main__":
    main()
