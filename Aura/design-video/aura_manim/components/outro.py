"""Outro beats — chapter 9 recap, links, end card."""

from __future__ import annotations

from manim import *

from components.layout import fit_center
from components.pipeline import dual_pipeline_group
from theme import ACCENT, MERGE_OK, MUTED, SUBTEXT, WHITE_TEXT
from typography import body_text, subtext


def _mini_pipeline() -> VGroup:
    bits = dual_pipeline_group()
    diagram = bits["diagram"]
    diagram.scale(0.72)
    return diagram


def recap_diagram() -> VGroup:
    """One-line recap + mini dual pipeline."""
    line = body_text(
        "One tap · on-device speech + sound · captions in view",
        font_size=18,
    )
    pipe = _mini_pipeline()
    group = VGroup(line, pipe).arrange(DOWN, buff=0.35)
    fit_center(group)
    group.shift(UP * 0.08)
    return group


def links_card() -> VGroup:
    """Repo link + pointer to YouTube description for full link list."""
    title = body_text("Links", font_size=22, color=WHITE_TEXT, weight=BOLD)
    repo = body_text(
        "github.com/RDX-Rajat-Savdekar/Aura-Vision-Pro",
        font_size=16,
        color=ACCENT,
    )
    note = subtext("All links in the video description")
    note.set_color(SUBTEXT)
    body = VGroup(title, repo, note).arrange(DOWN, buff=0.2, aligned_edge=LEFT)
    plate = RoundedRectangle(
        corner_radius=0.14,
        width=body.width + 0.7,
        height=body.height + 0.5,
        fill_color="#14141c",
        fill_opacity=1,
        stroke_color=MUTED,
        stroke_width=1.5,
    )
    body.move_to(plate.get_center())
    card = VGroup(plate, body)
    fit_center(card)
    return card


def end_card() -> VGroup:
    """Hackathon outcome — end slate."""
    title = body_text("2nd place · Oct 2025", font_size=28, color=WHITE_TEXT, weight=BOLD)
    sub = subtext("Aura · visionOS accessibility prototype")
    sub.set_color(MERGE_OK)
    body = VGroup(title, sub).arrange(DOWN, buff=0.22)
    plate = RoundedRectangle(
        corner_radius=0.16,
        width=body.width + 0.8,
        height=body.height + 0.55,
        fill_color="#14141c",
        fill_opacity=1,
        stroke_color=ACCENT,
        stroke_width=2,
    )
    body.move_to(plate.get_center())
    card = VGroup(plate, body)
    fit_center(card)
    return card
