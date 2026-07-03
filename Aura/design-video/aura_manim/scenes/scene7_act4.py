"""Chapter 7 · ACT 4 — Iron Man HUD pivot + D1/D3 montage"""

from __future__ import annotations

import sys
from pathlib import Path

from manim import *

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from broll import D1_LIVE_CAPTIONS, D3_WHISPER, play_montage
from components.hud_pivot import iron_man_hud_diagram, iron_man_hud_pieces
from components.labels import on_screen_label
from review import plop, setup_scene


def play_act4(scene: Scene, state: dict | None = None) -> dict:
    _ = state
    bits = iron_man_hud_pieces()
    head = bits["head"]
    fov = bits["fov"]
    fov_label = bits["fov_label"]
    panel = bits["panel"]
    tag = bits["tag"]
    unit = bits["unit"]
    pivot = bits["pivot"]
    panel_rest = bits["panel_rest"]
    label = on_screen_label("Iron Man HUD")

    scene.play(FadeIn(head, shift=UP * 0.06), run_time=0.6)
    scene.play(GrowFromPoint(fov, pivot), run_time=0.75)
    scene.play(FadeIn(fov_label, shift=UP * 0.06), run_time=0.35)
    panel_rest_scale = 0.4
    scene.play(
        panel.animate.move_to(panel_rest).scale(panel_rest_scale),
        run_time=0.8,
    )
    tag.scale(panel_rest_scale)
    tag.next_to(panel, UP, buff=0.22).align_to(panel, LEFT)
    scene.play(FadeIn(tag, shift=UP * 0.08), run_time=0.5)
    
    motion = VGroup(unit, tag)
    scene.play(motion.animate.scale(1.5), run_time=0.5)
    scene.play(Rotate(motion, angle=10 * DEGREES, about_point=pivot), run_time=0.55)
    scene.play(Rotate(motion, angle=-20 * DEGREES, about_point=pivot), run_time=0.75)
    scene.play(Rotate(motion, angle=10 * DEGREES, about_point=pivot), run_time=0.55)
    scene.play(motion.animate.shift(UP * 0.18), run_time=0.45, rate_func=smooth)
    scene.play(motion.animate.shift(DOWN * 0.36), run_time=0.65, rate_func=smooth)
    scene.play(motion.animate.shift(UP * 0.18), run_time=0.45, rate_func=smooth)
    #reset scale
    scene.play(motion.animate.scale(0.7), run_time=0.5)
    scene.play(FadeIn(label, shift=UP * 0.1), run_time=0.4)
    scene.wait(1.5)
    scene.play(FadeOut(motion, label), run_time=0.5)
    play_montage(
        scene,
        [
            (D1_LIVE_CAPTIONS, 0.0, 3.0),
            (D3_WHISPER, 0.0, 3.0),
        ],
    )
    scene.wait(2.0)
    return {}


class Scene7Act4Layout(Scene):
    def construct(self) -> None:
        setup_scene(self)
        plop(self, iron_man_hud_diagram()["diagram"], "Iron Man HUD", wait=3.0)
        plop(self, on_screen_label("Iron Man HUD"), "on_screen_label", wait=3.0)


class Scene7Act4(Scene):
    def construct(self) -> None:
        setup_scene(self)
        play_act4(self)
