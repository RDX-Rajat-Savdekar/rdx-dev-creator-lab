# Chapter 7 — Directional pins → Iron Man HUD

> **YouTube chapter:** *Iron Man HUD*  
> **Total duration:** `0:53.1` (53.1 s measured · `-ql`) · **SCENE-PLAN target:** `9:55` → `11:25` (~90 s)  
> **VO status:** draft (read-aloud pending) · **Measured:** 53.1 s — extend waits after read-aloud  
> **Preview:** `manim -ql scenes/scene7_full.py Scene7Full`  
> **layout QA:** pass (2026-07-03)

**Source acts:** `aura_manim/scenes/scene7_act{1…6}.py`  
**Script seed:** [`SCRIPT.md`](../SCRIPT.md) Chapter 7 (✅ draft) · [`HACKATHON-STORY.md`](../HACKATHON-STORY.md) rejected #6  
**Prev chapter:** [`scene6.md`](scene6.md) — MainActor bridge

---

## Story arc

Early hackathon hours: **world-locked sound pins** — markers anchored where audio seemed to originate. Two rejection reasons:

1. **No exact world coordinates** — mic gives azimuth, not a reliable 3D anchor (`azimuth ≠ position`).
2. **Off-screen hazard** — urgent sounds behind the user may never enter FOV (accessibility failure).

Pivot: **Iron Man–style HUD** — head-relative panel always in view (what the 2D demo ships). Azimuth still computed in DSP, not shown as directional UI. Spatial prototype demoed with **HEAD wiring caveat**. Unity clips = explainers only.

**VO checkpoint:** Name **both** rejection reasons before celebrating HUD.

---

## Locked decisions (2026-07-03)

| Question | Decision |
|----------|----------|
| Act count | **6 acts** — try → reject ×2 → HUD → azimuth honesty → spatial caveat |
| Spatial viz | **Manim only** this pass — label Unity deferred honestly |
| Rejection acts | `rejected.py` cross/strike + `hud_pivot.py` reason diagrams |
| B-roll | **D1 + D3** montage in act 4 (~3 s each) |
| Unity | **None** in render — honesty card act 6 |

---

## Act map

| Act | SCENE-PLAN beat | Target | On-screen label | File |
|-----|-----------------|--------|-----------------|------|
| 1 | Tried world-locked pins | ~15 s | Tried: world-locked pins | `scene7_act1.py` |
| 2 | Reject: no exact coords | ~15 s | azimuth ≠ position | `scene7_act2.py` |
| 3 | Reject: off-screen hazard | ~15 s | Off-screen = hazard | `scene7_act3.py` |
| 4 | Iron Man HUD pivot | ~15 s | Iron Man HUD | `scene7_act4.py` |
| 5 | Azimuth computed, not shown | ~15 s | Azimuth: computed, not shown | `scene7_act5.py` |
| 6 | Spatial caveat + honesty | ~15 s | Viz only · Swift app | `scene7_act6.py` |

---

## Act 1 — Tried world-locked pins

**VO seed:** *Early on we tried pinning each sound to the direction it came from — markers in the world where audio seemed to originate.*

**What the animation shows:** Head icon center, rays to labeled pins around the room. Honesty subtext: Manim stands in for Unity `AzimuthRays`.

```
PLAY CHECKLIST — Scene7Act1
  1      world_locked_pins_diagram() fades in
  2      Head center + rays to 5 pin markers
  3      Pin labels: siren, speech, clap, whisper, alert
  4      Subtext: Manim viz · Unity deferred
  5      Bottom label: Tried: world-locked pins
```

---

## Act 2 — Reject: no exact coords

**VO seed:** *First problem: Vision Pro gives direction from the mic, not an exact coordinate. The pin is guesswork — it drifts and feels wrong.*

```
PLAY CHECKLIST — Scene7Act2
  1      azimuth_reject_diagram() fades in
  2      Wobble pin + ? marker
  3      Label: azimuth ≠ position
  4      Red strikethrough on pin
  5      Bottom label: azimuth ≠ position
```

---

## Act 3 — Reject: off-screen hazard

**VO seed:** *Second — for accessibility — an urgent sound behind you might never enter your field of view. A baby crying pinned outside your gaze is a missed alert.*

```
PLAY CHECKLIST — Scene7Act3
  1      offscreen_hazard_diagram() fades in
  2      FOV cone in front of head
  3      Alert icon behind user, outside cone
  4      Red X on off-screen alert
  5      Bottom label: Off-screen = hazard
```

---

## Act 4 — Iron Man HUD pivot

**VO seed:** *So we pivoted to an Iron Man–style HUD — captions and sound labels on a panel that stays in view. Head-relative, not world-hunted. That's what the demo shows.*

```
PLAY CHECKLIST — Scene7Act4
  1      iron_man_hud_diagram() fades in
  2      Head-relative panel with sample captions
  3      Tag: head-relative · always in view
  4      Fade out → D1 + D3 montage ~3 s each
  5      Bottom label: Iron Man HUD
```

**B-roll:** `D1_live-en-captions.mp4`, `D3_whisper-detected.mp4`

---

## Act 5 — Azimuth computed, not shown

**VO seed:** *We still compute azimuth in the audio path for analysis, but we don't ship directional markers in the UI.*

```
PLAY CHECKLIST — Scene7Act5
  1      azimuth_grayed_pipeline() fades in
  2      L→R: azimuth computed → UI branch grayed
  3      Strikethrough on directional UI card
  4      Bottom label: Azimuth: computed, not shown
```

---

## Act 6 — Spatial caveat + honesty

**VO seed:** *Separately we built a spatial HUD prototype — texture-baked SwiftUI in RealityKit — demoed on video. Honest caveat: committed HEAD doesn't wire ImmersiveView into the app entry. Unity clips here are explainers only — Aura ships in Swift.*

```
PLAY CHECKLIST — Scene7Act6
  1      honesty_card fades in (spatial demoed · HEAD caveat)
  2      Second line: Unity clips = viz explainers only
  3      Bottom label: Viz only · Swift app
```

**Optional snippet:** `code_snippets/immersive_caveat.swift`

---

## Toolkit

| Module | Role |
|--------|------|
| `components/hud_pivot.py` | Pins, rejections, HUD, azimuth inset |
| `components/honesty_card.py` | Act 6 shipped vs caveat |
| `rejected.py` | Strike/cross patterns (reference) |
| `broll.py` | D1 + D3 montage act 4 |

---

## Status

- [x] VO doc + PLAY CHECKLISTs (from SCRIPT.md ch 7)
- [x] `-ql` render + layout QA per act (2026-07-03)
- [ ] VO draft + read-aloud
