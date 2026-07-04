"""
Chapter 0 · ACT 6 ONLY — Aura teaser · Vision Pro + dual pipeline stub
SCENE-PLAN: 0:55–1:05 · VO: on-device speech + sound classification

Prev: scene0_act5.py · Assembly: scene0_full.py

Render:
  manim -ql scenes/scene0_act6.py Scene0Act6Layout
  manim -ql scenes/scene0_act6.py Scene0Act6

Full scene (fast iteration — all enabled acts):
  manim -ql scenes/scene0_full.py Scene0Full

Final (4K · 60 fps — after layout + motion approved):
  ../../.venv/bin/manim -qk --frame_rate 60 scenes/scene0_act6.py Scene0Act6

──────────────────────────────────────────────────────────────────────────────
PLAY CHECKLIST — Scene0Act6Layout
  STEP   WHAT YOU SHOULD SEE ON SCREEN
  ────   ─────────────────────────────────────────────────────────────────
  1      "Aura" title + "visionOS · on-device" subtitle (top)
  2      + Vision Pro goggle silhouette (left)
  3      + Mic tap → Speech + SoundAnalysis pipeline stub (right)

──────────────────────────────────────────────────────────────────────────────
PLAY CHECKLIST — Scene0Act6 (motion · target ~0:55–1:05 · ~10 s)

  PLAY   WHAT YOU SHOULD SEE                         NARRATION / MEANING
  ────   ─────────────────────────────────────────   ─────────────────────────────
  1      Aura title + subtitle fade in               Product name + platform
  2      Vision Pro silhouette fades in              visionOS device
  3      Pipeline stub builds (mic → dual branches)  Speech + SoundAnalysis
  wait   Hold full frame                              VO finishes ch 0
  4      Fade out                                     End chapter 0
──────────────────────────────────────────────────────────────────────────────
"""

from __future__ import annotations

import sys
from pathlib import Path

from manim import *

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from review import plop, setup_scene
from theme import ACCENT, AURA_BG, FONT, MUTED, WHITE_TEXT


def aura_titles() -> VGroup:
    title = Text("Aura", font=FONT, font_size=52, color=WHITE_TEXT, weight=BOLD)
    subtitle = Text("visionOS · on-device", font=FONT, font_size=28, color=ACCENT)
    title.to_edge(UP, buff=0.55)
    subtitle.next_to(title, DOWN, buff=0.2)
    return VGroup(title, subtitle)


def vision_pro_silhouette() -> VGroup:
    """Rounded goggle silhouette — explainer only, not a product render."""
    band = RoundedRectangle(
        corner_radius=0.35,
        width=4.6,
        height=1.35,
        fill_color="#14141c",
        fill_opacity=1,
        stroke_color=ACCENT,
        stroke_width=2.5,
    )
    lens_l = RoundedRectangle(
        corner_radius=0.28,
        width=1.55,
        height=0.95,
        fill_color=AURA_BG,
        fill_opacity=1,
        stroke_color=MUTED,
        stroke_width=1.5,
    ).move_to(band.get_center() + LEFT * 1.05)
    lens_r = lens_l.copy().move_to(band.get_center() + RIGHT * 1.05)
    strap = Line(
        band.get_left() + LEFT * 0.5,
        band.get_right() + RIGHT * 0.5,
        color=MUTED,
        stroke_width=2,
    )
    strap.move_to(band.get_center() + DOWN * 0.72)
    return VGroup(strap, band, lens_l, lens_r)


def pipeline_stub() -> VGroup:
    """Mic tap → Speech + SoundAnalysis — teaser for ch 1–3."""
    mic = VGroup(
        Circle(radius=0.28, color=ACCENT, fill_opacity=0.2, stroke_width=2),
        Dot(radius=0.06, color=WHITE_TEXT),
    )
    mic_label = Text("mic tap", font=FONT, font_size=16, color=MUTED)
    mic_label.next_to(mic, DOWN, buff=0.12)

    speech_box = RoundedRectangle(
        corner_radius=0.12,
        width=2.2,
        height=0.85,
        fill_color="#14141c",
        fill_opacity=1,
        stroke_color=ACCENT,
        stroke_width=2,
    )
    speech_text = Text("Speech", font=FONT, font_size=22, color=WHITE_TEXT)
    speech_text.move_to(speech_box.get_center())

    sound_box = speech_box.copy()
    sound_text = Text("SoundAnalysis", font=FONT, font_size=20, color=WHITE_TEXT)
    sound_text.move_to(sound_box.get_center())

    speech_group = VGroup(speech_box, speech_text)
    sound_group = VGroup(sound_box, sound_text)
    speech_group.move_to(RIGHT * 2.2 + UP * 0.55)
    sound_group.move_to(RIGHT * 2.2 + DOWN * 0.75)

    mic_group = VGroup(mic, mic_label).move_to(LEFT * 2.4)
    arrow_speech = Arrow(
        mic_group.get_right(),
        speech_group.get_left(),
        buff=0.15,
        color=ACCENT,
        stroke_width=2.5,
        max_tip_length_to_length_ratio=0.15,
    )
    arrow_sound = Arrow(
        mic_group.get_right(),
        sound_group.get_left(),
        buff=0.15,
        color=ACCENT,
        stroke_width=2.5,
        max_tip_length_to_length_ratio=0.15,
    )
    on_device = Text("on-device", font=FONT, font_size=18, color=ACCENT)
    on_device.next_to(VGroup(speech_group, sound_group), DOWN, buff=0.35)

    return VGroup(mic_group, arrow_speech, arrow_sound, speech_group, sound_group, on_device)


def act6_pieces() -> dict[str, Mobject]:
    return {
        "Aura title": aura_titles(),
        "vision_pro_silhouette()": vision_pro_silhouette().scale(0.85).move_to(LEFT * 2.0),
        "pipeline_stub()": pipeline_stub().scale(0.82).move_to(RIGHT * 1.55),
    }


class Scene0Act6Layout(Scene):
    def construct(self) -> None:
        setup_scene(self)
        for name, mob in act6_pieces().items():
            plop(self, mob, name, wait=3.0)


def play_act6(scene: Scene) -> None:
    """ACT 6 motion — Aura teaser (0:55–1:05)."""
    pieces = act6_pieces()
    titles = pieces["Aura title"]
    headset = pieces["vision_pro_silhouette()"]
    pipes = pieces["pipeline_stub()"]

    # PLAY 1
    scene.play(FadeIn(titles), run_time=0.8)
    # PLAY 2
    scene.play(FadeIn(headset, shift=RIGHT * 0.15), run_time=0.9)
    # PLAY 3
    scene.play(
        LaggedStart(
            Create(pipes[1]),
            Create(pipes[2]),
            FadeIn(pipes[0]),
            FadeIn(pipes[3]),
            FadeIn(pipes[4]),
            FadeIn(pipes[5]),
            lag_ratio=0.18,
        ),
        run_time=2.4,
    )
    scene.wait(5.0)
    # PLAY 4
    scene.play(FadeOut(titles, headset, pipes), run_time=0.9)


class Scene0Act6(Scene):
    def construct(self) -> None:
        setup_scene(self)
        play_act6(self)
