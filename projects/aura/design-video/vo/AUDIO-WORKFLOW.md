# VO audio workflow — phone recordings → synced video

> **Canonical process:** [`../../../docs/video-production/02-VO-RECORDING-AND-SYNC.md`](../../../docs/video-production/02-VO-RECORDING-AND-SYNC.md)  
> **Raw:** `aura_manim/media/audio/audio_record_aura/{chapter}{act}.m4a` (e.g. `31.m4a` = ch3 act1)  
> **Processed:** `aura_manim/media/audio/processed/ch{N}_act{M}.wav`

---

## 1. Clean clips (done once per recording batch)

```bash
python Aura/design-video/tools/process_vo_audio.py
```

Each clip gets:
- Leading/trailing silence removed
- Light polish (highpass, denoise, loudnorm → broadcast-ish -16 LUFS)
- **1.0 s** silence pad at **start and end** (handles for editing)

Outputs:
- `vo/vo_clips.json` — machine-readable durations + deltas
- `vo/AUDIO-ALIGNMENT.md` — table vs 4K act lengths

Re-run anytime you drop new `.m4a` files in the raw folder.

---

## 2. Transcribe + alignment (recommended)

Whisper gives **speech_start / speech_end** so Δ ignores dead air and the 2×1s edit pads correctly.

```bash
# one-time: venv in design-video/ has whisper
Aura/design-video/.venv/bin/python Aura/design-video/tools/process_vo_audio.py --skip-process --transcribe
```

Adds `transcript.segments[]` with `{start, end, text}` plus `speech_sec`, `delta_align` in `vo_clips.json`.

**Δ (align)** = `(speech_end + 1s tail pad) − video act length`.

| Delta | Meaning | Fix (no Resolve) |
|-------|---------|------------------|
| **Negative** | Video hold longer than speech | `mux_chapter_vo.py` trims act tail · or `sync_vo_alignment.py --write-waits` + re-render |
| **Positive** | Speech runs past video end | `sync_vo_alignment.py --write-holds --apply-holds` · or `mux_chapter_vo.py` |
| **~0** | Aligned | mux or concat as-is |

**Suggested wait** = `current_wait + Δ` if you re-render Manim instead of ffmpeg trim.

---

## 3. Automated sync (no Resolve)

**Option A — mux VO onto video (fastest preview):**

```bash
python Aura/design-video/tools/mux_chapter_vo.py --chapter 0
# → output/scene0_chapter0_2160p60_vo.mp4
python Aura/design-video/tools/mux_chapter_vo.py --all
```

Per act: strip the fade-to-black tail, **freeze the last visible frame** through your full VO clip, mux cleaned WAV.

Uses `sceneN_actM.py` to find where content ends (before `FadeOut`, or before blank `wait` after b-roll).

Add **2s chapter title card** before each chapter (YouTube chapter name):

```bash
Aura/design-video/.venv/bin/python Aura/design-video/tools/mux_chapter_vo.py --all --banner
# → output/sceneN_chapterN_2160p60_vo.mp4 (each starts with banner)

Aura/design-video/.venv/bin/python Aura/design-video/tools/build_full_film.py
# → output/aura_design_video_2160p60_vo.mp4 (full concat)
```

**Option B — extend Manim holds then concat:**

```bash
python Aura/design-video/tools/sync_vo_alignment.py --write-holds
python Aura/design-video/tools/sync_vo_alignment.py --apply-holds --concat
```

---

## 4. Re-render path (optional, cleaner)

For acts with large negative Δ:

```bash
python Aura/design-video/tools/sync_vo_alignment.py --write-waits
# or per act:
python Aura/design-video/tools/adjust_waits.py --chapter 0 --act 1 --set 6.2
# re-render act 4K + re-concat chapter
```

Then re-run `process_vo_audio.py --skip-process --transcribe`.

---

## 5. Resolve assembly (optional)

Same act-start placement as before — only if you prefer manual editing.

---

## 6. Naming convention

| File | Chapter · Act |
|------|----------------|
| `01.m4a` | 0 · 1 |
| `15.m4a` | 1 · 5 |
| `71.m4a` | 7 · 1 |
| `93.m4a` | 9 · 3 |

Processed output uses explicit names: `ch7_act1.wav`.

---

## Related tools

| Tool | Role |
|------|------|
| [`process_vo_audio.py`](../tools/process_vo_audio.py) | Clean + transcribe + align |
| [`sync_vo_alignment.py`](../tools/sync_vo_alignment.py) | Write holds / waits from transcripts |
| [`mux_chapter_vo.py`](../tools/mux_chapter_vo.py) | ffmpeg mux — no Resolve |
| [`extend_act_holds.py`](../tools/extend_act_holds.py) | Extend video tail (VO longer) |
| [`adjust_waits.py`](../tools/adjust_waits.py) | Shorten Manim holds (VO shorter) |
| [`build_act_timestamps.py`](build_act_timestamps.py) | Act start times |
