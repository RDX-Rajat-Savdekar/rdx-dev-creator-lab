"""Vision Pro device boundary — chapter 1+ on-device diagrams."""

from __future__ import annotations

from manim import *

from icons import VISION_PRO, load_icon
from theme import ACCENT, FONT, MUTED, WHITE_TEXT

# Keep in sync with rejected.py DIAGRAM_Y / DEVICE_ANCHOR.
DIAGRAM_Y = 0.12
DEVICE_ANCHOR = LEFT * 2.65 + UP * DIAGRAM_Y

BOUNDARY_W = 3.35
BOUNDARY_H = 2.45


def device_boundary_box() -> RoundedRectangle:
    return RoundedRectangle(
        corner_radius=0.22,
        width=BOUNDARY_W,
        height=BOUNDARY_H,
        stroke_color=ACCENT,
        stroke_width=2.5,
        fill_color="#14141c",
        fill_opacity=0.55,
    )


def vision_pro_icon(*, height: float = 1.05) -> Mobject:
    try:
        return load_icon(VISION_PRO, color=WHITE_TEXT, height=height)
    except FileNotFoundError:
        return vision_pro_silhouette().scale(0.42)


def vision_pro_silhouette() -> VGroup:
    """Fallback goggle — same geometry as scene0 act 6."""
    band = RoundedRectangle(
        corner_radius=0.35,
        width=2.8,
        height=0.85,
        fill_color="#14141c",
        fill_opacity=1,
        stroke_color=ACCENT,
        stroke_width=2,
    )
    lens_l = RoundedRectangle(
        corner_radius=0.2,
        width=0.95,
        height=0.58,
        fill_color="#0a0a0f",
        fill_opacity=1,
        stroke_color=MUTED,
        stroke_width=1.2,
    ).move_to(band.get_center() + LEFT * 0.62)
    lens_r = lens_l.copy().move_to(band.get_center() + RIGHT * 0.62)
    return VGroup(band, lens_l, lens_r)


def device_boundary_group(*, anchor: np.ndarray = DEVICE_ANCHOR) -> VGroup:
    """Rounded trust boundary + Vision Pro glyph."""
    box = device_boundary_box()
    icon = vision_pro_icon()
    icon.move_to(box.get_center())
    group = VGroup(box, icon)
    group.move_to(anchor)
    return group
