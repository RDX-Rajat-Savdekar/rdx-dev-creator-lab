# Chapter 6 — MainActor bridge

> **YouTube chapter:** *MainActor bridge*  
> **Total duration:** `0:27.0` (27.0 s measured · `-ql`) · **SCENE-PLAN target:** `8:55` → `9:55` (~60 s)  
> **VO status:** draft (read-aloud pending) · **Measured:** 27.0 s — extend waits after read-aloud  
> **Preview:** `manim -ql scenes/scene6_full.py Scene6Full`  
> **layout QA:** pass (2026-07-03)

**Source acts:** `aura_manim/scenes/scene6_act{1…3}.py`  
**Script seed:** [`SCRIPT.md`](../SCRIPT.md) Chapter 6 (outline) · [`HACKATHON-STORY.md`](../HACKATHON-STORY.md) MainActor bridge  
**Prev chapter:** [`scene5.md`](scene5.md) — texture HUD vs 90 Hz (concat ✅)

---

## Story arc

Apple's speech and sound classifiers call back on **background threads**. SwiftUI state marked `@Published` must mutate on the **MainActor** — otherwise you get data races and missed UI updates.

We bridge with `Task { @MainActor in ... }` around caption mutations. The **realtime tap** from chapter 3 stays untouched; only the UI hop crosses threads safely.

Act 3 ties it to the product: captions refresh on main while analysis keeps streaming.

---

## Locked decisions (2026-07-03)

| Question | Decision |
|----------|----------|
| Act count | **3 acts** — two lanes → Swift bridge → caption payoff |
| Lane idiom | Extend ch 3 `thread_lane` pattern — different labels, same vertical dispatch |
| Act 2 layout | **`split_layout`** — rule diagram top, `mainactor_bridge.swift` bottom |
| B-roll | **D1** optional 3 s in act 3 (live captions proof) |
| Unity | **None** |

---

## Act map

| Act | SCENE-PLAN beat | Target | On-screen label | File |
|-----|-----------------|--------|-----------------|------|
| 1 | ML callback off main thread | ~15 s | Background thread · ML result | `scene6_act1.py` |
| 2 | `@Published` mutation rule | ~15 s | MainActor · UI updates | `scene6_act2.py` |
| 3 | Why it matters for captions | ~15 s | Captions update on main | `scene6_act3.py` |

---

## Act 1 — ML callback off main thread

**VO seed:** *Speech and sound delegates fire on background threads — not on MainActor. ML results arrive while the tap keeps running on the audio thread from chapter three.*

**What the animation shows:** Two-lane diagram. Top — muted callback ticks labeled **ML delegate · background thread**. Arrow down with **Task { @MainActor in }**. Bottom — accent UI blocks labeled **MainActor · @Published UI**. Footnote: tap unchanged.

```
PLAY CHECKLIST — Scene6Act1
  1      mainactor_lane_diagram() fades in
  2      Top lane: background ML delegate ticks
  3      Vertical arrow + Task { @MainActor in } chip
  4      Bottom lane: MainActor UI blocks
  5      Footnote: tap stays on audio thread
  6      Bottom label: Background thread · ML result
```

**Component:** `components/mainactor_bridge.py` → `mainactor_lane_diagram()`

---

## Act 2 — `@Published` mutation rule

**VO seed:** *Any `@Published` property that drives SwiftUI must mutate on MainActor. We wrap caption updates in `Task { @MainActor in }` so the panel refreshes safely.*

**What the animation shows:** Top pane — compact **L→R** rule: ML result → thread hop → `@Published captionText`. Bottom pane — `mainactor_bridge.swift` with `@MainActor` block highlighted.

```
PLAY CHECKLIST — Scene6Act2
  1      split_layout: published_rule_diagram() in visual pane
  2      Three stages LEFT → RIGHT with arrows after layout
  3      Note below diagram: @Published on MainActor
  4      Code pane: mainactor_bridge.swift fades in
  5      Highlight Task { @MainActor in } block
  6      Bottom label: MainActor · UI updates
```

**Snippet:** `code_snippets/mainactor_bridge.swift`  
**Component:** `published_rule_diagram()`

---

## Act 3 — Captions update on main

**VO seed:** *That's why live captions can refresh on screen while classification keeps streaming — UI work hops to main; the tap never waits.*

**What the animation shows:** Caption update inset (**transcript chunk → caption panel**). Optional **D1** b-roll (~3 s) showing live captions on device.

```
PLAY CHECKLIST — Scene6Act3
  1      caption_update_inset() fades in
  2      Header: Captions update on main thread
  3      L→R: ML callback chunk → MainActor UI panel
  4      Arrow after layout
  5      Fade out → D1 b-roll ~3 s (optional proof)
  6      Bottom label: Captions update on main
```

**Component:** `caption_update_inset()` · **B-roll:** `D1_live-en-captions.mp4`

---

## Toolkit

| Module | Role |
|--------|------|
| `components/mainactor_bridge.py` | Two-lane diagram, published rule, caption inset |
| `components/split_layout.py` | Act 2 visual + Swift |
| `components/thread_lane.py` | Pattern reference (ch 3 — do not edit) |
| `code_snippets/mainactor_bridge.swift` | `@MainActor` caption mutation |

---

## Transcript / test notes

- **Act 1:** Connect back to ch 3 — tap vs UI thread split.
- **Act 2:** Say `@Published` and `MainActor` once each, clearly.
- **Act 3:** Tie to visible caption refresh; D1 is proof not oversell.

---

## Status

- [x] VO doc + PLAY CHECKLISTs
- [x] `-ql` render + layout QA per act (2026-07-03)
- [ ] VO draft + read-aloud
