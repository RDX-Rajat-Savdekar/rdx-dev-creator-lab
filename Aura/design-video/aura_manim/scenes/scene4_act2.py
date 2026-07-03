"""Chapter 4 · ACT 2 — Pause threshold 1.1 s"""

from __future__ import annotations

import sys
from pathlib import Path

from manim import *

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from code_panel import play_highlight
from components.labels import on_screen_label
from components.segmentation import utterance_timeline
from components.split_layout import pane_divider, split_layout
from review import plop, setup_scene
from theme import ACCENT

SNIPPET = "pause_threshold.swift"
HIGHLIGHT_LINES = (0, 2)


def _layout() -> dict[str, Mobject]:
    return split_layout(utterance_timeline(), SNIPPET, highlight=HIGHLIGHT_LINES)


def play_act2(scene: Scene, state: dict | None = None) -> dict:
    _ = state
    bits = _layout()
    label = on_screen_label("Pause gap: 1.1 s")

    scene.play(FadeIn(bits["visual"], shift=DOWN * 0.08), run_time=0.85)
    scene.play(Indicate(bits["visual"][1], color=ACCENT, scale_factor=1.02), run_time=0.5)
    scene.play(FadeIn(bits["code_group"], shift=UP * 0.08), run_time=0.75)
    rects = play_highlight(scene, bits["code"], HIGHLIGHT_LINES, run_time=0.85)
    scene.play(FadeIn(label, shift=UP * 0.1), run_time=0.5)
    scene.wait(5.5)
    scene.play(FadeOut(bits["visual"], bits["code_group"], label, rects), run_time=0.7)
    return {}


class Scene4Act2Layout(Scene):
    def construct(self) -> None:
        setup_scene(self)
        bits = _layout()
        plop(self, bits["visual"], "visual pane", wait=3.0)
        plop(self, bits["code_group"], "code pane", wait=3.0)
        plop(self, pane_divider(), "pane divider", wait=3.0)


class Scene4Act2(Scene):
    def construct(self) -> None:
        setup_scene(self)
        play_act2(self)
