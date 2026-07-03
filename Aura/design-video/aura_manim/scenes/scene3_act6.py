"""
Chapter 3 · ACT 6 — Proof montage (D1 captions + D3 whisper)
SCENE-PLAN: 5:35–5:55

Prev: scene3_act5.py · Assembly: scene3_full.py

Render:
  manim -ql scenes/scene3_act6.py Scene3Act6Layout
  manim -ql scenes/scene3_act6.py Scene3Act6
"""

from __future__ import annotations

import sys
from pathlib import Path

from manim import *

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from broll import D1_LIVE_CAPTIONS, D3_WHISPER, play_montage
from components.labels import on_screen_label
from review import plop, setup_scene

MONTAGE_SEGMENTS = [
    (D1_LIVE_CAPTIONS, 0.0, 3.0),
    (D3_WHISPER, 0.0, 3.0),
]


def act6_pieces() -> dict[str, Mobject]:
    from broll import broll_still

    label = on_screen_label("Dual pipeline · live")
    still = broll_still(D1_LIVE_CAPTIONS, width=10.0)
    return {
        "D1 preview still": still,
        "on_screen_label": label,
    }


class Scene3Act6Layout(Scene):
    def construct(self) -> None:
        setup_scene(self)
        for name, mob in act6_pieces().items():
            plop(self, mob, name, wait=3.0)


def play_act6(scene: Scene, state: dict | None = None) -> dict:
    """ACT 6 — D1 live captions + D3 whisper detection."""
    _ = state
    label = on_screen_label("Dual pipeline · live")

    play_montage(scene, MONTAGE_SEGMENTS, fade_in=0.15, fade_out=0.15)
    scene.play(FadeIn(label, shift=UP * 0.1), run_time=0.5)
    scene.wait(4.5)
    scene.play(FadeOut(label), run_time=0.7)
    return {}


class Scene3Act6(Scene):
    def construct(self) -> None:
        setup_scene(self)
        play_act6(self)
