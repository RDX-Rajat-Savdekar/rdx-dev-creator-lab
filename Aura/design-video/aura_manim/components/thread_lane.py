"""Tap callback vs serial AnalysisQueue — chapter 3 act 3."""

from __future__ import annotations

from manim import *

from theme import ACCENT, FONT, MERGE_OK, MUTED, SUBTEXT, WHITE_TEXT
from typography import caption, chip_label, subtext

LANE_W = 9.2
TICK_W = 0.42
TICK_H = 0.28
PROC_W = 1.15
PROC_H = 0.52


def _tap_ticks(count: int = 8) -> VGroup:
    ticks = VGroup(
        *[
            RoundedRectangle(
                corner_radius=0.05,
                width=TICK_W,
                height=TICK_H,
                fill_color=ACCENT,
                fill_opacity=0.35 + (i % 2) * 0.12,
                stroke_color=ACCENT,
                stroke_width=1.2,
            )
            for i in range(count)
        ]
    )
    ticks.arrange(RIGHT, buff=0.08)
    return ticks


def _queue_blocks(count: int = 3) -> VGroup:
    items: list[VGroup] = []
    for i in range(count):
        block = RoundedRectangle(
            corner_radius=0.08,
            width=PROC_W,
            height=PROC_H,
            fill_color="#1e1e28",
            fill_opacity=1,
            stroke_color=MUTED,
            stroke_width=1.2,
        )
        label = Text(f"job {i + 1}", font=FONT, font_size=13, color=SUBTEXT)
        label.move_to(block.get_center())
        items.append(VGroup(block, label))
    blocks = VGroup(*items)
    blocks.arrange(RIGHT, buff=0.35)
    return blocks


def thread_lane_diagram(*, show_footnote: bool = True) -> dict[str, Mobject]:
    """Two lanes: realtime tap (top) dispatches to serial AnalysisQueue (bottom)."""
    tap_header = caption("Tap callback · realtime")
    tap_header.set_color(ACCENT)
    tap_lane = _tap_ticks()
    if tap_lane.width < LANE_W:
        tap_lane.stretch_to_fit_width(LANE_W)

    dispatch = chip_label("dispatch async", accent=True)
    block_warn = subtext("never block tap", font_size=16)
    block_warn.set_color(MERGE_OK)

    queue_header = caption("com.aura.AnalysisQueue · serial")
    queue_lane = _queue_blocks()
    target_w = min(LANE_W * 0.72, LANE_W)
    if queue_lane.width < target_w:
        queue_lane.stretch_to_fit_width(target_w)

    top = VGroup(tap_header, tap_lane).arrange(DOWN, buff=0.18, aligned_edge=LEFT)
    bottom = VGroup(queue_header, queue_lane).arrange(DOWN, buff=0.18, aligned_edge=LEFT)

    arrow = Arrow(
        tap_lane.get_bottom() + DOWN * 0.05,
        queue_lane.get_top() + UP * 0.05,
        buff=0.12,
        color=ACCENT,
        stroke_width=2,
        max_tip_length_to_length_ratio=0.2,
    )
    dispatch.next_to(arrow, RIGHT, buff=0.22)

    parts: list[Mobject] = [top, arrow, dispatch, bottom]
    if show_footnote:
        block_warn.next_to(bottom, DOWN, buff=0.22).align_to(bottom, LEFT)
        parts.append(block_warn)

    diagram = VGroup(*parts)
    diagram.arrange(DOWN, buff=0.28, aligned_edge=LEFT)
    diagram.move_to(ORIGIN + UP * 0.2)

    return {
        "diagram": diagram,
        "tap_lane": tap_lane,
        "queue_lane": queue_lane,
        "arrow": arrow,
    }
