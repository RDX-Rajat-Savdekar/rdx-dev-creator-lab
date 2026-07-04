"""
REFERENCE ONLY — old monolith with all 6 acts in one file.
Do not render. Use scene0_act1.py … scene0_act6.py instead, then scene0_full.py.

Chapter 0 — Problem + hackathon frame + sphere POC

Workflow (review one ACT at a time):
  1. Edit helpers below (grouped by ACT).
  2. Preview layout:  manim -ql … Scene0PreviewActN   ← plops pieces slowly
  3. Preview motion: manim -ql … Scene0PreviewActNMotion  ← after layout OK
  4. Add N to ENABLED_ACTS → render Scene0Problem when all acts approved.

Companion: SCRIPT.md ch 0 · SCENE-PLAN.md 0:00–1:05
"""

from __future__ import annotations

import sys
from pathlib import Path

from manim import *

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from theme import ACCENT, AURA_BG, FONT, MUTED, WARN, WHITE_TEXT

# Add acts here only after Scene0PreviewActN layout + motion look right.
ENABLED_ACTS: tuple[int, ...] = (1,)


# =============================================================================
# REVIEW HELPER — plop assets on screen one at a time (hold frame between adds)
# =============================================================================


def plop(scene: Scene, mob: Mobject, name: str, wait: float = 2.5) -> None:
    """Fade in one asset, show its helper name top-left, hold for inspection."""
    tag = Text(name, font=FONT, font_size=16, color=MUTED).to_corner(UL, buff=0.35)
    scene.play(FadeIn(mob), FadeIn(tag), run_time=0.5)
    scene.wait(wait)
    scene.play(FadeOut(tag), run_time=0.25)
    # mob stays on screen — next plop builds cumulative layout


def setup_scene(scene: Scene) -> None:
    scene.camera.background_color = AURA_BG


# =============================================================================
# SHARED — on-screen labels (every ACT)
# =============================================================================


def on_screen_label(text: str, font_size: int = 28) -> Text:
    """Bottom-third caption — matches 60s lower-third typography."""
    label = Text(text, font=FONT, font_size=font_size, color=WHITE_TEXT)
    label.to_edge(DOWN, buff=0.55)
    return label


# =============================================================================
# ACT 1 HELPERS — noisy room · speech + environmental sounds → ?
# SCENE-PLAN: 0:00–0:15 · label: Situational audio gap
# =============================================================================


def room_frame() -> VGroup:
    """Minimal room outline — floor + walls + faint ceiling + corner noise arcs."""
    floor = Line(LEFT * 5.8 + DOWN * 1.6, RIGHT * 5.8 + DOWN * 1.6, color=MUTED, stroke_width=2)
    left_wall = Line(floor.get_start(), floor.get_start() + UP * 2.4, color=MUTED, stroke_width=2)
    right_wall = Line(floor.get_end(), floor.get_end() + UP * 2.4, color=MUTED, stroke_width=2)
    ceiling = Line(left_wall.get_end(), right_wall.get_end(), color=MUTED, stroke_width=1.5, stroke_opacity=0.5)
    noise = VGroup(
        *[
            Arc(radius=0.12 + i * 0.05, angle=PI / 2, color=RED, stroke_width=1.2, stroke_opacity=0.35)
            for i in range(4)
        ]
    ).arrange(RIGHT, buff=0.04).move_to(UP * 2.0 + RIGHT * 4.2)
    return VGroup(floor, left_wall, right_wall, ceiling, noise)


def speech_bubble(text: str = "…") -> VGroup:
    """Chat bubble — ambient speech the viewer might miss."""
    body = RoundedRectangle(
        corner_radius=0.18,
        width=1.35,
        height=0.72,
        fill_color="#1c1c24",
        fill_opacity=0.95,
        stroke_color=ACCENT,
        stroke_width=1.2,
    )
    tail = Triangle(fill_color=GREEN, fill_opacity=0.95, stroke_width=0)
    tail.scale(0.16).next_to(body, DOWN + LEFT, buff=-0.02)
    words = Text(text, font=FONT, font_size=18, color=WHITE_TEXT)
    words.move_to(body.get_center())
    return VGroup(body, tail, words)


