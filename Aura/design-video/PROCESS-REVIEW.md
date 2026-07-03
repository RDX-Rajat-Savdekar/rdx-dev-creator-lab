# Process review — Aura design video (Manim pipeline)

> **Written:** 2026-07-03 · **Scope:** ch 0–5 shipped, layout/text bugs found late, user as repeated QA  
> **Purpose:** Honest postmortem + agent context. Read before building ch 6+ or handing work to another agent.

---

## Executive summary

The **chapter architecture is sound** (`play_actN` → `sceneN_full` → per-act 4K → concat → `vo/sceneN.md`). The **failure mode is quality gates**: agents ship motion and copy without **looking at frames**, **reuse typography inconsistently**, and **patch layout reactively** instead of composing from shared primitives. You end up as the visual QA loop—screenshot → describe → fix → screenshot again.

That is fixable without throwing away components. The gap is **enforcement**: one standards doc, one text API, one layout API, and a **mandatory post-render frame review** before you see output.

---

## What we are doing right

| Practice | Why it works |
|----------|----------------|
| **One act per file** + `play_actM(scene, state)` | Re-render one beat; concat stays stable |
| **`sceneN_full.py` at `-ql`** | Fast chapter timing without 4K cost |
| **`split_layout.py`** | Visual + Swift panes don’t overlap (ch 3–5) |
| **`code_panel.py` + `code_snippets/`** | Ground-truth Swift on screen |
| **`broll.py`** | Demo proof in Manim without Resolve round-trip |
| **`vo/sceneN.md` + `build_act_timestamps.py`** | Measured truth beats SCENE-PLAN guesses |
| **`review.plop()` + `SceneNActMLayout`** | Exists for layout—but underused by agents |
| **Chapter-specific components** (`workflow`, `segmentation`, `texture_bake`) | Right level of reuse for story beats |

---

## What we are doing wrong (critical)

### 1. No visual QA — you are the test harness

**Symptom:** Overlap, right-edge clipping, tiny illegible text, `dumpsat` / `differentrender` kerning—all caught by **you** after preview/4K, often multiple rounds per act.

**Root cause:** Agents treat “render succeeded” as “done.” Manim gives free artifacts:

```
aura_manim/media/videos/sceneN_actM/{480p15|2160p60}/partial_movie_files/SceneNActM/*.mp4
```

Each `self.play` / `self.wait` produces a partial clip. **Nobody inspects them** before handoff.

**What should happen after first `-ql` render of an act:**

1. Extract 1–3 stills from partials (hold frames, last frame of each animation).
2. Agent **reads the PNGs** (vision) and checks a short checklist (below).
3. Fix layout/text in code; re-render; repeat until clean.
4. Only then: `SceneNFull`, then ask you for narrative/VO feedback—not pixel nitpicks.

**You should not have to send screenshots for:** clipping, centering, overlap, unreadable font size, missing spaces in `Text`.

---

### 2. Components exist but agents bypass the standards layer

**Symptom:** Same text bugs every chapter (gaps, overlap, crush-scale, wrong anchor).

**Evidence from ch 4–5:**

| Intended standard | What actually happened |
|-------------------|------------------------|
| `typography.py` — `subtext`, `caption`, `chip_label` | ch 4–5 added **private** `_readable_text` / `_panel_text` with `disable_ligatures=True` |
| `typography.py` doc: “don’t use MUTED for readable copy” | Still mixed; some labels use raw `Text(...)` |
| `LEARNING.md` typography section | Written 2026-07-02; **not applied** when ch 4–5 were generated |
| `split_layout.place_visual_pane()` | Centers in **pane**, not frame; diagrams inside can still be **left-anchored at ORIGIN** → **right bias** |
| `fit_center()` in `components/fit.py` | Added **reactively** in ch 4–5 after user reports—not used in ch 0–3 |

**Diagnosis:** Components are **optional suggestions**, not a **required API**. `components/__init__.py` is empty. No linter, no agent rule, no “forbidden patterns” list.

---

### 3. Layout anti-patterns repeat because they were never written down

These caused real bugs in ch 4–5:

| Anti-pattern | Effect | Fix (now in code, not in standards) |
|--------------|--------|--------------------------------------|
| `mob.move_to(ORIGIN)` then `other.next_to(mob, RIGHT)` | Group grows **right** from center; clips right edge | Build with `VGroup(...).arrange(RIGHT)` then `fit_center()` |
| Arrow created **before** final positions | Arrow points wrong way / wrong attach | Layout first, arrow last |
| `Text(..., width=4.2)` then `scale(0.88)` on group | Kerning collapse (`gettranscription`) | Never scale readable `Text`; size plate instead |
| Manual `\n` in some cards, `width=` squeeze in others | Inconsistent gaps act to act | One `body_text()` API |
| `caption()` for multi-word titles without ligature disable | `differentrender` | `body_text()` or split lines explicitly |

