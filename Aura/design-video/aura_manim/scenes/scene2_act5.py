"""
Chapter 2 · ACT 5 — Outcome + B-roll proof
SCENE-PLAN: 3:35–3:50

Prev: scene2_act4.py · Next: scene2_act6.py · Assembly: scene2_full.py

Render:
  manim -ql scenes/scene2_act5.py Scene2Act5Layout
  manim -ql scenes/scene2_act5.py Scene2Act5
"""

from __future__ import annotations

import sys
from pathlib import Path

from manim import *

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from broll import D4_SIREN, D5_CLAPPING, broll_still, play_montage
from components.honesty_card import outcome_card
from components.labels import on_screen_label
from review import plop, setup_scene

MONTAGE_SEGMENTS = [
    (D4_SIREN, 0.0, 3.0),
    (D5_CLAPPING, 0.0, 3.0),
]


def act5_pieces() -> dict[str, Mobject]:
    card = outcome_card()
    still = broll_still(D4_SIREN, width=10.0).next_to(card, DOWN, buff=0.45)
    label = on_screen_label("2nd place · working demo")
    return {
        "outcome card": card,
        "broll preview (D4)": still,
        "on_screen_label": label,
    }


class Scene2Act5Layout(Scene):
    def construct(self) -> None:
        setup_scene(self)
        for name, mob in act5_pieces().items():
            plop(self, mob, name, wait=3.0)


def play_act5(scene: Scene, state: dict | None = None) -> dict:
    """ACT 5 — 2nd place card + D4/D5 montage."""
    _ = state
    card = outcome_card()
    label = on_screen_label("2nd place · working demo")

    # PLAY 1
    scene.play(FadeIn(card, shift=DOWN * 0.08), run_time=0.7)
    # PLAY 2
    play_montage(scene, MONTAGE_SEGMENTS, fade_in=0.15, fade_out=0.15)
    # PLAY 3
    scene.play(FadeIn(label, shift=UP * 0.1), run_time=0.5)
    scene.wait(4.5)
    # PLAY 4
    scene.play(FadeOut(card, label), run_time=0.7)
    return {}


class Scene2Act5(Scene):
    def construct(self) -> None:
        setup_scene(self)
        play_act5(self)
