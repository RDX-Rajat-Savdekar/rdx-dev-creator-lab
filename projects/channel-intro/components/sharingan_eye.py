"""Sharingan eye — SVG iris, rotating tomoe, eyelid reveal, look-at tracking."""

from __future__ import annotations

from pathlib import Path

from manim import *
import numpy as np

from theme import BG, SHARINGAN_DARK, SHARINGAN_RED, SHARINGAN_RING

SVG_PATH = Path(__file__).resolve().parent / "Mangekyou_Sharingan_Itachi.svg"


def mini_sharingan_icon(*, height: float = 0.32) -> VGroup:
    """Compact logo mark — ring + tomoe dots (no full-bleed iris blob)."""
    outer = Circle(
        radius=height * 0.5,
        color=SHARINGAN_RED,
        stroke_width=2.2,
        fill_color=SHARINGAN_DARK,
        fill_opacity=0.85,
    )
    pupil = Dot(radius=height * 0.07, color=BG)
    tomoes = VGroup()
    for angle in (90, 210, 330):
        dot = Dot(radius=height * 0.055, color=BG)
        dot.move_to(
            outer.get_center()
            + height * 0.22 * np.array([np.cos(angle * DEGREES), np.sin(angle * DEGREES), 0.0])
        )
        tomoes.add(dot)
    return VGroup(outer, tomoes, pupil)


def _load_sharingan_glyph(*, height: float = 1.6) -> VGroup:
    """Load iris + tomoe + pupil from SVG; return grouped for independent motion."""
    svg = SVGMobject(str(SVG_PATH))
    svg.set(height=height)

    if len(svg.submobjects) >= 3:
        iris, tomoe, pupil = svg.submobjects[:3]
    else:
        iris = svg
        tomoe = Dot(radius=0.001, fill_opacity=0)
        pupil = Dot(radius=0.001, fill_opacity=0)

    iris.set_fill(SHARINGAN_RED, opacity=1)
    iris.set_stroke(BG, width=2.5, opacity=1)

    tomoe.set_fill(BG, opacity=1)
    tomoe.set_stroke(width=0)

    pupil.set_fill(SHARINGAN_DARK, opacity=1)
    pupil.set_stroke(width=0)

    glyph = VGroup(iris, tomoe, pupil)
    glyph.move_to(ORIGIN)
    return glyph


class SharinganEye(VGroup):
    """One eye: rotating tomoe, pupil offset for tracking, cinematic eyelids."""

    def __init__(self, *, height: float = 1.55, mirror: bool = False, **kwargs):
        super().__init__(**kwargs)
        self.glyph = _load_sharingan_glyph(height=height)
        self.iris, self.tomoe, self.pupil = self.glyph.submobjects

        self.spinner = VGroup(self.tomoe)
        self.spinner.move_to(self.iris.get_center())

        self.pupil_anchor = self.iris.get_center()
        self.look_radius = height * 0.07
        self._look_point = self.pupil_anchor.copy()

        pad = height * 0.55
        w = height * 1.35
        self.upper_lid = Rectangle(
            width=w,
            height=pad,
            fill_color=BG,
            fill_opacity=1,
            stroke_width=0,
        ).next_to(self.iris, UP, buff=0).shift(UP * pad * 0.35)
        self.lower_lid = Rectangle(
            width=w,
            height=pad,
            fill_color=BG,
            fill_opacity=1,
            stroke_width=0,
        ).next_to(self.iris, DOWN, buff=0).shift(DOWN * pad * 0.35)

        self.add(self.glyph, self.upper_lid, self.lower_lid)
        if mirror:
            self.flip(axis=UP)

    def open_eyelids(self, run_time: float = 1.1) -> Animation:
        """Cinematic slit → full open ( lids slide away )."""
        up_shift = UP * self.iris.height * 0.62
        down_shift = DOWN * self.iris.height * 0.62
        return AnimationGroup(
            self.upper_lid.animate.shift(up_shift),
            self.lower_lid.animate.shift(down_shift),
            lag_ratio=0.08,
            run_time=run_time,
            rate_func=smooth,
        )

    def look_at(self, point: np.ndarray, run_time: float = 0.45) -> Animation:
        """Shift pupil toward world point; tomoe follows slightly."""
        delta = np.array(point[:2]) - np.array(self.pupil_anchor[:2])
        norm = np.linalg.norm(delta)
        if norm < 1e-6:
            target = self.pupil_anchor
        else:
            shift = (delta / norm) * min(self.look_radius, norm * 0.08)
            target = self.pupil_anchor + np.array([shift[0], shift[1], 0.0])

        self._look_point = target
        return AnimationGroup(
            self.pupil.animate.move_to(target),
            Rotate(self.spinner, angle=18 * DEGREES, about_point=self.iris.get_center()),
            run_time=run_time,
            rate_func=smooth,
        )

    def spin_up(self, run_time: float = 0.6) -> Animation:
        return Rotate(
            self.spinner,
            angle=360 * DEGREES,
            about_point=self.iris.get_center(),
            run_time=run_time,
            rate_func=linear,
        )

    def start_idle_spin(self, rate: float = 25 * DEGREES) -> None:
        self.spinner.add_updater(
            lambda m, dt: m.rotate(rate * dt, about_point=self.iris.get_center())
        )

    def stop_idle_spin(self) -> None:
        self.spinner.clear_updaters()
