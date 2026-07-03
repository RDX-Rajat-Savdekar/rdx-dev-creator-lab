"""
Chapter 0 — FULL SCENE (all acts concatenated)

Per-act files still own helpers + layout review + single-act motion.
This file wires approved `play_actN()` calls for fast whole-scene iteration.

Workflow:
  1. Tweak one act in scene0_actN.py (layout plop → single-act motion)
  2. Preview the full chapter here — trim waits / check transitions
  3. Final per-act -qk renders when each beat is locked

Toggle acts while drafting — comment out numbers you are still editing:

  ENABLED_ACTS = (1, 2, 3, 4, 5, 6)

Render (from aura_manim/):
  manim -ql scenes/scene0_full.py Scene0Full          ← whole ch 0 preview
  manim -ql scenes/scene0_full.py Scene0Full --from_animation_number 3  ← jump mid-scene

Final (4K · 60 fps — after all acts approved):
  ../../.venv/bin/manim -qk --frame_rate 60 scenes/scene0_full.py Scene0Full
"""

from __future__ import annotations

import sys
from pathlib import Path

from manim import Scene

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from review import setup_scene
from scene0_act1 import play_act1
from scene0_act2 import play_act2
from scene0_act3 import play_act3
from scene0_act4 import play_act4
from scene0_act5 import play_act5
from scene0_act6 import play_act6

# Comment out acts still in layout review — full scene grows as you approve each beat.
ENABLED_ACTS: tuple[int, ...] = (1, 2, 3, 4, 5, 6)

ACT_PLAYERS = {
    1: play_act1,
    2: play_act2,
    3: play_act3,
    4: play_act4,
    5: play_act5,
    6: play_act6,
}


class Scene0Full(Scene):
    """Full ch 0 clip — only acts listed in ENABLED_ACTS."""

    def construct(self) -> None:
        setup_scene(self)
        for act in (1, 2, 3, 4, 5, 6):
            if act in ENABLED_ACTS:
                ACT_PLAYERS[act](self)
