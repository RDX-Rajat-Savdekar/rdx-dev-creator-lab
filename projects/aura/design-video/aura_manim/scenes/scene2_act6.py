"""
Chapter 2 · ACT 6 — Honesty card
SCENE-PLAN: 3:50–4:05

Prev: scene2_act5.py · Assembly: scene2_full.py

Render:
  manim -ql scenes/scene2_act6.py Scene2Act6Layout
  manim -ql scenes/scene2_act6.py Scene2Act6
"""

from __future__ import annotations

import sys
from pathlib import Path

from manim import *

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from components.honesty_card import honesty_card
from components.labels import on_screen_label
from review import plop, setup_scene


def act6_pieces() -> dict[str, Mobject]:
    card = honesty_card(
        "Integrated, not trained",
        "Engineering = pipeline · segmentation · UI",
    )
    label = on_screen_label("Integrated, not trained")
    return {
        "honesty card": card,
        "on_screen_label": label,
    }


class Scene2Act6Layout(Scene):
    def construct(self) -> None:
        setup_scene(self)
        for name, mob in act6_pieces().items():
            plop(self, mob, name, wait=3.0)


def play_act6(scene: Scene, state: dict | None = None) -> dict:
    """ACT 6 — scope lock."""
    _ = state
    card = honesty_card(
        "Integrated, not trained",
        "Engineering = pipeline · segmentation · UI",
    )
    label = on_screen_label("Integrated, not trained")

    # PLAY 1
    scene.play(FadeIn(card, shift=UP * 0.08), run_time=0.75)
    # PLAY 2 — subtitle already on card; brief emphasis
    scene.play(Indicate(card, scale_factor=1.02), run_time=0.45)
    # PLAY 3
    scene.play(FadeIn(label, shift=UP * 0.1), run_time=0.5)
    scene.wait(5.5)
    # PLAY 4
    scene.play(FadeOut(card, label), run_time=0.7)
    return {}


class Scene2Act6(Scene):
    def construct(self) -> None:
        setup_scene(self)
        play_act6(self)
