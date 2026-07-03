"""Hackathon demo B-roll — embed trimmed clips from Aura/clips/ in Manim scenes.

D1 = ``D1_live-en-captions.mp4`` — live English captions on Vision Pro (14 s source).
Other clips (D2–D6) are documented in ``Aura/clips/README.md``.

Previously act 5 showed a Resolve placeholder; we bake the ~4 s D1 flash here so
``Scene0Full`` previews match the final cut without a separate NLE pass.
"""

from __future__ import annotations

from pathlib import Path

import av
import numpy as np
from manim import DOWN, FadeIn, FadeOut, Group, ImageMobject, RoundedRectangle, Scene

CLIPS_DIR = Path(__file__).resolve().parents[2] / "clips"
D1_LIVE_CAPTIONS = CLIPS_DIR / "D1_live-en-captions.mp4"
D4_SIREN = CLIPS_DIR / "D4_siren-emergency-vehicle.mp4"
D5_CLAPPING = CLIPS_DIR / "D5_clapping.mp4"
D3_WHISPER = CLIPS_DIR / "D3_whisper-detected.mp4"
D6_JAPANESE = CLIPS_DIR / "D6_japanese-locale.mp4"

# SCENE-PLAN ch 0 act 5: ~4 s flash of live captions after prototype card.
D1_FLASH_START = 0.0
D1_FLASH_DURATION = 4.0

BROLL_WIDTH = 12.0


def _require_clip(path: Path) -> Path:
    if not path.exists():
        raise FileNotFoundError(
            f"Missing B-roll clip: {path}\n"
            "Cut demo segments per Aura/clips/README.md (ffmpeg from hackathon source)."
        )
    return path


def load_video_frames(
    path: Path,
    *,
    start: float = 0.0,
    duration: float = 4.0,
    fps: float = 30.0,
) -> list[np.ndarray]:
    """Decode a clip segment as rgb24 frames, resampled to the scene frame rate."""
    _require_clip(path)
    container = av.open(str(path))
    stream = container.streams.video[0]

    collected: list[np.ndarray] = []
    for frame in container.decode(stream):
        if frame.time is None:
            continue
        if frame.time < start:
            continue
        if frame.time >= start + duration:
            break
        collected.append(frame.to_ndarray(format="rgb24"))

    target_count = max(1, int(duration * fps))
    if not collected:
        raise ValueError(f"No frames decoded from {path} (start={start}, duration={duration})")
    if len(collected) <= target_count:
        return collected

    indices = np.linspace(0, len(collected) - 1, target_count, dtype=int)
    return [collected[i] for i in indices]


def broll_still(
    path: Path = D1_LIVE_CAPTIONS,
    *,
    start: float = D1_FLASH_START,
    width: float = BROLL_WIDTH,
) -> ImageMobject:
    """First frame of a clip — for layout plop review."""
    frame = load_video_frames(path, start=start, duration=0.15, fps=1.0)[0]
    return ImageMobject(frame).set(width=width)


def broll_panel(frames: list[np.ndarray], *, width: float = BROLL_WIDTH) -> Group:
    """Demo footage inside a subtle rounded frame."""
    image = ImageMobject(frames[0]).set(width=width)
    border = RoundedRectangle(
        corner_radius=0.12,
        width=image.width + 0.2,
        height=image.height + 0.2,
        stroke_color="#3a3a44",
        stroke_width=2,
        fill_opacity=0,
    )
    border.move_to(image.get_center())
    return Group(border, image)


def play_broll(
    scene: Scene,
    path: Path = D1_LIVE_CAPTIONS,
    *,
    start: float = D1_FLASH_START,
    duration: float = D1_FLASH_DURATION,
    fade_in: float = 0.25,
    fade_out: float = 0.25,
) -> None:
    """Play a trimmed demo clip full-screen (fade in → hold → fade out)."""
    fps = float(scene.camera.frame_rate)
    frames = load_video_frames(path, start=start, duration=duration, fps=fps)
    panel = broll_panel(frames)
    image = panel[1]

    scene.play(FadeIn(panel, shift=DOWN * 0.06), run_time=fade_in)

    index = 0

    def advance(mob: ImageMobject, dt: float) -> None:
        nonlocal index
        index += 1
        if index < len(frames):
            mob.become(ImageMobject(frames[index]).set(width=BROLL_WIDTH))

    image.add_updater(advance)
    scene.wait(max(0.0, duration - fade_in - fade_out))
    image.clear_updaters()
    scene.play(FadeOut(panel), run_time=fade_out)


def play_montage(
    scene: Scene,
    segments: list[tuple[Path, float, float]],
    *,
    width: float = BROLL_WIDTH,
    fade_in: float = 0.2,
    fade_out: float = 0.2,
) -> None:
    """Play multiple clip segments back-to-back (e.g. D4 → D5)."""
    for i, (path, start, duration) in enumerate(segments):
        fps = float(scene.camera.frame_rate)
        frames = load_video_frames(path, start=start, duration=duration, fps=fps)
        panel = broll_panel(frames, width=width)
        image = panel[1]
        fin = fade_in if i == 0 else 0.12
        fout = fade_out if i == len(segments) - 1 else 0.12
        scene.play(FadeIn(panel, shift=DOWN * 0.05), run_time=fin)
        index = 0

        def advance(mob: ImageMobject, dt: float) -> None:
            nonlocal index
            index += 1
            if index < len(frames):
                mob.become(ImageMobject(frames[index]).set(width=width))

        image.add_updater(advance)
        scene.wait(max(0.0, duration - fin - fout))
        image.clear_updaters()
        if i < len(segments) - 1:
            scene.play(FadeOut(panel), run_time=fout)
        else:
            scene.play(FadeOut(panel), run_time=fout)