**These should be in a single `MANIM-LAYOUT.md`**, not re-learned per chapter.

---

### 4. Component sprawl vs component discipline

**Current `components/` (17 files):** mix of **primitives** (`workflow`, `labels`, `fit`) and **chapter visuals** (`segmentation`, `texture_bake`, `classifier_gate`).

**Not inherently bad**—if chapter files **only compose primitives**.

**Actually bad:**

- **`pipeline.py` vs `pipeline_stub.py`** — unclear contract; agents pick arbitrarily.
- **`fit.py`** — 12 lines, correct abstraction, arrived **late**; should live in `layout.py` with `flow_lr`, `card`, `tag_above`.
- **Duplicate text helpers** in `segmentation.py` and `texture_bake.py` instead of extending `typography.py`.
- **`scene0_problem_REFERENCE.py`** — 500+ lines reference; risk of copy-paste drift.
- **Reactive one-offs** that never merge up: each bug fix adds a local helper instead of fixing the shared layer.

**Rule of thumb:**

- **New file OK** → new **story visual** reused across acts (e.g. `segmentation.py`).
- **New file NOT OK** → fixing text spacing, centering, or arrows (belongs in `typography.py` / `layout.py`).

---

### 5. Process docs lag reality

| Doc | Issue |
|-----|--------|
| `vo/VO-WORKFLOW.md` ch index | Still showed ch 4–5 as “`-ql` preview” after 4K concat |
| `README.md` toolkit table | Missing `split_layout`, `fit`, `segmentation`, `texture_bake` |
| `LEARNING.md` | No entry for `fit_center`, `disable_ligatures`, L→R flow convention |
| VO depth | ch 4–5 VO docs were thin until **you** asked; should be default at act creation |

**Symptom:** Agents read stale docs and skip steps that exist on paper only.

---

### 6. Pacing validated too late — **resolved (visual-first)**

| Chapter | Measured | SCENE-PLAN target | Gap |
|---------|----------|-------------------|-----|
| 2 | 55.5 s | ~90 s | −35 s |
| 3 | 56.8 s | ~110 s | −53 s |
| 4 | 36.2 s | ~90 s | −54 s |
| 5 | 34.2 s | ~90 s | −56 s |

**Decision (2026-07-03):** Short first renders are **OK** before VO is recorded. Workflow:

1. Ship visuals with default `scene.wait(5.5)` per act.
2. Draft VO in `vo/sceneN.md` while watching concat (transcript emerges from read-aloud).
3. Read aloud → note gaps → **`tools/adjust_waits.py`** bulk add/trim holds.
4. Re-render acts → re-concat.

Script-first (write full VO before Manim) is optional for ch 6+; not required.

**Tool:** `python Aura/design-video/tools/adjust_waits.py --chapter N --show|--add|--set`

---

### 7. `SceneNActMLayout` exists but is not a gate

Every act file has a `Layout` scene with `plop()`—**good for humans**, ignored in agent workflow.

Agents jump to `play_actN` + full render. Layout scenes are the right place to validate **static composition** without animation time cost.

**Should be mandatory:** `-ql SceneNActMLayout` → frame extract → pass checklist → then motion.

---

## The partial_movie_files opportunity (your idea — expanded)

Manim already writes debug clips. Use them as **automated layout review input**.

### Suggested tool: `tools/extract_act_frames.py`

```bash
# After first -ql render of an act
python Aura/design-video/tools/extract_act_frames.py \
  --scene scene4_act3 \
  --quality 480p15 \
  --pick last   # last frame per partial (hold state)
# → writes vo/review_frames/scene4_act3/*.png
```

Agent workflow:

1. Render act `-ql`
2. Run extractor
3. Open PNGs (vision) — run checklist
4. Edit component/scene
5. Re-render until pass
6. Mark in `vo/sceneN.md`: `layout QA: pass (2026-07-03)`

**Optional later:** scriptable bounds check (content bbox vs frame width)—fragile with Manim, but frame vision is reliable **today**.

### Frame checklist (agent must pass before user review)

**Layout**

