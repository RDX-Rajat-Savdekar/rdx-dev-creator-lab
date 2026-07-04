"""Chapter 9 · ACT 3 — End card"""

from __future__ import annotations

import sys
from pathlib import Path

from manim import *

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from components.labels import on_screen_label
from components.outro import end_card
from review import plop, setup_scene
from theme import MERGE_OK


def play_act3(scene: Scene, state: dict | None = None) -> dict:
    _ = state
    card = end_card()
    label = on_screen_label("2nd place · Oct 2025")

    scene.play(FadeIn(card, shift=UP * 0.1), run_time=0.9)
    scene.play(Indicate(card[1][1], color=MERGE_OK, scale_factor=1.03), run_time=0.55)
    scene.play(FadeIn(label, shift=UP * 0.1), run_time=0.5)
    scene.wait(4.5)
    scene.play(FadeOut(card, label), run_time=0.8)
    return {}


class Scene9Act3Layout(Scene):
    def construct(self) -> None:
        setup_scene(self)
        plop(self, end_card(), "end card", wait=3.0)
        plop(self, on_screen_label("2nd place · Oct 2025"), "on_screen_label", wait=3.0)


class Scene9Act3(Scene):
    def construct(self) -> None:
        setup_scene(self)
        play_act3(self)
