# VO workflow — design video

> **Goal:** One `vo/sceneN.md` per chapter, filled **after** final per-act Manim renders, so VO recording matches what’s actually on screen.

**Companion files:**

| File | Role |
|------|------|
| [`SCRIPT.md`](../SCRIPT.md) | Chapter-level narration ideas (may lag visuals) |
| [`SCENE-PLAN.md`](../SCENE-PLAN.md) | Target timestamps + tool per beat |
| `aura_manim/scenes/sceneN_actM.py` | Ground truth — PLAY CHECKLIST + on-screen labels |
| `output/sceneN_chapter*_2160p60.mp4` | Concat preview for read-aloud |
| [`tools/prompter.html`](../tools/prompter.html) | Teleprompter (import narration from `sceneN.md`) |

---

## Per-chapter checklist (copy for every scene)

```
[ ] All acts rendered: manim -qk --frame_rate 60 scenes/sceneN_actM.py SceneNActM
[ ] Concat: output/sceneN_chapterN_2160p60.mp4 (absolute paths in concat.txt)
[ ] Copy vo/_TEMPLATE.md → vo/sceneN.md
[ ] Run build_act_timestamps.py --chapter N → paste timeline table
[ ] Fill act descriptions from each sceneN_actM.py PLAY CHECKLIST
[ ] Draft VO block (one paragraph per act)
[ ] Read aloud over concat MP4 — trim VO or Manim self.wait() until fit
[ ] Update SCRIPT.md chapter table if narration locked
[ ] Record VO → Resolve: Manim concat + VO track (no re-sync per act)
```

---

## Timestamp source of truth

**Use rendered MP4 duration**, not SCENE-PLAN targets. Plans drift when holds change (e.g. act 1’s 7.2 s VO hold).

From repo root:

```bash
python Aura/design-video/vo/build_act_timestamps.py --chapter 0
```

Or manually:

```bash
ffprobe -v error -show_entries format=duration -of csv=p=0 \
  Aura/design-video/aura_manim/media/videos/scene0_act1/2160p60/Scene0Act1.mp4
```

Concat acts (absolute paths in list file):

```bash
# See output/scene0_concat.txt — paths must be absolute if list lives outside aura_manim
ffmpeg -y -f concat -safe 0 -i Aura/design-video/output/scene0_concat.txt -c copy \
  Aura/design-video/output/scene0_chapter0_2160p60.mp4
```

---

## `vo/sceneN.md` sections

1. **Header** — chapter title, YouTube chapter name, render file, total duration, VO pace target  
2. **Act timeline** — act #, start, end, duration, on-screen label, source `.py`  
3. **Act descriptions** — what the viewer sees (for editors + future you)  
4. **VO draft** — speakable text timed to acts; word count + estimated seconds  
5. **Trim notes** — gaps vs SCENE-PLAN; which `self.wait()` to cut  
6. **Status** — draft / read-aloud / recorded  

Copy structure from [`_TEMPLATE.md`](_TEMPLATE.md). First completed example: [`scene0.md`](scene0.md).

---

## Manim ↔ VO iteration loop

```
Edit sceneN_actM.py  →  re-render that act only (-qk)
                    →  re-concat sceneN_chapter*_2160p60.mp4
                    →  update vo/sceneN.md timestamps (build_act_timestamps.py)
                    →  read-aloud again
```

Fast layout/motion iteration: `SceneNFull` at `-ql` (e.g. `scene0_full.py`, `scene1_full.py`).  
Acts that share a diagram: `state['chain']=True` in `sceneN_full.py` (device stays on screen ch 1 acts 1→3).  
**Do not** record VO until `-qk` per-act concat is approved.

---

## Chapter index (fill as you go)

| Ch | VO file | Concat output | Acts | Status |
|----|---------|---------------|------|--------|
| 0 | [`scene0.md`](scene0.md) | `output/scene0_chapter0_2160p60.mp4` | 6 | draft VO |
| 1 | [`scene1.md`](scene1.md) | `output/scene1_chapter1_2160p60.mp4` | 5 | draft VO · extend waits |
| 2 | [`scene2.md`](scene2.md) | `output/scene2_chapter2_2160p60.mp4` | 6 | draft VO · extend waits |
| 3 | [`scene3.md`](scene3.md) | `output/scene3_chapter3_2160p60.mp4` | 6 | draft VO · extend waits |
| 4–9 | `sceneN.md` | — | TBD | — |

---

## VO pace

- **Target:** ~140 wpm (same as `SCRIPT.md`)
- **Formula:** `seconds ≈ word_count / 140 × 60`
- Act 1 often has long `self.wait()` for VO — trim waits in code after read-aloud, not by rushing speech
