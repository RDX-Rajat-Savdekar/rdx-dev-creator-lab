"""
Chapter 0 · ACT 2 ONLY — Hackathon frame · 24h · Oct 2025 · team roles
SCENE-PLAN: 0:15–0:25 · SCRIPT: "Twenty-four hours. Three-person team."

Prev: scene0_act1.py · Next: scene0_act3.py · Assembly: scene0_full.py
Team roster: components/team.py (shared with act 3+)

Render:
  manim -ql scenes/scene0_act2.py Scene0Act2Layout
  manim -ql scenes/scene0_act2.py Scene0Act2

Final (4K · 60 fps — after layout + motion approved):
  ../../.venv/bin/manim -qk --frame_rate 60 scenes/scene0_act2.py Scene0Act2

──────────────────────────────────────────────────────────────────────────────
PLAY CHECKLIST — Scene0Act2Layout (layout plop)
  STEP   WHAT YOU SHOULD SEE ON SCREEN
  ────   ─────────────────────────────────────────────────────────────────
  0      Clock SVG + "24h" centered alone (review the glyph first)
  1      Time block at left (clock + 24h stacked)
  2      + "Oct 2025" + "LA Tech Week · USC ISI" beside time block
  3      + 2×2 team grid (4 role cards, Lead Developer highlighted)
  4      + Bottom label: "24h hackathon · Oct 2025"

──────────────────────────────────────────────────────────────────────────────
PLAY CHECKLIST — Scene0Act2 (motion · target ~0:15–0:25 · ~10 s)

  PLAY   run_time   WHAT YOU SHOULD SEE              NARRATION / MEANING
  ────   ────────   ─────────────────────────────   ─────────────────────────────
  1      1.0 s      Clock + "24h" fade in (left)     "24-hour hackathon…"
  2      0.9 s      Oct 2025 + USC ISI venue         "October 2025 · LA Tech Week"
  3      1.4 s      4 role cards fade in (2×2 grid)  Team frame
  4      0.6 s      Lead Developer card pulses         You = lead dev (highlight)
  5      0.5 s      Bottom label fades in            On-screen: 24h hackathon · Oct 2025
  wait   5.3 s      Hold — full frame                VO finishes beat
  6      0.7 s      Everything fades out             End of act 2 → act 3
──────────────────────────────────────────────────────────────────────────────
"""

from __future__ import annotations

import sys
from pathlib import Path

from manim import *

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from icons import CLOCK, load_icon
from components.labels import on_screen_label
from components.team import lead_card, team_grid
from review import plop, setup_scene
from theme import ACCENT, FONT, MUTED, WHITE_TEXT


# =============================================================================
# ACT 2 HELPERS (team cards → components/team.py)
# =============================================================================


def hackathon_time_block() -> VGroup:
    """Clock SVG + 24h caption — no hand-drawn clock hands."""
    clock = load_icon(CLOCK, color=ACCENT, height=0.85)
    hours = Text("24h", font=FONT, font_size=30, color=WHITE_TEXT, weight=BOLD)
    return VGroup(clock, hours).arrange(DOWN, buff=0.28)


def date_venue_block() -> VGroup:
    date = Text("Oct 2025", font=FONT, font_size=30, color=WHITE_TEXT, weight=BOLD)
    venue = Text("LA Tech Week · USC ISI", font=FONT, font_size=20, color=MUTED)
    return VGroup(date, venue).arrange(DOWN, buff=0.28, aligned_edge=LEFT)


def act2_left_column() -> VGroup:
    time_block = hackathon_time_block()
    dates = date_venue_block()
    column = VGroup(time_block, dates).arrange(RIGHT, buff=0.75, aligned_edge=UP)
    column.move_to(LEFT * 2.45 + UP * 0.15)
    return column


def act2_pieces() -> dict[str, Mobject]:
    left = act2_left_column()
    return {
        "time block · clock + 24h": left[0],
        "date + venue": left[1],
        "team grid · 4 roles": team_grid(),
        "on_screen_label": on_screen_label("24h hackathon · Oct 2025"),
    }


# =============================================================================
# STEP 1 — LAYOUT PREVIEW
# =============================================================================


class Scene0Act2Layout(Scene):
    def construct(self) -> None:
        setup_scene(self)
        solo = hackathon_time_block().move_to(ORIGIN)
        plop(self, solo, "clock + 24h SOLO", wait=4.0)
        self.play(FadeOut(solo), run_time=0.4)
        self.wait(0.3)
        for name, mob in act2_pieces().items():
            plop(self, mob, name, wait=3.0)


# =============================================================================
# STEP 2 — MOTION
# =============================================================================


class Scene0Act2(Scene):
    def construct(self) -> None:
        setup_scene(self)
        left = act2_left_column()
        time_block = left[0]
        dates = left[1]
        team = team_grid()
        lead_card_mob = lead_card(team)
        label = act2_pieces()["on_screen_label"]

        # PLAY 1
        self.play(FadeIn(time_block, shift=UP * 0.1), run_time=1.0)
        # PLAY 2
        self.play(FadeIn(dates, shift=RIGHT * 0.12), run_time=0.9)
        # PLAY 3
        self.play(FadeIn(team, shift=UP * 0.1), run_time=1.4)
        self.wait(1)
        # PLAY 4 — highlight lead developer (you)
        self.play(Indicate(lead_card_mob, color=ACCENT, scale_factor=1.06), run_time=0.6)
        # PLAY 5
        self.play(FadeIn(label, shift=UP * 0.1), run_time=0.5)
        self.wait(5.3)
        # PLAY 6
        self.play(FadeOut(left, team, label), run_time=0.7)
