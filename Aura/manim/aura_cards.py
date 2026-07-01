"""Manim text cards and lower-thirds for Aura 60s recruiter clip.

Render from repo root:
  uv run manim -ql Aura/manim/aura_cards.py HookCard
  uv run manim -ql -t Aura/manim/aura_cards.py ProductLowerThird   # transparent overlay

Or run the full assembly:
  uv run python Aura/manim/build_60s.py
"""

from __future__ import annotations

from manim import *

AURA_BG = "#0a0a0f"
ACCENT = "#5ac8fa"  # visionOS-adjacent cyan
MUTED = "#98989d"
FONT = "Helvetica"


def full_card(scene: Scene, headline: str, subline: str | None = None, hold: float = 2.0) -> None:
    scene.camera.background_color = AURA_BG
    head = Text(headline, font=FONT, font_size=44, color=WHITE, weight=BOLD)
    head.move_to(ORIGIN + UP * 0.15)
    group: list[Mobject] = [head]
    if subline:
        sub = Text(subline, font=FONT, font_size=28, color=MUTED)
        sub.next_to(head, DOWN, buff=0.35)
        group.append(sub)
    card = VGroup(*group)
    scene.play(FadeIn(card, shift=UP * 0.12), run_time=0.45)
    scene.wait(hold)
    scene.play(FadeOut(card, shift=UP * 0.08), run_time=0.35)


def lower_third(scene: Scene, text: str, hold: float = 1.5) -> None:
    """Bottom bar label on opaque scenes (unused in 60s build)."""
    bar = RoundedRectangle(
        corner_radius=0.08,
        width=9.2,
        height=0.72,
        fill_color=BLACK,
        fill_opacity=0.72,
        stroke_color=ACCENT,
        stroke_width=1.5,
    )
    bar.to_edge(DOWN, buff=0.35)
    label = Text(text, font=FONT, font_size=30, color=WHITE)
    label.move_to(bar.get_center())
    group = VGroup(bar, label)
    scene.play(FadeIn(group, shift=UP * 0.15), run_time=0.3)
    scene.wait(hold)
    scene.play(FadeOut(group), run_time=0.25)


class TransparentLowerThird(Scene):
    """Bottom bar overlay — render with `manim -t` for alpha."""

    LABEL = ""
    HOLD = 2.0

    def construct(self) -> None:
        bar = RoundedRectangle(
            corner_radius=0.08,
            width=9.2,
            height=0.72,
            fill_color=BLACK,
            fill_opacity=0.72,
            stroke_color=ACCENT,
            stroke_width=1.5,
        )
        bar.to_edge(DOWN, buff=0.35)
        label = Text(self.LABEL, font=FONT, font_size=30, color=WHITE)
        label.move_to(bar.get_center())
        self.add(VGroup(bar, label))
        self.wait(self.HOLD)


# --- Full-screen cards (opaque bg) ---


class HookCard(Scene):
    def construct(self) -> None:
        full_card(self, "Can't hear the room?", hold=2.1)


class ProblemCard(Scene):
    def construct(self) -> None:
        full_card(
            self,
            "Live captions + sound alerts",
            "zero cloud · on-device",
            hold=2.8,
        )


class PipelineCard(Scene):
    def construct(self) -> None:
        full_card(
            self,
            "One mic tap",
            "Speech  +  SoundAnalysis",
            hold=2.8,
        )


class ProofCard(Scene):
    def construct(self) -> None:
        full_card(
            self,
            "2nd place · LA Tech Week",
            "24 h hackathon · solo code",
            hold=4.5,
        )


class CTACard(Scene):
    def construct(self) -> None:
        self.camera.background_color = AURA_BG
        title = Text("Aura", font=FONT, font_size=56, color=WHITE, weight=BOLD)
        sub1 = Text("visionOS · on-device", font=FONT, font_size=30, color=ACCENT)
        sub2 = Text(
            "github.com/RDX-Rajat-Savdekar/Aura-Vision-Pro",
            font=FONT,
            font_size=22,
            color=MUTED,
        )
        foot = Text("Hackathon prototype · Oct 2025", font=FONT, font_size=18, color=MUTED)
        title.move_to(UP * 0.9)
        sub1.next_to(title, DOWN, buff=0.3)
        sub2.next_to(sub1, DOWN, buff=0.45)
        foot.next_to(sub2, DOWN, buff=0.35)
        card = VGroup(title, sub1, sub2, foot)
        self.play(FadeIn(card, shift=UP * 0.1), run_time=0.5)
        self.wait(4.8)
        self.play(FadeOut(card), run_time=0.4)


# --- Lower-thirds (transparent — render with -t) ---


class ProductLowerThird(TransparentLowerThird):
    LABEL = "Aura · visionOS"
    HOLD = 2.8


class SpeechLowerThird(TransparentLowerThird):
    LABEL = "On-device transcription"
    HOLD = 9.5


class SoundLowerThird(TransparentLowerThird):
    LABEL = "Whisper · siren · clap detected"
    HOLD = 11.5


class LocaleLowerThird(TransparentLowerThird):
    LABEL = "7 locales · EN → 日本語"
    HOLD = 9.5
