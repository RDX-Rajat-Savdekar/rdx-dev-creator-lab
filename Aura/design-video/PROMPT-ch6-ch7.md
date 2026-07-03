# Agent prompt — Chapters 6 & 7 (copy-paste)

> **Use:** Start a new Cursor/agent chat. Paste everything below the line.  
> **Repo:** `Manim-DSA-SD-Concepts` · **Path:** `Aura/design-video/`  
> **Prev work:** Ch 0–5 Manim renders frozen ✅ — do not refactor them.

---

## PROMPT START

You are building **Chapters 6 and 7** of the Aura system-design video (Manim + VO docs). This is a **Manim-first** project on visionOS / hackathon architecture storytelling.

### Read first (mandatory)

1. [`Aura/design-video/AGENTS.md`](Aura/design-video/AGENTS.md) — agent rules
2. [`Aura/design-video/MANIM-STANDARDS.md`](Aura/design-video/MANIM-STANDARDS.md) — text/layout APIs, frame checklist
3. [`Aura/design-video/PROCESS-REVIEW.md`](Aura/design-video/PROCESS-REVIEW.md) — why we failed on layout before ch 6
4. [`Aura/design-video/SCENE-PLAN.md`](Aura/design-video/SCENE-PLAN.md) — ch 6 & 7 beats
5. [`Aura/design-video/HACKATHON-STORY.md`](Aura/design-video/HACKATHON-STORY.md) — honesty / rejected paths
6. **Reference chapters (copy patterns, do not edit):**
   - [`vo/scene3.md`](Aura/design-video/vo/scene3.md) — VO doc depth + PLAY CHECKLISTs
   - [`scenes/scene3_act3.py`](Aura/design-video/aura_manim/scenes/scene3_act3.py) — `split_layout` + `thread_lane`
   - [`scenes/scene4_act*.py`](Aura/design-video/aura_manim/scenes/) — story components + before/after
   - [`scenes/scene5_act*.py`](Aura/design-video/aura_manim/scenes/) — rejected path + compare panels
   - [`scenes/_TEMPLATE_act.py`](Aura/design-video/aura_manim/scenes/_TEMPLATE_act.py) — ch 6+ act skeleton

### Hard rules

| Rule | Detail |
|------|--------|
| **Frozen** | Do **not** change `scene0`–`scene5` act files or `segmentation.py` / `texture_bake.py` |
| **Text** | `typography.body_text()` / `caption_line()` only — no raw `Text` for readable copy |
| **Layout** | `components.layout`: `flow_lr`, `fit_center`, `arrow_between`, `labeled_card` |
| **Arrows** | Draw **after** `arrange` — never before |
| **Scale** | Never scale groups containing readable `Text` |
| **Flow** | Data/pipeline diagrams default **left → right** |
| **VO doc first** | Create `vo/scene6.md` and `vo/scene7.md` with story arc + per-act PLAY CHECKLIST + VO seed **before** coding |
| **Layout QA** | After each act `-ql`: run `extract_act_frames.py` → inspect PNGs → pass MANIM-STANDARDS checklist **before** telling user act is done |
| **Waits** | Default `scene.wait(5.5)` per act; user extends later via `adjust_waits.py` after read-aloud |
| **Unity** | **Manim stands in** for Unity viz this pass (like ch 5 jitter). Label honestly if using Manim instead of `AzimuthRays.unity` |

### Manim path

```bash
cd Aura/design-video/aura_manim
../../.venv/bin/manim -ql scenes/scene6_act1.py Scene6Act1Layout
../../.venv/bin/manim -ql scenes/scene6_act1.py Scene6Act1
```

### Tools

```bash
# Layout QA (after -ql render)
python Aura/design-video/tools/extract_act_frames.py --scene scene6_act1

# VO pacing (after read-aloud — not during first build)
python Aura/design-video/tools/adjust_waits.py --chapter 6 --show
python Aura/design-video/tools/adjust_waits.py --chapter 6 --add 2.0

# 4K concat (when user asks)
python Aura/design-video/vo/build_act_timestamps.py --chapter 6 --markdown
```

### File conventions (match ch 2–5)

```
Aura/design-video/
  vo/scene6.md, vo/scene7.md
  code_snippets/mainactor_bridge.swift   # ch 6 — create
  code_snippets/immersive_caveat.swift   # ch 7 optional
  aura_manim/
    scenes/scene6_act{1…N}.py, scene6_full.py
    scenes/scene7_act{1…N}.py, scene7_full.py
    components/mainactor_bridge.py       # ch 6 story visuals (new)
    components/hud_pivot.py              # ch 7 story visuals (new) — name as you see fit
  output/scene6_concat.txt, scene7_concat.txt
```

Each act file exports: `play_actM(scene, state)`, `SceneNActMLayout`, `SceneNActM`.  
`sceneN_full.py`: `ENABLED_ACTS`, `ACT_PLAYERS`, calls `play_actM` in order.

---

## Chapter 6 — MainActor bridge

**YouTube chapter:** *MainActor bridge*  
**SCENE-PLAN:** `8:55` → `9:55` (~60 s target) · **~140 words VO**  
**Story:** ML callbacks arrive off the main thread; `@Published` UI state must mutate on **MainActor**. This is why caption updates hop threads safely while the tap stays realtime (connects to ch 3 queue story).

### Proposed acts (adjust if beats need splitting)

| Act | Beat | On-screen label | Visual | Swift / b-roll |
|-----|------|-----------------|--------|----------------|
| 1 | ML callback off main thread | Background thread · ML result | Two-lane diagram (callback lane vs MainActor lane) — extend or parallel `thread_lane.py` | — |
| 2 | `@Published` mutation rule | MainActor · UI updates | `split_layout`: diagram + `mainactor_bridge.swift` highlight | `mainactor_bridge.swift` |
| 3 | Why it matters for captions | Captions update on main | Live update card / pipeline inset → optional **D1** broll 3s | `broll.D1` |

