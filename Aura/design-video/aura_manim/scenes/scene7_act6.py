"""Chapter 7 · ACT 6 — Spatial caveat + Unity honesty"""

from __future__ import annotations

import sys
from pathlib import Path

from manim import *

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from components.honesty_card import honesty_card
from components.labels import on_screen_label
from review import plop, setup_scene
from theme import ACCENT


def play_act6(scene: Scene, state: dict | None = None) -> dict:
    _ = state
    card = honesty_card(
        "Spatial: demoed · HEAD caveat",
        "Unity clips = viz explainers · Swift ships on visionOS",
        stroke_color=ACCENT,
    )
    label = on_screen_label("Viz only · Swift app")

    scene.play(FadeIn(card, shift=UP * 0.1), run_time=0.8)
    scene.play(FadeIn(label, shift=UP * 0.1), run_time=0.5)
    scene.wait(5.5)
    scene.play(FadeOut(card, label), run_time=0.7)
    return {}


class Scene7Act6Layout(Scene):
    def construct(self) -> None:
        setup_scene(self)
        card = honesty_card(
            "Spatial: demoed · HEAD caveat",
            "Unity clips = viz explainers · Swift ships on visionOS",
            stroke_color=ACCENT,
        )
        plop(self, card, "honesty card", wait=3.0)
        plop(self, on_screen_label("Viz only · Swift app"), "on_screen_label", wait=3.0)


class Scene7Act6(Scene):
    def construct(self) -> None:
        setup_scene(self)
        play_act6(self)
