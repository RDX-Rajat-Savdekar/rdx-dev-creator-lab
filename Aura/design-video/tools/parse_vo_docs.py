"""Parse vo/sceneN.md files into narration lines for teleprompter + hold tools."""

from __future__ import annotations

import re
from dataclasses import asdict, dataclass
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
VO_DIR = REPO / "Aura" / "design-video" / "vo"

CHAPTER_HDR_RE = re.compile(r"^# Chapter (\d+) — (.+)$", re.MULTILINE)
YOUTUBE_CH_RE = re.compile(r"\*\*YouTube chapter:\*\*\s*\*([^*]+)\*")
VO_SEED_RE = re.compile(r"\*\*VO seed:\*\*\s*\*(.+?)\*", re.DOTALL)
ACT_TIMELINE_ROW_RE = re.compile(
    r"^\|\s*(\d+)\s*\|[^|]+\|[^|]+\|[^|]+\|\s*([^|]+?)\s*\|\s*`",
    re.MULTILINE,
)
ACT_DESC_RE = re.compile(r"^### Act (\d+) — (.+?)(?:\s*\(|$)", re.MULTILINE)
ACT_SECTION_RE = re.compile(r"^## Act (\d+) —", re.MULTILINE)
ACT_DRAFT_RE = re.compile(r"^### Act (\d+)", re.MULTILINE)
QUOTE_RE = re.compile(r"^> ([^>].*)$", re.MULTILINE)


@dataclass
class VoLine:
    chapter: int
    chapter_title: str
    youtube_chapter: str
    act: int
    act_title: str
    on_screen: str
    narration: str
    word_count: int
    target_seconds: float
    source: str  # "draft" | "seed"

    def to_dict(self) -> dict:
        return asdict(self)


def _strip_inline(text: str) -> str:
    text = re.sub(r"\*\*(.+?)\*\*", r"\1", text)
    text = re.sub(r"\*(.+?)\*", r"\1", text)
    text = re.sub(r"`([^`]+)`", r"\1", text)
    return " ".join(text.split())


def _words(text: str) -> int:
    clean = _strip_inline(text)
    return len(clean.split()) if clean else 0


def _target_seconds(words: int, wpm: float) -> float:
    if wpm <= 0:
        wpm = 140.0
    return round((words / wpm) * 60, 1) if words else 0.0


def _on_screen_map(text: str) -> dict[int, str]:
    labels: dict[int, str] = {}
    map_start = text.find("## Act map")
    if map_start >= 0:
        chunk = text[map_start : map_start + 4000]
        row_re = re.compile(
            r"^\|\s*(\d+)\s*\|[^|]+\|[^|]+\|\s*([^|]+?)\s*\|\s*`",
            re.MULTILINE,
        )
        for m in row_re.finditer(chunk):
            act = int(m.group(1))
            label = _strip_inline(m.group(2))
            if label and not label.startswith("~"):
                labels[act] = label
    if labels:
        return labels
    tl_start = text.find("## Act timeline")
    if tl_start >= 0:
        chunk = text[tl_start : tl_start + 4000]
        for m in ACT_TIMELINE_ROW_RE.finditer(chunk):
            labels[int(m.group(1))] = _strip_inline(m.group(2))
    return labels


def _draft_quotes(text: str) -> dict[int, str]:
    """### Act N blocks under ## VO draft with > quoted lines."""
    draft_start = text.find("## VO draft")
    if draft_start < 0:
        return {}
    draft = text[draft_start:]
    quotes: dict[int, str] = {}
    act_starts = list(ACT_DRAFT_RE.finditer(draft))
    for i, m in enumerate(act_starts):
        act = int(m.group(1))
        chunk_end = act_starts[i + 1].start() if i + 1 < len(act_starts) else len(draft)
        chunk = draft[m.end() : chunk_end]
        parts = [QUOTE_RE.match(line).group(1).strip() for line in chunk.splitlines() if QUOTE_RE.match(line)]
        if parts:
            quotes[act] = _strip_inline(" ".join(parts))
    return quotes


def _seed_by_act(text: str) -> dict[int, str]:
    """**VO seed:** under ## Act N — sections."""
    seeds: dict[int, str] = {}
    act_starts = list(ACT_SECTION_RE.finditer(text))
    for i, m in enumerate(act_starts):
        act = int(m.group(1))
        chunk_end = act_starts[i + 1].start() if i + 1 < len(act_starts) else len(text)
        chunk = text[m.start() : chunk_end]
        sm = VO_SEED_RE.search(chunk)
        if sm:
            seeds[act] = _strip_inline(sm.group(1))
    return seeds


def _act_titles(text: str) -> dict[int, str]:
    titles: dict[int, str] = {}
    map_start = text.find("## Act map")
    if map_start >= 0:
        chunk = text[map_start : map_start + 4000]
        row_re = re.compile(r"^\|\s*(\d+)\s*\|\s*([^|]+?)\s*\|", re.MULTILINE)
        for m in row_re.finditer(chunk):
            title = _strip_inline(m.group(2))
            low = title.lower()
            if low in ("scen-plan beat", "beat") or re.match(r"^[-:\s|]+$", title):
                continue
            titles[int(m.group(1))] = title
    desc_start = text.find("## Act descriptions")
    if desc_start >= 0:
        for m in ACT_DESC_RE.finditer(text[desc_start : desc_start + 12000]):
            act = int(m.group(1))
            if act not in titles:
                titles[act] = _strip_inline(m.group(2))
    for m in ACT_SECTION_RE.finditer(text):
        act = int(m.group(1))
        if act not in titles:
            line = m.group(0)
            title = line.split("—", 1)[-1].strip() if "—" in line else f"Act {act}"
            titles[act] = _strip_inline(title)
    return titles


