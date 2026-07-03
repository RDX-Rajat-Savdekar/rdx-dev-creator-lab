"""Chapter 8 — FULL SCENE (Scale)"""

from __future__ import annotations

import sys
from pathlib import Path

from manim import Scene

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from review import setup_scene
from scene8_act1 import play_act1
from scene8_act2 import play_act2
from scene8_act3 import play_act3

ACT_PLAYERS = {1: play_act1, 2: play_act2, 3: play_act3}


class Scene8Full(Scene):
    def construct(self) -> None:
        setup_scene(self)
        for act in (1, 2, 3):
            ACT_PLAYERS[act](self, {})
