"""Chapter 5 · ACT 3 — Jitter vs baked quad"""

from __future__ import annotations

import sys
from pathlib import Path

from manim import *

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from components.labels import on_screen_label
from components.texture_bake import jitter_vs_bake
from review import plop, setup_scene
from theme import WARN


def play_act3(scene: Scene, state: dict | None = None) -> dict:
    _ = state
    compare = jitter_vs_bake()
    panels = compare[1]
    jitter_panel = panels[0]
    baked_panel = panels[1]
    label = on_screen_label("Jitter vs baked quad")

    scene.play(FadeIn(compare, shift=UP * 0.08), run_time=0.85)
    scene.play(
        jitter_panel[1].animate.shift(RIGHT * 0.06 + DOWN * 0.04),
        rate_func=there_and_back,
        run_time=0.9,
    )
    scene.play(Indicate(baked_panel, color=WARN, scale_factor=1.02), run_time=0.55)
    scene.play(FadeIn(label, shift=UP * 0.1), run_time=0.5)
    scene.wait(5.5)
    scene.play(FadeOut(compare, label), run_time=0.7)
    return {}


class Scene5Act3Layout(Scene):
    def construct(self) -> None:
        setup_scene(self)
        plop(self, jitter_vs_bake(), "side-by-side", wait=3.0)
        plop(self, on_screen_label("Jitter vs baked quad"), "on_screen_label", wait=3.0)


class Scene5Act3(Scene):
    def construct(self) -> None:
        setup_scene(self)
        play_act3(self)
