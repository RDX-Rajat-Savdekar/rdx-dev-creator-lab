"""visionOS Recognition Language picker — chapter 1 act 5."""

from __future__ import annotations

from manim import *

from theme import ACCENT, FONT, MUTED, WHITE_TEXT
from typography import subtext

LOCALES: tuple[str, ...] = (
    "English (US)",
    "English (UK)",
    "Hindi",
    "Spanish",
    "French",
    "German",
    "Japanese",
)

SELECTED_LOCALE = "English (US)"

PANEL_W = 4.35
ROW_W = PANEL_W - 0.55
ROW_H = 0.4
ROW_BUFF = 0.12
PAD_X = 0.32
PAD_TOP = 0.42
PAD_BOTTOM = 0.34

# Manim default frame spans ~14.22 units; keep content inside.
FRAME_RIGHT = 6.55


def _row_band() -> Rectangle:
    return Rectangle(
        width=ROW_W,
        height=ROW_H,
        stroke_width=0,
        fill_opacity=0,
    )


def _locale_row(text: str, *, selected: bool = False) -> VGroup:
    band = _row_band()
    label = Text(text, font=FONT, font_size=18, color=WHITE_TEXT)
    label.align_to(band, LEFT).shift(RIGHT * 0.04)
    parts: list[Mobject] = [band, label]
    if selected:
        check = Text("✓", font=FONT, font_size=19, color=ACCENT)
        check.align_to(band, RIGHT).shift(LEFT * 0.04)
        parts.append(check)
    return VGroup(*parts)


def _row_dividers(rows: VGroup) -> VGroup:
    dividers = VGroup()
    x_left = rows.get_left()[0]
    x_right = rows.get_right()[0]
    for i in range(len(rows) - 1):
        y_mid = (rows[i].get_bottom()[1] + rows[i + 1].get_top()[1]) / 2
        dividers.add(
            Line(
                np.array([x_left, y_mid, 0]),
                np.array([x_right, y_mid, 0]),
                color=MUTED,
                stroke_width=0.7,
                stroke_opacity=0.35,
            )
        )
    return dividers


def recognition_language_panel() -> VGroup:
    title = Text("Recognition Language", font=FONT, font_size=16, color=WHITE_TEXT, weight=BOLD)
    done = Text("Done", font=FONT, font_size=16, color=WHITE_TEXT)
    done_pill = RoundedRectangle(
        corner_radius=0.12,
        width=0.88,
        height=0.36,
        fill_color="#2a2a34",
        fill_opacity=1,
        stroke_color=MUTED,
        stroke_width=1,
    )
    done.move_to(done_pill.get_center())
    done_btn = VGroup(done_pill, done)

    rows = VGroup(*[_locale_row(name, selected=(name == SELECTED_LOCALE)) for name in LOCALES])
    rows.arrange(DOWN, buff=ROW_BUFF, aligned_edge=LEFT)

    header_h = max(title.height, done_btn.height)
    body_h = PAD_TOP + header_h + 0.26 + rows.height + PAD_BOTTOM
    glass = RoundedRectangle(
        corner_radius=0.2,
        width=PANEL_W,
        height=body_h,
        fill_color="#1a1a22",
        fill_opacity=0.94,
        stroke_color=MUTED,
        stroke_width=1.5,
        stroke_opacity=0.5,
    )

    title.align_to(glass.get_left() + RIGHT * PAD_X, LEFT)
    title.align_to(glass.get_top() + DOWN * PAD_TOP, UP)
    done_btn.align_to(glass.get_right() + LEFT * PAD_X, RIGHT)
    done_btn.align_to(glass.get_top() + DOWN * PAD_TOP, UP)

    rows.next_to(glass.get_top() + DOWN * (PAD_TOP + header_h + 0.22), DOWN, buff=0)
    rows.move_to(np.array([glass.get_center()[0], rows.get_center()[1], 0]))
    dividers = _row_dividers(rows)

    return VGroup(glass, title, done_btn, rows, dividers).move_to(LEFT * 1.25 + UP * 0.45)


def tradeoff_note() -> Text:
    return subtext("Trade-off: locale models")


def fact_card() -> VGroup:
    title = Text(
        "0 external deps · ~1,475 LOC",
        font=FONT,
        font_size=20,
        color=WHITE_TEXT,
        weight=BOLD,
    )
    subtitle = subtext("Swift · Apple frameworks only")
    card = VGroup(title, subtitle).arrange(DOWN, buff=0.16, aligned_edge=LEFT)
    plate = RoundedRectangle(
        corner_radius=0.14,
        width=card.width + 0.5,
        height=card.height + 0.42,
        fill_color="#14141c",
        fill_opacity=1,
        stroke_color=ACCENT,
        stroke_width=1.5,
    )
    card.move_to(plate.get_center())
    return VGroup(plate, card)


def act5_layout() -> dict[str, Mobject]:
    picker = recognition_language_panel()
    note = tradeoff_note()
    card = fact_card()

    note.next_to(picker, RIGHT, buff=0.65)
    note.align_to(picker, UP).shift(DOWN * 0.55)
    card.next_to(note, DOWN, buff=0.38).align_to(note, LEFT)

    right_column = VGroup(note, card)
    if right_column.get_right()[0] > FRAME_RIGHT:
        right_column.shift(LEFT * (right_column.get_right()[0] - FRAME_RIGHT))

    return {
        "Recognition Language panel": picker,
        "trade-off note": note,
        "fact card": card,
    }


def locale_hotswap_panel(*, selected: str = "Japanese") -> VGroup:
    """Compact picker for ch 3 — highlights hot-swapped locale."""
    title = Text("Recognition Language", font=FONT, font_size=16, color=WHITE_TEXT, weight=BOLD)
    rows = VGroup(*[_locale_row(name, selected=(name == selected)) for name in LOCALES])
    rows.arrange(DOWN, buff=ROW_BUFF, aligned_edge=LEFT)
    header_h = title.height
    body_h = PAD_TOP + header_h + 0.26 + rows.height + PAD_BOTTOM
    glass = RoundedRectangle(
        corner_radius=0.2,
        width=PANEL_W,
        height=body_h,
        fill_color="#1a1a22",
        fill_opacity=0.94,
        stroke_color=ACCENT,
        stroke_width=1.5,
        stroke_opacity=0.6,
    )
    title.align_to(glass.get_left() + RIGHT * PAD_X, LEFT)
    title.align_to(glass.get_top() + DOWN * PAD_TOP, UP)
    rows.next_to(glass.get_top() + DOWN * (PAD_TOP + header_h + 0.22), DOWN, buff=0)
    rows.move_to(np.array([glass.get_center()[0], rows.get_center()[1], 0]))
    dividers = _row_dividers(rows)
    return VGroup(glass, title, rows, dividers).scale(0.92)


def locale_hotswap_group() -> dict[str, Mobject]:
    panel = locale_hotswap_panel(selected="Japanese")
    chip = subtext("7 locales · no engine restart")
    chip.next_to(panel, DOWN, buff=0.28)
    return {"panel": panel, "chip": chip, "diagram": VGroup(panel, chip)}
