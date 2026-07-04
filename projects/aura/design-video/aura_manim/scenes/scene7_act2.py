"""Chapter 7 · ACT 2 — Reject: azimuth ≠ position"""

from __future__ import annotations

import sys
from pathlib import Path

from manim import *

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from components.hud_pivot import azimuth_reject_diagram
from components.labels import on_screen_label
from review import plop, setup_scene


def play_act2(scene: Scene, state: dict | None = None) -> dict:
    _ = state
    bits = azimuth_reject_diagram()
    diagram = bits["diagram"]
    label = on_screen_label("azimuth ≠ position")

    scene.play(FadeIn(diagram, shift=UP * 0.08), run_time=0.85)
    scene.play(Create(bits["strike"]), run_time=0.55)
    scene.play(Wiggle(bits["pin"]), run_time=0.65)
    scene.play(FadeIn(label, shift=UP * 0.1), run_time=0.5)
    scene.wait(5.5)
    scene.play(FadeOut(diagram, label), run_time=0.7)
    return {}


class Scene7Act2Layout(Scene):
    def construct(self) -> None:
        setup_scene(self)
        plop(self, azimuth_reject_diagram()["diagram"], "azimuth reject", wait=3.0)
        plop(self, on_screen_label("azimuth ≠ position"), "on_screen_label", wait=3.0)


class Scene7Act2(Scene):
    def construct(self) -> None:
        setup_scene(self)
        play_act2(self)
