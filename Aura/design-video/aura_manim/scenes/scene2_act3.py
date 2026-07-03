"""
Chapter 2 · ACT 3 — Train path impractical (weeks vs hours)
SCENE-PLAN: 3:05–3:20

Prev: scene2_act2.py · Next: scene2_act4.py · Assembly: scene2_full.py

Render:
  manim -ql scenes/scene2_act3.py Scene2Act3Layout
  manim -ql scenes/scene2_act3.py Scene2Act3
"""

from __future__ import annotations

import sys
from pathlib import Path

from manim import *

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from components.fork import vertical_fork
from components.labels import on_screen_label
from components.timeline_bar import weeks_vs_hours_bar
from review import plop, setup_scene
from theme import WARN


def act3_pieces() -> dict[str, Mobject]:
    bits = vertical_fork(selected="right")
    timeline = weeks_vs_hours_bar()
    cross = Cross(stroke_color=WARN, stroke_width=3).scale(0.38)
    cross.move_to(bits["left"].get_center())
    label = on_screen_label("Train: weeks")
    return {
        "fork + timeline + cross (preview)": VGroup(bits["fork"], timeline, cross),
        "on_screen_label": label,
    }


class Scene2Act3Layout(Scene):
    def construct(self) -> None:
        setup_scene(self)
        for name, mob in act3_pieces().items():
            plop(self, mob, name, wait=3.0)


def play_act3(scene: Scene, state: dict | None = None) -> dict:
    """ACT 3 — dim train path; weeks >> hours."""
    _ = state
    bits = vertical_fork(selected="right")
    fork = bits["fork"]
    label = on_screen_label("Train: weeks")
    timeline = weeks_vs_hours_bar()
    cross = Cross(stroke_color=WARN, stroke_width=3).scale(0.38)
    cross.move_to(bits["left"].get_center())

    scene.play(FadeIn(fork, shift=UP * 0.08), run_time=0.8)
    scene.play(FadeIn(timeline, shift=UP * 0.06), run_time=0.7)
    scene.play(
        bits["left"].animate.set_opacity(0.22),
        Create(cross),
        run_time=0.85,
    )
    scene.play(FadeIn(label, shift=UP * 0.1), run_time=0.5)
    scene.wait(5.5)
    scene.play(FadeOut(fork, timeline, cross, label), run_time=0.75)
    return {}


class Scene2Act3(Scene):
    def construct(self) -> None:
        setup_scene(self)
        play_act3(self)
