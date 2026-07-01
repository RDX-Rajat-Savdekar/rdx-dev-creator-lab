"""SVG icon loader — reuse across scene0_actN files.

Icons live in assets/icons/ (stroke SVGs, Lucide-style paths).
Tint at load time instead of hand-drawing bells with Arc + Line.
"""

from __future__ import annotations

from pathlib import Path

from manim import SVGMobject

ICONS_DIR = Path(__file__).resolve().parent / "assets" / "icons"

# Names match SVG filenames without extension.
BELL = "bell"
ALERT = "alert"
AUDIO_WAVE = "audio-wave"
MESSAGE = "message"
CLOCK = "clock"
LAPTOP = "laptop"
MIC = "mic"
PALETTE = "palette"


def load_icon(name: str, *, color: str, height: float = 0.55) -> SVGMobject:
    """Load and tint one SVG icon from assets/icons/."""
    path = ICONS_DIR / f"{name}.svg"
    if not path.exists():
        raise FileNotFoundError(f"Missing icon SVG: {path}")

    # LEARN: SVGMobject — vector asset from file; scales cleanly vs hand-drawn lines
    icon = SVGMobject(str(path))
    icon.set(height=height)
    icon.set_stroke(color, width=2.5, opacity=1)
    icon.set_fill(color, opacity=0)
    return icon
