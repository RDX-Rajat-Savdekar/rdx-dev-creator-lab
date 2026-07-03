"""Classifier confidence + throttle gate — chapter 3 act 4."""

from __future__ import annotations

from manim import *

from theme import ACCENT, FONT, MUTED, SUBTEXT, WARN, WHITE_TEXT
from typography import caption, subtext

RULE_H = 0.56


def _rule_chip(text: str, *, accent: bool = False) -> VGroup:
    label = Text(text, font=FONT, font_size=17, color=WHITE_TEXT)
    plate = RoundedRectangle(
        corner_radius=0.1,
        width=label.width + 0.38,
        height=RULE_H,
        fill_color="#1e1e28",
        fill_opacity=1,
        stroke_color=ACCENT if accent else MUTED,
        stroke_width=1.5 if accent else 1.1,
        stroke_opacity=0.65 if accent else 0.4,
    )
    label.move_to(plate.get_center())
    return VGroup(plate, label)


def _flap_demo() -> VGroup:
    """Noisy labels dimmed; stable label kept."""
    flaky = VGroup(
        Text("clap?", font=FONT, font_size=15, color=SUBTEXT),
        Text("tap?", font=FONT, font_size=15, color=SUBTEXT),
    ).arrange(RIGHT, buff=0.28)
    for word in flaky:
        strike = Line(word.get_left(), word.get_right(), color=WARN, stroke_width=2)
        strike.move_to(word.get_center())
        word.set_opacity(0.45)

    stable = Text("clapping", font=FONT, font_size=16, color=ACCENT, weight=BOLD)
    row = VGroup(flaky, stable).arrange(DOWN, buff=0.22, aligned_edge=LEFT)
    return row


def classifier_gate_card() -> VGroup:
    title = caption("Anti-flap gate")
    rules = VGroup(
        _rule_chip("confidence ≥ 0.6", accent=True),
        _rule_chip("0.25 s throttle"),
    )
    rules.arrange(DOWN, buff=0.16, aligned_edge=LEFT)
    demo = _flap_demo()
    body = VGroup(title, rules, demo).arrange(DOWN, buff=0.28, aligned_edge=LEFT)
    glass = RoundedRectangle(
        corner_radius=0.16,
        width=body.width + 0.55,
        height=body.height + 0.5,
        fill_color="#14141c",
        fill_opacity=0.96,
        stroke_color=ACCENT,
        stroke_width=1.5,
        stroke_opacity=0.55,
    )
    body.move_to(glass.get_center())
    return VGroup(glass, body)


def classifier_gate_group() -> dict[str, Mobject]:
    card = classifier_gate_card()
    note = subtext("environmental sounds · no label spam")
    note.next_to(card, DOWN, buff=0.28)
    return {"card": card, "note": note, "diagram": VGroup(card, note)}
