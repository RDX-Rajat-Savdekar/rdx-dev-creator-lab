"""Rejected architecture paths — ghost arrows, reject cross, reason chips."""

from __future__ import annotations

from manim import *

from icons import CLOUD, load_icon
from theme import ACCENT, FONT, MUTED, WARN, WHITE_TEXT

# Shared Y — arrow stays horizontal between device and cloud.
DIAGRAM_Y = 0.12
DEVICE_ANCHOR = LEFT * 2.65 + UP * DIAGRAM_Y
CLOUD_ANCHOR = RIGHT * 2.85 + UP * DIAGRAM_Y

GHOST_OPACITY = 0.55


def cloud_glyph(*, color: str = MUTED, height: float = 1.15) -> Mobject:
    """Stroke cloud SVG (Lucide-style)."""
    return load_icon(CLOUD, color=color, height=height).move_to(CLOUD_ANCHOR)


def ghost_arrow(device: Mobject, cloud: Mobject) -> DashedLine:
    """Horizontal dashed line device → cloud."""
    y = device.get_center()[1]
    start = np.array([device.get_right()[0] + 0.2, y, 0])
    end = np.array([cloud.get_left()[0] - 0.15, y, 0])
    return DashedLine(
        start,
        end,
        dash_length=0.12,
        color=WHITE_TEXT,
        stroke_width=2.2,
        stroke_opacity=GHOST_OPACITY,
    )


def network_fallback_label(arrow: Mobject) -> Text:
    label = Text("network fallback", font=FONT, font_size=17, color=WHITE_TEXT)
    label.set_opacity(0.72)
    label.next_to(arrow, UP, buff=0.22)
    return label


def reject_cross(arrow: Mobject, cloud: Mobject) -> Cross:
    """Red X centered on the ghost connector."""
    _ = cloud
    cross = Cross(stroke_color=WARN, stroke_width=4)
    cross.scale(0.42)
    cross.move_to(arrow.get_center())
    cross.set_z_index(2)
    return cross


# Back-compat alias — act files import this name.
reject_path_strike = reject_cross


def reject_chips(labels: tuple[str, ...] = ("privacy", "latency")) -> VGroup:
    chips = VGroup(
        *[
            VGroup(
                RoundedRectangle(
                    corner_radius=0.1,
                    width=1.45,
                    height=0.48,
                    stroke_color=WARN,
                    stroke_width=1.5,
                    fill_color="#1c1010",
                    fill_opacity=0.9,
                ),
                Text(text, font=FONT, font_size=19, color=WHITE_TEXT),
            )
            for text in labels
        ]
    )
    for chip in chips:
        chip[1].move_to(chip[0].get_center())
    chips.arrange(RIGHT, buff=0.32).move_to(UP * 1.55)
    return chips


def cloud_temptation_group(device: Mobject) -> dict[str, Mobject]:
    """Act 2+ pieces — pass device so arrow endpoints are correct."""
    cloud = cloud_glyph()
    arrow = ghost_arrow(device, cloud)
    fallback = network_fallback_label(arrow)
    return {
        "cloud": cloud,
        "ghost arrow": arrow,
        "network fallback": fallback,
    }
