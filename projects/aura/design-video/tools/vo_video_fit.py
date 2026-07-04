"""Fit Manim act video to VO — hold last visible frame, strip fade-to-black tails."""

from __future__ import annotations

import re
import subprocess
from pathlib import Path

FADEOUT_RE = re.compile(r"FadeOut\([^)]+\),\s*run_time=([0-9.]+)")
WAIT_RE = re.compile(r"scene\.wait\(([0-9.]+(?:\.[0-9]+)?)\)")
PLAY_BODY_RE = re.compile(
    r"def play_act\d*\([^)]*\)[^:]*:(.*?)(?=\nclass |\nif __name__|\Z)",
    re.DOTALL,
)
BROLL_THEN_WAIT_RE = re.compile(
    r"play_(?:broll|montage)\([^)]*\)\s*\n\s*scene\.wait\(",
    re.MULTILINE,
)


def probe_duration(path: Path) -> float:
    out = subprocess.check_output(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "csv=p=0",
            str(path),
        ],
        text=True,
    ).strip()
    return float(out)


def parse_content_end(scene_py: Path | None, video_dur: float) -> float:
    """Timestamp of last frame with on-screen content (before fade / blank tail)."""
    if scene_py is None or not scene_py.is_file():
        return max(0.5, video_dur - 0.75)

    source = scene_py.read_text(encoding="utf-8")
    m = PLAY_BODY_RE.search(source)
    body = m.group(1) if m else source

    waits = [float(x) for x in WAIT_RE.findall(body)]
    fades = [float(x) for x in FADEOUT_RE.findall(body)]

    # VO often continues on a blank hold after b-roll / montage — freeze last clip frame.
    if BROLL_THEN_WAIT_RE.search(body) and waits:
        return max(0.5, video_dur - waits[-1])

    if fades:
        return max(0.5, video_dur - fades[-1])

    return max(0.5, video_dur - 0.75)


def fit_video_vo_hold(
    src: Path,
    dst: Path,
    target: float,
    scene_py: Path | None,
    *,
    dry_run: bool = False,
) -> float:
    """Trim black tails and extend the last content frame to ``target`` seconds."""
    base = probe_duration(src)
    content_end = min(parse_content_end(scene_py, base), base)
    target = max(0.5, target)

    if dry_run:
        return content_end

    dst.parent.mkdir(parents=True, exist_ok=True)

    if target <= content_end + 0.04:
        vf = f"trim=duration={target:.3f},setpts=PTS-STARTPTS"
    else:
        extra = target - content_end
        vf = (
            f"trim=duration={content_end:.3f},setpts=PTS-STARTPTS,"
            f"tpad=stop_mode=clone:stop_duration={extra:.3f}"
        )

    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-i",
            str(src),
            "-vf",
            vf,
            "-c:v",
            "libx264",
            "-preset",
            "fast",
            "-crf",
            "18",
            "-pix_fmt",
            "yuv420p",
            "-an",
            str(dst),
        ],
        check=True,
        capture_output=True,
    )
    return content_end
