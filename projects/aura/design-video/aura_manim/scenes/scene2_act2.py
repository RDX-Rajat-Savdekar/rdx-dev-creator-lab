"""
Chapter 2 · ACT 2 — Inbox reveal (Apple Core ML models)
SCENE-PLAN: 2:50–3:05

Prev: scene2_act1.py · Next: scene2_act3.py · Assembly: scene2_full.py

Render:
  manim -ql scenes/scene2_act2.py Scene2Act2Layout
  manim -ql scenes/scene2_act2.py Scene2Act2
"""

from __future__ import annotations

import sys
from pathlib import Path

from manim import *

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from components.inbox import inbox_scene_group, mail_expanded, play_inbox_reveal
from components.labels import on_screen_label
from review import plop, setup_scene


def act2_pieces() -> dict[str, Mobject]:
    bits = inbox_scene_group()
    label = on_screen_label("Apple Speech + SoundAnalysis")
    return {
        "inbox skit (layout)": VGroup(bits["inbox"], bits["collapsed message"]),
        "expanded message (preview)": mail_expanded(),
        "on_screen_label": label,
    }


class Scene2Act2Layout(Scene):
    def construct(self) -> None:
        setup_scene(self)
        for name, mob in act2_pieces().items():
            plop(self, mob, name, wait=3.0)


def play_act2(scene: Scene, state: dict | None = None) -> dict:
    """ACT 2 — mail click → Apple ML announcement → Speech + SoundAnalysis."""
    state = state or {}
    chain = state.get("chain", False)
    label = on_screen_label("Apple Speech + SoundAnalysis")

    if chain:
        fade_outs = [m for m in (state.get("fork"), state.get("act1_label")) if m is not None]
        if fade_outs:
            scene.play(FadeOut(*fade_outs), run_time=0.35)

    group = play_inbox_reveal(scene, run_time=0.85)
    scene.play(FadeIn(label, shift=UP * 0.1), run_time=0.5)
    scene.wait(5.5)
    scene.play(FadeOut(group, label), run_time=0.7)
    return {}


class Scene2Act2(Scene):
    def construct(self) -> None:
        setup_scene(self)
        play_act2(self)
