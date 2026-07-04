# Manim standards — Aura design video (ch 6+)

> **Enforced by:** [`AGENTS.md`](AGENTS.md) · [`.cursor/rules/aura-manim.mdc`](../.cursor/rules/aura-manim.mdc)  
> **Postmortem:** [`PROCESS-REVIEW.md`](PROCESS-REVIEW.md)  
> **Ch 0–5:** frozen renders — do not refactor; new rules apply from ch 6 onward.

---

## Required APIs

### Text — `aura_manim/typography.py`

| Function | Use for |
|----------|---------|
| `body_text()` | Any sentence the viewer must read |
| `caption_line()` | Short tags above panels (`utterance → sentences`) |
| `subtext()` | Secondary readable lines (alias of `body_text`) |
| `chip_label()` | Small keyword under a node |
| `node_label()` | Text inside pipeline boxes |

**Forbidden:** raw `Text(...)` for readable copy · `Text(..., width=)` squeeze on sentences · scaling a group that contains readable `Text`.

### Layout — `aura_manim/components/layout.py`

| Function | Use for |
|----------|---------|
| `fit_center(group)` | Center diagram in frame; scale down if too wide |
| `flow_lr(a, b, c)` | Left → right flow, then `fit_center` |
| `arrow_between(left, right)` | Arrow **after** layout |
| `labeled_card(text, tag=...)` | Plate + readable body |
| `tag_above(panel, text)` | Header aligned to panel |

**Forbidden:** `move_to(ORIGIN)` + chain of `next_to(RIGHT)` without final `fit_center`.

### Patterns — compose primitives

| Module | Use for |
|--------|---------|
| `split_layout` | Visual top + Swift bottom |
| `workflow` | Capture → ML → Buffer → Present |
| `honesty_card` | Shipped vs planned |
| `rejected` | Ghost path + strikethrough |
| `code_panel` | Swift snippets |
| `broll` | Demo clips D1–D6 |
| `labels.on_screen_label` | Bottom-third chapter label |

### Story components (chapter-specific)

Create `components/foo.py` only for a **story visual** reused across acts in one chapter. Inside: only `body_text`, `layout`, `theme` — no private `_foo_text()`.

| Module | Chapter | Notes |
|--------|---------|-------|
| `pipeline.py` | 3+ | Full dual-pipeline diagram (`workflow` wrapper) |
| `pipeline_stub.py` | 2 | Simplified pipeline for ch 2 only — do not use in ch 6+ |
| `segmentation` | 4 | Legacy private text helpers — do not copy |
| `texture_bake` | 5 | Legacy — do not copy |

---

## Per-act workflow (ch 6+)

```
1. vo/sceneN.md        — PLAY CHECKLIST + VO seed (before code)
2. components/         — story module if needed; compose layout + typography
3. sceneN_actM.py      — play_actM; default scene.wait(5.5) VO hold
4. manim -ql SceneNActMLayout
5. extract_act_frames.py → vision QA (checklist below)
6. manim -ql SceneNActM → re-extract if composition changes
7. manim -ql SceneNFull
8. User review         — story / pacing / VO tone (not pixels)
9. manim -qk per act → concat → read-aloud → adjust_waits.py → re-render
```

Mark in `vo/sceneN.md` when layout QA passes: `layout QA: pass (YYYY-MM-DD)`.

---

## Frame checklist (after `extract_act_frames.py`)

**Layout**

- [ ] Nothing clipped at frame edges (reserve bottom for `on_screen_label`)
- [ ] Diagram visually centered
- [ ] Data flow arrows left → right unless story says otherwise
- [ ] No text-on-text overlap
- [ ] Split-layout: visual pane clear of code + bottom label

**Typography**

- [ ] Readable copy via `body_text` / `caption_line`
- [ ] No glued words (`dumpsat`, `differentrender`)
- [ ] No crush-scaled paragraphs

---

## Pacing / VO (visual-first — agreed 2026-07-03)

1. **Ship visuals** with default `scene.wait(5.5)` per act.
2. **Draft VO** in `vo/sceneN.md` while watching concat (no recording yet).
3. **Read aloud** over concat — note where you run short or long.
4. **Bulk adjust** waits:

```bash
python Aura/design-video/tools/adjust_waits.py --chapter 6 --show
python Aura/design-video/tools/adjust_waits.py --chapter 6 --add 2.0
```

5. Re-render affected acts → re-concat → `build_act_timestamps.py`.

You do **not** need a final transcript before first 4K. Visual-first + `adjust_waits` is the default; script-first is optional if you prefer writing VO before Manim.

---

## Tools

| Tool | Purpose |
|------|---------|
| `tools/extract_act_frames.py` | partial_movie → PNG for layout QA |
| `tools/adjust_waits.py` | bulk add/set `scene.wait()` per chapter |
| `vo/build_act_timestamps.py` | measured act timeline from 4K renders |
| `review.plop()` | manual static layout in `SceneNActMLayout` |

---

## Anti-pattern quick reference

| Don't | Do instead |
|-------|------------|
| `Text("long sentence...")` | `body_text("long sentence...")` |
| Scale group with text inside | Wider plate / smaller font |
| Arrow before `arrange` | `arrange` → `arrow_between` |
| Anchor at ORIGIN, grow right | `flow_lr` → `fit_center` |
| New `_readable_text` in component | `body_text` |
| Skip frame review | `-ql` → extract → checklist |
