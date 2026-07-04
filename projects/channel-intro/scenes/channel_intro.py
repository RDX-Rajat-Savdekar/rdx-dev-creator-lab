"""
Channel intro — cinematic Sharingan bumper (~11 s)

ACT 1  Eyelids open — two eyes reveal
ACT 2  Synchronized tracking — API · Git · JSON · HTTP · ML · Swift
ACT 3  Eyes collide → flash + shockwave
ACT 4  RDX logo + tagline reveal → fade out

Render (from channel-intro/):
  ../.venv/bin/manim -ql scenes/channel_intro.py ChannelIntroCinematic
  ../.venv/bin/manim -qh --frame_rate 60 scenes/channel_intro.py ChannelIntroCinematic
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from manim import *

from components.logo_card import channel_logo
from components.sharingan_eye import SharinganEye
from theme import ACCENT, BG, CHIP_BG, CHIP_STROKE, MUTED, SHARINGAN_RED, WHITE


class ChannelIntroCinematic(MovingCameraScene):
    """Sharingan tracking bumper → RDX logo."""

    def construct(self) -> None:
        self.camera.background_color = BG

        left_eye = SharinganEye(height=1.55).shift(LEFT * 2.35 + UP * 0.05)
        right_eye = SharinganEye(height=1.55, mirror=True).shift(RIGHT * 2.35 + UP * 0.05)
        eyes = VGroup(left_eye, right_eye)
        self.add(eyes)

        vignette = self._vignette()
        self.add(vignette)
        eyes.set_z_index(2)

        # ── ACT 1 — eyelids open ──────────────────────────────────────────
        self.play(
            AnimationGroup(
                left_eye.open_eyelids(run_time=1.15),
                right_eye.open_eyelids(run_time=1.15),
                lag_ratio=0.06,
            )
        )
        left_eye.start_idle_spin()
        right_eye.start_idle_spin()
        self.wait(0.25)

        # ── ACT 2 — track floating tech chips ─────────────────────────────
        track_points = [
            np.array([-5.2, 2.0, 0.0]),
            np.array([-1.5, 2.65, 0.0]),
            np.array([2.2, 2.35, 0.0]),
            np.array([5.0, 1.55, 0.0]),
            np.array([4.6, -1.8, 0.0]),
            np.array([-4.8, -2.1, 0.0]),
        ]
        labels = ["API", "Git", "JSON", "HTTP", "ML", "Swift"]

        chips: list[VGroup] = []
        sight_lines = VGroup()

        for point, label in zip(track_points, labels):
            chip = self._chip(label).move_to(point)
            chips.append(chip)

        for chip in chips:
            self.play(FadeIn(chip, scale=0.85, shift=UP * 0.08), run_time=0.18)

        for chip in chips:
            target = chip.get_center()
            line = DashedLine(
                left_eye.iris.get_center(),
                target,
                dash_length=0.06,
                color=SHARINGAN_RED,
                stroke_width=1.1,
                stroke_opacity=0.35,
            )
            sight_lines.add(line)
            self.play(
                AnimationGroup(
                    left_eye.look_at(target, run_time=0.38),
                    right_eye.look_at(target, run_time=0.38),
                    Create(line, run_time=0.28),
                    Indicate(chip, color=ACCENT, scale_factor=1.06, run_time=0.32),
                    chip[2].animate.set_stroke(opacity=0.55),
                )
            )
            self.play(FadeOut(line, run_time=0.12))

        self.play(
            LaggedStart(*[FadeOut(c, shift=UP * 0.12) for c in chips], lag_ratio=0.04),
            run_time=0.45,
        )

        # ── ACT 3 — collide + flash ───────────────────────────────────────
        left_eye.stop_idle_spin()
        right_eye.stop_idle_spin()

        self.play(
            left_eye.spin_up(run_time=0.35),
            right_eye.spin_up(run_time=0.35),
        )

        collide = AnimationGroup(
            left_eye.animate.move_to(LEFT * 0.08).scale(1.18),
            right_eye.animate.move_to(RIGHT * 0.08).scale(1.18),
            run_time=0.72,
            rate_func=rush_into,
        )
        self.play(collide)

        shock = Circle(radius=0.15, stroke_color=SHARINGAN_RED, stroke_width=3, stroke_opacity=0.9)
        shock.set_fill(SHARINGAN_RED, opacity=0.08)
        shock.move_to(ORIGIN)
        flash_core = Circle(radius=0.08, fill_color=WHITE, fill_opacity=1, stroke_width=0)
        flash_halo = Annulus(
            inner_radius=0.05,
            outer_radius=0.22,
            fill_color=WHITE,
            fill_opacity=0.55,
            stroke_width=0,
        )
        burst = VGroup(flash_core, flash_halo, shock).move_to(ORIGIN)

        self.add(burst)
        self.play(
            flash_core.animate.scale(22).set_opacity(0),
            flash_halo.animate.scale(18).set_opacity(0),
            shock.animate.scale(14).set_stroke(opacity=0).set_fill(opacity=0),
            FadeOut(eyes, run_time=0.35),
            run_time=0.65,
            rate_func=rush_from,
        )
        self.remove(burst, eyes, left_eye, right_eye)

        # ── ACT 4 — logo reveal (post-flash) ─────────────────────────────
        logo = channel_logo(scale=1.0)
        brand, reflection = logo
        logo.set_z_index(5)
        self.add(logo)
        self.play(
            FadeIn(brand, shift=UP * 0.15, scale=0.94),
            FadeIn(reflection, shift=DOWN * 0.08),
            run_time=0.9,
            rate_func=smooth,
        )
        self.play(
            Flash(
                brand[0],
                color=SHARINGAN_RED,
                flash_radius=1.8,
                line_length=0.35,
                num_lines=18,
                run_time=0.55,
            )
        )
        self.wait(0.85)
        self.play(FadeOut(logo), FadeOut(vignette), run_time=0.45)

    def _chip(self, label: str) -> VGroup:
        text = Text(label, font="Helvetica Neue", weight=BOLD, font_size=24)
        text.set_color(WHITE)
        pad_w = max(text.width + 0.62, 1.05)
        pad_h = 0.52
        box = RoundedRectangle(
            corner_radius=0.12,
            width=pad_w,
            height=pad_h,
            fill_color=CHIP_BG,
            fill_opacity=0.96,
            stroke_color=CHIP_STROKE,
            stroke_width=1.2,
            stroke_opacity=0.85,
        )
        text.move_to(box.get_center())
        glow = box.copy().set_stroke(SHARINGAN_RED, width=2.2, opacity=0).set_fill(opacity=0)
        return VGroup(box, text, glow)

    def _vignette(self) -> VGroup:
        frame = Rectangle(
            width=config.frame_width,
            height=config.frame_height,
            stroke_width=0,
            fill_color=BG,
            fill_opacity=0,
        )
        ring = Circle(
            radius=config.frame_width * 0.72,
            stroke_color=BLACK,
            stroke_width=2.8,
            stroke_opacity=0.55,
        )
        ring.set_fill(BG, opacity=0.22)
        return VGroup(frame, ring)


class ChannelIntroSample(ChannelIntroCinematic):
    """Alias for quick preview renders."""

    pass
