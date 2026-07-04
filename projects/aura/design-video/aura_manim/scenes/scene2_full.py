"""
Chapter 2 — FULL SCENE (build vs train)

  manim -ql scenes/scene2_full.py Scene2Full
  manim -qk --frame_rate 60 scenes/scene2_full.py Scene2Full
"""

from __future__ import annotations

import sys
from pathlib import Path

from manim import Scene

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from review import setup_scene
from scene2_act1 import play_act1
from scene2_act2 import play_act2
from scene2_act3 import play_act3
from scene2_act4 import play_act4
from scene2_act5 import play_act5
from scene2_act6 import play_act6

ENABLED_ACTS: tuple[int, ...] = (1, 2, 3, 4, 5, 6)

ACT_PLAYERS = {
    1: play_act1,
    2: play_act2,
    3: play_act3,
    4: play_act4,
    5: play_act5,
    6: play_act6,
}


class Scene2Full(Scene):
    def construct(self) -> None:
        setup_scene(self)
        state: dict = {"chain": True}
        for act in ENABLED_ACTS:
            if act == 1:
                state = ACT_PLAYERS[act](self, state)
            else:
                ACT_PLAYERS[act](self, state)
