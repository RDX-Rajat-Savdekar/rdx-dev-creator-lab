"""
Chapter 3 · ACT 2 — Dual pipeline split (Speech + SoundAnalysis)
SCENE-PLAN: 4:20–4:40

Prev: scene3_act1.py · Next: scene3_act3.py · Assembly: scene3_full.py

Render:
  manim -ql scenes/scene3_act2.py Scene3Act2Layout
  manim -ql scenes/scene3_act2.py Scene3Act2
"""

from __future__ import annotations

import sys
from pathlib import Path

from manim import *

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from components.labels import on_screen_label
from components.pipeline import dual_pipeline_group
from review import plop, setup_scene


def act2_pieces() -> dict[str, Mobject]:
    bits = dual_pipeline_group()
    label = on_screen_label("Speech + SoundAnalysis")
    return {
        "dual pipeline": bits["diagram"].scale(0.94),
        "on_screen_label": label,
    }


class Scene3Act2Layout(Scene):
    def construct(self) -> None:
        setup_scene(self)
        for name, mob in act2_pieces().items():
            plop(self, mob, name, wait=3.0)


def play_act2(scene: Scene, state: dict | None = None) -> dict:
    """ACT 2 — one tap feeds parallel on-device ML branches."""
    _ = state
    bits = dual_pipeline_group()
    diagram = bits["diagram"].scale(0.94)
    stages = bits["stages"]
    edges = bits["edges"]
    label = on_screen_label("Speech + SoundAnalysis")

    scene.play(
        LaggedStart(*[FadeIn(stage, shift=RIGHT * 0.1) for stage in stages], lag_ratio=0.18),
        run_time=1.0,
    )
    scene.play(LaggedStart(*[Create(edge) for edge in edges], lag_ratio=0.1), run_time=0.9)
    scene.play(FadeIn(label, shift=UP * 0.1), run_time=0.5)
    scene.wait(5.5)
    scene.play(FadeOut(diagram, label), run_time=0.7)
    return {}


class Scene3Act2(Scene):
    def construct(self) -> None:
        setup_scene(self)
        play_act2(self)
