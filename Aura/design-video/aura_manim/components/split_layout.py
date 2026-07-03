"""Two-pane layout — visual (top) + Swift code (bottom).

Use for any act that pairs a diagram with a code snippet. Each pane has fixed
max width/height; content is scaled to fit so panes never overlap.

    from components.split_layout import split_layout

    bits = split_layout(my_diagram, "tap_install.swift", highlight=(1, 4))
    scene.play(FadeIn(bits["visual"]), ...)
    scene.play(FadeIn(bits["code_group"]), ...)
"""

from __future__ import annotations

from manim import *

from code_panel import highlight_lines, panel_title, swift_panel
from theme import MUTED

# Manim frame ≈ 14.22 × 8. Bottom label sits at DOWN*0.55 — keep panes above it.
LABEL_RESERVE = 0.9

DIVIDER_Y = 0.35
PANE_GAP = 0.28

VISUAL_REGION_TOP = 3.15
VISUAL_REGION_BOTTOM = DIVIDER_Y + PANE_GAP
VISUAL_PANE_MAX_W = 12.4

CODE_REGION_TOP = DIVIDER_Y - PANE_GAP
CODE_REGION_BOTTOM = -2.75
CODE_PANE_MAX_W = 7.0
CODE_FONT_SIZE = 16


def _region_center_and_size(top: float, bottom: float) -> tuple[np.ndarray, float]:
    return np.array([0.0, (top + bottom) / 2, 0.0]), top - bottom


def _fit_in_region(
    mob: Mobject,
    *,
    top: float,
    bottom: float,
    max_w: float,
) -> Mobject:
    center, max_h = _region_center_and_size(top, bottom)
    mob.move_to(center)
    if mob.width > max_w:
        mob.scale(max_w / mob.width)
    if mob.height > max_h:
        mob.scale(max_h / mob.height)
    mob.move_to(center)
    if mob.get_top()[1] > top:
        mob.shift(DOWN * (mob.get_top()[1] - top))
    if mob.get_bottom()[1] < bottom:
        mob.shift(UP * (bottom - mob.get_bottom()[1]))
    return mob


def place_visual_pane(visual: Mobject) -> Mobject:
    """Scale and place a diagram into the top region (cannot cross divider)."""
    return _fit_in_region(
        visual,
        top=VISUAL_REGION_TOP,
        bottom=VISUAL_REGION_BOTTOM,
        max_w=VISUAL_PANE_MAX_W,
    )


def build_code_pane(
    filename: str,
    *,
    highlight: tuple[int, ...] = (),
    font_size: int = CODE_FONT_SIZE,
) -> dict[str, Mobject]:
    """Fixed-width code block for the bottom region."""
    code = swift_panel(filename, font_size=font_size)
    title = panel_title(filename)
    title.next_to(code, UP, buff=0.2, aligned_edge=LEFT)
    group = VGroup(title, code)
    _fit_in_region(
        group,
        top=CODE_REGION_TOP,
        bottom=CODE_REGION_BOTTOM,
        max_w=CODE_PANE_MAX_W,
    )
    rects = highlight_lines(code, highlight) if highlight else VGroup()
    return {
        "code": code,
        "title": title,
        "code_group": group,
        "highlights": rects,
    }


def pane_divider(*, opacity: float = 0.22) -> Line:
    """Optional guide for layout plop — faint split between panes."""
    line = Line(LEFT * 6.6, RIGHT * 6.6, color=MUTED, stroke_width=1)
    line.move_to(np.array([0.0, DIVIDER_Y, 0.0]))
    line.set_opacity(opacity)
    return line


def split_layout(
    visual: Mobject,
    snippet: str,
    *,
    highlight: tuple[int, ...] = (),
    font_size: int = CODE_FONT_SIZE,
) -> dict[str, Mobject]:
    """Place visual in top pane + code in bottom pane. Returns animation handles."""
    place_visual_pane(visual)
    code_bits = build_code_pane(snippet, highlight=highlight, font_size=font_size)
    return {
        "visual": visual,
        **code_bits,
    }
