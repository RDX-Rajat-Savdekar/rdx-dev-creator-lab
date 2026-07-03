"""Reusable workflow / pipeline diagrams — stage lanes, fork-merge edges, icon nodes.

Use ``aura_capture_pipeline()`` for the standard Aura mic → ML → queue → UI topology.
Other scenes pass a custom ``WorkflowSpec`` or compose stages manually.
"""

from __future__ import annotations

from dataclasses import dataclass

from manim import *

from icons import MIC, SOUND_ANALYSIS, load_icon
from theme import ACCENT, FONT, MUTED, SUBTEXT, WHITE_TEXT
from typography import caption, chip_label, node_label

STAGE_BUFF = 1.05
STAGE_HEADER_BUFF = 0.24
PANEL_FILL = "#14141c"
PANEL_STROKE = "#1e1e28"
NODE_CHIP_H = 0.5
NODE_CHIP_PAD = 0.22


def _glass_panel(
    width: float,
    height: float,
    *,
    accent: bool = False,
    corner_radius: float = 0.14,
) -> RoundedRectangle:
    return RoundedRectangle(
        corner_radius=corner_radius,
        width=width,
        height=height,
        fill_color=PANEL_FILL,
        fill_opacity=0.92,
        stroke_color=ACCENT if accent else MUTED,
        stroke_width=2 if accent else 1.4,
        stroke_opacity=0.75 if accent else 0.42,
    )


def _stage_header(title: str) -> Text:
    header = caption(title)
    header.set_opacity(0.9)
    return header


def _icon_chip(label: str, icon_name: str, *, accent: bool = False) -> VGroup:
    icon = load_icon(icon_name, color=ACCENT if accent else WHITE_TEXT, height=0.34)
    text = node_label(label)
    row = VGroup(icon, text).arrange(RIGHT, buff=0.14)
    plate = RoundedRectangle(
        corner_radius=0.09,
        width=row.width + NODE_CHIP_PAD,
        height=NODE_CHIP_H,
        fill_color=PANEL_STROKE,
        fill_opacity=1,
        stroke_color=ACCENT if accent else MUTED,
        stroke_width=1.2 if accent else 0.9,
        stroke_opacity=0.55 if accent else 0.35,
    )
    row.move_to(plate.get_center())
    return VGroup(plate, row)


def _capture_node() -> VGroup:
    ring = Circle(
        radius=0.4,
        color=ACCENT,
        stroke_width=2.2,
        fill_color=ACCENT,
        fill_opacity=0.14,
    )
    mic = load_icon(MIC, color=ACCENT, height=0.46)
    mic.move_to(ring.get_center())
    core = VGroup(ring, mic)
    tag = chip_label("tap", accent=True)
    tag.next_to(core, DOWN, buff=0.16)
    return VGroup(core, tag)


def _process_node(label: str, *, accent: bool = False, subtitle: str | None = None) -> VGroup:
    text = node_label(label, accent=accent)
    parts = [text]
    if subtitle:
        sub = Text(subtitle, font=FONT, font_size=14, color=SUBTEXT)
        parts.append(sub)
    stack = VGroup(*parts).arrange(DOWN, buff=0.08)
    plate = RoundedRectangle(
        corner_radius=0.1,
        width=max(stack.width + 0.36, 1.35),
        height=stack.height + 0.3,
        fill_color=PANEL_STROKE,
        fill_opacity=1,
        stroke_color=ACCENT if accent else MUTED,
        stroke_width=1.8 if accent else 1.1,
        stroke_opacity=0.7 if accent else 0.4,
    )
    stack.move_to(plate.get_center())
    return VGroup(plate, stack)


def _junction_dot(*, accent: bool = False) -> Dot:
    return Dot(
        radius=0.055,
        color=ACCENT if accent else MUTED,
        fill_opacity=1,
    )


def _curved_flow(
    start: np.ndarray,
    end: np.ndarray,
    *,
    accent: bool = False,
    bend: float = 0.55,
) -> VMobject:
    if abs(start[1] - end[1]) < 0.05:
        ctrl1 = start + RIGHT * 0.55
        ctrl2 = end + LEFT * 0.55
    else:
        ctrl1 = np.array([start[0] + 0.65, start[1] + bend, 0.0])
        ctrl2 = np.array([end[0] - 0.65, end[1] - bend * 0.35, 0.0])
    curve = CubicBezier(start, ctrl1, ctrl2, end)
    color = ACCENT if accent else MUTED
    curve.set_stroke(color, width=2.2 if accent else 1.6, opacity=0.85 if accent else 0.55)
    tip = Arrow(
        curve.point_from_proportion(0.92),
        end,
        buff=0,
        color=color,
        stroke_width=2.2 if accent else 1.6,
        max_tip_length_to_length_ratio=0.28,
        max_stroke_width_to_length_ratio=8,
    )
    return VGroup(curve, tip)


