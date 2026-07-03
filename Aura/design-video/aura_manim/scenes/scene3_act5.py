"""
Chapter 3 · ACT 5 — Locale hot-swap (7 locales)
SCENE-PLAN: 5:20–5:35

Prev: scene3_act4.py · Next: scene3_act6.py · Assembly: scene3_full.py

Render:
  manim -ql scenes/scene3_act5.py Scene3Act5Layout
  manim -ql scenes/scene3_act5.py Scene3Act5
"""

from __future__ import annotations

import sys
from pathlib import Path

from manim import *

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from broll import D6_JAPANESE, play_broll
from components.labels import on_screen_label
from components.locale_picker import locale_hotswap_group
from review import plop, setup_scene
from theme import ACCENT

D6_START = 0.0
D6_DURATION = 2.5


def act5_pieces() -> dict[str, Mobject]:
    bits = locale_hotswap_group()
    label = on_screen_label("7 locales · hot-swap")
    return {
        "locale picker (JA selected)": bits["diagram"],
        "on_screen_label": label,
    }


class Scene3Act5Layout(Scene):
    def construct(self) -> None:
        setup_scene(self)
        for name, mob in act5_pieces().items():
            plop(self, mob, name, wait=3.0)


def play_act5(scene: Scene, state: dict | None = None) -> dict:
    """ACT 5 — switch locale without restarting engine + D6 flash."""
    _ = state
    bits = locale_hotswap_group()
    panel = bits["panel"]
    chip = bits["chip"]
    label = on_screen_label("7 locales · hot-swap")

    scene.play(FadeIn(panel, shift=UP * 0.1), run_time=0.8)
    scene.play(Indicate(panel, color=ACCENT, scale_factor=1.02), run_time=0.5)
    scene.play(FadeIn(chip), run_time=0.4)
    scene.play(FadeIn(label, shift=UP * 0.1), run_time=0.5)
    scene.wait(2.0)
    scene.play(FadeOut(panel, chip, label), run_time=0.5)
    play_broll(scene, D6_JAPANESE, start=D6_START, duration=D6_DURATION, fade_in=0.15, fade_out=0.15)
    scene.wait(2.5)
    return {}


class Scene3Act5(Scene):
    def construct(self) -> None:
        setup_scene(self)
        play_act5(self)
