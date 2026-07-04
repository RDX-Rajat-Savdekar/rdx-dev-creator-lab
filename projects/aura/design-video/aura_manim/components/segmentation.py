"""Caption segmentation visuals — chapter 4."""

from __future__ import annotations

from manim import *

from components.fit import fit_center
from theme import ACCENT, FONT, MERGE_OK, MUTED, SUBTEXT, WARN, WHITE_TEXT
from typography import caption, subtext

# Short copy for compact panels — avoid scaling text into illegibility.
WALL_FULL = (
    "So um the thing is we were trying to get the transcription to show up on screen "
    "but formatted string just dumps everything at once with no pauses no sentences "
    "no structure and it becomes this unreadable wall of text"
)

WALL_COMPACT = (
    "Everything dumps at once.\n"
    "No pauses. No sentences.\n"
    "Unreadable during live speech."
)

READABLE_LINES = (
    "So we were trying to get transcription on screen.",
    "Formatted string dumps everything at once.",
    "Two-layer split fixed readability.",
)


def _readable_text(
    text: str,
    *,
    font_size: int = 16,
    color: str = WHITE_TEXT,
    width: float | None = None,
) -> Text:
    """Consistent label spacing — disable ligatures, explicit line breaks."""
    kwargs: dict = dict(
        font=FONT,
        font_size=font_size,
        color=color,
        disable_ligatures=True,
        line_spacing=1.15,
    )
    if width is not None:
        kwargs["width"] = width
    return Text(text, **kwargs)


def _caption_card(text: Text, *, stroke: str = ACCENT, min_w: float = 3.6) -> VGroup:
    plate = RoundedRectangle(
        corner_radius=0.1,
        width=max(text.width + 0.48, min_w),
        height=text.height + 0.32,
        fill_color="#1e1e28",
        fill_opacity=1,
        stroke_color=stroke,
        stroke_width=1.2,
        stroke_opacity=0.55,
    )
    text.move_to(plate.get_center())
    return VGroup(plate, text)


def wall_of_text(*, compact: bool = False) -> VGroup:
    """Raw formattedString — dense unreadable block."""
    sample = WALL_COMPACT if compact else WALL_FULL
    font_size = 16 if compact else 15
    body = _readable_text(
        sample,
        font_size=font_size,
        color=SUBTEXT,
        width=9.2 if not compact else None,
    )
    plate = RoundedRectangle(
        corner_radius=0.14,
        width=body.width + 0.5,
        height=body.height + 0.42,
        fill_color="#14141c",
        fill_opacity=1,
        stroke_color=WARN,
        stroke_width=1.5,
        stroke_opacity=0.55,
    )
    body.move_to(plate.get_center())
    tag = caption("formattedString → UI")
    tag.next_to(plate, UP, buff=0.22).align_to(plate, LEFT)
    return VGroup(tag, plate, body)


def readable_caption_chunks() -> VGroup:
    cards = VGroup(
        *[
            _caption_card(_readable_text(line, font_size=15), min_w=4.55)
            for line in READABLE_LINES
        ]
    )
    cards.arrange(DOWN, buff=0.14, aligned_edge=LEFT)
    tag = caption("utterance → sentences")
    tag.set_color(MERGE_OK)
    tag.next_to(cards, UP, buff=0.22).align_to(cards, LEFT)
    return VGroup(tag, cards)


def before_after_segmentation() -> VGroup:
    """Before (wall) LEFT → arrow → after (chunks) RIGHT — centered in frame."""
    before = wall_of_text(compact=True)
    after = readable_caption_chunks()
    VGroup(before, after).arrange(RIGHT, buff=0.65, aligned_edge=UP)
    arrow = Arrow(
        before.get_right(),
        after.get_left(),
        buff=0.12,
        color=ACCENT,
        stroke_width=2.5,
    )
    return fit_center(VGroup(before, arrow, after), margin=1.1)


def _timeline_tick(*, accent: bool = False, wide: bool = False) -> VGroup:
    w = 1.35 if wide else 0.55
    rect = RoundedRectangle(
        corner_radius=0.06,
        width=w,
        height=0.32,
        fill_color=ACCENT if accent else "#1e1e28",
        fill_opacity=0.45 if accent else 0.9,
        stroke_color=ACCENT if accent else MUTED,
        stroke_width=1.2,
    )
    return VGroup(rect)


def utterance_timeline(*, pause_s: float = 1.1) -> VGroup:
    """Speech tokens with visible pause gaps — 1.1 s threshold."""
    ticks = VGroup(
        _timeline_tick(),
        _timeline_tick(),
        _timeline_tick(wide=True),
        _timeline_tick(),
        _timeline_tick(),
    )
    ticks.arrange(RIGHT, buff=0.12)

    gaps = VGroup()
    for i in (1, 2):
        left = ticks[i].get_right()
        right = ticks[i + 1].get_left()
        mid = (left + right) / 2
        brace = Text("‖", font=FONT, font_size=22, color=WARN, disable_ligatures=True)
        brace.move_to(mid + UP * 0.22)
        gap_label = Text(f">{pause_s}s", font=FONT, font_size=14, color=WARN, disable_ligatures=True)
        gap_label.next_to(brace, UP, buff=0.06)
        gaps.add(VGroup(brace, gap_label))

    header = caption("Pause gaps → new utterance")
    header.set_color(ACCENT)
    header.next_to(ticks, UP, buff=0.55).align_to(ticks, LEFT)
    note = subtext("temporal layer · 1.1 s threshold", font_size=16)
    note.next_to(ticks, DOWN, buff=0.28).align_to(ticks, LEFT)

    return VGroup(header, ticks, gaps, note)


def sentence_split_preview() -> VGroup:
    """One utterance in (left) → sentence chips out (right)."""
    header = caption("Grammatical layer")

    utterance = _readable_text("Dr. Smith arrived e.g. before noon.", font_size=17)
    input_card = _caption_card(utterance, stroke=MUTED, min_w=4.6)

    out_a = _caption_card(_readable_text("Dr. Smith arrived", font_size=15, color=SUBTEXT), min_w=3.4)
    out_b = _caption_card(_readable_text("e.g. before noon.", font_size=15, color=SUBTEXT), min_w=3.4)
    outputs = VGroup(out_a, out_b).arrange(DOWN, buff=0.14, aligned_edge=LEFT)

    VGroup(input_card, outputs).arrange(RIGHT, buff=0.5, aligned_edge=UP)
    arrow = Arrow(
        input_card.get_right(),
        outputs.get_left(),
        buff=0.12,
        color=MUTED,
        stroke_width=2,
    )
    flow = VGroup(input_card, arrow, outputs)
    header.next_to(flow, UP, buff=0.28)
    header.match_x(flow)

    stack = VGroup(header, flow)
    plate = RoundedRectangle(
        corner_radius=0.14,
        width=stack.width + 0.55,
        height=stack.height + 0.48,
        fill_color="#14141c",
        fill_opacity=0.95,
        stroke_color=MUTED,
        stroke_width=1.2,
        stroke_opacity=0.4,
    )
    stack.move_to(plate.get_center())
    return VGroup(plate, stack)
