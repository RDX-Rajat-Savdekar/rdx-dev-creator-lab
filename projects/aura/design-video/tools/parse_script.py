"""Parse Aura design-video SCRIPT.md into narration lines for VO tools."""

from __future__ import annotations

import re
from dataclasses import asdict, dataclass


@dataclass
class NarrationLine:
    chapter: int
    chapter_title: str
    line_index: int
    narration: str
    on_screen: str
    visual: str
    word_count: int
    target_seconds: float

    def to_dict(self) -> dict:
        return asdict(self)


CHAPTER_RE = re.compile(r"^## Chapter (\d+)\s*[—–-]\s*(.+)$", re.MULTILINE)
TABLE_ROW_RE = re.compile(r"^\|(.+)\|$")


def _strip_md_inline(text: str) -> str:
    """Light cleanup for teleprompter display."""
    text = re.sub(r"\*\*(.+?)\*\*", r"\1", text)
    text = re.sub(r"\*(.+?)\*", r"\1", text)
    text = re.sub(r"`([^`]+)`", r"\1", text)
    return text.strip()


def _word_count(text: str) -> int:
    clean = _strip_md_inline(text)
    if not clean:
        return 0
    return len(clean.split())


def _split_table_row(row: str) -> list[str]:
    parts = [p.strip() for p in row.split("|")]
    if parts and parts[0] == "":
        parts = parts[1:]
    if parts and parts[-1] == "":
        parts = parts[:-1]
    return parts


def parse_script(markdown: str, wpm: float = 140.0) -> list[NarrationLine]:
    """Extract narration rows from SCRIPT.md chapter tables."""
    if wpm <= 0:
        wpm = 140.0

    chapters: list[tuple[int, str, int, int]] = []
    for m in CHAPTER_RE.finditer(markdown):
        chapters.append((int(m.group(1)), m.group(2).strip(), m.start(), m.end()))

    if not chapters:
        return []

    lines: list[NarrationLine] = []
    for i, (num, title, _start, end) in enumerate(chapters):
        chunk_end = chapters[i + 1][2] if i + 1 < len(chapters) else len(markdown)
        chunk = markdown[end:chunk_end]

        in_table = False
        line_index = 0
        for raw in chunk.splitlines():
            if not raw.strip().startswith("|"):
                in_table = False
                continue

            cells = _split_table_row(raw.strip())
            if len(cells) < 3:
                continue

            header = cells[0].lower()
            if header == "narration":
                in_table = True
                continue
            if not in_table:
                continue
            if re.match(r"^[-:\s|]+$", raw):
                continue

            narration = _strip_md_inline(cells[0])
            if not narration or narration.lower() == "narration":
                continue

            on_screen = _strip_md_inline(cells[1]) if len(cells) > 1 else ""
            visual = _strip_md_inline(cells[2]) if len(cells) > 2 else ""
            words = _word_count(narration)
            target_seconds = round((words / wpm) * 60, 1)

            lines.append(
                NarrationLine(
                    chapter=num,
                    chapter_title=title,
                    line_index=line_index,
                    narration=narration,
                    on_screen=on_screen,
                    visual=visual,
                    word_count=words,
                    target_seconds=target_seconds,
                )
            )
            line_index += 1

    return lines


def export_teleprompter_text(lines: list[NarrationLine], chapter: int | None = None) -> str:
    """Plain narration export for phone teleprompter apps."""
    out: list[str] = []
    current_ch: int | None = None
    for line in lines:
        if chapter is not None and line.chapter != chapter:
            continue
        if line.chapter != current_ch:
            current_ch = line.chapter
            out.append("")
            out.append(f"=== Chapter {line.chapter} — {line.chapter_title} ===")
            out.append("")
        out.append(line.narration)
        out.append("")
    return "\n".join(out).strip() + "\n"


def summarize_by_chapter(lines: list[NarrationLine]) -> list[dict]:
    """Per-chapter word totals and estimated duration."""
    by_ch: dict[int, dict] = {}
    for line in lines:
        bucket = by_ch.setdefault(
            line.chapter,
            {
                "chapter": line.chapter,
                "title": line.chapter_title,
                "lines": 0,
                "words": 0,
                "seconds": 0.0,
            },
        )
        bucket["lines"] += 1
        bucket["words"] += line.word_count
        bucket["seconds"] = round(bucket["seconds"] + line.target_seconds, 1)
    return [by_ch[k] for k in sorted(by_ch)]
