"""
Chapter 1 · ACT 2 — Cloud temptation
SCENE-PLAN: 1:20–1:40 · VO: hackathon cheat path

Prev: scene1_act1.py · Next: scene1_act3.py · Assembly: scene1_full.py

Render:
  manim -ql scenes/scene1_act2.py Scene1Act2Layout
  manim -ql scenes/scene1_act2.py Scene1Act2

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
from rejected import cloud_temptation_group
from review import plop, setup_scene


def act2_pieces() -> dict[str, Mobject]:
    device = device_boundary_group()
    cloud_bits = cloud_temptation_group(device)
    label = on_screen_label("Temptation: cloud ASR")
    return {
        "device boundary": device,
        "cloud": cloud_bits["cloud"],
        "ghost arrow + network fallback": VGroup(cloud_bits["ghost arrow"], cloud_bits["network fallback"]),
        "on_screen_label": label,
    }


class Scene1Act2Layout(Scene):
    def construct(self) -> None:
        setup_scene(self)
        for name, mob in act2_pieces().items():
            plop(self, mob, name, wait=3.0)


def play_act2(scene: Scene, state: dict | None = None) -> dict:
    """ACT 2 — ghost path to cloud ASR."""
    state = state or {}
    chain = state.get("chain", False)
    label = on_screen_label("Temptation: cloud ASR")

    if chain and state.get("device"):
        device = state["device"]
        if state.get("act1_label"):
            scene.play(FadeOut(state["act1_label"]), run_time=0.25)
    else:
        device = device_boundary_group()
        scene.play(FadeIn(device), run_time=0.8)

    cloud_bits = cloud_temptation_group(device)
    cloud = cloud_bits["cloud"]
    arrow = cloud_bits["ghost arrow"]
    fallback = cloud_bits["network fallback"]

    # PLAY 2
    scene.play(FadeIn(cloud), Create(arrow), run_time=1.1)
    # PLAY 3
    scene.play(FadeIn(fallback), run_time=0.45)
    # PLAY 4
    scene.play(FadeIn(label, shift=UP * 0.1), run_time=0.5)
    scene.wait(5.5)

    state["device"] = device
    state["cloud"] = cloud
    state["arrow"] = arrow
    state["fallback"] = fallback
    state["act2_label"] = label
    if not chain:
        scene.play(FadeOut(device, cloud, arrow, fallback, label), run_time=0.7)
    return state


class Scene1Act2(Scene):
    def construct(self) -> None:
        setup_scene(self)
        play_act2(self)
