"""Bottom-third on-screen labels (every act)."""

from __future__ import annotations

from manim import DOWN, Text

from theme import FONT, WHITE_TEXT


def on_screen_label(text: str, font_size: int = 28) -> Text:
    label = Text(text, font=FONT, font_size=font_size, color=WHITE_TEXT)
    label.to_edge(DOWN, buff=0.55)
    return label
