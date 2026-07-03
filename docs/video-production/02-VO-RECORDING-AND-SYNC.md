# VO recording and sync

Generic pipeline for **phone-recorded narration** synced to Manim acts **without Resolve**.

**Reference implementation:** `Aura/design-video/tools/` (battle-tested on 46 act clips).

---

## Overview

```
Phone .m4a  →  process_vo_audio.py  →  processed WAV
Manim 4K acts  →  mux_chapter_vo.py  →  chapter MP4 + VO (+ optional banner)
All chapters  →  build_full_film.py  →  full portfolio MP4
```

Adapt paths when adding a new project ([07-NEW-PROJECT-SETUP.md](07-NEW-PROJECT-SETUP.md)).

---

## 1. Raw recording

| Item | Convention |
|------|------------|
| **Naming** | `{chapter}{act}.m4a` two digits — `31` = ch3 act1 |
| **Prompter** | `serve.py` + `prompter.html` — teleprompter + synced act video |
| **Script** | `build_teleprompter.py` from `vo/sceneN.md` |

One clip per act; per-act sync is enough.

---

## 2. Audio cleanup

```bash
python {project}/tools/process_vo_audio.py
```

- Trim head/tail silence  
- highpass + denoise + loudnorm (~−16 LUFS)  
- **1.0 s pad** start + end  

Outputs: `processed/chN_actM.wav`, `vo/vo_clips.json`, `vo/AUDIO-ALIGNMENT.md`

---

## 3. Transcription (recommended)

```bash
{project}/.venv/bin/pip install openai-whisper pillow
{project}/.venv/bin/python {project}/tools/process_vo_audio.py --skip-process --transcribe
```

Whisper adds `speech_start`, `speech_end`, `transcript.segments[]` — use to verify script coverage and detect mislabeled files.

---

## 4. Video ↔ VO sync (critical)

### Problems we solved once (apply everywhere)

| Symptom | Cause | Fix |
|---------|-------|-----|
| Black screen while speaking | Mux extended last frame **after FadeOut** | `vo_video_fit.py` — hold last **content** frame |
| Blank after b-roll | `scene.wait()` after b-roll with no visuals | Parser freezes last b-roll frame |
| Resolve not available | Manual NLE | ffmpeg mux only |

### Algorithm (`vo_video_fit.py`)

1. Parse act `.py` for content end (before terminal fade, or before blank tail wait)  
2. Strip fade-to-black from video  
3. **Freeze last visible frame** to match cleaned WAV duration  
4. Mux audio  

Target duration = **full cleaned WAV** (`clean_sec`).

```bash
{project}/.venv/bin/python {project}/tools/mux_chapter_vo.py --all --banner
{project}/.venv/bin/python {project}/tools/build_full_film.py
```

---

## 5. Chapter banners (optional)

2s title card before each chapter — chapter number + section title from `vo/sceneN.md`.  
Tool: `chapter_banners.py` (requires Pillow).

---

## 6. Optional: re-render Manim instead of mux trim

```bash
python {project}/tools/adjust_waits.py --chapter N --act M --set X
# re-render 4K → re-concat → re-mux
```

---

## Related

- [03-TOOLS-REFERENCE.md](03-TOOLS-REFERENCE.md)
- [05-LESSONS-LEARNED.md](05-LESSONS-LEARNED.md)
- Aura living copy: `Aura/design-video/vo/AUDIO-WORKFLOW.md`
