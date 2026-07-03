"""Readable on-screen text — use instead of ``Text(..., color=MUTED, font_size=15)``.

Rule (Aura dark theme):
- **MUTED** → strokes, dividers, plop layout tags, de-emphasized *chrome* (not sentences).
- **SUBTEXT** + **≥ SUBTEXT_SIZE** → secondary lines viewers must read (captions, subtitles, chips).
- **WHITE_TEXT** → primary labels inside cards and nodes.
- **ACCENT** → highlighted keywords only (short chips, not paragraphs).
"""

from __future__ import annotations

from manim import BOLD, Text

from theme import (
    ACCENT,
    BODY_SIZE,
    CAPTION_SIZE,
    CHIP_SIZE,
    FONT,
    NODE_SIZE,
    SUBTEXT,
    SUBTEXT_SIZE,
    WHITE_TEXT,
)


def subtext(
    text: str,
    *,
    font_size: int = SUBTEXT_SIZE,
    color: str = SUBTEXT,
) -> Text:
    """Secondary readable line on dark panels."""
    return Text(text, font=FONT, font_size=font_size, color=color)


def caption(text: str) -> Text:
    """Short annotation (e.g. timeline footnotes)."""
    return Text(text, font=FONT, font_size=CAPTION_SIZE, color=SUBTEXT)


def chip_label(text: str, *, accent: bool = False) -> Text:
    """Small keyword under a diagram node."""
    return Text(
        text,
        font=FONT,
        font_size=CHIP_SIZE,
        color=ACCENT if accent else SUBTEXT,
    )


def node_label(text: str, *, accent: bool = False) -> Text:
    """Text inside a pipeline / fork node box."""
    return Text(
        text,
        font=FONT,
        font_size=NODE_SIZE,
        color=WHITE_TEXT if accent else SUBTEXT,
    )


def title_line(text: str, *, font_size: int = BODY_SIZE) -> Text:
    """Primary line inside a card."""
    return Text(text, font=FONT, font_size=font_size, color=WHITE_TEXT, weight=BOLD)
