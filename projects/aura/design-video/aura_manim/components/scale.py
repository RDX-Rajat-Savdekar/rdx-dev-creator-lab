"""Prototype vs product scale — chapter 8 story visuals."""

from __future__ import annotations

from manim import *

from components.layout import arrow_between, fit_center, flow_lr, labeled_card
from theme import ACCENT, MUTED, SUBTEXT, WARN, WHITE_TEXT
from typography import body_text, caption_line, subtext

STAMP_FILL = "#1c1010"


def prototype_limits_diagram() -> VGroup:
    """What the hackathon prototype is — honest scope."""
    header = caption_line("Hackathon prototype · not production")
    header.set_color(SUBTEXT)
    chips = flow_lr(
        labeled_card("single user", tag="today", stroke=MUTED, min_w=2.8),
        labeled_card("no benchmarks", tag="today", stroke=MUTED, min_w=2.8),
        labeled_card("qualitative only", tag="today", stroke=MUTED, min_w=2.8),
        buff=0.45,
    )
    note = subtext("thermal · battery · latency — not measured")
    group = VGroup(header, chips, note)
    header.next_to(chips, UP, buff=0.28).align_to(chips, LEFT)
    note.next_to(chips, DOWN, buff=0.28).align_to(chips, LEFT)
    fit_center(group)
    group.shift(UP * 0.1)
    return group


def product_would_change_diagram() -> VGroup:
    """Two-column: today vs product architecture."""
    today = labeled_card(
        "on-device only\nsingle locale bundle",
        tag="today",
        stroke=MUTED,
        min_w=4.2,
    )
    today.set_opacity(0.55)
    product = labeled_card(
        "locale CDN · observability\nmulti-user · fleet metrics",
        tag="product would add",
        stroke=ACCENT,
        min_w=4.2,
    )
    row = flow_lr(today, product, buff=0.75)
    arrow = arrow_between(today, product, tip_length=0.18, max_tip_length_to_length_ratio=0.32)
    note = subtext("same core pipeline — different ops envelope")
    note.next_to(row, DOWN, buff=0.28)
    group = VGroup(row, arrow, note)
    fit_center(group)
    group.shift(UP * 0.08)
    return group


def never_claim_stamp() -> VGroup:
    """Red stamp — metrics we do not claim."""
    title = body_text("Never claim", font_size=22, color=WHITE_TEXT, weight=BOLD)
    lines = VGroup(
        body_text("latency % or speedup", font_size=16, color=WHITE_TEXT),
        body_text("production user metrics", font_size=16, color=WHITE_TEXT),
        body_text("benchmark artifacts", font_size=16, color=WHITE_TEXT),
    ).arrange(DOWN, buff=0.14, aligned_edge=LEFT)
    body = VGroup(title, lines).arrange(DOWN, buff=0.22, aligned_edge=LEFT)
    plate = RoundedRectangle(
        corner_radius=0.14,
        width=body.width + 0.65,
        height=body.height + 0.5,
        fill_color=STAMP_FILL,
        fill_opacity=1,
        stroke_color=WARN,
        stroke_width=2.5,
    )
    body.move_to(plate.get_center())
    stamp = VGroup(plate, body)
    cross = Line(
        stamp.get_corner(UL) + UP * 0.08 + LEFT * 0.08,
        stamp.get_corner(DR) + DOWN * 0.08 + RIGHT * 0.08,
        color=WARN,
        stroke_width=3.5,
    )
    group = VGroup(stamp, cross)
    fit_center(group)
    return group
