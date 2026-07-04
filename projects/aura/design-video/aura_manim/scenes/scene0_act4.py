"""
Chapter 0 · ACT 4 ONLY — Sphere POC (first Vision Pro build)
SCENE-PLAN: 0:35–0:48 · VO: "red" → color, louder → scale

Prev: scene0_act3.py · Next: scene0_act5.py · Assembly: scene0_full.py

Render:
  manim -ql scenes/scene0_act4.py Scene0Act4Layout
  manim -ql scenes/scene0_act4.py Scene0Act4

Full scene (fast iteration — all enabled acts):
  manim -ql scenes/scene0_full.py Scene0Full

Final (4K · 60 fps — after layout + motion approved):
  ../../.venv/bin/manim -qk --frame_rate 60 scenes/scene0_act4.py Scene0Act4

──────────────────────────────────────────────────────────────────────────────
PLAY CHECKLIST — Scene0Act4Layout
  STEP   WHAT YOU SHOULD SEE ON SCREEN
  ────   ─────────────────────────────────────────────────────────────────
  1      "First Vision Pro build" note (top)
  2      + Neutral gray sphere (center)
  3      + '"red"' cue above sphere
  4      + "louder" cue + audio-wave icon below
  5      + Bottom label: "Day 0: sphere POC"

──────────────────────────────────────────────────────────────────────────────
PLAY CHECKLIST — Scene0Act4 (motion · target ~0:35–0:48 · ~13 s)

  PLAY   WHAT YOU SHOULD SEE                         NARRATION / MEANING
  ────   ─────────────────────────────────────────   ─────────────────────────────
  1      Note + neutral sphere fade in               First Vision Pro build
  2      "red" cue appears                           Say "red" → color
  3      Sphere turns red                            Color word maps to color
  4      "louder" + volume bars appear               RMS / loudness cue
  5      Sphere + bars pulsate 3× (louder cue)        Louder → bigger sphere
  6      Bottom label fades in                       Day 0: sphere POC
  wait   Hold full frame                              VO finishes beat
  7      Fade out                                     End act 4 → act 5
──────────────────────────────────────────────────────────────────────────────
"""

from __future__ import annotations

import sys
from pathlib import Path

from manim import *

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from icons import AUDIO_WAVE, load_icon
from components.labels import on_screen_label
from review import plop, setup_scene
from theme import ACCENT, FONT, MUTED, WARN, WHITE_TEXT


def headset_note() -> Text:
    return Text(
        "First Vision Pro build",
        font=FONT,
        font_size=22,
        color=MUTED,
    ).to_edge(UP, buff=0.7)


def neutral_sphere() -> Circle:
    return Circle(
        radius=0.75,
        color=MUTED,
        fill_opacity=0.35,
        stroke_width=2,
    ).move_to(ORIGIN)


def cue_red() -> Text:
    return Text('"red"', font=FONT, font_size=36, color=WHITE_TEXT, slant=ITALIC)


def cue_loud_group() -> VGroup:
    cue = Text("louder", font=FONT, font_size=28, color=MUTED)
    bars = load_icon(AUDIO_WAVE, color=ACCENT, height=0.42)
    group = VGroup(cue, bars).arrange(DOWN, buff=0.25)
    return group


def act4_pieces() -> dict[str, Mobject]:
    sphere = neutral_sphere()
    red_cue = cue_red().next_to(sphere, UP, buff=0.55)
    loud = cue_loud_group().next_to(sphere, DOWN, buff=0.55)
    return {
        "headset note": headset_note(),
        "sphere (neutral)": sphere,
        'cue: "red"': red_cue,
        "cue: louder + vol bars": loud,
        "on_screen_label": on_screen_label("Day 0: sphere POC"),
    }


class Scene0Act4Layout(Scene):
    def construct(self) -> None:
        setup_scene(self)
        for name, mob in act4_pieces().items():
            plop(self, mob, name, wait=3.0)


def play_act4(scene: Scene) -> None:
    """ACT 4 motion — sphere POC (0:35–0:48)."""
    pieces = act4_pieces()
    note = pieces["headset note"]
    sphere = pieces["sphere (neutral)"]
    cue_red = pieces['cue: "red"']
    loud_group = pieces["cue: louder + vol bars"]
    cue_loud = loud_group[0]
    vol_bars = loud_group[1]
    label = pieces["on_screen_label"]

    # PLAY 1
    scene.play(FadeIn(note), FadeIn(sphere), run_time=0.9)
    # PLAY 2
    scene.play(FadeIn(cue_red, shift=DOWN * 0.08), run_time=0.5)
    # PLAY 3
    red_sphere = sphere.copy().set_color(WARN).set_fill(WARN, opacity=0.55)
    scene.play(ReplacementTransform(sphere, red_sphere), run_time=1.0)
    sphere = red_sphere
    scene.wait(0.8)
    # PLAY 4
    scene.play(FadeIn(cue_loud), FadeIn(vol_bars), run_time=0.5)
    # PLAY 5 — sphere + volume bars pulsate 3× (louder → bigger)
    for _ in range(3):
        scene.play(
            sphere.animate.scale(1.45),
            vol_bars.animate.scale(1.25),
            run_time=0.5,
            rate_func=there_and_back,
        )
        scene.wait(0.5)
    # PLAY 6
    scene.play(FadeIn(label, shift=UP * 0.1), run_time=0.5)
    scene.wait(7.0)
    # PLAY 7
    scene.play(FadeOut(note, sphere, cue_red, cue_loud, vol_bars, label), run_time=0.7)


class Scene0Act4(Scene):
    def construct(self) -> None:
        setup_scene(self)
        play_act4(self)