def sound_icon(kind: str = "bell") -> VGroup:
    """Environmental sound glyph — bell | siren | wave (default wave = RMS bars)."""
    if kind == "bell":
        dome = Arc(radius=0.22, start_angle=PI, angle=PI, stroke_color=ACCENT, stroke_width=3)
        base = Line(LEFT * 0.28, RIGHT * 0.28, color=ACCENT, stroke_width=3)
        base.next_to(dome, DOWN, buff=0.02)
        clapper = Dot(radius=0.05, color=ACCENT).next_to(base, DOWN, buff=0.08)
        icon = VGroup(dome, base, clapper)
    elif kind == "siren":
        icon = RegularPolygon(n=3, color=WARN, fill_opacity=0.25, stroke_width=2).scale(0.35)
        bang = Text("!", font=FONT, font_size=22, color=WARN)
        bang.move_to(icon.get_center())
        icon = VGroup(icon, bang)
    else:
        bars = VGroup(
            *[
                Line(ORIGIN, UP * h, color=ACCENT, stroke_width=4)
                for h in (0.18, 0.32, 0.24, 0.38)
            ]
        ).arrange(RIGHT, buff=0.08)
        icon = bars
    return icon


def question_mark() -> Text:
    """Replacement glyph when speech/sound context is lost."""
    return Text("?", font=FONT, font_size=44, color=MUTED, weight=BOLD)


def act1_layout() -> VGroup:
    """Full ACT 1 composition — positions for preview + motion."""
    room = room_frame()
    bubble_a = speech_bubble("Hey—")
    bubble_b = speech_bubble("…wait")
    bubble_c = speech_bubble("Behind you")
    bubbles = VGroup(bubble_a, bubble_b, bubble_c)
    bubbles.arrange(RIGHT, buff=0.55).move_to(UP * 0.35)

    bell = sound_icon("bell").scale(0.9).move_to(LEFT * 3.2 + DOWN * 0.35)
    siren = sound_icon("siren").scale(0.9).move_to(DOWN * 0.15)
    waves = sound_icon("wave").scale(0.9).move_to(RIGHT * 3.1 + DOWN * 0.25)
    sounds = VGroup(bell, siren, waves)
    label = on_screen_label("Situational audio gap")

    return VGroup(room, bubbles, sounds, label)


# =============================================================================
# ACT 2 HELPERS — hackathon frame · 24h · Oct 2025 · team roles
# SCENE-PLAN: 0:15–0:25 · label: 24h hackathon · Oct 2025
# =============================================================================


def hackathon_clock() -> VGroup:
    """
    24h hackathon clock glyph — TODO: layout under review (Scene0PreviewAct2).

    Parts: face circle, hour hand, minute tick, '24h' caption below face.
    """
    face = Circle(radius=0.85, color=ACCENT, stroke_width=3)
    hand = Line(ORIGIN, UP * 0.55, color=WHITE_TEXT, stroke_width=4)
    hand.rotate(-PI / 3)
    tick = Line(ORIGIN, UP * 0.7, color=ACCENT, stroke_width=2).rotate(PI / 2)
    label = Text("24h", font=FONT, font_size=26, color=WHITE_TEXT, weight=BOLD)
    label.next_to(face, DOWN, buff=0.25)
    return VGroup(face, hand, tick, label)


def role_icon(role: str) -> VGroup:
    """Team role stick figure — coder (laptop) vs presenter (mic)."""
    head = Circle(radius=0.22, color=WHITE_TEXT, fill_opacity=0.15, stroke_color=ACCENT, stroke_width=2)
    body = Line(DOWN * 0.22, DOWN * 0.65, color=ACCENT, stroke_width=3)
    person = VGroup(head, body)
    if role == "coder":
        laptop = RoundedRectangle(
            corner_radius=0.06,
            width=0.55,
            height=0.34,
            fill_color="#1c1c24",
            fill_opacity=1,
            stroke_color=ACCENT,
            stroke_width=1.5,
        ).next_to(body, DOWN, buff=0.05)
        glyph = Text("<>", font=FONT, font_size=16, color=ACCENT).move_to(laptop.get_center())
        badge = Text("code", font=FONT, font_size=14, color=MUTED)
        badge.next_to(laptop, DOWN, buff=0.12)
        return VGroup(person, laptop, glyph, badge)
    mic = Line(ORIGIN, UP * 0.28, color=ACCENT, stroke_width=3).next_to(head, RIGHT, buff=0.18)
    mic_head = Circle(radius=0.08, color=ACCENT, fill_opacity=0.4, stroke_width=1.5).move_to(mic.get_end())
    badge = Text("present", font=FONT, font_size=14, color=MUTED)
    badge.next_to(body, DOWN, buff=0.35)
    return VGroup(person, mic, mic_head, badge)


