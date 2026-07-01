"""
Chapter 0 · ACT 3 ONLY — Shared codebase (team contributions)
SCENE-PLAN: 0:25–0:35 · VO idea: everyone contributed code to the hackathon project.

Prev: scene0_act2.py · Next: scene0_act4.py · Assembly: scene0_full.py

Cross-act reuse: `components/team.py` — same TEAM roster as act 2 role cards.

Render:
  manim -ql scenes/scene0_act3.py Scene0Act3Layout
  manim -ql scenes/scene0_act3.py Scene0Act3

Final (4K · 60 fps — after layout + motion approved):
  ../../.venv/bin/manim -qk --frame_rate 60 scenes/scene0_act3.py Scene0Act3

──────────────────────────────────────────────────────────────────────────────
PLAY CHECKLIST — Scene0Act3Layout
  STEP   WHAT YOU SHOULD SEE ON SCREEN
  ────   ─────────────────────────────────────────────────────────────────
  1      Single trunk line + "shared codebase"
  2      + 3 dividers + 4 section segments on the trunk
  3      + All four merges complete (icons on line, green sections, names)

──────────────────────────────────────────────────────────────────────────────
PLAY CHECKLIST — Scene0Act3 (motion · target ~0:25–0:35 · ~10 s)

  PLAY   WHAT YOU SHOULD SEE                         NARRATION / MEANING
  ────   ─────────────────────────────────────────   ─────────────────────────────
  1      Trunk line draws in + header                 Shared repo / main line
  2      Dividers appear → 4 sections               Line splits for each dev
  3–6    Per dev (×4): icon above → drops onto       Each person merges code;
         section · segment flashes green · name       green pulse on merge
  7      Top note + bottom label                      Team-built · shared code
  wait   Hold full frame                              VO finishes beat
  8      Fade out                                     End act 3 → act 4
──────────────────────────────────────────────────────────────────────────────
"""

from __future__ import annotations

import sys
from pathlib import Path

from manim import *

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from components.labels import on_screen_label
from components.team import (
    merge_lane_all_slots,
    merge_lane_complete,
    merge_lane_dividers,
    merge_lane_header,
    merge_lane_sections,
    merge_lane_trunk,
)
from review import plop, setup_scene
from theme import ACCENT, FONT, MERGE_OK, MUTED


LANE_OFFSET = DOWN * 0.05


def team_note() -> Text:
    return Text(
        "Everyone contributed to the codebase",
        font=FONT,
        font_size=20,
        color=MUTED,
    ).to_edge(UP, buff=0.65)


def _shift(*mobs: Mobject) -> None:
    for mob in mobs:
        mob.shift(LANE_OFFSET)


def act3_pieces() -> dict[str, Mobject]:
    trunk = merge_lane_trunk()
    header = merge_lane_header(trunk)
    dividers = merge_lane_dividers()
    sections = merge_lane_sections()
    complete = merge_lane_complete()
    _shift(trunk, header, dividers, sections, complete)
    return {
        "trunk + header": VGroup(header, trunk),
        "dividers + 4 sections": VGroup(dividers, sections),
        "all merges complete": complete,
        "team note": team_note(),
        "on_screen_label": on_screen_label("Team-built · shared code"),
    }


class Scene0Act3Layout(Scene):
    def construct(self) -> None:
        setup_scene(self)
        for name, mob in act3_pieces().items():
            plop(self, mob, name, wait=3.0)


class Scene0Act3(Scene):
    def construct(self) -> None:
        setup_scene(self)
        trunk = merge_lane_trunk()
        header = merge_lane_header(trunk)
        dividers = merge_lane_dividers()
        sections = merge_lane_sections()
        slots = merge_lane_all_slots()
        note = team_note()
        label = act3_pieces()["on_screen_label"]

        _shift(trunk, header, dividers, sections, note, label)
        for slot in slots:
            _shift(slot["section"], slot["icon"], slot["label"], slot["junction"])

        # PLAY 1 — main trunk
        self.play(Create(trunk), FadeIn(header), run_time=0.9)

        # PLAY 2 — split into four sections
        self.play(FadeOut(trunk), run_time=0.25)
        self.play(Create(dividers), FadeIn(sections), run_time=0.75)

        # PLAY 3–6 — each dev merges onto their section (green pulse)
        for slot in slots:
            icon = slot["icon"]
            section = slot["section"]
            junction = slot["junction"]
            label_mob = slot["label"]
            landed = slot["icon_landed"]

            self.play(FadeIn(icon, shift=DOWN * 0.15), run_time=0.35)
            self.play(icon.animate.move_to(landed), run_time=0.5)
            self.play(
                section.animate.set_color(MERGE_OK),
                junction.animate.set_color(MERGE_OK),
                icon.animate.set_stroke(MERGE_OK, width=2.5),
                Indicate(section, color=MERGE_OK, scale_factor=1.03),
                run_time=0.45,
            )
            self.play(FadeIn(label_mob, shift=UP * 0.08), run_time=0.3)

        # PLAY 7
        self.play(FadeIn(note), FadeIn(label, shift=UP * 0.1), run_time=0.5)
        self.wait(4.5)

        # PLAY 8
        all_mobs = VGroup(
            header,
            dividers,
            sections,
            note,
            label,
            *[mob for slot in slots for mob in (slot["icon"], slot["label"], slot["junction"])],
        )
        self.play(FadeOut(all_mobs), run_time=0.7)
