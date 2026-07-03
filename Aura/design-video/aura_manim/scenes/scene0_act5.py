"""
Chapter 0 · ACT 5 ONLY — Prototype disclaimer + D1 live-captions B-roll
SCENE-PLAN: 0:48–0:55 · VO: system design story · hackathon prototype

Prev: scene0_act4.py · Next: scene0_act6.py · Assembly: scene0_full.py

D1 B-roll:
  ``Aura/clips/D1_live-en-captions.mp4`` — trimmed hackathon demo showing live EN
  captions on Vision Pro (source 01:06–01:20 of the full demo). SCENE-PLAN calls
  for a ~4 s flash here as proof the prototype actually worked.

Render:
  manim -ql scenes/scene0_act5.py Scene0Act5Layout
  manim -ql scenes/scene0_act5.py Scene0Act5

Full scene (fast iteration — all enabled acts):
  manim -ql scenes/scene0_full.py Scene0Full

Final (4K · 60 fps — after layout + motion approved):
  ../../.venv/bin/manim -qk --frame_rate 60 scenes/scene0_act5.py Scene0Act5

──────────────────────────────────────────────────────────────────────────────
PLAY CHECKLIST — Scene0Act5Layout
  STEP   WHAT YOU SHOULD SEE ON SCREEN
  ────   ─────────────────────────────────────────────────────────────────
  1      Title card: "System design · prototype"
  2      + Subtitle: "Hackathon Prototype"
  3      + D1 still frame (live captions demo) below card

──────────────────────────────────────────────────────────────────────────────
PLAY CHECKLIST — Scene0Act5 (motion · target ~0:48–0:55 · ~7 s)

  PLAY   WHAT YOU SHOULD SEE                         NARRATION / MEANING
  ────   ─────────────────────────────────────────   ─────────────────────────────
  1      Title + subtitle fade in                    System design · prototype
  wait   Hold — disclaimer card                      VO disclaimer
  2      Card fades out                              Hand off to proof clip
  3      D1 B-roll plays ~4 s (live captions)        Real demo — captions work
  4      B-roll fades out                            Ready for act 6 teaser
──────────────────────────────────────────────────────────────────────────────
"""

from __future__ import annotations

import sys
from pathlib import Path

from manim import *

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from broll import D1_FLASH_DURATION, broll_still, play_broll
from review import plop, setup_scene
from theme import FONT, MUTED, WHITE_TEXT


def prototype_card() -> VGroup:
    title = Text(
        "System design · prototype",
        font=FONT,
        font_size=38,
        color=WHITE_TEXT,
        weight=BOLD,
    )
    subtitle = Text(
        "Hackathon Prototype",
        font=FONT,
        font_size=22,
        color=MUTED,
    )
    subtitle.next_to(title, DOWN, buff=0.35)
    return VGroup(title, subtitle).move_to(ORIGIN)


def act5_pieces() -> dict[str, Mobject]:
    card = prototype_card()
    still = broll_still().next_to(card, DOWN, buff=0.55)
    return {
        "title card": card,
        "D1 b-roll still (live captions)": still,
    }


class Scene0Act5Layout(Scene):
    def construct(self) -> None:
        setup_scene(self)
        for name, mob in act5_pieces().items():
            plop(self, mob, name, wait=3.0)


def play_act5(scene: Scene) -> None:
    """ACT 5 motion — prototype disclaimer + D1 B-roll (0:48–0:55)."""
    card = prototype_card()

    # PLAY 1
    scene.play(FadeIn(card, shift=UP * 0.12), run_time=0.9)
    scene.wait(3.3)
    # PLAY 2
    scene.play(FadeOut(card), run_time=0.4)
    # PLAY 3 — D1 live-captions flash (~4 s)
    play_broll(scene, duration=D1_FLASH_DURATION)


class Scene0Act5(Scene):
    def construct(self) -> None:
        setup_scene(self)
        play_act5(self)
