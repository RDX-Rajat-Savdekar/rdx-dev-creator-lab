# Agent instructions — Aura design video (Manim)

> **Process playbook (all projects):** [`../../docs/video-production/README.md`](../../docs/video-production/README.md)  
> **Ch 6+ only:** standards below. **Ch 0–5:** frozen — do not refactor scene/component code.

---

## Before handing work to the user

1. Render each new/changed act: `manim -ql scenes/sceneN_actM.py SceneNActM`
2. Run `python Aura/design-video/tools/extract_act_frames.py --scene sceneN_actM`
3. **Inspect PNGs** in `vo/review_frames/sceneN_actM/` — pass [`MANIM-STANDARDS.md`](MANIM-STANDARDS.md) checklist
4. Fix layout/text; re-render until pass
5. Only then run `SceneNFull` and report to user

**Do not ask the user to QA:** clipping, centering, overlap, kerning, unreadable font size.

---

## Code rules (ch 6+)

| Rule | Detail |
|------|--------|
| Text | `typography.body_text()` / `caption_line()` — never raw `Text` for readable copy |
| Layout | `components.layout.flow_lr`, `fit_center`, `arrow_between` |
| Arrows | Draw **after** final positions |
| Scale | Never scale groups containing readable `Text` |
| Flow | Default **left → right** for data/pipeline diagrams |
| Components | Story modules compose primitives — no private text helpers |
| VO doc | Create `vo/sceneN.md` with PLAY CHECKLIST + VO seed **when creating acts** |
| Layout gate | Run `SceneNActMLayout` before motion when composition changes |
| Waits | Default `scene.wait(5.5)` in `play_actM`; user adjusts via `adjust_waits.py` after read-aloud |

---

## File layout per chapter

```
vo/sceneN.md              — plan + checklist + VO (draft early)
aura_manim/scenes/
  sceneN_act{1…M}.py      — play_actM + SceneNActMLayout + SceneNActM
  sceneN_full.py          — ENABLED_ACTS, calls play_actM in order
aura_manim/components/    — story module only if reused across acts
code_snippets/*.swift     — one concept per file
output/sceneN_concat.txt  — absolute paths for ffmpeg
```

---

## Render commands

From `aura_manim/`:

```bash
.venv/bin/manim -ql scenes/scene6_act1.py Scene6Act1Layout   # layout QA
.venv/bin/manim -ql scenes/scene6_act1.py Scene6Act1       # motion preview
.venv/bin/manim -ql scenes/scene6_full.py Scene6Full       # chapter timing
.venv/bin/manim -qk --frame_rate 60 scenes/scene6_act1.py Scene6Act1  # 4K act
```

---

## Pacing workflow

Visual-first is intentional. Chapters ship short (~35–55s); user extends waits after VO read-aloud:

```bash
python Aura/design-video/tools/adjust_waits.py --chapter 6 --show
python Aura/design-video/tools/adjust_waits.py --chapter 6 --add 2.0
```

Do not block chapter delivery on hitting SCENE-PLAN duration targets.

---

## Component tiers

| Tier | Examples | Action |
|------|----------|--------|
| Primitives | `typography`, `layout`, `theme`, `labels` | Extend, never fork |
| Patterns | `split_layout`, `workflow`, `honesty_card`, `broll` | Reuse across chapters |
| Story | `components/your_chapter.py` | One chapter; compose primitives only |

---

## Related

- [`../../docs/video-production/README.md`](../../docs/video-production/README.md) — **repo-wide portfolio pipeline**
- [`../../docs/video-production/projects/aura-design-video.md`](../../docs/video-production/projects/aura-design-video.md) — this project
- [`vo/VO-WORKFLOW.md`](vo/VO-WORKFLOW.md) — concat + timestamps
- [`vo/AUDIO-WORKFLOW.md`](vo/AUDIO-WORKFLOW.md) — phone VO → final MP4
- [`LEARNING.md`](LEARNING.md) — Manim concepts
- [`README.md`](README.md) — full production phases
