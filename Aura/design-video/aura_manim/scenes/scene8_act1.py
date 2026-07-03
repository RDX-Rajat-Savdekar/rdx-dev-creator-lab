"""Chapter 8 · ACT 1 — Prototype limits today"""

from __future__ import annotations

import sys
from pathlib import Path

from manim import *

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from components.labels import on_screen_label
from components.scale import prototype_limits_diagram
from review import plop, setup_scene
from theme import MUTED


def play_act1(scene: Scene, state: dict | None = None) -> dict:
    _ = state
    diagram = prototype_limits_diagram()
    label = on_screen_label("Prototype · today")

    scene.play(FadeIn(diagram, shift=UP * 0.08), run_time=0.85)
    scene.play(Indicate(diagram[1], color=MUTED, scale_factor=1.01), run_time=0.55)
    scene.play(FadeIn(label, shift=UP * 0.1), run_time=0.5)
    scene.wait(5.5)
    scene.play(FadeOut(diagram, label), run_time=0.7)
    return {}


class Scene8Act1Layout(Scene):
    def construct(self) -> None:
        setup_scene(self)
        plop(self, prototype_limits_diagram(), "prototype limits", wait=3.0)
        plop(self, on_screen_label("Prototype · today"), "on_screen_label", wait=3.0)


class Scene8Act1(Scene):
    def construct(self) -> None:
        setup_scene(self)
        play_act1(self)
