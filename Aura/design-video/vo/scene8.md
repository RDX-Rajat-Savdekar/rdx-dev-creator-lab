# Chapter 8 — Scale

> **YouTube chapter:** *Scale*  
> **Total duration:** `0:25.3` (25.3 s measured · `-ql`) · **SCENE-PLAN target:** `11:25` → `12:15` (~50 s)  
> **VO status:** draft (read-aloud pending) · **Measured 4K:** 25.3 s — extend waits after read-aloud  
> **Preview:** `manim -ql scenes/scene8_full.py Scene8Full`  
> **layout QA:** pass (2026-07-03)

**Source acts:** `aura_manim/scenes/scene8_act{1…3}.py`  
**Script seed:** [`SCRIPT.md`](../SCRIPT.md) Chapter 8 · [`HACKATHON-STORY.md`](../HACKATHON-STORY.md) scale + never claim  
**Prev chapter:** [`scene7.md`](scene7.md) — Iron Man HUD (concat ✅)

---

## Story arc

Aura shipped as a **24-hour hackathon prototype** — one user, one headset, qualitative demos only. The **core on-device pipeline** could scale to a product envelope (locale CDN, observability, fleet metrics), but we **never claim** latency percentages, production user metrics, or benchmark artifacts.

Honesty beat before the outro — no victory lap on numbers we did not measure.

---

## Locked decisions (2026-07-03)

| Question | Decision |
|----------|----------|
| Act count | **3 acts** — limits → product delta → never claim stamp |
| Visual style | Cards + L→R arch compare + red stamp (Manim only) |
| Swift / B-roll | **None** |
| Unity | **None** |

---

## Act map

| Act | SCENE-PLAN beat | Target | On-screen label | File |
|-----|-----------------|--------|-----------------|------|
| 1 | Prototype limits today | ~17 s | Prototype · today | `scene8_act1.py` |
| 2 | Product would change | ~17 s | Product · would change | `scene8_act2.py` |
| 3 | Never claim list | ~16 s | Never claim | `scene8_act3.py` |

---

## Act 1 — Prototype limits today

**VO seed:** *This was a hackathon prototype — one user, one headset, no benchmarks. We demoed live captions and sound alerts qualitatively; we did not measure thermal, battery, or latency.*

**What the animation shows:** Three muted cards — **single user**, **no benchmarks**, **qualitative only** — with header *Hackathon prototype · not production* and footnote on unmeasured ops metrics.

```
PLAY CHECKLIST — Scene8Act1
  1      prototype_limits_diagram() fades in
  2      Header: Hackathon prototype · not production
  3      Three today-tagged cards in L→R flow
  4      Footnote: thermal · battery · latency — not measured
  5      Bottom label: Prototype · today
```

**Component:** `components/scale.py` → `prototype_limits_diagram()`

---

## Act 2 — Product would change

**VO seed:** *The same core pipeline could grow into a product — locale bundles on CDN, observability, multi-user fleet metrics. That is a different ops envelope, not what we shipped in twenty-four hours.*

**What the animation shows:** Dim **today** card (on-device only · single locale bundle) → arrow → accent **product would add** card (locale CDN · observability · multi-user). Footnote: same core pipeline — different ops envelope.

```
PLAY CHECKLIST — Scene8Act2
  1      product_would_change_diagram() fades in
  2      Today card dimmed left; product card accent right
  3      Arrow after layout (arrow_between)
  4      Footnote below row
  5      Bottom label: Product · would change
```

**Component:** `components/scale.py` → `product_would_change_diagram()`

---

## Act 3 — Never claim

**VO seed:** *We never claim latency percentages, production user metrics, or benchmark artifacts. The demo is proof of concept — not a performance study.*

**What the animation shows:** Red-bordered stamp listing three **never claim** lines with diagonal cross.

```
PLAY CHECKLIST — Scene8Act3
  1      never_claim_stamp() fades in
  2      Title: Never claim
  3      Three bullet lines (latency %, production metrics, benchmarks)
  4      Red diagonal cross over stamp
  5      Bottom label: Never claim
```

**Component:** `components/scale.py` → `never_claim_stamp()`

---

## Concat / 4K

```bash
cd aura_manim
../../../.venv/bin/manim -qk --frame_rate 60 scenes/scene8_act1.py Scene8Act1
../../../.venv/bin/manim -qk --frame_rate 60 scenes/scene8_act2.py Scene8Act2
../../../.venv/bin/manim -qk --frame_rate 60 scenes/scene8_act3.py Scene8Act3
ffmpeg -y -f concat -safe 0 -i output/scene8_concat.txt -c copy output/scene8_chapter8_2160p60.mp4
```

**4K concat:** `output/scene8_chapter8_2160p60.mp4` — **25.3 s**

| Act | Start | End | Dur |
|-----|-------|-----|-----|
| 1 | 0:00.0 | 0:08.1 | 8.1s |
| 2 | 0:08.1 | 0:16.8 | 8.7s |
| 3 | 0:16.8 | 0:25.3 | 8.6s |

---

## Status

- [x] VO doc + PLAY CHECKLISTs
- [x] `-ql` render + layout QA per act (2026-07-03)
- [x] 4K concat (25.3 s)
- [ ] VO draft + read-aloud
