"""Chapter 7 · ACT 5 — Azimuth computed, not shown in UI"""

from __future__ import annotations

import sys
from pathlib import Path

from manim import *

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from components.hud_pivot import azimuth_grayed_pipeline
from components.labels import on_screen_label
from review import plop, setup_scene


def play_act5(scene: Scene, state: dict | None = None) -> dict:
    _ = state
    diagram = azimuth_grayed_pipeline()
    label = on_screen_label("Azimuth: computed, not shown")

    scene.play(FadeIn(diagram, shift=UP * 0.08), run_time=0.85)
    scene.play(FadeIn(label, shift=UP * 0.1), run_time=0.5)
    scene.wait(5.5)
    scene.play(FadeOut(diagram, label), run_time=0.7)
    return {}


class Scene7Act5Layout(Scene):
    def construct(self) -> None:
        setup_scene(self)
        plop(self, azimuth_grayed_pipeline(), "azimuth pipeline", wait=3.0)
        plop(self, on_screen_label("Azimuth: computed, not shown"), "on_screen_label", wait=3.0)


class Scene7Act5(Scene):
    def construct(self) -> None:
        setup_scene(self)
        play_act5(self)
