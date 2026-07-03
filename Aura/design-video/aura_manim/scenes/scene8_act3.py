"""Chapter 8 · ACT 3 — Never claim"""

from __future__ import annotations

import sys
from pathlib import Path

from manim import *

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from components.labels import on_screen_label
from components.scale import never_claim_stamp
from review import plop, setup_scene
from theme import WARN


def play_act3(scene: Scene, state: dict | None = None) -> dict:
    _ = state
    stamp = never_claim_stamp()
    label = on_screen_label("Never claim")

    scene.play(FadeIn(stamp[0], shift=UP * 0.08), run_time=0.75)
    scene.play(Create(stamp[1]), run_time=0.6)
    scene.play(Indicate(stamp[0], color=WARN, scale_factor=1.01), run_time=0.5)
    scene.play(FadeIn(label, shift=UP * 0.1), run_time=0.5)
    scene.wait(5.5)
    scene.play(FadeOut(stamp, label), run_time=0.7)
    return {}


class Scene8Act3Layout(Scene):
    def construct(self) -> None:
        setup_scene(self)
        plop(self, never_claim_stamp(), "never claim stamp", wait=3.0)
        plop(self, on_screen_label("Never claim"), "on_screen_label", wait=3.0)


class Scene8Act3(Scene):
    def construct(self) -> None:
        setup_scene(self)
        play_act3(self)
