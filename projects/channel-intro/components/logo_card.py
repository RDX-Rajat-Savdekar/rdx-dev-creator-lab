"""RDX channel logo — reveal after Sharingan flash."""

from __future__ import annotations

from manim import *

from theme import ACCENT, CHANNEL_NAME, MUTED, SHARINGAN_RED, TAGLINE, WHITE
from components.sharingan_eye import mini_sharingan_icon


def channel_logo(*, scale: float = 1.0) -> VGroup:
    badge = mini_sharingan_icon(height=0.34 * scale)

    title = Text(CHANNEL_NAME, font="Helvetica Neue", weight=BOLD, font_size=78 * scale)
    title.set_color(WHITE)

    tagline = Text(TAGLINE, font="Helvetica Neue", font_size=24 * scale)
    tagline.set_color(MUTED)

    stack = VGroup(title, tagline).arrange(DOWN, buff=0.24 * scale)
    badge.next_to(title, UP, buff=0.3 * scale)

    frame = SurroundingRectangle(VGroup(badge, stack), color=SHARINGAN_RED, buff=0.38 * scale)
    frame.set_stroke(opacity=0)
    frame.set_fill(opacity=0)
    ring = Circle(radius=frame.width * 0.52, color=SHARINGAN_RED, stroke_width=1.4, stroke_opacity=0.5)
    ring.set_fill(opacity=0)
    ring.move_to(frame.get_center())

    brand = VGroup(ring, badge, stack)

    refl_title = title.copy().set_color(ACCENT).set_opacity(0.18)
    refl_tag = tagline.copy().set_opacity(0.1)
    reflection = VGroup(refl_title, refl_tag).arrange(DOWN, buff=0.24 * scale)
    reflection.stretch(factor=-1, dim=1)
    reflection.next_to(stack, DOWN, buff=0.14 * scale)

    return VGroup(brand, reflection)
