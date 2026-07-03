"""Chapter 9 · ACT 2 — Links"""

from __future__ import annotations

import sys
from pathlib import Path

from manim import *

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from components.labels import on_screen_label
from components.outro import links_card
from review import plop, setup_scene
from theme import ACCENT


def play_act2(scene: Scene, state: dict | None = None) -> dict:
    _ = state
    card = links_card()
    label = on_screen_label("Links")

    scene.play(FadeIn(card, shift=UP * 0.08), run_time=0.85)
    scene.play(Indicate(card[1][1], color=ACCENT, scale_factor=1.02), run_time=0.55)
    scene.play(Indicate(card[1][2], scale_factor=1.02), run_time=0.45)
    scene.play(FadeIn(label, shift=UP * 0.1), run_time=0.5)
    scene.wait(4.0)
    scene.play(FadeOut(card, label), run_time=0.7)
    return {}


class Scene9Act2Layout(Scene):
    def construct(self) -> None:
        setup_scene(self)
        plop(self, links_card(), "links card", wait=3.0)
        plop(self, on_screen_label("Links"), "on_screen_label", wait=3.0)


class Scene9Act2(Scene):
    def construct(self) -> None:
        setup_scene(self)
        play_act2(self)
