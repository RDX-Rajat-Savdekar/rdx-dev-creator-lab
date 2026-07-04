"""Layout primitives — ch 6+ must use these instead of ad-hoc ORIGIN anchoring.

Rules:
- Build with ``VGroup(...).arrange(RIGHT|DOWN)``, then ``fit_center``.
- Draw arrows **after** final positions.
- Never scale a group that contains readable ``Text`` (use ``typography.body_text``).
"""

from __future__ import annotations

from manim import Arrow, LEFT, Mobject, ORIGIN, RoundedRectangle, RIGHT, UP, VGroup, config

from theme import ACCENT, WHITE_TEXT
from typography import body_text, caption_line


def fit_center(group: Mobject, *, margin: float = 1.0) -> Mobject:
    """Keep the whole group inside the frame and center on ORIGIN."""
    max_w = config.frame_width - margin
    if group.width > max_w:
        group.scale_to_fit_width(max_w)
    group.move_to(ORIGIN)
    return group


def flow_lr(*parts: Mobject, buff: float = 0.6, margin: float = 1.0) -> VGroup:
    """Arrange parts left → right, then center in frame."""
    row = VGroup(*parts).arrange(RIGHT, buff=buff, aligned_edge=UP)
    return fit_center(row, margin=margin)


def arrow_between(
    left: Mobject,
    right: Mobject,
    *,
    buff: float = 0.15,
    color=ACCENT,
    stroke_width: float = 2.8,
    tip_length: float = 0.16,
    max_tip_length_to_length_ratio: float = 0.28,
) -> Arrow:
    """Arrow after layout — attach right edge of ``left`` to left edge of ``right``."""
    return Arrow(
        left.get_right(),
        right.get_left(),
        buff=buff,
        color=color,
        stroke_width=stroke_width,
        tip_length=tip_length,
        max_tip_length_to_length_ratio=max_tip_length_to_length_ratio,
        max_stroke_width_to_length_ratio=12,
    )


def tag_above(
    panel: Mobject,
    text: str,
    *,
    color: str | None = None,
    align_left: bool = True,
) -> VGroup:
    """Caption tag above a panel."""
    tag = caption_line(text)
    if color is not None:
        tag.set_color(color)
    tag.next_to(panel, UP, buff=0.22)
    if align_left:
        tag.align_to(panel, LEFT)
    else:
        tag.match_x(panel)
    return VGroup(tag, panel)


def labeled_card(
    text: str,
    *,
    tag: str | None = None,
    stroke: str = ACCENT,
    font_size: int = 16,
    min_w: float = 3.6,
    color: str | None = None,
) -> VGroup:
    """Readable text inside a rounded plate; optional tag above."""
    body = body_text(text, font_size=font_size, color=color or WHITE_TEXT)
    plate = RoundedRectangle(
        corner_radius=0.1,
        width=max(body.width + 0.48, min_w),
        height=body.height + 0.32,
        fill_color="#1e1e28",
        fill_opacity=1,
        stroke_color=stroke,
        stroke_width=1.2,
        stroke_opacity=0.55,
    )
    body.move_to(plate.get_center())
    card = VGroup(plate, body)
    if tag is None:
        return card
    return tag_above(card, tag)
