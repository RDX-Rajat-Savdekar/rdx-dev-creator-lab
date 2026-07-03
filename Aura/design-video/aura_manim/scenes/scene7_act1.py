"""Chapter 7 · ACT 1 — Tried world-locked sound pins"""

from __future__ import annotations

import sys
from pathlib import Path

from manim import *

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from components.hud_pivot import world_locked_pins_diagram
from components.labels import on_screen_label
from review import plop, setup_scene
from theme import ACCENT


def play_act1(scene: Scene, state: dict | None = None) -> dict:
    _ = state
    bits = world_locked_pins_diagram()
    diagram = bits["diagram"]
    label = on_screen_label("Tried: world-locked pins")

    scene.play(FadeIn(diagram, shift=UP * 0.08), run_time=0.9)
    scene.play(Indicate(bits["rays"], color=ACCENT, scale_factor=1.01), run_time=0.55)
    scene.play(FadeIn(label, shift=UP * 0.1), run_time=0.5)
    scene.wait(5.5)
    scene.play(FadeOut(diagram, label), run_time=0.7)
    return {}


class Scene7Act1Layout(Scene):
    def construct(self) -> None:
        setup_scene(self)
        plop(self, world_locked_pins_diagram()["diagram"], "world pins", wait=3.0)
        plop(self, on_screen_label("Tried: world-locked pins"), "on_screen_label", wait=3.0)


class Scene7Act1(Scene):
    def construct(self) -> None:
        setup_scene(self)
        play_act1(self)
