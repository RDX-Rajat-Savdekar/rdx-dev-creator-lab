"""Chapter 4 · ACT 1 — formattedString wall of text"""

from __future__ import annotations

import sys
from pathlib import Path

from manim import *

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from components.labels import on_screen_label
from components.segmentation import wall_of_text
from review import plop, setup_scene


def play_act1(scene: Scene, state: dict | None = None) -> dict:
    _ = state
    wall = wall_of_text()
    label = on_screen_label("Wall of text")

    scene.play(FadeIn(wall, shift=UP * 0.08), run_time=0.85)
    scene.play(FadeIn(label, shift=UP * 0.1), run_time=0.5)
    scene.wait(5.5)
    scene.play(FadeOut(wall, label), run_time=0.7)
    return {}


class Scene4Act1Layout(Scene):
    def construct(self) -> None:
        setup_scene(self)
        plop(self, wall_of_text(), "wall of text", wait=3.0)
        plop(self, on_screen_label("Wall of text"), "on_screen_label", wait=3.0)


class Scene4Act1(Scene):
    def construct(self) -> None:
        setup_scene(self)
        play_act1(self)
