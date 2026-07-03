# Chapter 5 — Texture HUD vs 90 Hz

> **YouTube chapter:** *Texture HUD vs 90 Hz*  
> **Render:** [`output/scene5_chapter5_2160p60.mp4`](../output/scene5_chapter5_2160p60.mp4)  
> **Total duration:** `0:34.2` (34.2 s measured) · **SCENE-PLAN target:** `7:25` → `8:55` (~90 s)  
> **VO status:** draft (read-aloud pending) · **Measured:** 34.2 s — **add ~56 s wait** after read-aloud or trim SCRIPT  
> **Preview:** `manim -ql scenes/scene5_full.py Scene5Full`

**Source acts:** `aura_manim/scenes/scene5_act{1…4}.py`  
**Script seed:** [`SCRIPT.md`](../SCRIPT.md) Chapter 5 (TBD)  
**Prev chapter:** [`scene4.md`](scene4.md) — segmentation (concat ✅)

---

## Act timeline (2160p60 · 2026-07-03)

| Act | Start | End | Dur | On-screen label | Manim file |
|-----|-------|-----|-----|-----------------|------------|
| 1 | 0:00.0 | 0:08.1 | 8.1s | 90 Hz · layout every frame | `scene5_act1.py` |
| 2 | 0:08.1 | 0:17.7 | 9.6s | Texture bake · 100 ms | `scene5_act2.py` |
| 3 | 0:17.7 | 0:26.7 | 9.0s | Jitter vs baked quad | `scene5_act3.py` |
| 4 | 0:26.7 | 0:34.2 | 7.5s | 2D HUD shipped in demo | `scene5_act4.py` |

**Concat:** [`output/scene5_concat.txt`](../output/scene5_concat.txt)

---

## Story arc

Readable captions still need to **render** without stealing frame budget. **ViewAttachment** in RealityKit re-layouts SwiftUI every frame — that couples UI work to the **90 Hz** render loop. We **reject** that path.

Instead: bake captions **off-screen** — SwiftUI → texture snapshot → draw on a simple **RK quad** in world space, with **100 ms debounce** so we don't rebake on every partial transcript update.

Side-by-side: **jitter** (per-frame layout) vs **stable baked texture**. Honesty card: what actually shipped in the demo.

*Unity jitter clip deferred — Manim comparison stands in for SCENE-PLAN Unity beat.*

---

## Locked decisions (2026-07-03)

| Question | Decision |
|----------|----------|
| Act count | **4 acts** — rejected path → bake pipeline → compare → honesty |
| Flow direction | All diagrams **LEFT → RIGHT**; arrows drawn after layout |
| Compare layout | Jitter panel **LEFT** → arrow → baked panel **RIGHT** |
| Debounce | **100 ms** chip under texture stage |
| Unity | **None** this chapter |

---

## Act map

| Act | SCENE-PLAN beat | Target | On-screen label | File |
|-----|-----------------|--------|-----------------|------|
| 1 | 90 Hz ViewAttachment | ~15 s | 90 Hz · layout every frame | `scene5_act1.py` |
| 2 | Texture bake pipeline | ~15 s | Texture bake · 100 ms | `scene5_act2.py` |
| 3 | Jitter vs baked | ~15 s | Jitter vs baked quad | `scene5_act3.py` |
| 4 | Honesty card | ~15 s | 2D HUD shipped in demo | `scene5_act4.py` |

---

## Act 1 — 90 Hz loop (rejected)

**VO seed:** *RealityKit runs at 90 Hz. Hooking captions via ViewAttachment means SwiftUI re-layout on every frame — layout cost tied directly to the render loop. We marked this path rejected.*

**What the animation shows:** Circle labeled **90 Hz** → arrow **L→R** → **ViewAttachment** box with `re-layout each frame` warning above. Red **cross** over attachment. Note below: layout cost tied to render loop.

