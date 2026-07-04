"""MainActor bridge — ML delegate callbacks → @Published UI (chapter 6)."""

from __future__ import annotations

from manim import *

from components.layout import arrow_between, fit_center, flow_lr, labeled_card, tag_above
from theme import ACCENT, MERGE_OK, MUTED, SUBTEXT, WHITE_TEXT
from typography import body_text, caption_line, chip_label, subtext

LANE_W = 9.0
TICK_W = 0.42
TICK_H = 0.28
PROC_W = 1.2
PROC_H = 0.52


def _callback_ticks(count: int = 7) -> VGroup:
    ticks = VGroup(
        *[
            RoundedRectangle(
                corner_radius=0.05,
                width=TICK_W,
                height=TICK_H,
                fill_color=MUTED,
                fill_opacity=0.28 + (i % 2) * 0.1,
                stroke_color=MUTED,
                stroke_width=1.1,
            )
            for i in range(count)
        ]
    )
    ticks.arrange(RIGHT, buff=0.08)
    return ticks


def _ui_blocks(count: int = 3) -> VGroup:
    items: list[VGroup] = []
    for i in range(count):
        block = RoundedRectangle(
            corner_radius=0.08,
            width=PROC_W,
            height=PROC_H,
            fill_color="#1e1e28",
            fill_opacity=1,
            stroke_color=ACCENT,
            stroke_width=1.3,
        )
        label = chip_label(f"UI {i + 1}", accent=True)
        label.move_to(block.get_center())
        items.append(VGroup(block, label))
    blocks = VGroup(*items)
    blocks.arrange(RIGHT, buff=0.32)
    return blocks


def mainactor_lane_diagram(*, show_footnote: bool = True) -> dict[str, Mobject]:
    """Two lanes: ML delegate on background thread → MainActor for @Published UI."""
    bg_header = caption_line("ML delegate · background thread")
    bg_header.set_color(MUTED)
    bg_lane = _callback_ticks()
    if bg_lane.width < LANE_W:
        bg_lane.stretch_to_fit_width(LANE_W)

    bridge = chip_label("Task { @MainActor in }", accent=True)
    ui_header = caption_line("MainActor · @Published UI")
    ui_header.set_color(ACCENT)
    ui_lane = _ui_blocks()
    target_w = min(LANE_W * 0.72, LANE_W)
    if ui_lane.width < target_w:
        ui_lane.stretch_to_fit_width(target_w)

    top = VGroup(bg_header, bg_lane).arrange(DOWN, buff=0.18, aligned_edge=LEFT)
    bottom = VGroup(ui_header, ui_lane).arrange(DOWN, buff=0.18, aligned_edge=LEFT)

    arrow = Arrow(
        bg_lane.get_bottom() + DOWN * 0.05,
        ui_lane.get_top() + UP * 0.05,
        buff=0.12,
        color=ACCENT,
        stroke_width=2.8,
        tip_length=0.16,
        max_tip_length_to_length_ratio=0.28,
        max_stroke_width_to_length_ratio=12,
    )
    bridge.next_to(arrow, RIGHT, buff=0.22)

    parts: list[Mobject] = [top, arrow, bridge, bottom]
    if show_footnote:
        note = subtext("tap stays on audio thread — ch 3 queue unchanged")
        note.next_to(bottom, DOWN, buff=0.22).align_to(bottom, LEFT)
        parts.append(note)

    diagram = VGroup(*parts)
    diagram.arrange(DOWN, buff=0.28, aligned_edge=LEFT)
    fit_center(diagram)
    diagram.shift(UP * 0.15)

    return {
        "diagram": diagram,
        "bg_lane": bg_lane,
        "ui_lane": ui_lane,
        "arrow": arrow,
        "bridge": bridge,
    }


def published_rule_diagram() -> VGroup:
    """Compact L→R: ML result → MainActor hop → @Published caption."""
    ml = labeled_card("ML result", tag="delegate callback", stroke=MUTED)
    hop = labeled_card("Task { @MainActor in }", tag="thread hop", stroke=ACCENT)
    ui = labeled_card("@Published captionText", tag="MainActor · UI", stroke=MERGE_OK)
    row = flow_lr(ml, hop, ui, buff=0.85)
    a1 = arrow_between(ml, hop)
    a2 = arrow_between(hop, ui)
    note = body_text("@Published mutations must run on MainActor", font_size=15, color=SUBTEXT)
    note.next_to(row, DOWN, buff=0.28)
    group = VGroup(row, a1, a2, note)
    fit_center(group)
    group.shift(UP * 0.1)
    return group


def caption_update_inset() -> VGroup:
    """Live caption update — transcript chunk hops to MainActor UI."""
    header = caption_line("Captions update on main thread")
    header.set_color(ACCENT)
    chunk = labeled_card("transcript chunk", tag="ML callback", stroke=MUTED)
    panel = labeled_card("caption panel refresh", tag="MainActor UI", stroke=MERGE_OK)
    row = flow_lr(chunk, panel, buff=0.85)
    arrow = arrow_between(chunk, panel)
    group = VGroup(header, row, arrow)
    header.next_to(row, UP, buff=0.28).align_to(row, LEFT)
    fit_center(group)
    group.shift(UP * 0.12)
    return group
