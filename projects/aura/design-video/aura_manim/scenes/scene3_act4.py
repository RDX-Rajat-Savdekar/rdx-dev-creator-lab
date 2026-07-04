"""
Chapter 3 · ACT 4 — Classifier gate (0.6 / 0.25 s)
SCENE-PLAN: 5:05–5:20

Prev: scene3_act3.py · Next: scene3_act5.py · Assembly: scene3_full.py

Render:
  manim -ql scenes/scene3_act4.py Scene3Act4Layout
  manim -ql scenes/scene3_act4.py Scene3Act4
"""

from __future__ import annotations

import sys
from pathlib import Path

from manim import *

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from components.classifier_gate import classifier_gate_group
from components.labels import on_screen_label
from review import plop, setup_scene


def act4_pieces() -> dict[str, Mobject]:
    bits = classifier_gate_group()
    label = on_screen_label("Anti-flap: 0.6 · 0.25 s")
    return {
        "classifier gate card": bits["diagram"],
        "on_screen_label": label,
    }


class Scene3Act4Layout(Scene):
    def construct(self) -> None:
        setup_scene(self)
        for name, mob in act4_pieces().items():
            plop(self, mob, name, wait=3.0)


def play_act4(scene: Scene, state: dict | None = None) -> dict:
    """ACT 4 — confidence gate + throttle stops label flapping."""
    _ = state
    bits = classifier_gate_group()
    diagram = bits["diagram"]
    card = bits["card"]
    label = on_screen_label("Anti-flap: 0.6 · 0.25 s")

    scene.play(FadeIn(card, shift=UP * 0.1), run_time=0.8)
    scene.play(FadeIn(bits["note"], shift=UP * 0.06), run_time=0.45)
    scene.play(FadeIn(label, shift=UP * 0.1), run_time=0.5)
    scene.wait(5.5)
    scene.play(FadeOut(diagram, label), run_time=0.7)
    return {}


class Scene3Act4(Scene):
    def construct(self) -> None:
        setup_scene(self)
        play_act4(self)
