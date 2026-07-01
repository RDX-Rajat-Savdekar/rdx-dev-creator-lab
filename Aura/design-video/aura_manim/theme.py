"""Shared Aura design-video palette — matches Aura/manim/aura_cards.py (60s clip)."""

from __future__ import annotations

AURA_BG = "#0a0a0f"
ACCENT = "#5ac8fa"  # visionOS-adjacent cyan
MUTED = "#98989d"
WHITE_TEXT = "#ffffff"
WARN = "#ff6b6b"
MERGE_OK = "#30d158"  # green pulse when a dev merges into trunk
FONT = "Helvetica"

# Shared merge-lane geometry (act 3)
MERGE_LANE_Y = 0.0
MERGE_LANE_LEFT = -4.5
MERGE_LANE_RIGHT = 4.5
MERGE_SECTION_W = (MERGE_LANE_RIGHT - MERGE_LANE_LEFT) / 4
