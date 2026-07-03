"""Chapter 5 · ACT 1 — 90 Hz loop + ViewAttachment rejected"""

from __future__ import annotations

import sys
from pathlib import Path

from manim import *

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from components.labels import on_screen_label
from components.texture_bake import hz_loop_diagram
from review import plop, setup_scene


def play_act1(scene: Scene, state: dict | None = None) -> dict:
    _ = state
    bits = hz_loop_diagram()
    diagram = bits["diagram"]
    label = on_screen_label("90 Hz · layout every frame")

    scene.play(FadeIn(diagram, shift=UP * 0.08), run_time=0.85)
    scene.play(Create(bits["cross"]), run_time=0.55)
    scene.play(FadeIn(label, shift=UP * 0.1), run_time=0.5)
    scene.wait(5.5)
    scene.play(FadeOut(diagram, label), run_time=0.7)
    return {}


class Scene5Act1Layout(Scene):
    def construct(self) -> None:
        setup_scene(self)
        plop(self, hz_loop_diagram()["diagram"], "90 Hz loop", wait=3.0)
        plop(self, on_screen_label("90 Hz · layout every frame"), "on_screen_label", wait=3.0)


class Scene5Act1(Scene):
    def construct(self) -> None:
        setup_scene(self)
        play_act1(self)
