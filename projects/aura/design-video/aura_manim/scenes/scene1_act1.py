"""
Chapter 1 · ACT 1 — Device boundary
SCENE-PLAN: 1:05–1:20 · VO: everything stays on-device

Next: scene1_act2.py · Assembly: scene1_full.py

Render:
  manim -ql scenes/scene1_act1.py Scene1Act1Layout
  manim -ql scenes/scene1_act1.py Scene1Act1

Full scene:
  manim -ql scenes/scene1_full.py Scene1Full
"""

from __future__ import annotations

import sys
from pathlib import Path

from manim import *

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from components.device import device_boundary_group
from components.labels import on_screen_label
from review import plop, setup_scene
from theme import ACCENT


def act1_pieces() -> dict[str, Mobject]:
    device = device_boundary_group()
    label = on_screen_label("Decision 1: on-device only")
    return {
        "device boundary + Vision Pro": device,
        "on_screen_label": label,
    }


class Scene1Act1Layout(Scene):
    def construct(self) -> None:
        setup_scene(self)
        for name, mob in act1_pieces().items():
            plop(self, mob, name, wait=3.0)


def play_act1(scene: Scene, state: dict | None = None) -> dict:
    """ACT 1 — device trust boundary. Pass state['chain']=True from scene1_full."""
    state = state or {}
    chain = state.get("chain", False)
    device = device_boundary_group()
    label = act1_pieces()["on_screen_label"]

    # PLAY 1
    scene.play(Create(device[0]), FadeIn(device[1]), run_time=1.0)
    # PLAY 2 — (icon included above)
    # PLAY 3
    scene.play(FadeIn(label, shift=UP * 0.1), run_time=0.5)
    scene.wait(5.5)

    state["device"] = device
    state["act1_label"] = label
    if not chain:
        scene.play(FadeOut(device, label), run_time=0.7)
    return state


class Scene1Act1(Scene):
    def construct(self) -> None:
        setup_scene(self)
        play_act1(self)