def parse_scene_file(path: Path, *, wpm: float = 140.0) -> list[VoLine]:
    text = path.read_text(encoding="utf-8")
    ch_m = CHAPTER_HDR_RE.search(text)
    if not ch_m:
        return []
    chapter = int(ch_m.group(1))
    chapter_title = ch_m.group(2).strip()
    yt_m = YOUTUBE_CH_RE.search(text)
    youtube = yt_m.group(1).strip() if yt_m else chapter_title

    on_screen = _on_screen_map(text)
    drafts = _draft_quotes(text)
    seeds = _seed_by_act(text)
    titles = _act_titles(text)

    acts = sorted(set(drafts) | set(seeds) | set(on_screen))
    lines: list[VoLine] = []
    for act in acts:
        if act in drafts:
            narration = drafts[act]
            source = "draft"
        elif act in seeds:
            narration = seeds[act]
            source = "seed"
        else:
            continue
        words = _words(narration)
        lines.append(
            VoLine(
                chapter=chapter,
                chapter_title=chapter_title,
                youtube_chapter=youtube,
                act=act,
                act_title=titles.get(act, f"Act {act}"),
                on_screen=on_screen.get(act, ""),
                narration=narration,
                word_count=words,
                target_seconds=_target_seconds(words, wpm),
                source=source,
            )
        )
    return lines


def parse_all_vo_docs(*, wpm: float = 140.0, max_chapter: int = 9) -> list[VoLine]:
    out: list[VoLine] = []
    for ch in range(max_chapter + 1):
        path = VO_DIR / f"scene{ch}.md"
        if path.is_file():
            out.extend(parse_scene_file(path, wpm=wpm))
    return out


def export_teleprompter_txt(lines: list[VoLine], chapter: int | None = None) -> str:
    parts: list[str] = []
    cur_ch: int | None = None
    for ln in lines:
        if chapter is not None and ln.chapter != chapter:
            continue
        if ln.chapter != cur_ch:
            cur_ch = ln.chapter
            parts.extend(["", f"=== Chapter {ln.chapter} — {ln.youtube_chapter} ===", ""])
        parts.append(ln.narration)
        parts.append("")
    return "\n".join(parts).strip() + "\n"


def export_teleprompter_md(lines: list[VoLine], *, wpm: float = 140.0) -> str:
    total_words = sum(ln.word_count for ln in lines)
    total_sec = round(sum(ln.target_seconds for ln in lines), 1)
    parts = [
        "# Aura design video — full teleprompter script",
        "",
        f"> **Generated from** `vo/scene0.md` … `vo/scene9.md` · **Pace:** ~{wpm:g} wpm",
        f"> **Acts:** {len(lines)} · **Words:** ~{total_words} · **Est. VO:** ~{total_sec}s ({total_sec / 60:.1f} min)",
        "",
        "Read over chapter concat MP4s in `output/`. Extend holds with `tools/extend_act_holds.py` (no Manim re-render).",
        "",
        "---",
        "",
    ]
    cur_ch: int | None = None
    for ln in lines:
        if ln.chapter != cur_ch:
            cur_ch = ln.chapter
            parts.extend(
                [
                    f"## Chapter {ln.chapter} — {ln.youtube_chapter}",
                    "",
                    f"*{ln.chapter_title}*",
                    "",
                ]
            )
        parts.append(f"### Act {ln.act} — {ln.act_title}")
        if ln.on_screen:
            parts.append(f"**On screen:** {ln.on_screen}")
        parts.append("")
        parts.append(f"> {ln.narration}")
        parts.append("")
        parts.append(f"*{ln.word_count} words · ~{ln.target_seconds}s @ {wpm:g} wpm · source: {ln.source}*")
        parts.append("")
    return "\n".join(parts)


def summarize_chapters(lines: list[VoLine]) -> list[dict]:
    by: dict[int, dict] = {}
    for ln in lines:
        b = by.setdefault(
            ln.chapter,
            {
                "chapter": ln.chapter,
                "title": ln.chapter_title,
                "youtube": ln.youtube_chapter,
                "acts": 0,
                "words": 0,
                "seconds": 0.0,
            },
        )
        b["acts"] += 1
        b["words"] += ln.word_count
        b["seconds"] = round(b["seconds"] + ln.target_seconds, 1)
    return [by[k] for k in sorted(by)]


if __name__ == "__main__":
    import argparse
    import json

    p = argparse.ArgumentParser(description="Parse vo/sceneN.md → teleprompter exports")
    p.add_argument("--wpm", type=float, default=140.0)
    p.add_argument("--json", action="store_true")
    args = p.parse_args()
    lines = parse_all_vo_docs(wpm=args.wpm)
    if args.json:
        print(json.dumps([ln.to_dict() for ln in lines], indent=2))
    else:
        print(export_teleprompter_txt(lines))
