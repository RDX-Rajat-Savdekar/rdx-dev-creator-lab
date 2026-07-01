"""
Chapter 0 · ACT 1 ONLY — Noisy room → situational audio gap
SCENE-PLAN: 0:00–0:15 · SCRIPT: "Speech and environmental sounds both carry context."

Learning workflow (this repo):
  scene0_act1.py              ← ACT 1 (this file)
  scene0_act3.py              ← ACT 3 (solo code honesty)
  …
  scene0_full.py              ← joins approved acts (last step)
  scene0_problem_REFERENCE.py ← old monolith — do not render

Render:
  manim -ql scenes/scene0_act1.py Scene0Act1Layout   ← layout plop (step 1)
  manim -ql scenes/scene0_act1.py Scene0Act1          ← motion (step 2)

Final (4K · 60 fps — after layout + motion approved):
  ../../.venv/bin/manim -qk --frame_rate 60 scenes/scene0_act1.py Scene0Act1

──────────────────────────────────────────────────────────────────────────────
PLAY CHECKLIST — Scene0Act1Layout (layout plop, not story timing)
Verify each step adds one layer; previous layers stay on screen.

  STEP   WHAT YOU SHOULD SEE ON SCREEN
  ────   ─────────────────────────────────────────────────────────────────
  1      Room rectangle + red noise arcs (top-right corner of box)
  2      Column 1: "Hey..." bubble + bell icon below it
  3      + Column 2: "...wait" bubble + red alert triangle below
  4      + Column 3: "Behind you!" bubble + audio-wave icon below
  5      + Bottom label: "Situational audio gap"
         (Top-left tag shows helper name briefly, then fades — ignore in final)

──────────────────────────────────────────────────────────────────────────────
PLAY CHECKLIST — Scene0Act1 (motion · target ~0:00–0:15)
Match each PLAY # in construct() to what you see in the exported video.

  PLAY   run_time   WHAT YOU SHOULD SEE              NARRATION / MEANING
  ────   ────────   ─────────────────────────────   ─────────────────────────────
  1      0.8 s      Room box fades in                "A noisy room…"
  2      2.2 s      3 columns fade in (shift up):    Speech + environmental
                      Hey/bell · wait/alert ·           sounds compete at once
                      Behind you/wave
  wait   0.5 s      Hold — room + all columns        Brief beat before loss
  3      3.0 s      Columns fade out;                Context lost — you miss
                      6 yellow "?" fade in              what was said + heard
  4      0.6 s      Bottom label fades in:           On-screen: Situational
                      "Situational audio gap"         audio gap
  wait   7.2 s      Hold — room + ? marks + label    VO line finishes
  5      0.9 s      Everything fades out             End of act 1

  Final frame before PLAY 5: room + six ? + bottom label.
  After PLAY 5: black (AURA_BG) — ready to cut to act 2.
──────────────────────────────────────────────────────────────────────────────
"""

from __future__ import annotations

import sys
from pathlib import Path

from manim import *

# Manim loads scene files directly — add aura_manim/ to import path.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from icons import ALERT, AUDIO_WAVE, BELL, load_icon
from review import plop, setup_scene
from theme import ACCENT, FONT, MUTED, WARN, WHITE_TEXT


# =============================================================================
# ACT 1 HELPERS
# =============================================================================


def on_screen_label(text: str, font_size: int = 28) -> Text:
    """Bottom-third caption for this beat."""
    label = Text(text, font=FONT, font_size=font_size, color=WHITE_TEXT)
    label.to_edge(DOWN, buff=0.55)
    return label


def room_frame() -> VGroup:
    """Simple room box + red noise ripples in the corner."""
    room = Rectangle(
        width=11.0,
        height=4.2,
        stroke_color=MUTED,
        stroke_width=2,
        fill_color="#12121a",
        fill_opacity=0.35,
    ).move_to(UP * 0.15)
    noise = VGroup(
        *[
            Arc(radius=0.12 + i * 0.05, angle=PI / 2, color=WARN, stroke_width=1.4, stroke_opacity=0.55)
            for i in range(4)
        ]
    ).arrange(RIGHT, buff=0.04).move_to(room.get_corner(UR) + LEFT * 0.55 + DOWN * 0.45)
    return VGroup(room, noise)


