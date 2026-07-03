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
VISION_PRO = "vision-pro"
CLOUD = "cloud"
MAIL = "mail"
SOUND_ANALYSIS = "sound-analysis"
CURSOR = "cursor"


def load_icon(name: str, *, color: str, height: float = 0.55) -> SVGMobject:
    """Load and tint one stroke SVG icon from assets/icons/."""
    path = ICONS_DIR / f"{name}.svg"
    if not path.exists():
        raise FileNotFoundError(f"Missing icon SVG: {path}")

    # LEARN: SVGMobject — vector asset from file; scales cleanly vs hand-drawn lines
    icon = SVGMobject(str(path))
    icon.set(height=height)
    icon.set_stroke(color, width=2.5, opacity=1)
    icon.set_fill(color, opacity=0)
    return icon


def load_filled_icon(
    name: str,
    *,
    color: str,
    height: float = 0.55,
    stroke_color: str = "#1e1e28",
) -> SVGMobject:
    """Filled SVG glyphs — use when the asset is fill-based (not stroke icons like cursor)."""
    path = ICONS_DIR / f"{name}.svg"
    if not path.exists():
        raise FileNotFoundError(f"Missing icon SVG: {path}")

    icon = SVGMobject(str(path))
    icon.set(height=height)
    icon.set_fill(color, opacity=1)
    icon.set_stroke(stroke_color, width=1.5, opacity=1)
    return icon
