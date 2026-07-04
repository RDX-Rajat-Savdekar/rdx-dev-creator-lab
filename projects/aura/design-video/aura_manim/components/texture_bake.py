"""Texture bake vs 90 Hz loop — chapter 5."""

from __future__ import annotations

from manim import *

from components.fit import fit_center
from theme import ACCENT, CAPTION_SIZE, FONT, MERGE_OK, MUTED, SUBTEXT, WARN, WHITE_TEXT
from typography import caption, chip_label, subtext


def _panel_text(text: str, *, font_size: int = 16, color: str = WHITE_TEXT) -> Text:
    return Text(
        text,
        font=FONT,
        font_size=font_size,
        color=color,
        disable_ligatures=True,
        line_spacing=1.12,
    )


PANEL_W = 3.35
PANEL_H = 2.1


def _hud_panel(label: str, *, jitter: bool = False) -> VGroup:
    plate = RoundedRectangle(
        corner_radius=0.12,
        width=PANEL_W,
        height=PANEL_H,
        fill_color="#1a1a22",
        fill_opacity=1,
        stroke_color=WARN if jitter else MERGE_OK,
        stroke_width=1.8,
    )
    line1 = _panel_text("Live captions here")
    line2 = _panel_text("Sound: clapping", font_size=14, color=SUBTEXT)
    content = VGroup(line1, line2).arrange(DOWN, buff=0.14)
    if jitter:
        content.shift(RIGHT * 0.08 + UP * 0.05)
    content.move_to(plate.get_center())
    tag = chip_label(label, accent=not jitter)
    tag.next_to(plate, DOWN, buff=0.18)
    return VGroup(plate, content, tag)


def hz_loop_diagram() -> dict[str, Mobject]:
    """90 Hz → ViewAttachment (left to right) — rejected path."""
    loop = Circle(radius=0.42, color=ACCENT, stroke_width=2, fill_opacity=0.1)
    loop_lbl = _panel_text("90 Hz", font_size=17, color=ACCENT)
    loop_lbl.move_to(loop.get_center())
    loop_grp = VGroup(loop, loop_lbl)

    attach = RoundedRectangle(
        corner_radius=0.1,
        width=2.4,
        height=0.62,
        stroke_color=MUTED,
        stroke_width=1.5,
        fill_color="#1e1e28",
        fill_opacity=1,
    )
    attach_txt = _panel_text("ViewAttachment", font_size=16)
    attach_txt.move_to(attach.get_center())
    attach_grp = VGroup(attach, attach_txt)

    flow = VGroup(loop_grp, attach_grp).arrange(RIGHT, buff=0.9, aligned_edge=DOWN)
    arrow = Arrow(
        loop_grp.get_right(),
        attach_grp.get_left(),
        buff=0.14,
        color=MUTED,
        stroke_width=2,
    )
    relayout = _panel_text("re-layout each frame", font_size=15, color=WARN)
    relayout.next_to(arrow, UP, buff=0.38)

    cross = Cross(stroke_color=WARN, stroke_width=3.5).scale(0.42)
    cross.move_to(attach.get_center())

    core = VGroup(flow, arrow, relayout, cross)
    note = _panel_text("layout cost tied to render loop", font_size=16, color=SUBTEXT)
    note.next_to(core, DOWN, buff=0.42)

    diagram = fit_center(VGroup(core, note), margin=1.0)
    return {"diagram": diagram, "attach": attach, "cross": cross}


def bake_pipeline_diagram() -> VGroup:
    """SwiftUI → texture → RK quad (left to right)."""
    swift = RoundedRectangle(
        corner_radius=0.1,
        width=1.55,
        height=0.72,
        fill_color="#1e1e28",
        fill_opacity=1,
        stroke_color=ACCENT,
        stroke_width=1.5,
    )
    swift_lbl = _panel_text("SwiftUI", font_size=16)
    swift_lbl.move_to(swift.get_center())
    swift_grp = VGroup(swift, swift_lbl)

    tex = RoundedRectangle(
        corner_radius=0.08,
        width=1.35,
        height=0.62,
        fill_color="#2a2a34",
        fill_opacity=1,
        stroke_color=MUTED,
        stroke_width=1.2,
    )
    tex_lbl = _panel_text("texture", font_size=15, color=SUBTEXT)
    tex_lbl.move_to(tex.get_center())
    tex_grp = VGroup(tex, tex_lbl)

    quad = RoundedRectangle(
        corner_radius=0.1,
        width=1.45,
        height=0.95,
        fill_color="#0f2a38",
        fill_opacity=0.85,
        stroke_color=ACCENT,
        stroke_width=2,
    )
    quad_lbl = _panel_text("RK quad", font_size=15, color=ACCENT)
    quad_lbl.move_to(quad.get_center())
    quad_grp = VGroup(quad, quad_lbl)

    stages = VGroup(swift_grp, tex_grp, quad_grp).arrange(RIGHT, buff=0.55, aligned_edge=DOWN)
    a1 = Arrow(swift_grp.get_right(), tex_grp.get_left(), buff=0.08, color=MUTED, stroke_width=2)
    a2 = Arrow(tex_grp.get_right(), quad_grp.get_left(), buff=0.08, color=ACCENT, stroke_width=2)

    debounce = chip_label("100 ms debounce", accent=True)
    debounce.next_to(tex_grp, DOWN, buff=0.28)
    header = caption("Off-screen bake path")
    header.next_to(stages, UP, buff=0.32)
    header.match_x(stages)

    return fit_center(VGroup(header, stages, a1, a2, debounce), margin=1.0)


def jitter_vs_bake() -> VGroup:
    """Bad path LEFT → good path RIGHT — centered in frame."""
    jitter = _hud_panel("per-frame layout", jitter=True)
    baked = _hud_panel("baked texture", jitter=False)
    panels = VGroup(jitter, baked).arrange(RIGHT, buff=0.7)
    flow = Arrow(
        jitter.get_right(),
        baked.get_left(),
        buff=0.12,
        color=ACCENT,
        stroke_width=2.5,
    )

    title_a = _panel_text("Same captions", font_size=CAPTION_SIZE, color=SUBTEXT)
    title_b = _panel_text("different render path", font_size=CAPTION_SIZE, color=SUBTEXT)
    title = VGroup(title_a, title_b).arrange(DOWN, buff=0.12)
    title.next_to(panels, UP, buff=0.38)
    title.match_x(panels)

    return fit_center(VGroup(title, panels, flow), margin=1.0)
