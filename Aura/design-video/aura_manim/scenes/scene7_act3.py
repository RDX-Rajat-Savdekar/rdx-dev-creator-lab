"""Chapter 7 · ACT 3 — Reject: off-screen hazard"""

from __future__ import annotations

import sys
from pathlib import Path

from manim import *

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from components.hud_pivot import offscreen_hazard_diagram
from components.labels import on_screen_label
from review import plop, setup_scene


def play_act3(scene: Scene, state: dict | None = None) -> dict:
    _ = state
    bits = offscreen_hazard_diagram()
    diagram = bits["diagram"]
    label = on_screen_label("Off-screen = hazard")

    scene.play(FadeIn(diagram, shift=UP * 0.08), run_time=0.85)
    scene.play(Create(bits["cross"]), run_time=0.55)
    scene.play(FadeIn(label, shift=UP * 0.1), run_time=0.5)
    scene.wait(5.5)
    scene.play(FadeOut(diagram, label), run_time=0.7)
    return {}


class Scene7Act3Layout(Scene):
    def construct(self) -> None:
        setup_scene(self)
        plop(self, offscreen_hazard_diagram()["diagram"], "FOV hazard", wait=3.0)
        plop(self, on_screen_label("Off-screen = hazard"), "on_screen_label", wait=3.0)


class Scene7Act3(Scene):
    def construct(self) -> None:
        setup_scene(self)
        play_act3(self)
