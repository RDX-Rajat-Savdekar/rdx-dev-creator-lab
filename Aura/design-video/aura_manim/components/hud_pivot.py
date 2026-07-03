"""Directional pins → Iron Man HUD pivot — chapter 7 story visuals."""

from __future__ import annotations

import math

from manim import *

from components.layout import arrow_between, fit_center, flow_lr, labeled_card
from icons import ALERT, VISION_PRO, load_icon
from theme import ACCENT, MERGE_OK, MUTED, SUBTEXT, WARN, WHITE_TEXT
from typography import body_text, caption_line, chip_label, subtext

HEAD_CENTER = ORIGIN + UP * 0.05


def _head_node(*, height: float = 0.85) -> VGroup:
    icon = load_icon(VISION_PRO, color=ACCENT, height=height)
    tag = chip_label("user head", accent=True)
    tag.next_to(icon, DOWN, buff=0.12)
    return VGroup(icon, tag)


def _pin_marker(label: str, *, color: str = ACCENT) -> VGroup:
    dot = Dot(radius=0.09, color=color, fill_opacity=1)
    ring = Circle(radius=0.16, color=color, stroke_width=1.8, fill_opacity=0)
    chip = chip_label(label, accent=color == ACCENT)
    chip.next_to(ring, DOWN, buff=0.08)
    return VGroup(dot, ring, chip)


def _ray(from_point: np.ndarray, to_point: np.ndarray, *, color: str = ACCENT) -> Line:
    line = Line(from_point, to_point, color=color, stroke_width=2.2, stroke_opacity=0.75)
    return line


def world_locked_pins_diagram() -> dict[str, Mobject]:
    """Head at center with rays to world-locked sound pins (Manim stands in for Unity)."""
    head = _head_node()
    head.move_to(HEAD_CENTER)

    angles = (-120, -55, 35, 110, 165)
    pins: list[VGroup] = []
    rays: list[Line] = []
    labels = ("siren", "speech", "clap", "whisper", "alert")
    radius = 2.35
    for angle, name in zip(angles, labels):
        rad = math.radians(angle)
        pos = HEAD_CENTER + np.array([radius * math.cos(rad), radius * math.sin(rad), 0.0])
        pin = _pin_marker(name)
        pin.move_to(pos)
        pins.append(pin)
        rays.append(_ray(head[0].get_center(), pin[0].get_center()))

    note = subtext("Manim viz · Unity AzimuthRays deferred")
    group = VGroup(head, VGroup(*rays), VGroup(*pins), note)
    note.next_to(head, DOWN, buff=0.55)
    fit_center(group)
    group.shift(UP * 0.08)

    return {"diagram": group, "head": head, "pins": VGroup(*pins), "rays": VGroup(*rays)}


def azimuth_reject_diagram() -> dict[str, Mobject]:
    """Wobble pin + azimuth ≠ position — hardware has direction, not coords."""
    pin = _pin_marker("sound pin", color=WARN)
    pin.shift(RIGHT * 1.8 + UP * 0.35)
    question = body_text("?", font_size=34, color=WARN)
    question.next_to(pin[1], UR, buff=0.05)

    wobble_note = body_text("azimuth ≠ position", font_size=18, color=WHITE_TEXT)
    wobble_note.next_to(pin, DOWN, buff=0.35)

    sub = subtext("direction from mic — no exact world coordinate")
    sub.next_to(wobble_note, DOWN, buff=0.18)

    strike = Line(
        pin.get_left() + LEFT * 0.15 + UP * 0.35,
        pin.get_right() + RIGHT * 0.15 + DOWN * 0.35,
        color=WARN,
        stroke_width=4,
    )

    group = VGroup(pin, question, wobble_note, sub, strike)
    fit_center(group)
    group.shift(UP * 0.12)

    return {"diagram": group, "pin": pin, "strike": strike, "question": question}


HUD_FOV_RADIUS = 3.45
HUD_FOV_ANGLE = 76 * DEGREES
# Panel center distance from head — must sit where wedge is wide enough for the plate.
HUD_PANEL_RADIUS_FRAC = 0.84


def _head_fov(*, radius: float = 2.2, angle: float = 70 * DEGREES) -> tuple[Sector, Text]:
    """FOV wedge anchored at head forward edge (vertex on right of icon)."""
    half = angle / 2
    fov = Sector(
        radius=radius,
        angle=angle,
        start_angle=-half,
        color=ACCENT,
        fill_opacity=0.12,
        stroke_color=ACCENT,
        stroke_width=1.5,
    )
    fov_label = chip_label("field of view", accent=True)
    return fov, fov_label


def _place_fov_on_head(fov: Sector, fov_label: Text, head: VGroup) -> None:
    """Pivot FOV at the head icon's right edge, opening forward."""
    fov.move_to(head[0].get_right())
    fov_label.next_to(fov, DOWN, buff=0.12)
    fov_label.shift(RIGHT * (fov.radius * 0.2))