def _straight_flow(start: np.ndarray, end: np.ndarray, *, accent: bool = False) -> Arrow:
    return Arrow(
        start,
        end,
        buff=0.06,
        color=ACCENT if accent else MUTED,
        stroke_width=2.4 if accent else 1.8,
        max_tip_length_to_length_ratio=0.18,
    )


def workflow_stage(
    title: str,
    body: Mobject,
    *,
    accent: bool = False,
    panel_pad: tuple[float, float] = (0.38, 0.32),
) -> VGroup:
    """One lane: caption header + optional glass wrap."""
    header = _stage_header(title)
    pad_x, pad_y = panel_pad
    panel = _glass_panel(body.width + pad_x, body.height + pad_y, accent=accent)
    body.move_to(panel.get_center())
    column = VGroup(panel, body)
    header.next_to(column, UP, buff=STAGE_HEADER_BUFF)
    return VGroup(header, column)


@dataclass
class WorkflowStage:
    title: str
    body: Mobject
    accent: bool = False


def build_workflow_row(stages: list[WorkflowStage]) -> dict[str, Mobject]:
    """Horizontal stage lanes — returns layout pieces for animation."""
    columns = VGroup(
        *[
            workflow_stage(s.title, s.body, accent=s.accent)
            for s in stages
        ]
    )
    columns.arrange(RIGHT, buff=STAGE_BUFF, aligned_edge=DOWN)
    return {
        "stages": columns,
        "columns": VGroup(*[col[1] for col in columns]),  # body+panel only
        "headers": VGroup(*[col[0] for col in columns]),
    }


def aura_capture_pipeline() -> dict[str, Mobject]:
    """Standard Aura integration pipeline — mic tap → ML fork → queue → UI."""
    capture_body = _capture_node()
    capture = workflow_stage("Capture", capture_body, accent=True, panel_pad=(0.42, 0.38))

    speech = _icon_chip("Speech", MIC)
    sound = _icon_chip("SoundAnalysis", SOUND_ANALYSIS)
    ml_stack = VGroup(speech, sound).arrange(DOWN, buff=0.2, aligned_edge=LEFT)
    ml = workflow_stage("On-device ML", ml_stack, accent=True, panel_pad=(0.48, 0.4))

    queue_body = _process_node("queue", subtitle="realtime")
    queue = workflow_stage("Buffer", queue_body)

    ui_body = _process_node("UI @ 90 Hz", accent=True)
    ui = workflow_stage("Present", ui_body, accent=True)

    row = VGroup(capture, ml, queue, ui)
    row.arrange(RIGHT, buff=STAGE_BUFF, aligned_edge=DOWN)
    row.move_to(ORIGIN + UP * 0.05)

    cap_panel = capture[1]
    ml_panel_grp = ml[1]
    queue_panel = queue[1]
    ui_panel = ui[1]

    fork_top = _curved_flow(
        cap_panel.get_right(),
        speech.get_left(),
        accent=True,
        bend=0.45,
    )
    fork_bot = _curved_flow(
        cap_panel.get_right(),
        sound.get_left(),
        accent=True,
        bend=-0.45,
    )
    merge_top = _curved_flow(
        speech.get_right(),
        queue_panel.get_left() + UP * 0.12,
        bend=0.35,
    )
    merge_bot = _curved_flow(
        sound.get_right(),
        queue_panel.get_left() + DOWN * 0.12,
        bend=-0.35,
    )
    to_ui = _straight_flow(queue_panel.get_right(), ui_panel.get_left(), accent=True)

    junction_ml = _junction_dot().move_to(
        np.array(
            [
                (speech.get_right()[0] + queue_panel.get_left()[0]) / 2,
                queue_panel.get_left()[1],
                0,
            ]
        )
    )
    junction_cap = _junction_dot(accent=True).move_to(
        np.array(
            [
                (cap_panel.get_right()[0] + ml_panel_grp.get_left()[0]) / 2,
                cap_panel.get_center()[1],
                0,
            ]
        )
    )

    edges = VGroup(fork_top, fork_bot, merge_top, merge_bot, to_ui, junction_ml, junction_cap)
    diagram = VGroup(row, edges)

    return {
        "diagram": diagram,
        "stages": row,
        "stage_columns": VGroup(capture, ml, queue, ui),
        "edges": edges,
        "headers": VGroup(capture[0], ml[0], queue[0], ui[0]),
        "annotations": VGroup(),  # stage headers replace bottom chips
    }
