# Chapter N — [Title]

> **YouTube chapter:** *[short name]*  
> **Render:** `output/sceneN_chapter*_2160p60.mp4`  
> **Total duration:** `0:00.0` (measured) · **SCENE-PLAN target:** `0:00` → `0:00`  
> **VO status:** draft · read-aloud · recorded  
> **Pace target:** ~140 wpm  

**Source acts:** `aura_manim/scenes/sceneN_act{1…M}.py`  
**Script seed:** [`SCRIPT.md`](../SCRIPT.md) Chapter N  

---

## Act timeline (measured from 2160p60 renders)

| Act | Start | End | Dur | On-screen label | Manim file |
|-----|-------|-----|-----|-----------------|------------|
| 1 | 0:00.0 | | | | `sceneN_act1.py` |
| 2 | | | | | `sceneN_act2.py` |
| … | | | | | |

*Regenerate starts/ends:* `python Aura/design-video/vo/build_act_timestamps.py --chapter N`

---

## Act descriptions

### Act 1 — [short name] (`0:00` → `0:00`)

**What the viewer sees**

- …

**Story beat**

- …

---

### Act 2 — [short name] (`0:00` → `0:00`)

**What the viewer sees**

- …

**Story beat**

- …

---

## VO draft (first read-aloud)

Read over `output/sceneN_chapter*_2160p60.mp4`. One block per act.

### Act 1 (`0:00` → `0:00`) — ~__ s · ~__ words

> …

### Act 2 (`0:00` → `0:00`) — ~__ s · ~__ words

> …

**Chapter totals:** ~__ words · ~__ s at 140 wpm

---

## Trim notes

| Issue | Fix |
|-------|-----|
| Total runtime vs SCENE-PLAN | |
| Long holds | `self.wait()` in `sceneN_actM.py` |
| SCRIPT.md out of sync | Update chapter table after VO lock |

---

## Recording notes

- Room / mic:
- Punch-in acts:
- Music under VO: 0.05–0.07 (see `Aura/manim/add_music.py`)
