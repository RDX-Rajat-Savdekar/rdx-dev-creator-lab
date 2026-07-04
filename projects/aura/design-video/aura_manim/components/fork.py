"""Vertical split decision fork — chapter 2 build vs train."""

from __future__ import annotations

from manim import *

from theme import ACCENT, FONT, MUTED, WHITE_TEXT

COL_W = 3.35
COL_H = 2.75
DIVIDER_BUFF = 0.28


def _column_box(*, accent: bool = False) -> RoundedRectangle:
    return RoundedRectangle(
        corner_radius=0.18,
        width=COL_W,
        height=COL_H,
        stroke_color=ACCENT if accent else MUTED,
        stroke_width=2.5 if accent else 1.5,
        stroke_opacity=1 if accent else 0.55,
        fill_color="#14141c",
        fill_opacity=0.65 if accent else 0.35,
    )


def vertical_fork(
    *,
    left_label: str = "Train custom model",
    right_label: str = "Integrate Apple ML",
    selected: str = "right",
) -> dict[str, Mobject]:
    """Two-column fork. ``selected``: ``left`` | ``right`` | ``none``."""
    left_box = _column_box(accent=(selected == "left"))
    right_box = _column_box(accent=(selected == "right"))
    left_text = Text(left_label, font=FONT, font_size=20, color=WHITE_TEXT)
    right_text = Text(right_label, font=FONT, font_size=20, color=WHITE_TEXT)
    left_text.move_to(left_box.get_center())
    right_text.move_to(right_box.get_center())
    left_col = VGroup(left_box, left_text)
    right_col = VGroup(right_box, right_text)

    divider = Line(UP * COL_H / 2, DOWN * COL_H / 2, color=MUTED, stroke_width=1.2, stroke_opacity=0.4)
    fork = VGroup(left_col, divider, right_col)
    fork.arrange(RIGHT, buff=DIVIDER_BUFF, aligned_edge=DOWN)
    fork.move_to(ORIGIN + UP * 0.15)

    return {
        "fork": fork,
        "left": left_col,
        "right": right_col,
        "left_box": left_box,
        "right_box": right_box,
        "divider": divider,
    }