def act2_layout() -> dict[str, Mobject]:
    """ACT 2 pieces — returned as dict so preview can plop each key separately."""
    clock = hackathon_clock().move_to(LEFT * 2.6)
    date = Text("Oct 2025", font=FONT, font_size=30, color=WHITE_TEXT, weight=BOLD)
    venue = Text("LA Tech Week · USC ISI", font=FONT, font_size=20, color=MUTED)
    date.next_to(clock, RIGHT, buff=0.9).align_to(clock, UP)
    venue.next_to(date, DOWN, buff=0.25, aligned_edge=LEFT)

    coder = role_icon("coder").scale(0.95).move_to(RIGHT * 2.6 + UP * 0.55)
    presenters = VGroup(role_icon("present"), role_icon("present"))
    presenters.scale(0.9).arrange(RIGHT, buff=0.65).move_to(RIGHT * 2.5 + DOWN * 0.85)
    label = on_screen_label("24h hackathon · Oct 2025")

    return {
        "hackathon_clock()": clock,
        "date + venue": VGroup(date, venue),
        "role_icon(coder)": coder,
        "role_icon(present) x2": presenters,
        "on_screen_label": label,
    }


# =============================================================================
# ACT 3 HELPERS — solo code lane
# SCENE-PLAN: 0:25–0:35 · label: All code: Rajat
# =============================================================================


def author_lane() -> VGroup:
    """Git-style commit lane — four dots → single author name."""
    lane = Line(LEFT * 4.5, RIGHT * 4.5, color=MUTED, stroke_width=2)
    commits = VGroup(
        *[
            VGroup(
                Dot(radius=0.07, color=ACCENT),
                Text("commit", font=FONT, font_size=12, color=MUTED),
            ).arrange(DOWN, buff=0.08)
            for _ in range(4)
        ]
    ).arrange(RIGHT, buff=1.1)
    commits.move_to(lane.get_center() + UP * 0.35)
    for commit, x in zip(commits, [-1.65, -0.55, 0.55, 1.65]):
        commit[0].move_to(lane.get_center() + UP * 0.35 + RIGHT * x)
        commit[1].next_to(commit[0], DOWN, buff=0.08)
    author = Text("Rajat", font=FONT, font_size=32, color=WHITE_TEXT, weight=BOLD)
    author.next_to(lane, DOWN, buff=0.55)
    arrow = Arrow(
        commits[-1][0].get_center() + UP * 0.55,
        author.get_top(),
        buff=0.08,
        color=ACCENT,
        stroke_width=3,
        max_tip_length_to_length_ratio=0.18,
    )
    return VGroup(lane, commits, arrow, author)


def act3_layout() -> dict[str, Mobject]:
    teammates = Text("Teammates · README + on-camera demo", font=FONT, font_size=20, color=MUTED)
    teammates.to_edge(UP, buff=0.65)
    return {
        "author_lane()": author_lane(),
        "teammates note": teammates,
        "on_screen_label": on_screen_label("All code: Rajat"),
    }


# =============================================================================
# ACT 4 HELPERS — sphere POC (first Vision Pro build)
# SCENE-PLAN: 0:35–0:48 · label: Day 0: sphere POC
# =============================================================================


def act4_layout() -> dict[str, Mobject]:
    headset_note = Text("First Vision Pro build", font=FONT, font_size=22, color=MUTED)
    headset_note.to_edge(UP, buff=0.7)
    sphere = Circle(radius=0.75, color=MUTED, fill_opacity=0.35, stroke_width=2)
    sphere.move_to(ORIGIN)
    cue_red = Text('"red"', font=FONT, font_size=36, color=WHITE_TEXT, slant=ITALIC)
    cue_red.next_to(sphere, UP, buff=0.55)
    cue_loud = Text("louder", font=FONT, font_size=28, color=MUTED)
    cue_loud.next_to(sphere, DOWN, buff=0.55)
    vol_bars = sound_icon("wave").scale(0.7).next_to(cue_loud, DOWN, buff=0.25)
    return {
        "headset note": headset_note,
        "sphere (neutral)": sphere,
        "cue: red": cue_red,
        "cue: louder + vol bars": VGroup(cue_loud, vol_bars),
        "on_screen_label": on_screen_label("Day 0: sphere POC"),
    }


