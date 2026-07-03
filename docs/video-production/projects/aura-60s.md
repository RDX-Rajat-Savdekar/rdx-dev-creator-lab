# Aura 60s recruiter clip

**Tier B** — short Manim text cards + demo B-roll + licensed music. **No VO.**

**Journal:** [`Aura/journal.md`](../../../Aura/journal.md) (entry 2026-07-01)

---

## Paths

| What | Where |
|------|--------|
| Manim scenes | `Aura/manim/aura_cards.py` |
| Assembly | `Aura/manim/build_60s.py` |
| Music mix | `Aura/manim/add_music.py` |
| Clips D1–D6 | `Aura/clips/` |
| **Ship file** | `Aura/output/aura-60s-with-music.mp4` |

---

## Commands

```bash
.venv/bin/python Aura/manim/build_60s.py
.venv/bin/python Aura/manim/add_music.py --music Aura/music/leberch-documentary-517370.mp3 --volume 0.10
```

---

## Notes

- Mute all source demo audio.  
- Pixabay license in `Aura/music/solo-piano-documentary-517370-license.txt`.  
- Beat sheet: `project-sources/projects/aura-visionos/60s-beat-sheet.md`
