"""Chapter 9 — FULL SCENE (Outro)"""

from __future__ import annotations

import sys
from pathlib import Path

from manim import Scene

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from review import setup_scene
from scene9_act1 import play_act1
from scene9_act2 import play_act2
from scene9_act3 import play_act3

ACT_PLAYERS = {1: play_act1, 2: play_act2, 3: play_act3}


class Scene9Full(Scene):
    def construct(self) -> None:
        setup_scene(self)
        for act in (1, 2, 3):
            ACT_PLAYERS[act](self, {})
