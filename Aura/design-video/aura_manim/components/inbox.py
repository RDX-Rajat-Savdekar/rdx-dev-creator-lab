"""Mail inbox skit — chapter 2 act 2 (Apple Core ML announcement)."""

from __future__ import annotations

from manim import *

from icons import CURSOR, MAIL, MIC, SOUND_ANALYSIS, load_icon
from theme import ACCENT, FONT, MUTED, WARN, WHITE_TEXT
from typography import caption, subtext, title_line

SUBJECT = "Apple released new Core ML models"


def _cursor_hotspot(cursor: Mobject) -> np.ndarray:
    """Stroke ``cursor.svg`` — pointer tip sits just inside the upper-left."""
    return cursor.get_corner(UL) + RIGHT * cursor.width * 0.06 + DOWN * cursor.height * 0.1


def _move_cursor_tip_to(cursor: Mobject, point: np.ndarray) -> None:
    cursor.shift(point - _cursor_hotspot(cursor))


def cursor_pointer(*, color: str = WHITE_TEXT, height: float = 0.52) -> Mobject:
    return load_icon(CURSOR, color=color, height=height)


def inbox_icon(*, height: float = 0.95) -> VGroup:
    mail = load_icon(MAIL, color=WHITE_TEXT, height=height)
    badge_dot = Circle(radius=0.11, color=WARN, fill_color=WARN, fill_opacity=1, stroke_width=0)
    badge_num = Text("1", font=FONT, font_size=14, color=WHITE_TEXT, weight=BOLD)
    badge = VGroup(badge_dot, badge_num)
    badge_num.move_to(badge_dot.get_center())
    badge.move_to(mail.get_corner(UR) + LEFT * 0.05 + DOWN * 0.05)
    return VGroup(mail, badge)


def _framework_chip(name: str, icon_name: str) -> VGroup:
    icon = load_icon(icon_name, color=ACCENT, height=0.38)
    label = Text(name, font=FONT, font_size=17, color=WHITE_TEXT)
    row = VGroup(icon, label).arrange(RIGHT, buff=0.18)
    plate = RoundedRectangle(
        corner_radius=0.1,
        width=row.width + 0.35,
        height=0.52,
        fill_color="#1a1a22",
        fill_opacity=1,
        stroke_color=MUTED,
        stroke_width=1,
        stroke_opacity=0.45,
    )
    row.move_to(plate.get_center())
    return VGroup(plate, row)


def mail_collapsed(subject: str = SUBJECT) -> VGroup:
    subj = Text(subject, font=FONT, font_size=19, color=WHITE_TEXT, weight=BOLD)
    preview = subtext("Apple · on-device Speech + SoundAnalysis", font_size=17)
    body = VGroup(subj, preview).arrange(DOWN, buff=0.14, aligned_edge=LEFT)
    glass = RoundedRectangle(
        corner_radius=0.14,
        width=body.width + 0.55,
        height=body.height + 0.45,
        fill_color="#1a1a22",
        fill_opacity=0.96,
        stroke_color=MUTED,
        stroke_width=1.5,
        stroke_opacity=0.5,
    )
    body.move_to(glass.get_center())
    return VGroup(glass, body)


def mail_expanded() -> VGroup:
    subject = title_line(SUBJECT, font_size=20)
    speech = _framework_chip("Speech", MIC)
    sound = _framework_chip("SoundAnalysis", SOUND_ANALYSIS)
    chips = VGroup(speech, sound).arrange(DOWN, buff=0.22, aligned_edge=LEFT)
    note = caption("100+ built-in sound labels")
    content = VGroup(subject, chips, note).arrange(DOWN, buff=0.32, aligned_edge=LEFT)
    glass = RoundedRectangle(
        corner_radius=0.16,
        width=max(content.width + 0.65, 5.2),
        height=content.height + 0.65,
        fill_color="#1a1a22",
        fill_opacity=0.96,
        stroke_color=ACCENT,
        stroke_width=1.5,
        stroke_opacity=0.65,
    )
    content.move_to(glass.get_center())
    return VGroup(glass, content)


def inbox_scene_group() -> dict[str, Mobject]:
    inbox = inbox_icon().move_to(LEFT * 2.85 + UP * 0.55)
    cursor = cursor_pointer()
    _move_cursor_tip_to(cursor, inbox.get_center() + RIGHT * 2.2 + UP * 0.8)
    collapsed = mail_collapsed().next_to(inbox, RIGHT, buff=0.75).align_to(inbox, UP)
    expanded = mail_expanded().move_to(collapsed.get_center())
    return {
        "inbox": inbox,
        "cursor": cursor,
        "collapsed message": collapsed,
        "expanded message (preview)": expanded,
    }


def play_inbox_reveal(scene: Scene, *, run_time: float = 0.85) -> VGroup:
    """Animate inbox → cursor click → collapsed → expanded."""
    bits = inbox_scene_group()
    inbox = bits["inbox"]
    cursor = bits["cursor"]
    collapsed = bits["collapsed message"]
    expanded = bits["expanded message (preview)"]

    click_target = inbox.get_center() + RIGHT * 0.28 + DOWN * 0.08

    scene.play(FadeIn(inbox, shift=UP * 0.08), run_time=0.55)
    scene.play(cursor.animate.shift(click_target - _cursor_hotspot(cursor)), run_time=0.45)
    scene.play(Indicate(inbox, color=ACCENT, scale_factor=1.05), run_time=0.35)
    scene.play(FadeIn(collapsed, shift=RIGHT * 0.12), run_time=0.4)
    expanded = mail_expanded().move_to(collapsed.get_center())
    scene.play(Transform(collapsed, expanded), run_time=run_time)
    return VGroup(inbox, cursor, collapsed)
