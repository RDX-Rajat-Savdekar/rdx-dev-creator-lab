"""Weeks vs hours timeline comparison — chapter 2 act 3."""

from __future__ import annotations

from manim import *

from theme import ACCENT, FONT, MUTED, SUBTEXT, SUBTEXT_SIZE
from typography import caption, subtext

WEEKS_W = 4.6
HOURS_W = 1.35
BAR_H = 0.52


def weeks_vs_hours_bar() -> VGroup:
    weeks_rect = RoundedRectangle(
        corner_radius=0.1,
        width=WEEKS_W,
        height=BAR_H,
        fill_color="#1c1c26",
        fill_opacity=1,
        stroke_color=MUTED,
        stroke_width=1.2,
        stroke_opacity=0.5,
    )
    weeks_label = subtext("weeks")
    weeks_label.move_to(weeks_rect.get_center())
    weeks = VGroup(weeks_rect, weeks_label)

    hours_rect = RoundedRectangle(
        corner_radius=0.1,
        width=HOURS_W,
        height=BAR_H,
        fill_color="#0f2a38",
        fill_opacity=1,
        stroke_color=ACCENT,
        stroke_width=2,
    )
    hours_label = Text("hours", font=FONT, font_size=SUBTEXT_SIZE, color=ACCENT)
    hours_label.move_to(hours_rect.get_center())
    hours = VGroup(hours_rect, hours_label)

    group = VGroup(weeks, hours).arrange(RIGHT, buff=0.35, aligned_edge=DOWN)
    cap = caption("24h hackathon")
    cap.next_to(hours, UP, buff=0.18).align_to(hours, LEFT)
    return VGroup(group, cap).move_to(DOWN * 2.05)
