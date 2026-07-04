"""
Hackathon team — single source of truth for acts 2+.

Import `team_grid()` in act 2, derive names/icons in act 3, Transform in act 4+, etc.
Do NOT duplicate role names or card styling in each act file.

Example (later act):
    from components.team import team_grid
    grid = team_grid()  # same 2×2 cards as act 2

Act 3 uses `merge_lane_*` builders — trunk → 4 sections → progressive merge pulses.
"""

from __future__ import annotations

from dataclasses import dataclass

from manim import *

from icons import LAPTOP, MIC, PALETTE, load_icon
from theme import ACCENT, FONT, MERGE_LANE_LEFT, MERGE_LANE_RIGHT, MERGE_LANE_Y, MERGE_OK, MERGE_SECTION_W, MUTED, WHITE_TEXT

CARD_W = 2.05
CARD_H = 1.55

# Default position from act 2 layout — pass `move_to=` if a later act needs another spot.
TEAM_GRID_ANCHOR = RIGHT * 3.15 + DOWN * 0.05


def merge_section_center(index: int) -> np.ndarray:
    """Center x of merge section 0…3 on the shared trunk."""
    x = MERGE_LANE_LEFT + (index + 0.5) * MERGE_SECTION_W
    return np.array([x, MERGE_LANE_Y, 0.0])


@dataclass(frozen=True)
class TeamMember:
    """One person — used for role cards (act 2) and commit columns (act 3)."""

    short_name: str  # under commit lane
    role_title: str  # on role card
    icon: str
    card_subtitle: str | None = None
    highlight: bool = False
    lane_subtitle: str = ""  # smaller text under short_name on commit lane


TEAM: tuple[TeamMember, ...] = (
    TeamMember("Rajat", "Lead Developer", LAPTOP, "Rajat", True, "Lead dev"),
    TeamMember("Designer", "Designer", PALETTE),
    TeamMember("Technical", "Technical", MIC, lane_subtitle="Tech · audio"),
    TeamMember("Technical", "Technical", MIC, lane_subtitle="Tech · demo"),
)


def role_card(member: TeamMember) -> VGroup:
    icon_color = ACCENT if member.highlight else MUTED
    icon = load_icon(member.icon, color=icon_color, height=0.46)

    title_text = Text(
        member.role_title,
        font=FONT,
        font_size=14,
        color=WHITE_TEXT if member.highlight else MUTED,
        weight=BOLD if member.highlight else NORMAL,
    )
    if member.card_subtitle:
        sub = Text(member.card_subtitle, font=FONT, font_size=13, color=ACCENT)
        labels = VGroup(title_text, sub).arrange(DOWN, buff=0.12)
    else:
        labels = title_text

    stack = VGroup(icon, labels).arrange(DOWN, buff=0.38)
    plate = RoundedRectangle(
        corner_radius=0.14,
        width=CARD_W,
        height=CARD_H,
        fill_color="#1c1c24" if not member.highlight else "#152028",
        fill_opacity=0.95 if not member.highlight else 1.0,
        stroke_color=ACCENT if member.highlight else MUTED,
        stroke_width=2.8 if member.highlight else 1.2,
    )
    if member.highlight:
        plate.set_fill(ACCENT, opacity=0.08)
    stack.move_to(plate.get_center())
    return VGroup(plate, stack)


def team_grid(*, move_to: np.ndarray = TEAM_GRID_ANCHOR) -> VGroup:
    """Act 2 · 2×2 role cards — reuse this VGroup in later acts if visuals should match."""
    cards = VGroup(*[role_card(m) for m in TEAM]).arrange_in_grid(rows=2, cols=2, buff=(0.5, 0.72))
    cards.move_to(move_to)
    return cards


def lead_card(grid: VGroup) -> Mobject:
    """First card in grid — Lead Developer (Rajat)."""
    return grid[0]


def merge_lane_trunk() -> Line:
    """Single shared trunk before it splits into four sections."""
    return Line(
        np.array([MERGE_LANE_LEFT, MERGE_LANE_Y, 0.0]),
        np.array([MERGE_LANE_RIGHT, MERGE_LANE_Y, 0.0]),
        color=MUTED,
        stroke_width=3,
    )


def merge_lane_header(trunk: Line) -> Text:
    header = Text("shared codebase", font=FONT, font_size=14, color=MUTED)
    header.next_to(trunk, UP, buff=0.35)
    return header


def merge_lane_dividers() -> VGroup:
    """Vertical ticks — trunk split into four sections."""
    ticks = VGroup()
    for i in range(1, 4):
        x = MERGE_LANE_LEFT + i * MERGE_SECTION_W
        tick = Line(
            np.array([x, MERGE_LANE_Y - 0.18, 0.0]),
            np.array([x, MERGE_LANE_Y + 0.18, 0.0]),
            color=MUTED,
            stroke_width=2,
        )
        ticks.add(tick)
    return ticks


def merge_section_line(index: int) -> Line:
    """One horizontal section segment (turns green on merge)."""
    x0 = MERGE_LANE_LEFT + index * MERGE_SECTION_W
    x1 = x0 + MERGE_SECTION_W
    return Line(
        np.array([x0, MERGE_LANE_Y, 0.0]),
        np.array([x1, MERGE_LANE_Y, 0.0]),
        color=MUTED,
        stroke_width=6,
    )


def merge_lane_sections() -> VGroup:
    return VGroup(*[merge_section_line(i) for i in range(len(TEAM))])


def merge_slot(member: TeamMember, index: int) -> dict[str, Mobject]:
    """One dev's merge — icon drops onto section center; section pulses green."""
    center = merge_section_center(index)
    section = merge_section_line(index)
    icon = load_icon(member.icon, color=ACCENT, height=0.44)
    icon.move_to(center + UP * 1.2)

    name = Text(member.short_name, font=FONT, font_size=15, color=WHITE_TEXT, weight=BOLD)
    sub_text = member.lane_subtitle or member.role_title
    sub = Text(sub_text, font=FONT, font_size=11, color=MUTED)
    label = VGroup(name, sub).arrange(DOWN, buff=0.1)
    label.move_to(center + DOWN * 0.78)

    junction = Dot(center + UP * 0.06, radius=0.08, color=MUTED)
    icon_landed = center + UP * 0.24

    return {
        "section": section,
        "icon": icon,
        "label": label,
        "junction": junction,
        "icon_landed": icon_landed,
    }


def merge_lane_all_slots() -> list[dict[str, Mobject]]:
    return [merge_slot(member, i) for i, member in enumerate(TEAM)]


def merge_lane_shift(group: Mobject, offset: np.ndarray = DOWN * 0.05) -> Mobject:
    group.shift(offset)
    return group


def merge_lane_complete(*, move_to: np.ndarray = ORIGIN) -> VGroup:
    """All four merges done — for layout plop / end-state reference."""
    trunk = merge_lane_trunk()
    header = merge_lane_header(trunk)
    dividers = merge_lane_dividers()
    parts: list[Mobject] = [header, dividers, trunk]
    for i, slot in enumerate(merge_lane_all_slots()):
        slot["section"].set_color(MERGE_OK)
        slot["icon"].move_to(slot["icon_landed"])
        slot["icon"].set_stroke(MERGE_OK, width=2.5)
        slot["junction"].set_color(MERGE_OK)
        parts.extend([slot["section"], slot["icon"], slot["label"], slot["junction"]])
    block = VGroup(*parts)
    block.move_to(move_to)
    return block
