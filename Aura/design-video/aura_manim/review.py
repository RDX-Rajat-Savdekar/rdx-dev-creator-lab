"""Shared review helpers — plop assets one at a time while learning each act."""

from __future__ import annotations

from manim import *

from theme import AURA_BG, FONT, MUTED


def setup_scene(scene: Scene) -> None:
    scene.camera.background_color = AURA_BG


def plop(scene: Scene, mob: Mobject, name: str, wait: float = 2.5) -> None:
    """Fade in one asset, tag it top-left, hold so you can inspect the frame."""
    tag = Text(name, font=FONT, font_size=16, color=MUTED).to_corner(UL, buff=0.35)
    scene.play(FadeIn(mob), FadeIn(tag), run_time=0.5)
    scene.wait(wait)
    scene.play(FadeOut(tag), run_time=0.25)
