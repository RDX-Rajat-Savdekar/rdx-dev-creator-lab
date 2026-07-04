"""Chapter 9 · ACT 1 — On-device dual pipeline recap"""

from __future__ import annotations

import sys
from pathlib import Path

from manim import *

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from components.labels import on_screen_label
from components.outro import recap_diagram
from review import plop, setup_scene
from theme import ACCENT


def play_act1(scene: Scene, state: dict | None = None) -> dict:
    _ = state
    diagram = recap_diagram()
    label = on_screen_label("On-device dual pipeline")

    scene.play(FadeIn(diagram[0], shift=UP * 0.08), run_time=0.7)
    scene.play(FadeIn(diagram[1], shift=UP * 0.06), run_time=0.75)
    scene.play(Indicate(diagram[1], color=ACCENT, scale_factor=1.01), run_time=0.55)
    scene.play(FadeIn(label, shift=UP * 0.1), run_time=0.5)
    scene.wait(4.5)
    scene.play(FadeOut(diagram, label), run_time=0.7)
    return {}


class Scene9Act1Layout(Scene):
    def construct(self) -> None:
        setup_scene(self)
        plop(self, recap_diagram(), "recap + pipeline", wait=3.0)
        plop(self, on_screen_label("On-device dual pipeline"), "on_screen_label", wait=3.0)


class Scene9Act1(Scene):
    def construct(self) -> None:
        setup_scene(self)
        play_act1(self)
