"""Chapter 4 — FULL SCENE (segmentation)"""

from __future__ import annotations

import sys
from pathlib import Path

from manim import Scene

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from review import setup_scene
from scene4_act1 import play_act1
from scene4_act2 import play_act2
from scene4_act3 import play_act3
from scene4_act4 import play_act4

ACT_PLAYERS = {1: play_act1, 2: play_act2, 3: play_act3, 4: play_act4}


class Scene4Full(Scene):
    def construct(self) -> None:
        setup_scene(self)
        for act in (1, 2, 3, 4):
            ACT_PLAYERS[act](self, {})