# =============================================================================
# ACT 5 HELPERS — prototype disclaimer + Resolve B-roll slot
# SCENE-PLAN: 0:48–0:55 · label: System design · prototype
# =============================================================================


def act5_layout() -> dict[str, Mobject]:
    title = Text("System design · prototype", font=FONT, font_size=38, color=WHITE_TEXT, weight=BOLD)
    subtitle = Text("Hackathon prototype — not a production app", font=FONT, font_size=22, color=MUTED)
    subtitle.next_to(title, DOWN, buff=0.35)
    card = VGroup(title, subtitle)
    broll_slot = Text("[ D1 live captions — Resolve ]", font=FONT, font_size=18, color=MUTED)
    broll_slot.next_to(card, DOWN, buff=0.65)
    return {
        "title card": card,
        "broll slot marker": broll_slot,
    }


# =============================================================================
# ACT 6 HELPERS — Aura teaser · Vision Pro + dual pipeline stub
# SCENE-PLAN: 0:55–1:05 · label: Aura · visionOS · on-device
# =============================================================================


def vision_pro_silhouette() -> VGroup:
    """Rounded goggle silhouette — explainer only, not a product render."""
    band = RoundedRectangle(
        corner_radius=0.35,
        width=4.6,
        height=1.35,
        fill_color="#14141c",
        fill_opacity=1,
        stroke_color=ACCENT,
        stroke_width=2.5,
    )
    lens_l = RoundedRectangle(
        corner_radius=0.28,
        width=1.55,
        height=0.95,
        fill_color=AURA_BG,
        fill_opacity=1,
        stroke_color=MUTED,
        stroke_width=1.5,
    ).move_to(band.get_center() + LEFT * 1.05)
    lens_r = lens_l.copy().move_to(band.get_center() + RIGHT * 1.05)
    strap = Line(band.get_left() + LEFT * 0.5, band.get_right() + RIGHT * 0.5, color=MUTED, stroke_width=2)
    strap.move_to(band.get_center() + DOWN * 0.72)
    return VGroup(strap, band, lens_l, lens_r)


def pipeline_stub() -> VGroup:
    """Mic tap → Speech + SoundAnalysis — teaser for ch 1–3."""
    mic = VGroup(
        Circle(radius=0.28, color=ACCENT, fill_opacity=0.2, stroke_width=2),
        Dot(radius=0.06, color=WHITE_TEXT),
    )
    mic_label = Text("mic tap", font=FONT, font_size=16, color=MUTED)
    mic_label.next_to(mic, DOWN, buff=0.12)

    speech_box = RoundedRectangle(
        corner_radius=0.12,
        width=2.2,
        height=0.85,
        fill_color="#14141c",
        fill_opacity=1,
        stroke_color=ACCENT,
        stroke_width=2,
    )
    speech_text = Text("Speech", font=FONT, font_size=22, color=WHITE_TEXT)
    speech_text.move_to(speech_box.get_center())

    sound_box = speech_box.copy()
    sound_text = Text("SoundAnalysis", font=FONT, font_size=20, color=WHITE_TEXT)
    sound_text.move_to(sound_box.get_center())

    speech_group = VGroup(speech_box, speech_text)
    sound_group = VGroup(sound_box, sound_text)
    speech_group.move_to(RIGHT * 2.2 + UP * 0.55)
    sound_group.move_to(RIGHT * 2.2 + DOWN * 0.75)

    mic_group = VGroup(mic, mic_label).move_to(LEFT * 2.4)
    arrow_speech = Arrow(
        mic_group.get_right(),
        speech_group.get_left(),
        buff=0.15,
        color=ACCENT,
        stroke_width=2.5,
        max_tip_length_to_length_ratio=0.15,
    )
    arrow_sound = Arrow(
        mic_group.get_right(),
        sound_group.get_left(),
        buff=0.15,
        color=ACCENT,
        stroke_width=2.5,
        max_tip_length_to_length_ratio=0.15,
    )
    on_device = Text("on-device", font=FONT, font_size=18, color=ACCENT)
    on_device.next_to(VGroup(speech_group, sound_group), DOWN, buff=0.35)

    return VGroup(mic_group, arrow_speech, arrow_sound, speech_group, sound_group, on_device)


