#!/usr/bin/env python3
"""Clean phone VO clips + alignment report vs Manim act durations.

Input:  aura_manim/media/audio/audio_record_aura/{chapter}{act}.m4a  (e.g. 01, 71, 93)
Output: aura_manim/media/audio/processed/ch{N}_act{M}.wav
        vo/vo_clips.json + vo/AUDIO-ALIGNMENT.md

Pipeline (ffmpeg):
  1. Trim leading/trailing silence (silenceremove both ends)
  2. Voice polish: highpass, light denoise, loudnorm
  3. Pad 1.0 s silence at start and end

Alignment uses Whisper speech_end + tail pad as required act length (not raw file
guess). Delta ≈ 0 when speech fits the Manim act slot.

Usage (repo root):
  python Aura/design-video/tools/process_vo_audio.py --dry-run
  python Aura/design-video/tools/process_vo_audio.py
  python Aura/design-video/tools/process_vo_audio.py --skip-process --transcribe
  python Aura/design-video/tools/process_vo_audio.py --transcribe   # needs: pip install openai-whisper
  python Aura/design-video/tools/process_vo_audio.py --chapter 3
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
sys.path.insert(0, str(TOOLS))
from video_catalog import find_act_mp4, probe_duration  # noqa: E402

REPO = TOOLS.parents[2]
DESIGN = REPO / "Aura" / "design-video"
RAW_DIR = DESIGN / "aura_manim" / "media" / "audio" / "audio_record_aura"
OUT_DIR = DESIGN / "aura_manim" / "media" / "audio" / "processed"
VO_DIR = DESIGN / "vo"

PAD_SEC = 1.0
SILENCE_THRESHOLD = "-42dB"
SILENCE_MIN = "0.25"

WAIT_RE = re.compile(r"scene\.wait\(\s*([0-9]+(?:\.[0-9]+)?)\s*\)")

_whisper_model = None


def parse_chapter_act(stem: str) -> tuple[int, int] | None:
    """01 → ch0 act1 · 71 → ch7 act1 · 93 → ch9 act3."""
    if not stem.isdigit() or len(stem) != 2:
        return None
    return int(stem[0]), int(stem[1])


def main_vo_wait(scene_file: Path) -> float | None:
    """Longest scene.wait() in act file ≈ VO hold."""
    if not scene_file.is_file():
        return None
    waits = [float(m.group(1)) for m in WAIT_RE.finditer(scene_file.read_text())]
    return max(waits) if waits else None


def clean_filter_chain() -> str:
    """Trim head/tail silence only (start_periods ×2 via reverse), then polish + pad."""
    thr = SILENCE_THRESHOLD
    dur = SILENCE_MIN
    trim = (
        f"silenceremove=start_periods=1:start_duration={dur}:"
        f"start_threshold={thr}:detection=peak,"
        "areverse,"
        f"silenceremove=start_periods=1:start_duration={dur}:"
        f"start_threshold={thr}:detection=peak,"
        "areverse,"
    )
    polish = "highpass=f=90,afftdn=nr=10:nf=-30,loudnorm=I=-16:TP=-1.5:LRA=11,"
    pad = f"apad=pad_dur={PAD_SEC},areverse,apad=pad_dur={PAD_SEC},areverse"
    return trim + polish + pad


def process_clip(src: Path, dst: Path, *, dry_run: bool) -> bool:
    dst.parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        "ffmpeg",
        "-y",
        "-i",
        str(src),
        "-af",
        clean_filter_chain(),
        "-ar",
        "48000",
        "-ac",
        "1",
        str(dst),
    ]
    if dry_run:
        return True
    subprocess.run(cmd, check=True, capture_output=True)
    return True


def get_whisper_model():
    global _whisper_model
    if _whisper_model is not None:
        return _whisper_model
    try:
        import whisper
    except ImportError:
        return None
    print("Loading Whisper base model (one-time)…")
    _whisper_model = whisper.load_model("base")
    return _whisper_model


def transcribe_whisper(wav: Path) -> dict | None:
    model = get_whisper_model()
    if model is None:
        return None
    result = model.transcribe(str(wav), word_timestamps=True, verbose=False)
    segments = [
        {
            "start": round(s["start"], 2),
            "end": round(s["end"], 2),
            "text": s["text"].strip(),
        }
        for s in result.get("segments", [])
    ]
    return {
        "text": result.get("text", "").strip(),
        "segments": segments,
    }


def speech_metrics(transcript: dict | None) -> dict:
    if not transcript or not transcript.get("segments"):
        return {}
    segs = transcript["segments"]
    start = float(segs[0]["start"])
    end = float(segs[-1]["end"])
    return {
        "speech_start": round(start, 2),
        "speech_end": round(end, 2),
        "speech_sec": round(end - start, 2),
        "required_video_sec": round(end + PAD_SEC, 2),
    }


def align_action(delta: float, current_wait: float | None) -> tuple[str, float | None, float]:
    suggested_wait = None
    hold_extra = 0.0
    if delta < -0.3 and current_wait is not None:
        suggested_wait = round(max(1.5, current_wait + delta), 1)
        action = f"trim video ~{-delta:.1f}s (wait→{suggested_wait:g}s)"
    elif delta > 0.3:
        hold_extra = delta
        action = f"extend video ~{delta:.1f}s"
    else:
        action = "ok"
    return action, suggested_wait, hold_extra


def collect_raw_files(chapter: int | None) -> list[tuple[int, int, Path]]:
    rows: list[tuple[int, int, Path]] = []
    for p in sorted(RAW_DIR.glob("*.m4a")):
        parsed = parse_chapter_act(p.stem)
        if parsed is None:
            continue
        ch, act = parsed
        if chapter is not None and ch != chapter:
            continue
        rows.append((ch, act, p))
    return rows


def out_name(ch: int, act: int) -> str:
    return f"ch{ch}_act{act}.wav"


def build_report(rows: list[dict]) -> str:
    lines = [
        "# VO audio alignment",
        "",
        "> Generated by `tools/process_vo_audio.py` · processed clips in `aura_manim/media/audio/processed/`",
        "",
        "**Δ (align)** = `(speech_end + 1s tail pad) − video act length` from Whisper timestamps.",
        "- **Δ &lt; 0** → video longer than speech → trim tail or shorten `scene.wait()`",
        "- **Δ &gt; 0** → speech runs past video → extend holds or use `mux_chapter_vo.py`",
        "",
        f"Every cleaned clip has **{PAD_SEC}s** head + tail pad in the WAV file.",
        "",
        "Automated sync (no Resolve):",
        "```bash",
        "python Aura/design-video/tools/sync_vo_alignment.py --write-holds --apply-holds --concat",
        "python Aura/design-video/tools/mux_chapter_vo.py --chapter N",
        "```",
        "",
        "| Ch | Act | Speech | Req | Video | Δ | Wait | Action |",
        "|----|-----|--------|-----|-------|---|------|--------|",
    ]
    for r in rows:
        sp = f"{r.get('speech_sec', 0):.1f}s" if r.get("speech_sec") else "—"
        req = f"{r.get('required_video_sec', r['clean_sec']):.1f}s"
        sug = f"{r['suggested_wait']:.1f}s" if r.get("suggested_wait") else "—"
        delta = r.get("delta_align", r["delta"])
        lines.append(
            f"| {r['chapter']} | {r['act']} | {sp} | {req} | "
            f"{r['video_sec']:.1f}s | {delta:+.1f}s | {sug} | {r['action']} |"
        )
    lines.extend(
        [
            "",
            "---",
            "",
            "## Transcripts",
            "",
            "Full segment timestamps live in `vo/vo_clips.json` under `transcript.segments`.",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Clean phone VO + alignment report")
    parser.add_argument("--chapter", type=int, default=None)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--skip-process", action="store_true", help="Only transcribe existing WAVs")
    parser.add_argument("--transcribe", action="store_true")
    parser.add_argument("--threshold", default=SILENCE_THRESHOLD)
    args = parser.parse_args()

    if not args.skip_process and not RAW_DIR.is_dir():
        print(f"Missing {RAW_DIR}", file=sys.stderr)
        sys.exit(1)

    if args.skip_process:
        raw_files = []
        for wav in sorted(OUT_DIR.glob("ch*_act*.wav")):
            m = re.match(r"ch(\d+)_act(\d+)\.wav$", wav.name)
            if not m:
                continue
            ch, act = int(m.group(1)), int(m.group(2))
            if args.chapter is not None and ch != args.chapter:
                continue
            raw = RAW_DIR / f"{ch}{act}.m4a"
            raw_files.append((ch, act, raw if raw.is_file() else wav))
    else:
        raw_files = collect_raw_files(args.chapter)

    if not raw_files:
        print("No clips to process", file=sys.stderr)
        sys.exit(1)

    report_rows: list[dict] = []
    manifest: list[dict] = []

    for ch, act, src in raw_files:
        dst = OUT_DIR / out_name(ch, act)
        video = find_act_mp4(ch, act, "2160p60")
        scene_py = DESIGN / "aura_manim" / "scenes" / f"scene{ch}_act{act}.py"
        raw_sec = probe_duration(src) if src.is_file() else 0.0
        video_sec = probe_duration(video) if video else 0.0
        current_wait = main_vo_wait(scene_py)

        if args.dry_run:
            clean_sec = raw_sec
        elif args.skip_process:
            if not dst.is_file():
                print(f"Missing {dst}", file=sys.stderr)
                continue
            clean_sec = probe_duration(dst) or 0.0
        else:
            print(f"ch{ch} act{act}: {src.name} → {dst.name}")
            process_clip(src, dst, dry_run=False)
            clean_sec = probe_duration(dst) or 0.0

        entry: dict = {
            "chapter": ch,
            "act": act,
            "key": f"{ch}:{act}",
            "raw": str(src.relative_to(REPO)) if src.is_file() else None,
            "processed": str(dst.relative_to(REPO)),
            "raw_sec": raw_sec,
            "clean_sec": clean_sec,
            "video_sec": video_sec,
            "delta": round(clean_sec - video_sec, 2),
            "current_wait": current_wait,
            "pad_sec_each_end": PAD_SEC,
        }

        if args.transcribe and not args.dry_run and dst.is_file():
            print(f"  transcribing ch{ch} act{act}…")
            tx = transcribe_whisper(dst)
            if tx:
                entry["transcript"] = tx
                entry.update(speech_metrics(tx))
            else:
                print("  (skip transcript — pip install openai-whisper)", file=sys.stderr)

        req = entry.get("required_video_sec") or clean_sec
        delta_align = round(req - video_sec, 2)
        action, suggested_wait, hold_extra = align_action(delta_align, current_wait)
        entry["required_video_sec"] = round(req, 2)
        entry["delta_align"] = delta_align
        entry["suggested_wait"] = suggested_wait
        entry["hold_extra"] = hold_extra
        entry["action"] = action

        if raw_sec > 3 and clean_sec < raw_sec * 0.35 and not entry.get("speech_sec"):
            entry["action"] = f"⚠ check trim — {action}"

        report_rows.append(entry)
        manifest.append(entry)

    if args.transcribe and get_whisper_model() is None:
        print("\nInstall Whisper: pip install openai-whisper", file=sys.stderr)

    VO_DIR.mkdir(parents=True, exist_ok=True)
    if not args.dry_run:
        (VO_DIR / "vo_clips.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
        (VO_DIR / "AUDIO-ALIGNMENT.md").write_text(build_report(report_rows), encoding="utf-8")

    trim_count = sum(1 for r in report_rows if r.get("delta_align", r["delta"]) < -0.3)
    extend_count = sum(1 for r in report_rows if r.get("delta_align", r["delta"]) > 0.3)
    ok_count = len(report_rows) - trim_count - extend_count

    print(f"\n{len(report_rows)} clip(s) · ok={ok_count} trim={trim_count} extend={extend_count}")
    if not args.dry_run:
        print(f"  {OUT_DIR.relative_to(REPO)}/")
        print(f"  {VO_DIR.relative_to(REPO)}/vo_clips.json")
        print(f"  {VO_DIR.relative_to(REPO)}/AUDIO-ALIGNMENT.md")
        if args.transcribe and get_whisper_model():
            print("\nNext: sync_vo_alignment.py --write-holds  OR  mux_chapter_vo.py --chapter N")


if __name__ == "__main__":
    main()
