"""
Chapter 1 · ACT 3 — Reject cloud (privacy + latency)
SCENE-PLAN: 1:40–2:00

Prev: scene1_act2.py · Next: scene1_act4.py · Assembly: scene1_full.py

Render:
  manim -ql scenes/scene1_act3.py Scene1Act3Layout
  manim -ql scenes/scene1_act3.py Scene1Act3

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
from rejected import cloud_temptation_group, reject_chips, reject_cross
from review import plop, setup_scene
from theme import ACCENT


def act3_pieces() -> dict[str, Mobject]:
    device = device_boundary_group()
    bits = cloud_temptation_group(device)
    cloud_path = VGroup(bits["cloud"], bits["ghost arrow"], bits["network fallback"])
    reject_mark = reject_cross(bits["ghost arrow"], bits["cloud"])
    chips = reject_chips()
    label = on_screen_label("Rejected: privacy + latency")
    return {
        "device (bright)": device,
        "cloud path": cloud_path,
        "reject cross preview": reject_mark,
        "privacy · latency chips": chips,
        "on_screen_label": label,
    }


class Scene1Act3Layout(Scene):
    def construct(self) -> None:
        setup_scene(self)
        for name, mob in act3_pieces().items():
            plop(self, mob, name, wait=3.0)


def play_act3(scene: Scene, state: dict | None = None) -> dict:
    """ACT 3 — red cross on cloud path; device stays bright."""
    state = state or {}
    chain = state.get("chain", False)

    if chain and state.get("device"):
        device = state["device"]
        cloud = state["cloud"]
        arrow = state["arrow"]
        fallback = state["fallback"]
        if state.get("act2_label"):
            scene.play(FadeOut(state["act2_label"]), run_time=0.25)
    else:
        device = device_boundary_group()
        bits = cloud_temptation_group(device)
        cloud = bits["cloud"]
        arrow = bits["ghost arrow"]
        fallback = bits["network fallback"]
        scene.play(FadeIn(device), FadeIn(cloud), Create(arrow), FadeIn(fallback), run_time=1.2)

    label = on_screen_label("Rejected: privacy + latency")
    chips = reject_chips()
    reject_mark = reject_cross(arrow, cloud)

    # PLAY 2
    scene.play(
        Create(reject_mark),
        cloud.animate.set_opacity(0.2),
        arrow.animate.set_stroke(opacity=0.15),
        fallback.animate.set_opacity(0.25),
        run_time=1.0,
    )
    # PLAY 3
    scene.play(FadeIn(chips, shift=DOWN * 0.08), run_time=0.6)
    # PLAY 4
    scene.play(Indicate(device, color=ACCENT, scale_factor=1.04), run_time=0.55)
    # PLAY 5
    scene.play(FadeIn(label, shift=UP * 0.1), run_time=0.5)
    scene.wait(5.0)

    # PLAY 6 — clear cloud; device fades for act 4 unless standalone
    cloud_path = VGroup(cloud, arrow, fallback, reject_mark)
    scene.play(FadeOut(cloud_path, chips, label, device), run_time=0.8)
    return state


class Scene1Act3(Scene):
    def construct(self) -> None:
        setup_scene(self)
        play_act3(self)
