"""Chapter 6 · ACT 3 — Captions update on main + D1 proof"""

from __future__ import annotations

import sys
from pathlib import Path

from manim import *

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from broll import D1_LIVE_CAPTIONS, play_broll
from components.labels import on_screen_label
from components.mainactor_bridge import caption_update_inset
from review import plop, setup_scene

D1_START = 0.0
D1_DURATION = 3.0


def play_act3(scene: Scene, state: dict | None = None) -> dict:
    _ = state
    inset = caption_update_inset()
    label = on_screen_label("Captions update on main")

    scene.play(FadeIn(inset, shift=UP * 0.08), run_time=0.85)
    scene.play(FadeIn(label, shift=UP * 0.1), run_time=0.5)
    scene.wait(2.0)
    scene.play(FadeOut(inset, label), run_time=0.5)
    play_broll(scene, D1_LIVE_CAPTIONS, start=D1_START, duration=D1_DURATION, fade_in=0.15, fade_out=0.15)
    scene.wait(2.5)
    return {}


class Scene6Act3Layout(Scene):
    def construct(self) -> None:
        setup_scene(self)
        plop(self, caption_update_inset(), "caption inset", wait=3.0)
        plop(self, on_screen_label("Captions update on main"), "on_screen_label", wait=3.0)


class Scene6Act3(Scene):
    def construct(self) -> None:
        setup_scene(self)
        play_act3(self)
