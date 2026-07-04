"""Chapter 8 · ACT 2 — Product would change"""

from __future__ import annotations

import sys
from pathlib import Path

from manim import *

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from components.labels import on_screen_label
from components.scale import product_would_change_diagram
from review import plop, setup_scene
from theme import ACCENT


def play_act2(scene: Scene, state: dict | None = None) -> dict:
    _ = state
    diagram = product_would_change_diagram()
    label = on_screen_label("Product · would change")

    scene.play(FadeIn(diagram, shift=UP * 0.08), run_time=0.85)
    scene.play(Create(diagram[1]), run_time=0.55)
    scene.play(Indicate(diagram[0][1], color=ACCENT, scale_factor=1.02), run_time=0.55)
    scene.play(FadeIn(label, shift=UP * 0.1), run_time=0.5)
    scene.wait(5.5)
    scene.play(FadeOut(diagram, label), run_time=0.7)
    return {}


class Scene8Act2Layout(Scene):
    def construct(self) -> None:
        setup_scene(self)
        plop(self, product_would_change_diagram(), "today vs product", wait=3.0)
        plop(self, on_screen_label("Product · would change"), "on_screen_label", wait=3.0)


class Scene8Act2(Scene):
    def construct(self) -> None:
        setup_scene(self)
        play_act2(self)