def act6_layout() -> dict[str, Mobject]:
    aura_title = Text("Aura", font=FONT, font_size=52, color=WHITE_TEXT, weight=BOLD)
    aura_sub = Text("visionOS · on-device", font=FONT, font_size=28, color=ACCENT)
    aura_title.to_edge(UP, buff=0.55)
    aura_sub.next_to(aura_title, DOWN, buff=0.2)
    return {
        "Aura title": VGroup(aura_title, aura_sub),
        "vision_pro_silhouette()": vision_pro_silhouette().scale(0.85).move_to(LEFT * 2.0),
        "pipeline_stub()": pipeline_stub().scale(0.82).move_to(RIGHT * 1.55),
    }


# =============================================================================
# ACT MOTION — timing + story (wire after layout preview passes)
# =============================================================================


def play_act1(scene: Scene) -> None:
    """ACT 1 motion — noisy room → ? → label (0:00–0:15)."""
    layout = act1_layout()
    room, bubbles, sounds, label = layout[0], layout[1], layout[2], layout[3]

    scene.play(FadeIn(room), run_time=0.8)
    scene.play(
        LaggedStart(
            FadeIn(bubbles, shift=UP * 0.12),
            FadeIn(sounds, shift=UP * 0.08),
            lag_ratio=0.25,
        ),
        run_time=2.2,
    )
    scene.wait(1.5)

    q_marks = VGroup(
        *[
            question_mark().move_to(src.get_center())
            for src in (
                bubbles[0],
                bubbles[1],
                bubbles[2],
                sounds[0],
                sounds[1],
                sounds[2],
            )
        ]
    )
    scene.play(FadeOut(bubbles, sounds), FadeIn(q_marks, scale=0.6), run_time=1.8)
    scene.play(FadeIn(label, shift=UP * 0.1), run_time=0.6)
    scene.wait(7.2)
    scene.play(FadeOut(room, q_marks, label), run_time=0.9)


def play_act2(scene: Scene) -> None:
    """ACT 2 motion — hackathon frame (0:15–0:25). Layout TBD after preview."""
    pieces = act2_layout()
    clock = pieces["hackathon_clock()"]
    date_venue = pieces["date + venue"]
    coder = pieces["role_icon(coder)"]
    presenters = pieces["role_icon(present) x2"]
    label = pieces["on_screen_label"]

    scene.play(FadeIn(clock), Create(clock[1]), run_time=1.2)
    scene.play(FadeIn(date_venue), run_time=0.9)
    scene.play(FadeIn(coder), FadeIn(presenters), run_time=1.4)
    scene.play(FadeIn(label, shift=UP * 0.1), run_time=0.5)
    scene.wait(5.3)
    scene.play(FadeOut(clock, date_venue, coder, presenters, label), run_time=0.7)


def play_act3(scene: Scene) -> None:
    pieces = act3_layout()
    lane = pieces["author_lane()"]
    teammates = pieces["teammates note"]
    label = pieces["on_screen_label"]

    scene.play(FadeIn(lane), run_time=1.2)
    scene.play(Indicate(lane[-1], color=ACCENT, scale_factor=1.08), FadeIn(teammates), run_time=1.4)
    scene.play(FadeIn(label, shift=UP * 0.1), run_time=0.5)
    scene.wait(6.2)
    scene.play(FadeOut(lane, teammates, label), run_time=0.7)


def play_act4(scene: Scene) -> None:
    pieces = act4_layout()
    headset_note = pieces["headset note"]
    sphere = pieces["sphere (neutral)"]
    cue_red = pieces["cue: red"]
    cue_loud, vol_bars = pieces["cue: louder + vol bars"]
    label = pieces["on_screen_label"]

    scene.play(FadeIn(headset_note), FadeIn(sphere), run_time=0.9)
    scene.play(FadeIn(cue_red, shift=DOWN * 0.08), run_time=0.5)
    red_sphere = sphere.copy().set_color(WARN).set_fill(WARN, opacity=0.55)
    scene.play(ReplacementTransform(sphere, red_sphere), run_time=1.0)
    sphere = red_sphere
    scene.wait(0.8)
    scene.play(FadeIn(cue_loud), FadeIn(vol_bars), run_time=0.5)
    scene.play(sphere.animate.scale(1.45), vol_bars.animate.scale(1.25), run_time=1.2)
    scene.play(FadeIn(label, shift=UP * 0.1), run_time=0.5)
    scene.wait(7.0)
    scene.play(FadeOut(headset_note, sphere, cue_red, cue_loud, vol_bars, label), run_time=0.7)


