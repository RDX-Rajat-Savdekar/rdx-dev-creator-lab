"""
Chapter 1 · ACT 5 — Locale picker + metrics
SCENE-PLAN: 2:15–2:35

Prev: scene1_act4.py · Assembly: scene1_full.py

Render:
  manim -ql scenes/scene1_act5.py Scene1Act5Layout
  manim -ql scenes/scene1_act5.py Scene1Act5

Full scene:
  manim -ql scenes/scene1_full.py Scene1Full
"""

from __future__ import annotations

import sys
from pathlib import Path

from manim import *

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from components.labels import on_screen_label
from components.locale_picker import act5_layout
from review import plop, setup_scene


def act5_pieces() -> dict[str, Mobject]:
    layout = act5_layout()
    layout["on_screen_label"] = on_screen_label("0 external deps · ~1,475 LOC")
    return layout


class Scene1Act5Layout(Scene):
    def construct(self) -> None:
        setup_scene(self)
        for name, mob in act5_pieces().items():
            plop(self, mob, name, wait=3.0)


def play_act5(scene: Scene, state: dict | None = None) -> dict:
    """ACT 5 — locale trade-off + honest metrics."""
    _ = state
    pieces = act5_layout()
    picker = pieces["Recognition Language panel"]
    note = pieces["trade-off note"]
    card = pieces["fact card"]
    label = on_screen_label("0 external deps · ~1,475 LOC")

    # PLAY 1
    scene.play(FadeIn(picker, shift=UP * 0.1), run_time=1.0)
    # PLAY 2
    scene.play(FadeIn(note), run_time=0.5)
    # PLAY 3
    scene.play(FadeIn(card, shift=RIGHT * 0.12), run_time=0.7)
    # PLAY 4
    scene.play(FadeIn(label, shift=UP * 0.1), run_time=0.5)
    scene.wait(5.5)
    # PLAY 5
    scene.play(FadeOut(picker, note, card, label), run_time=0.7)
    return {}


class Scene1Act5(Scene):
    def construct(self) -> None:
        setup_scene(self)
        play_act5(self)
