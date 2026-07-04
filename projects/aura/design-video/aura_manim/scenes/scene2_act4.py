"""
Chapter 2 · ACT 4 — Pipeline + UI teaser
SCENE-PLAN: 3:20–3:35

Prev: scene2_act3.py · Next: scene2_act5.py · Assembly: scene2_full.py

Render:
  manim -ql scenes/scene2_act4.py Scene2Act4Layout
  manim -ql scenes/scene2_act4.py Scene2Act4
"""

from __future__ import annotations

import sys
from pathlib import Path

from manim import *

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from components.labels import on_screen_label
from components.pipeline_stub import pipeline_stub_group
from review import plop, setup_scene


def act4_pieces() -> dict[str, Mobject]:
    bits = pipeline_stub_group()
    label = on_screen_label("Our work: pipeline + UI")
    return {
        "workflow pipeline": bits["diagram"],
        "on_screen_label": label,
    }


class Scene2Act4Layout(Scene):
    def construct(self) -> None:
        setup_scene(self)
        for name, mob in act4_pieces().items():
            plop(self, mob, name, wait=3.0)


def play_act4(scene: Scene, state: dict | None = None) -> dict:
    """ACT 4 — integration engineering preview (ch 3 foreshadow)."""
    _ = state
    bits = pipeline_stub_group()
    diagram = bits["diagram"]
    stages = bits["stages"]
    edges = bits["edges"]
    label = on_screen_label("Our work: pipeline + UI")

    scene.play(
        LaggedStart(*[FadeIn(stage, shift=RIGHT * 0.1) for stage in stages], lag_ratio=0.18),
        run_time=1.0,
    )
    scene.play(LaggedStart(*[Create(edge) for edge in edges], lag_ratio=0.1), run_time=0.9)
    scene.play(FadeIn(label, shift=UP * 0.1), run_time=0.5)
    scene.wait(5.5)
    scene.play(FadeOut(diagram, label), run_time=0.7)
    return {}


class Scene2Act4(Scene):
    def construct(self) -> None:
        setup_scene(self)
        play_act4(self)
