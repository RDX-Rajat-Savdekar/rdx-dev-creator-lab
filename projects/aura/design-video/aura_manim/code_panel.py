"""Swift code panels — snippet file + line highlight (ch 1, 3, 4, 5, 6)."""

from __future__ import annotations

from pathlib import Path

from manim import *

from theme import ACCENT, FONT, MUTED, WARN, WHITE_TEXT
from typography import subtext

SNIPPETS_DIR = Path(__file__).resolve().parents[1] / "code_snippets"

# Readable on #12121a — Pygments default Swift comment blue is too dark.
SWIFT_COMMENT = "#7c8f9f"
SWIFT_KEYWORD = "#ff7ab2"
SWIFT_TYPE = "#d9c97c"
SWIFT_IDENT = "#9cdcfe"
SWIFT_BOOL = "#d9c97c"

DEFAULT_PARAGRAPH = {
    "font": "Monospace",
    "font_size": 18,
    "line_spacing": 0.34,
}

COMPACT_PARAGRAPH = {
    "font": "Monospace",
    "font_size": 16,
    "line_spacing": 0.3,
}


def snippet_path(name: str) -> Path:
    path = SNIPPETS_DIR / name
    if not path.exists():
        raise FileNotFoundError(f"Missing snippet: {path}")
    return path


def _token_text(token: Mobject) -> str:
    if hasattr(token, "text"):
        return str(token.text)
    if token.submobjects:
        return "".join(_token_text(c) for c in token.submobjects)
    return ""


def _tone_swift_line(line: Mobject) -> None:
    for token in line.submobjects:
        raw = _token_text(token)
        if raw in {"let", "true", "false", "private"}:
            token.set_color(SWIFT_KEYWORD)
        elif raw.startswith("SFSpeech") or raw.endswith("()"):
            token.set_color(SWIFT_TYPE)
        elif raw in {"request", "analysisQueue"}:
            token.set_color(SWIFT_IDENT)
        elif raw.startswith("//"):
            token.set_color(SWIFT_COMMENT)
        else:
            token.set_color(WHITE_TEXT)


def swift_panel(
    filename: str,
    *,
    add_line_numbers: bool = False,
    font_size: int = 18,
) -> Code:
    paragraph = {**DEFAULT_PARAGRAPH, "font_size": font_size}
    if font_size <= 16:
        paragraph = {**COMPACT_PARAGRAPH, "font_size": font_size}
    code = Code(
        code_file=str(snippet_path(filename)),
        language="swift",
        tab_width=4,
        add_line_numbers=add_line_numbers,
        background="window",
        background_config={
            "fill_color": "#12121a",
            "fill_opacity": 1,
            "stroke_color": MUTED,
            "stroke_width": 1.5,
            "corner_radius": 0.12,
        },
        paragraph_config=paragraph,
    )
    for line in code.code_lines:
        if line.submobjects:
            _tone_swift_line(line)
    return code


def panel_title(filename: str) -> Text:
    return subtext(filename, font_size=17)


def highlight_lines(
    panel: Code,
    line_indices: tuple[int, ...],
    *,
    color: str = ACCENT,
) -> VGroup:
    """0-based indices into ``panel.code_lines``."""
    rects = VGroup(
        *[
            BackgroundRectangle(
                panel.code_lines[i],
                color=color,
                buff=0.08,
                fill_opacity=0.22,
                stroke_width=0,
            )
            for i in line_indices
            if i < len(panel.code_lines.submobjects)
        ]
    )
    return rects


def swift_panel_group(
    filename: str,
    *,
    highlight: tuple[int, ...] = (),
    font_size: int = 18,
    position: np.ndarray | None = None,
) -> tuple[Code, Text, VGroup]:
    """Title + code block — use ``position`` for stacked layouts (diagram above)."""
    code = swift_panel(filename, font_size=font_size)
    title = panel_title(filename)
    title.next_to(code, UP, buff=0.22, aligned_edge=LEFT)
    if position is not None:
        VGroup(title, code).move_to(position)
    rects = highlight_lines(code, highlight) if highlight else VGroup()
    return code, title, rects


def play_highlight(
    scene: Scene,
    panel: Code,
    line_indices: tuple[int, ...],
    *,
    run_time: float = 0.9,
) -> VGroup:
    rects = highlight_lines(panel, line_indices)
    scene.play(FadeIn(rects), run_time=run_time)
    return rects
