"""Chapter 7 — FULL SCENE (directional pins → Iron Man HUD)"""

from __future__ import annotations

import sys
from pathlib import Path

from manim import Scene

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from review import setup_scene
from scene7_act1 import play_act1
from scene7_act2 import play_act2
from scene7_act3 import play_act3
from scene7_act4 import play_act4
from scene7_act5 import play_act5
from scene7_act6 import play_act6

ACT_PLAYERS = {
    1: play_act1,
    2: play_act2,
    3: play_act3,
    4: play_act4,
    5: play_act5,
    6: play_act6,
}


class Scene7Full(Scene):
    def construct(self) -> None:
        setup_scene(self)
        for act in (1, 2, 3, 4, 5, 6):
            ACT_PLAYERS[act](self, {})
