"""
Chapter 3 · ACT 1 — Single AVAudioEngine tap
SCENE-PLAN: 4:05–4:20

Next: scene3_act2.py · Assembly: scene3_full.py

Render:
  manim -ql scenes/scene3_act1.py Scene3Act1Layout
  manim -ql scenes/scene3_act1.py Scene3Act1
"""

from __future__ import annotations

import sys
from pathlib import Path

from manim import *

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from code_panel import play_highlight
from components.labels import on_screen_label
from components.split_layout import pane_divider, split_layout
from icons import MIC, load_icon
from review import plop, setup_scene
from theme import ACCENT

SNIPPET = "tap_install.swift"
HIGHLIGHT_LINES = (1, 4)


def _mic_glyph() -> VGroup:
    mic = load_icon(MIC, color=ACCENT, height=0.72)
    ring = Circle(
        radius=0.46,
        color=ACCENT,
        stroke_width=2.2,
        fill_color=ACCENT,
        fill_opacity=0.12,
    )
    mic.move_to(ring.get_center())
    return VGroup(ring, mic)


def _act1_layout() -> dict[str, Mobject]:
    return split_layout(_mic_glyph(), SNIPPET, highlight=HIGHLIGHT_LINES)


def act1_pieces() -> dict[str, Mobject]:
    bits = _act1_layout()
    label = on_screen_label("One AVAudioEngine tap")
    return {
        "visual pane (top)": bits["visual"],
        "code pane (bottom)": bits["code_group"],
        "pane divider (layout guide)": pane_divider(),
        "highlight (preview)": bits["highlights"],
        "on_screen_label": label,
    }


class Scene3Act1Layout(Scene):
    def construct(self) -> None:
        setup_scene(self)
        for name, mob in act1_pieces().items():
            plop(self, mob, name, wait=3.0)


def play_act1(scene: Scene, state: dict | None = None) -> dict:
    """ACT 1 — installTap on one input node."""
    _ = state
    bits = _act1_layout()
    visual = bits["visual"]
    code_group = bits["code_group"]
    code = bits["code"]
    label = on_screen_label("One AVAudioEngine tap")

    scene.play(FadeIn(visual, shift=DOWN * 0.08), run_time=0.7)
    scene.play(FadeIn(code_group, shift=UP * 0.08), run_time=0.85)
    rects = play_highlight(scene, code, HIGHLIGHT_LINES, run_time=0.85)
    scene.play(FadeIn(label, shift=UP * 0.1), run_time=0.5)
    scene.wait(5.5)
    scene.play(FadeOut(visual, code_group, label, rects), run_time=0.7)
    return {}


class Scene3Act1(Scene):
    def construct(self) -> None:
        setup_scene(self)
        play_act1(self)