def _hud_panel() -> VGroup:
    panel_body = VGroup(
        body_text("Live captions…", font_size=15),
        body_text("siren · emergency vehicle", font_size=14, color=SUBTEXT),
    ).arrange(DOWN, buff=0.12, aligned_edge=LEFT)
    plate = RoundedRectangle(
        corner_radius=0.12,
        width=max(panel_body.width + 0.55, 3.4),
        height=panel_body.height + 0.45,
        fill_color="#14141c",
        fill_opacity=1,
        stroke_color=MERGE_OK,
        stroke_width=2.2,
    )
    panel_body.move_to(plate.get_center())
    return VGroup(plate, panel_body)


def offscreen_hazard_diagram() -> dict[str, Mobject]:
    """Alert behind user — outside FOV cone."""
    head = _head_node(height=0.75)
    head.move_to(LEFT * 0.4 + UP * 0.1)

    fov, fov_label = _head_fov()
    _place_fov_on_head(fov, fov_label, head)

    alert = load_icon(ALERT, color=WARN, height=0.62)
    alert.move_to(LEFT * 3.2 + UP * 0.55)
    alert_tag = body_text("baby cry · behind you", font_size=16, color=WARN)
    alert_tag.next_to(alert, UP, buff=0.12)

    cross = Cross(stroke_color=WARN, stroke_width=4)
    cross.scale(0.38)
    cross.move_to(alert.get_center())

    hazard = body_text("Off-screen alert = missed cue", font_size=17, color=WHITE_TEXT)
    hazard.next_to(head, DOWN, buff=0.45).align_to(head, LEFT)

    group = VGroup(head, fov, fov_label, alert, alert_tag, cross, hazard)
    fit_center(group)
    group.shift(UP * 0.08)

    return {"diagram": group, "alert": alert, "cross": cross, "fov": fov}


def _panel_rest_in_fov(head: VGroup, fov: Sector) -> np.ndarray:
    """Rest position for HUD panel — deep enough in wedge to clear edges."""
    dist = fov.radius * HUD_PANEL_RADIUS_FRAC
    return head[0].get_right() + RIGHT * dist


def iron_man_hud_pieces() -> dict[str, Mobject]:
    """Animatable HUD beat — head, FOV, panel, tag (act 4 motion)."""
    head = _head_node(height=0.68)
    head.move_to(LEFT * 2.05 + UP * 0.02)

    fov, fov_label = _head_fov(radius=HUD_FOV_RADIUS, angle=HUD_FOV_ANGLE)
    _place_fov_on_head(fov, fov_label, head)

    panel = _hud_panel()
    panel_rest = _panel_rest_in_fov(head, fov)
    panel_start = panel_rest + RIGHT * 2.8 + UP * 0.25
    panel.move_to(panel_start)

    tag = caption_line("head-relative · always in view")
    tag.set_color(MERGE_OK)

    unit = VGroup(head, fov, fov_label, panel)
    fit_center(unit)
    unit.shift(UP * 0.12)

    panel_rest = _panel_rest_in_fov(head, fov)
    panel_start = panel_rest + RIGHT * 2.8 + UP * 0.25
    panel.move_to(panel_start)
    pivot = head[0].get_right()

    return {
        "head": head,
        "fov": fov,
        "fov_label": fov_label,
        "panel": panel,
        "tag": tag,
        "unit": unit,
        "pivot": pivot,
        "panel_rest": panel_rest,
        "panel_start": panel_start,
    }


def iron_man_hud_diagram() -> dict[str, Mobject]:
    """Static head-relative HUD — panel seated in FOV (layout plop)."""
    bits = iron_man_hud_pieces()
    bits["panel"].move_to(bits["panel_rest"])
    bits["tag"].next_to(bits["panel"], UP, buff=0.24).align_to(bits["panel"], LEFT)
    diagram = VGroup(bits["unit"], bits["tag"])
    return {
        "diagram": diagram,
        "panel": bits["panel"],
        "head": bits["head"],
        "fov": bits["fov"],
        "unit": bits["unit"],
        "tag": bits["tag"],
    }


def azimuth_grayed_pipeline() -> VGroup:
    """Azimuth computed in DSP — directional UI branch grayed out."""
    compute = labeled_card("azimuth + RMS", tag="computed in DSP", stroke=ACCENT)
    branch = labeled_card("directional pins UI", tag="not shipped", stroke=MUTED)
    branch.set_opacity(0.38)
    row = flow_lr(compute, branch, buff=0.65)
    arrow = arrow_between(compute, branch)
    arrow.set_opacity(0.35)
    strike = Line(
        branch.get_corner(UL) + UP * 0.05 + LEFT * 0.05,
        branch.get_corner(DR) + DOWN * 0.05 + RIGHT * 0.05,
        color=WARN,
        stroke_width=3,
    )
    note = subtext("analysis path keeps azimuth · UI stays head-relative")
    note.next_to(row, DOWN, buff=0.28)
    group = VGroup(row, arrow, strike, note)
    fit_center(group)
    group.shift(UP * 0.12)
    return group