```
PLAY CHECKLIST — Scene5Act1
  1      hz_loop_diagram() fades in
  2      90 Hz circle LEFT → arrow → ViewAttachment RIGHT
  3      Warning label above arrow: re-layout each frame
  4      Red cross appears on ViewAttachment
  5      Subtext below diagram
  6      Bottom label: 90 Hz · layout every frame
```

**Component:** `components/texture_bake.py` → `hz_loop_diagram()`

---

## Act 2 — Texture bake pipeline

**VO seed:** *Off-screen bake: render captions in SwiftUI, snapshot to a texture, composite on a lightweight RK quad in the scene. Debounce rebakes to 100 milliseconds so partial transcripts don't thrash the GPU.*

**What the animation shows:** Top pane — **SwiftUI** → **texture** → **RK quad** pipeline (all **L→R**). **100 ms debounce** chip under texture stage. Bottom pane — `debounce_texture.swift`.

```
PLAY CHECKLIST — Scene5Act2
  1      split_layout: bake_pipeline_diagram() in visual pane
  2      Header: Off-screen bake path
  3      Three stages LEFT → RIGHT with connecting arrows
  4      Debounce chip under texture stage
  5      Code pane: debounce_texture.swift + highlight
  6      Bottom label: Texture bake · 100 ms
```

**Snippet:** `code_snippets/debounce_texture.swift`  
**Component:** `bake_pipeline_diagram()`

---

## Act 3 — Jitter vs baked quad

**VO seed:** *Same caption content — different render path. Per-frame layout jitters the HUD; the baked texture stays pinned. Watch the left panel wobble while the right stays stable.*

**What the animation shows:** Two-line title (`Same captions` / `different render path`). **LEFT** panel — warn stroke, `per-frame layout` tag, content shifts jitter animation. **Arrow L→R**. **RIGHT** panel — green stroke, `baked texture` tag, stable.

```
PLAY CHECKLIST — Scene5Act3
  1      jitter_vs_bake() fades in
  2      Title above panels (two lines — no cramped middle-dot spacing)
  3      LEFT: jitter panel (warn border)
  4      Arrow LEFT → RIGHT between panels
  5      RIGHT: baked panel (green border)
  6      Jitter wobble animation on left content only
  7      Indicate stable right panel
  8      Bottom label: Jitter vs baked quad
```

**Component:** `jitter_vs_bake()`

---

## Act 4 — Honesty card

**VO seed:** *What we actually shipped in the demo: a 2D HUD overlay — not the full world-space texture path. Honest about the gap between prototype and production.*

**What the animation shows:** `honesty_card()` with shipped vs aspirational bullets (from act file).

```
PLAY CHECKLIST — Scene5Act4
  1      honesty_card fades in
  2      Read headline + bullet contrast (shipped vs planned)
  3      Bottom label: 2D HUD shipped in demo
```

**Component:** `components/honesty_card.py`

---

## Toolkit

| Module | Role |
|--------|------|
| `components/texture_bake.py` | 90 Hz loop, bake pipeline, jitter compare |
| `components/split_layout.py` | Act 2 visual + Swift |
| `code_snippets/debounce_texture.swift` | 100 ms debounce |
| `components/honesty_card.py` | Act 4 shipped vs planned |

---

## Transcript / test notes

- **Act 1:** Emphasize **rejected** when cross appears; don't oversell ViewAttachment.
- **Act 2:** Trace pipeline L→R with cursor; call out **100 ms** debounce.
- **Act 3:** Narrate during jitter wobble — "left jitters, right stable."
- **Act 4:** Tone shift to honesty — demo used 2D HUD.
- **Spacing QA:** All panel text uses `disable_ligatures=True`; compare title is two lines.

---

## Status

- [x] Code + layout fixes (L→R flow, title spacing, arrow after layout)
- [x] `-qk` per act → concat → measured timestamps
- [ ] VO draft + read-aloud