- [ ] No mobject clipped by frame edge (left/right/top; reserve bottom for `on_screen_label`)
- [ ] Diagram **visually centered** (not growing right from ORIGIN)
- [ ] Arrows point **left → right** for data flow unless story says otherwise
- [ ] No text-on-text overlap
- [ ] Split-layout: visual pane clear of code pane and bottom label

**Typography**

- [ ] All readable sentences via `typography.body_text()` (see below)—not raw `Text`
- [ ] No word appears glued to the next (`dumpsat`, `differentrender`)
- [ ] No paragraph scaled below ~14pt equivalent at 1080p preview
- [ ] Multi-line cards use explicit breaks or natural wrap—not `width=` squeeze

**Composition**

- [ ] Tags (`formattedString → UI`) aligned to **their** panel, not floating
- [ ] Compare/before-after: both sides readable at same scale order of magnitude

---

## Standardization proposal (for agents)

### A. Extend `typography.py` — single text API

Add and **require** (no private `_readable_text` in chapter files):

```python
def body_text(text, *, font_size=16, color=WHITE_TEXT, width=None) -> Text:
    """Readable copy on dark panels. disable_ligatures always on."""
    ...

def caption_line(text) -> Text:
    """Short tag above a panel; same spacing rules."""
    ...
```

Migrate `segmentation.py` / `texture_bake.py` private helpers → delete duplicates.

### B. Add `components/layout.py` — single layout API

Merge `fit.py` into:

```python
def fit_center(group, *, margin=1.0) -> Mobject: ...
def flow_lr(*parts, buff=0.6, arrow=False) -> VGroup:
    """Arrange left→right, optional arrows between, then fit_center."""
    ...
def labeled_card(text, *, tag: str, stroke=ACCENT) -> VGroup: ...
```

**Rule:** Any diagram wider than one card uses `flow_lr` + `fit_center`. **Forbidden:** `move_to(ORIGIN)` + chain of `next_to(RIGHT)` without final `fit_center`.

### C. Component tiers (document in README)

| Tier | Examples | When to create |
|------|----------|----------------|
| **Primitives** | `typography`, `layout`, `labels`, `theme`, `code_panel`, `broll` | Never fork; extend |
| **Patterns** | `split_layout`, `workflow`, `honesty_card`, `rejected` | Cross-chapter UI patterns |
| **Story** | `segmentation`, `texture_bake`, `thread_lane` | One chapter arc; compose primitives only |

### D. Agent rule file

Create **`.cursor/rules/aura-manim.md`** (or `Aura/design-video/AGENTS.md`) with:

1. Render `-ql` → extract frames → vision QA → fix → re-render
2. Never raw `Text` for on-screen readable copy
3. Never scale groups containing `Text`
4. L→R flow default; arrow after layout
5. `vo/sceneN.md` PLAY CHECKLIST + VO seed **at act creation**, not after user asks
6. Run `SceneNActMLayout` before `SceneNActM` when touching composition

### E. Consolidate duplicates (tech debt backlog)

| Item | Action |
|------|--------|
| `_readable_text` / `_panel_text` | → `typography.body_text` |
| `fit.py` | → `layout.py` |
| `pipeline` vs `pipeline_stub` | Document or merge |
| `VO-WORKFLOW` ch index | Keep in sync when concat lands |
| `LEARNING.md` | Add layout + ligature entries |

---

## One-off Python files — good or bad?

| Verdict | Examples |
|---------|----------|
| **Good** | `broll.py`, `code_panel.py`, `review.py`, `build_act_timestamps.py` — clear boundary, reused |
| **Good if composed** | `segmentation.py`, `texture_bake.py` — chapter story, should not redefine text/layout |
| **Warning** | `fit.py` — right idea, too late, too small alone |
| **Bad pattern** | Private `_foo_text()` in every new component — copy-paste of fixes |
| **Bad** | Growing `scene0_problem_REFERENCE.py` as source of truth |

**Principle:** A one-off is fine for **exploration** (`Layout` plop scenes). Before 4K, one-offs must **merge up** or they become debt (ch 4–5 text helpers are the current example).

---

## Revised per-act workflow (target state)

```
1. vo/sceneN.md     — act map + PLAY CHECKLIST + VO seed (draft)
2. components/      — compose typography + layout primitives; story module if needed
3. sceneN_actM.py   — play_actM only; no inline layout hacks
4. -ql SceneNActMLayout → extract frames → agent vision QA (checklist)
5. -ql SceneNActM   — motion; re-extract holds if composition animates
6. -ql SceneNFull  — chapter timing
7. User review      — story, pacing, VO tone (not pixels)
8. -qk per act → concat → build_act_timestamps → read-aloud → extend waits
```

