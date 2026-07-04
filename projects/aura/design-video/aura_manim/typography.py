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


def body_text(
    text: str,
    *,
    font_size: int = 16,
    color: str = WHITE_TEXT,
    width: float | None = None,
    line_spacing: float = 1.15,
    weight=None,
) -> Text:
    """Readable copy on dark panels — ch 6+ default for any sentence viewers read.

    Always uses ``disable_ligatures=True`` to avoid glued words (``dumpsat``).
    Do **not** put ``body_text`` inside a scaled ``VGroup`` — size the plate instead.
    """
    kwargs: dict = dict(
        font=FONT,
        font_size=font_size,
        color=color,
        disable_ligatures=True,
        line_spacing=line_spacing,
    )
    if width is not None:
        kwargs["width"] = width
    if weight is not None:
        kwargs["weight"] = weight
    return Text(text, **kwargs)


def caption_line(text: str, *, color: str = SUBTEXT, font_size: int = CAPTION_SIZE) -> Text:
    """Short tag above a panel (``formattedString → UI``). Same spacing rules as ``body_text``."""
    return body_text(text, font_size=font_size, color=color)


def subtext(
    text: str,
    *,
    font_size: int = SUBTEXT_SIZE,
    color: str = SUBTEXT,
) -> Text:
    """Secondary readable line on dark panels."""
    return body_text(text, font_size=font_size, color=color)


def caption(text: str) -> Text:
    """Short annotation (e.g. timeline footnotes)."""
    return caption_line(text)


def chip_label(text: str, *, accent: bool = False) -> Text:
    """Small keyword under a diagram node."""
    return body_text(
        text,
        font_size=CHIP_SIZE,
        color=ACCENT if accent else SUBTEXT,
    )


def node_label(text: str, *, accent: bool = False) -> Text:
    """Text inside a pipeline / fork node box."""
    return body_text(
        text,
        font_size=NODE_SIZE,
        color=WHITE_TEXT if accent else SUBTEXT,
    )


def title_line(text: str, *, font_size: int = BODY_SIZE) -> Text:
    """Primary line inside a card."""
    return body_text(text, font_size=font_size, color=WHITE_TEXT, weight=BOLD)