def play_act5(scene: Scene) -> None:
    pieces = act5_layout()
    card = pieces["title card"]
    broll_slot = pieces["broll slot marker"]

    scene.play(FadeIn(card, shift=UP * 0.12), run_time=0.9)
    scene.play(FadeIn(broll_slot), run_time=0.4)
    scene.wait(3.3)
    scene.play(FadeOut(card, broll_slot), run_time=0.4)
    scene.wait(2.0)  # black hold for Resolve D1


def play_act6(scene: Scene) -> None:
    pieces = act6_layout()
    titles = pieces["Aura title"]
    headset = pieces["vision_pro_silhouette()"]
    pipes = pieces["pipeline_stub()"]

    scene.play(FadeIn(titles), run_time=0.8)
    scene.play(FadeIn(headset, shift=RIGHT * 0.15), run_time=0.9)
    scene.play(
        LaggedStart(
            Create(pipes[1]),
            Create(pipes[2]),
            FadeIn(pipes[0]),
            FadeIn(pipes[3]),
            FadeIn(pipes[4]),
            FadeIn(pipes[5]),
            lag_ratio=0.18,
        ),
        run_time=2.4,
    )
    scene.wait(5.0)
    scene.play(FadeOut(titles, headset, pipes), run_time=0.9)


ACT_PLAYERS = {
    1: play_act1,
    2: play_act2,
    3: play_act3,
    4: play_act4,
    5: play_act5,
    6: play_act6,
}


# =============================================================================
# LAYOUT PREVIEWS — render these to review helpers before motion
# =============================================================================


class Scene0PreviewAct1(Scene):
    """Plop ACT 1 pieces one by one. Render: Scene0PreviewAct1"""

    def construct(self) -> None:
        setup_scene(self)
        layout = act1_layout()
        plop(self, layout[0], "room_frame()")
        plop(self, layout[1], "speech_bubbles x3")
        plop(self, layout[2], "sound_icon bell/siren/wave")
        plop(self, layout[3], "on_screen_label", wait=3.0)


class Scene0PreviewAct2(Scene):
    """Plop ACT 2 pieces one by one — clock isolated first for review. Render: Scene0PreviewAct2"""

    def construct(self) -> None:
        setup_scene(self)
        pieces = act2_layout()
        # Clock alone, centered first — easiest to critique
        clock_solo = hackathon_clock().move_to(ORIGIN)
        plop(self, clock_solo, "hackathon_clock() SOLO", wait=4.0)
        self.play(FadeOut(clock_solo), run_time=0.4)
        self.wait(0.3)

        for name, mob in pieces.items():
            plop(self, mob, name, wait=3.0)


class Scene0PreviewAct3(Scene):
    def construct(self) -> None:
        setup_scene(self)
        for name, mob in act3_layout().items():
            plop(self, mob, name, wait=3.0)


class Scene0PreviewAct4(Scene):
    def construct(self) -> None:
        setup_scene(self)
        for name, mob in act4_layout().items():
            plop(self, mob, name, wait=3.0)


class Scene0PreviewAct5(Scene):
    def construct(self) -> None:
        setup_scene(self)
        for name, mob in act5_layout().items():
            plop(self, mob, name, wait=3.0)


class Scene0PreviewAct6(Scene):
    def construct(self) -> None:
        setup_scene(self)
        for name, mob in act6_layout().items():
            plop(self, mob, name, wait=3.0)


# =============================================================================
# MOTION PREVIEWS — one ACT animation in isolation (after layout OK)
# =============================================================================


class Scene0PreviewAct1Motion(Scene):
    def construct(self) -> None:
        setup_scene(self)
        play_act1(self)


class Scene0PreviewAct2Motion(Scene):
    def construct(self) -> None:
        setup_scene(self)
        play_act2(self)


# =============================================================================
# FULL SCENE — grows as you add acts to ENABLED_ACTS
# =============================================================================


class Scene0Problem(Scene):
    """Full ch 0 clip — only acts listed in ENABLED_ACTS."""

    def construct(self) -> None:
        setup_scene(self)
        for act in (1, 2, 3, 4, 5, 6):
            if act in ENABLED_ACTS:
                ACT_PLAYERS[act](self)