**Your role shifts** from pixel QA at step 4 to narrative QA at step 7.

---

## Bugs we found in ch 4–5 (keep as regression memory)

| Bug | Cause | Fix applied |
|-----|-------|-------------|
| Utterance + chips overlapping | Vertical stack shared coordinates | L→R split preview |
| `formattedString` wall tiny | `width` + group scale | Compact copy, no crush-scale |
| `gettranscription`, `dumpsat` | `Text` width squeeze / scale | `disable_ligatures`, no width on body |
| `differentrender` | `caption()` without ligature disable | `_panel_text` / split title lines |
| Right-edge clip | ORIGIN anchor + extend right | `fit_center` after `arrange` |
| Arrow wrong direction | Arrow before layout | Layout then arrow |
| `re-layout` over 90Hz box | `buff` too small | Increase vertical buff |
| Right-biased compare panels | No center pass | `fit_center` on whole diagram |

**If standards + frame QA existed, most would not have reached you.**

---

## Bugs / learnings from ch 6–7 (keep as regression memory)

| Issue | Cause | Fix applied |
|-------|-------|-------------|
| Arrow tips “big big” | `get_tip().scale(1.85)` after layout | Remove tip scale; tune `tip_length` + ratio + spacing in `arrow_between()` |
| Arrows too small (first pass) | Default Manim tip on short spans | Moderate `tip_length=0.16–0.2`, ratio ~0.28–0.38 — not tip scale |
| FOV cone wrong anchor | Pivot at head **center** | Pivot at **`head[0].get_right()`** · large `HUD_FOV_RADIUS` (~3.45) |
| HUD panel overlaps FOV arc | Panel at default radius | Panel at ~84% radius; act 4 **scale-down settle** (0.82) after slide |
| `extract_act_frames` crash | EOF seek on partials &lt; 2 s | Use mid-frame for short clips |
| ch 7 act 4 loved by user | — | Keep slide + scale settle + tag fade pattern as reference beat |

**Ch 8–9:** video ends at chapter 9 (~12:45 total). No chapter 10 in SCENE-PLAN.

---

## Immediate next steps (recommended order)

1. ~~**This file** — keep as agent context; link from `README.md`~~ ✅
2. ~~**`typography.body_text()`**~~ ✅ — ch 6+; ch 4–5 frozen
3. ~~**`components/layout.py`**~~ ✅ — `fit.py` re-exports for compat
4. ~~**`tools/extract_act_frames.py`**~~ ✅
5. ~~**`tools/adjust_waits.py`**~~ ✅
6. ~~**`AGENTS.md` + `.cursor/rules/aura-manim.mdc`**~~ ✅
7. ~~**`MANIM-STANDARDS.md`**~~ ✅
8. ~~**Update `LEARNING.md`**~~ ✅
9. ~~**Sync `VO-WORKFLOW.md`**~~ ✅

**Start ch 6** using `_TEMPLATE_act.py`, `MANIM-STANDARDS.md`, frame QA loop.

**Ch 6–7 shipped (2026-07-03).** Next: ch 8 Scale + ch 9 Outro using same pipeline.

---

## Closing (blunt)

We are **good at shipping chapters quickly** and **bad at shipping them right the first time**. The component library is not the problem—**discipline and visual verification** are. Manim code is not inspectable like a web page; **partial_movie_files are the closest thing to a unit test for layout**, and we ignore them.

Fixing that is higher leverage than adding more `components/*.py` files.

---

## Related docs

| File | Role |
|------|------|
| [`AGENTS.md`](AGENTS.md) | Agent instructions (ch 6+) |
| [`MANIM-STANDARDS.md`](MANIM-STANDARDS.md) | APIs, checklist, anti-patterns |
| [`README.md`](README.md) | Phase 0–5 process |
| [`LEARNING.md`](LEARNING.md) | Manim concepts |
| [`vo/VO-WORKFLOW.md`](vo/VO-WORKFLOW.md) | VO + concat SOP |
| [`tools/adjust_waits.py`](tools/adjust_waits.py) | Bulk VO hold adjustment |
| [`tools/extract_act_frames.py`](tools/extract_act_frames.py) | Layout frame QA |
| [`typography.py`](aura_manim/typography.py) | `body_text`, `caption_line` |
| [`components/layout.py`](aura_manim/components/layout.py) | `fit_center`, `flow_lr` |
| [`components/split_layout.py`](aura_manim/components/split_layout.py) | Two-pane pattern |
| [`review.py`](aura_manim/review.py) | `plop()` for manual layout |