def speech_bubble(text: str) -> VGroup:
    """
    Speech the viewer might miss — label + small message icon (SVG).
    Text stays Manim Text (editable per bubble); icon is SVG not hand-drawn lines.
    """
    icon = load_icon("message", color=ACCENT, height=0.42)
    words = Text(text, font=FONT, font_size=20, color=WHITE_TEXT)
    row = VGroup(icon, words).arrange(RIGHT, buff=0.18)
    plate = RoundedRectangle(
        corner_radius=0.14,
        width=row.width + 0.45,
        height=row.height + 0.35,
        fill_color="#1c1c24",
        fill_opacity=0.95,
        stroke_color=ACCENT,
        stroke_width=1.2,
    )
    row.move_to(plate.get_center())
    return VGroup(plate, row)


def speech_sound_column(bubble_text: str, sound_name: str, *, sound_color: str = ACCENT) -> VGroup:
    """One speech bubble stacked above one sound icon — no overlap."""
    bubble = speech_bubble(bubble_text)
    sound = load_icon(sound_name, color=sound_color, height=0.48)
    sound.next_to(bubble, DOWN, buff=0.55)
    return VGroup(bubble, sound)


def act1_content_row() -> VGroup:
    """Three columns: speech on top, environmental sound below."""
    columns = VGroup(
        speech_sound_column("Hey...", BELL, sound_color=ACCENT),
        speech_sound_column("...wait", ALERT, sound_color=WARN),
        speech_sound_column("Behind you!", AUDIO_WAVE, sound_color=ACCENT),
    )
    columns.arrange(RIGHT, buff=0.9).move_to(UP * 0.35)
    return columns


def question_mark() -> Text:
    return Text("?", font=FONT, font_size=44, color=YELLOW, weight=BOLD)


def act1_pieces() -> dict[str, Mobject]:
    """Named layout pieces — Scene0Act1Layout plops these one at a time."""
    columns = act1_content_row()
    return {
        "room_frame()": room_frame(),
        "column 1 · Hey + bell": columns[0],
        "column 2 · wait + alert": columns[1],
        "column 3 · Behind you + wave": columns[2],
        "on_screen_label": on_screen_label("Situational audio gap"),
    }


# =============================================================================
# STEP 1 — LAYOUT PREVIEW (render this first)
# =============================================================================


class Scene0Act1Layout(Scene):
    """Plop ACT 1 pieces slowly — verify positions before motion."""

    def construct(self) -> None:
        setup_scene(self)
        # Layout STEPS 1–5 — see PLAY CHECKLIST at top of file
        for name, mob in act1_pieces().items():
            plop(self, mob, name, wait=3.0)


# =============================================================================
# STEP 2 — MOTION (render after layout looks right)
# =============================================================================


class Scene0Act1(Scene):
    """ACT 1 story motion — 0:00–0:15 target."""

    def construct(self) -> None:
        setup_scene(self)
        pieces = act1_pieces()
        room = pieces["room_frame()"]
        columns = act1_content_row()
        label = pieces["on_screen_label"]

        # PLAY 1 — room fades in (see checklist at top of file)
        self.play(FadeIn(room), run_time=0.8)
        # PLAY 2 — three speech+sound columns fade in together
        self.play(FadeIn(columns, shift=UP * 0.12), run_time=2.2)
        self.wait(0.5)

        # PLAY 3 — columns out → six yellow ? marks in (context lost)
        q_marks = VGroup(
            *[
                question_mark().move_to(src.get_center())
                for col in columns
                for src in (col[0], col[1])
            ]
        )
        self.play(FadeOut(columns), FadeIn(q_marks, scale=0.6), run_time=3)
        # PLAY 4 — bottom label
        self.play(FadeIn(label, shift=UP * 0.1), run_time=0.6)
        self.wait(7.2)  # VO hold — trim after read-aloud
        # PLAY 5 — act end, clear frame for act 2
        self.play(FadeOut(room, q_marks, label), run_time=0.9)
