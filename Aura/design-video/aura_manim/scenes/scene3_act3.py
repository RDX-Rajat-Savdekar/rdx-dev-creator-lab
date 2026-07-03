"""
Chapter 3 · ACT 3 — Serial AnalysisQueue
SCENE-PLAN: 4:40–5:05

Prev: scene3_act2.py · Next: scene3_act4.py · Assembly: scene3_full.py

Render:
  manim -ql scenes/scene3_act3.py Scene3Act3Layout
  manim -ql scenes/scene3_act3.py Scene3Act3
"""

from __future__ import annotations

import sys
from pathlib import Path

from manim import *

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from code_panel import play_highlight
from components.labels import on_screen_label
from components.split_layout import pane_divider, split_layout
from components.thread_lane import thread_lane_diagram
from review import plop, setup_scene
from theme import ACCENT

SNIPPET = "analysis_queue.swift"
HIGHLIGHT_LINES = (1, 4)


def _act3_layout() -> dict[str, Mobject]:
    bits = thread_lane_diagram(show_footnote=False)
    return split_layout(bits["diagram"], SNIPPET, highlight=HIGHLIGHT_LINES)


def act3_pieces() -> dict[str, Mobject]:
    bits = _act3_layout()
    label = on_screen_label("Never block the tap")
    label.shift(LEFT * 0.35)
    return {
        "visual pane (top)": bits["visual"],
        "code pane (bottom)": bits["code_group"],
        "pane divider (layout guide)": pane_divider(),
        "highlight (preview)": bits["highlights"],
        "on_screen_label": label,
    }


class Scene3Act3Layout(Scene):
    def construct(self) -> None:
        setup_scene(self)
        for name, mob in act3_pieces().items():
            plop(self, mob, name, wait=3.0)


def play_act3(scene: Scene, state: dict | None = None) -> dict:
    """ACT 3 — tap stays realtime; analysis runs on serial queue."""
    _ = state
    bits = _act3_layout()
    visual = bits["visual"]
    code_group = bits["code_group"]
    code = bits["code"]
    label = on_screen_label("Never block the tap")
    label.shift(LEFT * 0.35)

    scene.play(FadeIn(visual, shift=DOWN * 0.08), run_time=0.85)
    scene.play(Indicate(visual[0], color=ACCENT, scale_factor=1.02), run_time=0.55)
    scene.play(FadeIn(code_group, shift=UP * 0.08), run_time=0.75)
    rects = play_highlight(scene, code, HIGHLIGHT_LINES, run_time=0.85)
    scene.play(FadeIn(label, shift=UP * 0.2), run_time=0.5)
    scene.wait(5.5)
    scene.play(FadeOut(visual, code_group, label, rects), run_time=0.7)
    return {}


class Scene3Act3(Scene):
    def construct(self) -> None:
        setup_scene(self)
        play_act3(self)
