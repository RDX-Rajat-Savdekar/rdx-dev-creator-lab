"""Chapter 4 · ACT 4 — Readable captions + D2 proof"""

from __future__ import annotations

import sys
from pathlib import Path

from manim import *

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from broll import D2_SECOND_SPEAKER, play_broll
from components.labels import on_screen_label
from components.segmentation import before_after_segmentation
from review import plop, setup_scene

D2_START = 0.0
D2_DURATION = 3.0


def play_act4(scene: Scene, state: dict | None = None) -> dict:
    _ = state
    compare = before_after_segmentation()
    label = on_screen_label("Readable captions")

    scene.play(FadeIn(compare, shift=UP * 0.08), run_time=0.9)
    scene.play(FadeIn(label, shift=UP * 0.1), run_time=0.5)
    scene.wait(2.5)
    scene.play(FadeOut(compare, label), run_time=0.5)
    play_broll(scene, D2_SECOND_SPEAKER, start=D2_START, duration=D2_DURATION, fade_in=0.15, fade_out=0.15)
    scene.wait(2.5)
    return {}


class Scene4Act4Layout(Scene):
    def construct(self) -> None:
        setup_scene(self)
        plop(self, before_after_segmentation(), "before / after", wait=3.0)
        plop(self, on_screen_label("Readable captions"), "on_screen_label", wait=3.0)


class Scene4Act4(Scene):
    def construct(self) -> None:
        setup_scene(self)
        play_act4(self)
