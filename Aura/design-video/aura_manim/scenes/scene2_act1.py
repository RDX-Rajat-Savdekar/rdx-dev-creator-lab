"""
Chapter 2 · ACT 1 — Decision fork (build vs train)
SCENE-PLAN: 2:35–2:50

Next: scene2_act2.py · Assembly: scene2_full.py

Render:
  manim -ql scenes/scene2_act1.py Scene2Act1Layout
  manim -ql scenes/scene2_act1.py Scene2Act1
"""

from __future__ import annotations

import sys
from pathlib import Path

from manim import *

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from components.fork import vertical_fork
from components.labels import on_screen_label
from review import plop, setup_scene
from theme import ACCENT


def act1_pieces() -> dict[str, Mobject]:
    bits = vertical_fork(selected="right")
    label = on_screen_label("Decision 2: build vs train")
    return {
        "vertical fork": bits["fork"],
        "on_screen_label": label,
    }


class Scene2Act1Layout(Scene):
    def construct(self) -> None:
        setup_scene(self)
        for name, mob in act1_pieces().items():
            plop(self, mob, name, wait=3.0)


def play_act1(scene: Scene, state: dict | None = None) -> dict:
    """ACT 1 — vertical split: train vs integrate."""
    state = state or {}
    chain = state.get("chain", False)
    bits = vertical_fork(selected="right")
    fork = bits["fork"]
    label = on_screen_label("Decision 2: build vs train")

    # PLAY 1
    scene.play(FadeIn(fork, shift=UP * 0.08), run_time=0.9)
    # PLAY 2
    scene.play(Indicate(bits["right"], color=ACCENT, scale_factor=1.03), run_time=0.55)
    # PLAY 3
    scene.play(FadeIn(label, shift=UP * 0.1), run_time=0.5)
    scene.wait(5.5)

    state["fork"] = fork
    state["fork_bits"] = bits
    state["act1_label"] = label
    if not chain:
        scene.play(FadeOut(fork, label), run_time=0.7)
    return state


class Scene2Act1(Scene):
    def construct(self) -> None:
        setup_scene(self)
        play_act1(self)
