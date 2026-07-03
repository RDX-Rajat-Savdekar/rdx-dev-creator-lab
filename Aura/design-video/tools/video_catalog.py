"""Discover Manim act + chapter MP4s for prompter video sync."""

from __future__ import annotations

import subprocess
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
DESIGN = REPO / "Aura" / "design-video"
MEDIA = DESIGN / "aura_manim" / "media" / "videos"
OUTPUT = DESIGN / "output"

ACT_QUALITIES = ("480p15", "2160p60")
CHAPTER_VARIANTS = ("2160p60", "2160p60_vo")


def probe_duration(path: Path) -> float | None:
    if not path.is_file():
        return None
    try:
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
        return round(float(out), 2)
    except (subprocess.CalledProcessError, ValueError):
        return None


def find_act_mp4(chapter: int, act: int, quality: str) -> Path | None:
    folder = MEDIA / f"scene{chapter}_act{act}" / quality
    p = folder / f"Scene{chapter}Act{act}.mp4"
    return p if p.is_file() else None


def find_act_vo_mp4(chapter: int, act: int) -> Path | None:
    p = MEDIA / f"scene{chapter}_act{act}" / "2160p60" / f"Scene{chapter}Act{act}_vo.mp4"
    return p if p.is_file() else None


def find_chapter_mp4(chapter: int, variant: str = "2160p60") -> Path | None:
    suffix = "" if variant == "2160p60" else "_vo"
    p = OUTPUT / f"scene{chapter}_chapter{chapter}_2160p60{suffix}.mp4"
    return p if p.is_file() else None


def list_act_numbers(chapter: int, max_acts: int = 12) -> list[int]:
    acts: list[int] = []
    for act in range(1, max_acts + 1):
        if find_act_mp4(chapter, act, "480p15") or find_act_mp4(chapter, act, "2160p60"):
            acts.append(act)
        elif act == 1:
            break
    return acts


def resolve_act_path(chapter: int, act: int, quality: str) -> Path | None:
    if quality == "vo":
        return find_act_vo_mp4(chapter, act)
    return find_act_mp4(chapter, act, quality)


def resolve_chapter_path(chapter: int, variant: str) -> Path | None:
    return find_chapter_mp4(chapter, variant)


def build_catalog() -> dict:
    acts: list[dict] = []
    chapters: list[dict] = []

    for ch in range(10):
        act_nums = list_act_numbers(ch)
        if not act_nums:
            continue

        act_rows: list[dict] = []
        t = 0.0
        for act in act_nums:
            sources: dict[str, str | None] = {}
            durations: dict[str, float | None] = {}
            for q in ACT_QUALITIES:
                p = find_act_mp4(ch, act, q)
                sources[q] = str(p) if p else None
                durations[q] = probe_duration(p) if p else None
            vo_p = find_act_vo_mp4(ch, act)
            sources["vo"] = str(vo_p) if vo_p else None
            durations["vo"] = probe_duration(vo_p) if vo_p else None

            dur = durations.get("480p15") or durations.get("2160p60") or 0.0
            row = {
                "chapter": ch,
                "act": act,
                "key": f"{ch}:{act}",
                "sources": sources,
                "durations": durations,
                "duration": dur,
                "chapter_start": round(t, 2),
            }
            act_rows.append(row)
            acts.append(row)
            t += dur or 0.0

        for variant in CHAPTER_VARIANTS:
            cp = find_chapter_mp4(ch, variant)
            if not cp:
                continue
            chapters.append(
                {
                    "chapter": ch,
                    "variant": variant,
                    "path": str(cp),
                    "duration": probe_duration(cp),
                    "acts": act_rows,
                }
            )
            break  # prefer 2160p60 entry first; vo listed in sources

        # Also expose vo chapter if exists
        vo_ch = find_chapter_mp4(ch, "2160p60_vo")
        if vo_ch and not any(c.get("variant") == "2160p60_vo" for c in chapters if c["chapter"] == ch):
            chapters.append(
                {
                    "chapter": ch,
                    "variant": "2160p60_vo",
                    "path": str(vo_ch),
                    "duration": probe_duration(vo_ch),
                    "acts": act_rows,
                }
            )

    return {"acts": acts, "chapters": chapters}
