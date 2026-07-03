"""Bold honesty cards — chapter 2 act 6, reusable."""

from __future__ import annotations

from manim import *

from theme import ACCENT, FONT, MERGE_OK, MUTED, WHITE_TEXT
from typography import subtext


def honesty_card(
    title: str,
    subtitle: str,
    *,
    stroke_color: str = MERGE_OK,
) -> VGroup:
    title_mob = Text(title, font=FONT, font_size=26, color=WHITE_TEXT, weight=BOLD)
    subtitle_mob = subtext(subtitle)
    body = VGroup(title_mob, subtitle_mob).arrange(DOWN, buff=0.22, aligned_edge=LEFT)
    plate = RoundedRectangle(
        corner_radius=0.16,
        width=body.width + 0.75,
        height=body.height + 0.55,
        fill_color="#14141c",
        fill_opacity=1,
        stroke_color=stroke_color,
        stroke_width=2,
    )
    body.move_to(plate.get_center())
    return VGroup(plate, body)


def outcome_card() -> VGroup:
    title = Text("2nd place · working demo", font=FONT, font_size=26, color=WHITE_TEXT, weight=BOLD)
    subtitle = subtext("Traded ML research for a shipped prototype")
    body = VGroup(title, subtitle).arrange(DOWN, buff=0.2, aligned_edge=LEFT)
    plate = RoundedRectangle(
        corner_radius=0.14,
        width=body.width + 0.6,
        height=body.height + 0.5,
        fill_color="#14141c",
        fill_opacity=1,
        stroke_color=ACCENT,
        stroke_width=1.5,
    )
    body.move_to(plate.get_center())
    return VGroup(plate, body).move_to(UP * 2.35)
