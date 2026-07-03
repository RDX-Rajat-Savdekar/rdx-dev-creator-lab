"""
Chapter 1 — FULL SCENE (on-device only)

  manim -ql scenes/scene1_full.py Scene1Full
  manim -qk --frame_rate 60 scenes/scene1_full.py Scene1Full
"""

from __future__ import annotations

import sys
from pathlib import Path

from manim import Scene

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from review import setup_scene
from scene1_act1 import play_act1
from scene1_act2 import play_act2
from scene1_act3 import play_act3
from scene1_act4 import play_act4
from scene1_act5 import play_act5

ENABLED_ACTS: tuple[int, ...] = (1, 2, 3, 4, 5)

ACT_PLAYERS = {
    1: play_act1,
    2: play_act2,
    3: play_act3,
    4: play_act4,
    5: play_act5,
}


class Scene1Full(Scene):
    def construct(self) -> None:
        setup_scene(self)
        state: dict = {"chain": True}
        for act in (1, 2, 3, 4, 5):
            if act in ENABLED_ACTS:
                if act <= 3:
                    state = ACT_PLAYERS[act](self, state)
                else:
                    ACT_PLAYERS[act](self, state)
