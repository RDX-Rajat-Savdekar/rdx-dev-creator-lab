# Aura design video

**Tier C** — multi-chapter Manim explainer with phone VO (ch 0–9).  
**Journal:** [`Aura/journal.md`](../../../Aura/journal.md) (entry 2026-07-03 = shipped)

---

## Paths

| What | Where |
|------|--------|
| Manim | `Aura/design-video/aura_manim/` |
| Plan + VO | `Aura/design-video/vo/sceneN.md` |
| Tools | `Aura/design-video/tools/` |
| Story / honesty | `Aura/design-video/HACKATHON-STORY.md` |
| Standards ch 6+ | `Aura/design-video/MANIM-STANDARDS.md` |
| Agent checklist | `Aura/design-video/AGENTS.md` |

---

## Deliverables

| Output | Path |
|--------|------|
| **Full film** | `Aura/design-video/output/aura_design_video_2160p60_vo.mp4` (~553s) |
| Per chapter + VO | `Aura/design-video/output/sceneN_chapterN_2160p60_vo.mp4` |
| Silent concat | `Aura/design-video/output/sceneN_chapterN_2160p60.mp4` |

---

## Quick commands

```bash
# Remux after re-recording VO
Aura/design-video/.venv/bin/python Aura/design-video/tools/process_vo_audio.py --skip-process --transcribe
Aura/design-video/.venv/bin/python Aura/design-video/tools/mux_chapter_vo.py --all --banner
Aura/design-video/.venv/bin/python Aura/design-video/tools/build_full_film.py
```

---

## Notes

- Ch 0–5 Manim code frozen — no standards refactors.  
- VO naming: `audio_record_aura/01.m4a` = ch0 act1.  
- YouTube chapter names in each `vo/sceneN.md` header.
