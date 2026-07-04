"""
Chapter 1 · ACT 4 — Swift evidence (on-device speech)
SCENE-PLAN: 2:00–2:15

Prev: scene1_act3.py · Next: scene1_act5.py · Assembly: scene1_full.py

Render:
  manim -ql scenes/scene1_act4.py Scene1Act4Layout
  manim -ql scenes/scene1_act4.py Scene1Act4

Full scene:
  manim -ql scenes/scene1_full.py Scene1Full
"""

from __future__ import annotations

import sys
from pathlib import Path

from manim import *

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from code_panel import highlight_lines, panel_title, play_highlight, swift_panel
from components.labels import on_screen_label
from review import plop, setup_scene

SNIPPET = "on_device_speech.swift"
# 0-based: requiresOnDeviceRecognition + partial results
HIGHLIGHT_LINES = (1, 2)


def act4_pieces() -> dict[str, Mobject]:
    code = swift_panel(SNIPPET)
    title = panel_title(SNIPPET)
    title.next_to(code, UP, buff=0.28, aligned_edge=LEFT)
    group = VGroup(title, code).move_to(ORIGIN)
    rects = highlight_lines(code, HIGHLIGHT_LINES)
    label = on_screen_label("SFSpeechRecognizer")
    return {
        "code panel + title": group,
        "highlight (preview)": rects,
        "on_screen_label": label,
    }


class Scene1Act4Layout(Scene):
    def construct(self) -> None:
        setup_scene(self)
        for name, mob in act4_pieces().items():
            plop(self, mob, name, wait=3.0)


def play_act4(scene: Scene, state: dict | None = None) -> dict:
    """ACT 4 — baked Swift snippet."""
    _ = state
    code = swift_panel(SNIPPET)
    title = panel_title(SNIPPET)
    title.next_to(code, UP, buff=0.28, aligned_edge=LEFT)
    label = on_screen_label("SFSpeechRecognizer")

    # PLAY 1
    scene.play(FadeIn(title), FadeIn(code, shift=UP * 0.08), run_time=0.9)
    # PLAY 2
    rects = play_highlight(scene, code, HIGHLIGHT_LINES, run_time=0.85)
    # PLAY 3
    scene.play(FadeIn(label, shift=UP * 0.1), run_time=0.5)
    scene.wait(4.5)
    # PLAY 4
    scene.play(FadeOut(title, code, label, rects), run_time=0.7)
    return {}


class Scene1Act4(Scene):
    def construct(self) -> None:
        setup_scene(self)
        play_act4(self)
