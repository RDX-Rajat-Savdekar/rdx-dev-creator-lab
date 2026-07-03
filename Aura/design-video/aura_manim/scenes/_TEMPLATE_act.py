"""TEMPLATE — copy to sceneN_actM.py when starting a new act (ch 6+).

Replace N, M, labels, imports. See MANIM-STANDARDS.md + AGENTS.md.
"""

from __future__ import annotations

import sys
from pathlib import Path

from manim import *

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from components.labels import on_screen_label
from components.layout import fit_center, flow_lr  # compose your visual
from review import plop, setup_scene
from typography import body_text

# from components.your_chapter import your_diagram


def play_actM(scene: Scene, state: dict | None = None) -> dict:
    _ = state
    # visual = fit_center(your_diagram())
    visual = fit_center(flow_lr(body_text("Replace me")))
    label = on_screen_label("On-screen label")

    scene.play(FadeIn(visual, shift=UP * 0.08), run_time=0.85)
    scene.play(FadeIn(label, shift=UP * 0.1), run_time=0.5)
    scene.wait(5.5)  # VO hold — adjust via tools/adjust_waits.py after read-aloud
    scene.play(FadeOut(visual, label), run_time=0.7)
    return {}


class SceneNActMLayout(Scene):
    def construct(self) -> None:
        setup_scene(self)
        plop(self, body_text("Layout plop"), "visual", wait=3.0)
        plop(self, on_screen_label("On-screen label"), "on_screen_label", wait=3.0)


class SceneNActM(Scene):
    def construct(self) -> None:
        setup_scene(self)
        play_actM(self)
