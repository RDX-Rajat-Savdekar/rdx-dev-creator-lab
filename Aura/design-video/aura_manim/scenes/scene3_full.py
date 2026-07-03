"""
Chapter 3 — FULL SCENE (one tap, dual pipeline)

  manim -ql scenes/scene3_full.py Scene3Full
  manim -qk --frame_rate 60 scenes/scene3_full.py Scene3Full
"""

from __future__ import annotations

import sys
from pathlib import Path

from manim import Scene

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from review import setup_scene
from scene3_act1 import play_act1
from scene3_act2 import play_act2
from scene3_act3 import play_act3
from scene3_act4 import play_act4
from scene3_act5 import play_act5
from scene3_act6 import play_act6

ENABLED_ACTS: tuple[int, ...] = (1, 2, 3, 4, 5, 6)

ACT_PLAYERS = {
    1: play_act1,
    2: play_act2,
    3: play_act3,
    4: play_act4,
    5: play_act5,
    6: play_act6,
}


class Scene3Full(Scene):
    def construct(self) -> None:
        setup_scene(self)
        for act in ENABLED_ACTS:
            ACT_PLAYERS[act](self, {})