### Reuse

- `components/thread_lane.py` — tap vs queue pattern (ch 3); ch 6 is **ML delegate → MainActor** (different labels, same lane idiom)
- `components/split_layout.py` — act 2
- `components/workflow.py` — optional small inset in act 3
- `rejected.py` — **not** this chapter (nothing rejected — it's a bridge pattern)

### Swift snippet to create

`code_snippets/mainactor_bridge.swift` — minimal `@MainActor` / `Task { @MainActor in ... }` around `@Published` caption mutation. Header comment with Aura-Vision-Pro source path.

### Deliverables ch 6

- [ ] `vo/scene6.md` (full depth like `vo/scene3.md`)
- [ ] `scene6_act{1…3}.py` + `scene6_full.py`
- [ ] `components/mainactor_bridge.py` (or similar)
- [ ] `code_snippets/mainactor_bridge.swift`
- [ ] `-ql` all acts + `Scene6Full` preview
- [ ] Frame QA pass per act (`extract_act_frames.py`)
- [ ] **Do not** 4K until user asks

---

## Chapter 7 — Directional pins → Iron Man HUD

**YouTube chapter:** *Iron Man HUD*  
**SCENE-PLAN:** `9:55` → `11:25` (~90 s target) · **~245 words VO** · **SCRIPT.md ch 7 has draft narration**  
**Story:** We **tried** world-locked directional sound pins → **rejected** (no exact coords; off-screen hazard) → pivoted to **head-relative Iron Man HUD** (what demo ships). Azimuth still computed, not shown. Spatial prototype demoed with HEAD caveat. Unity = viz only.

**VO checkpoint:** Name **both** rejection reasons before celebrating HUD.

### Proposed acts (Manim-first; Unity deferred)

| Act | Beat | On-screen label | Visual | Support |
|-----|------|-----------------|--------|---------|
| 1 | Tried world-locked pins | Tried: world-locked pins | Head + rays to pins around room (Manim) | — |
| 2 | Reject: no exact coords | azimuth ≠ position | Wobble pin + `?` · strikethrough / `rejected.py` pattern | — |
| 3 | Reject: off-screen hazard | Off-screen = hazard | Baby-cry / alert **behind** user, outside FOV cone, red X | — |
| 4 | Iron Man HUD pivot | Iron Man HUD | Head-relative panel sketch + **D1/D3** montage 3s each | broll |
| 5 | Azimuth computed, not shown | Azimuth: computed, not shown | Pipeline inset — UI branch grayed | — |
| 6 | Spatial caveat + honesty | Viz only · Swift app | `honesty_card` — spatial demoed · HEAD caveat · Unity explainers | optional `immersive_caveat.swift` |

### Reuse

- `rejected.py` — acts 2–3 (ghost path, strikethrough, reason chips)
- `components/honesty_card.py` — act 6 (like ch 2 act 6, ch 5 act 4)
- `broll.py` — `D1`, `D3` in act 4
- `components/workflow.py` or `pipeline.py` — act 5 grayed branch
- `components/fork.py` — optional act 1–4 transition (pins path vs HUD path)

### Unity note

SCENE-PLAN lists `AzimuthRays.unity` / `SpatialCaptionRoom.unity`. **For this agent pass: Manim diagrams only**, with on-screen honesty that Unity clips are explainers. Do not block on Unity builds.

### Deliverables ch 7

- [ ] `vo/scene7.md` (pull narration from `SCRIPT.md` ch 7 into VO seeds + PLAY CHECKLISTs)
- [ ] `scene7_act{1…6}.py` + `scene7_full.py`
- [ ] `components/hud_pivot.py` (or split `directional_pins.py` + reuse `honesty_card`)
- [ ] `-ql` all acts + `Scene7Full` preview
- [ ] Frame QA pass per act
- [ ] **Do not** 4K until user asks

---

## Workflow per chapter (execute in order)

```
1. Write vo/sceneN.md — story arc, act map, per-act VO seed + PLAY CHECKLIST
2. Create code_snippets/*.swift if needed
3. Create components/<story>.py using body_text + layout only
4. Create sceneN_actM.py from _TEMPLATE_act.py
5. Create sceneN_full.py (ENABLED_ACTS)
6. For each act:
   a. manim -ql SceneNActMLayout
   b. extract_act_frames.py → vision QA → fix
   c. manim -ql SceneNActM → re-extract if needed
7. manim -ql SceneNFull
8. Report to user: preview paths, act count, measured -ql duration, layout QA status
```

**Do not ask user to QA:** clipping, centering, overlap, kerning, tiny text.

---

## Quality reference (what “done” looks like)

- VO doc matches [`vo/scene4.md`](Aura/design-video/vo/scene4.md) / [`vo/scene5.md`](Aura/design-video/vo/scene5.md) structure
- Acts match [`scene5_act1.py`](Aura/design-video/aura_manim/scenes/scene5_act1.py) pattern (`play_actM`, Layout scene, 5.5s wait)
- Diagrams centered (`fit_center`), L→R flow, no glued words
- Honesty beats sourced from `HACKATHON-STORY.md` — no overselling spatial/Unity

---

## Suggested first message to agent

> Build **Chapter 6** first (all acts + `scene6_full.py` + `vo/scene6.md`), pass layout QA, then **Chapter 7** the same way. Manim only for ch 7 spatial beats. Follow AGENTS.md and MANIM-STANDARDS.md strictly. Ch 0–5 are frozen.

## PROMPT END
