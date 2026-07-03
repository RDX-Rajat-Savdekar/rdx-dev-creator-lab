"""Chapter 6 · ACT 1 — ML callback off main thread"""

from __future__ import annotations

import sys
from pathlib import Path

from manim import *

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from components.labels import on_screen_label
from components.mainactor_bridge import mainactor_lane_diagram
from review import plop, setup_scene
from theme import ACCENT


def play_act1(scene: Scene, state: dict | None = None) -> dict:
    _ = state
    bits = mainactor_lane_diagram()
    diagram = bits["diagram"]
    label = on_screen_label("Background thread · ML result")

    scene.play(FadeIn(diagram, shift=UP * 0.08), run_time=0.85)
    scene.play(Indicate(bits["ui_lane"], color=ACCENT, scale_factor=1.02), run_time=0.55)
    scene.play(FadeIn(label, shift=UP * 0.1), run_time=0.5)
    scene.wait(5.5)
    scene.play(FadeOut(diagram, label), run_time=0.7)
    return {}


class Scene6Act1Layout(Scene):
    def construct(self) -> None:
        setup_scene(self)
        plop(self, mainactor_lane_diagram()["diagram"], "two-lane bridge", wait=3.0)
        plop(self, on_screen_label("Background thread · ML result"), "on_screen_label", wait=3.0)


class Scene6Act1(Scene):
    def construct(self) -> None:
        setup_scene(self)
        play_act1(self)
